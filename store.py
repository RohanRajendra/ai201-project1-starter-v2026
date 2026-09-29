"""
Stages 3 and 4 of the pipeline: embedding chunks and retrieving them.

Four things in here are worth knowing about, because they'd quietly break the
rest of the project if they were wrong:

1. The Chroma collection is created with cosine distance, explicitly. Chroma
   defaults to squared L2, and the 0.6 threshold the course uses is calibrated
   against cosine. Getting this wrong makes every distance number meaningless.

2. `search` returns the distance alongside each chunk. Milestone 4 has you
   compare distances, so they have to be visible.

3. The embedding model is the one Chroma bundles, not one loaded through
   `sentence-transformers`. It is the same model — `all-MiniLM-L6-v2`, 384
   dimensions — but it arrives as an ONNX build from Chroma's own CDN, so the
   install needs neither PyTorch nor a reachable Hugging Face. See `_embedder`.

4. `search` is hybrid since unit 2: a BM25 keyword ranking is fused with the
   embedding ranking (see `_fuse`), so its results are best-first rather than
   strictly nearest-first. Every result still carries its real cosine
   distance, which is what the relevance gate reads. `AI201_HYBRID=0` turns
   the keyword half off.
"""

import os
import re
import shutil
from dataclasses import dataclass

# Must be set BEFORE chromadb is imported. Without it, some Chroma versions
# print "Failed to send telemetry event ..." on every single call — which looks
# exactly like a real error, isn't one, and cost a previous cohort a lot of
# confused help-channel messages.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

import chromadb  # noqa: E402

import config
from chunker import Chunk


@dataclass
class Result:
    """One retrieved chunk and how far it was from the question."""

    text: str
    source: str
    label: str
    distance: float   # LOWER IS BETTER. 0.3 is close, 0.9 is unrelated.
    produced_by: str


_model = None

# The model Chroma bundles. Anything else in config.EMBEDDING_MODEL means
# "fetch that one from Hugging Face instead" — see `_embedder`.
BUNDLED_MODEL = "all-MiniLM-L6-v2"


class _OnnxEmbedder:
    """
    Chroma's built-in embedder, wrapped to look like the other two.

    Chroma's embedding functions are called directly and hand back numpy
    arrays. The rest of this file wants `.encode(texts)`, so the adapter lives
    here rather than making every caller care which embedder it got.
    """

    def __init__(self):
        from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

        # CPU provider only. Left to itself, Chroma hands ONNX Runtime every
        # provider installed — CoreML first, on a Mac — and for this model that
        # made embedding one question about 4x slower for an identical vector.
        # Unit 2 measured it: results/c5_diagnosis.md.
        self._ef = ONNXMiniLM_L6_V2(preferred_providers=["CPUExecutionProvider"])

    def encode(self, texts, show_progress_bar: bool = False):
        return [vector.tolist() for vector in self._ef(list(texts))]


def _sentence_transformer(name: str):
    """
    The escape hatch: any model that isn't the bundled one.

    Unit 2's "try a second embedding model" stretch option comes through here,
    and so does anything you set `EMBEDDING_MODEL` to. This path *does* need
    `sentence-transformers` and a reachable Hugging Face, neither of which the
    default install has — which is the whole point of the default install.
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            f"config.EMBEDDING_MODEL is set to {name!r}, which isn't the model "
            f"Chroma bundles ({BUNDLED_MODEL!r}), so it has to be downloaded "
            f"from Hugging Face.\n"
            f"Install the optional dependency first:\n"
            f"    pip install 'sentence-transformers>=3.4,<3.5'\n"
            f"Or set EMBEDDING_MODEL back to {BUNDLED_MODEL!r}."
        ) from exc

    return SentenceTransformer(name)


def _embedder():
    """
    Load the embedding model once and keep it.

    First call is slow — it downloads about 80 MB. That's why setup happens
    before class.
    """
    global _model

    if _model is not None:
        return _model

    # Used only by this repo's own smoke test, which runs where no model can be
    # downloaded at all. Never set this yourself.
    if os.getenv("AI201_FAKE_EMBEDDINGS") == "1":
        from _smoke_embedder import FakeEmbedder

        _model = FakeEmbedder()
    elif config.EMBEDDING_MODEL == BUNDLED_MODEL:
        _model = _OnnxEmbedder()
    else:
        _model = _sentence_transformer(config.EMBEDDING_MODEL)

    return _model


def embed(texts: list[str]) -> list[list[float]]:
    """Turn text into vectors. Runs on your machine, costs no API quota."""
    vectors = _embedder().encode(texts, show_progress_bar=False)
    # sentence-transformers and the smoke stand-in return something with a
    # .tolist(); _OnnxEmbedder has already done that conversion itself.
    return vectors.tolist() if hasattr(vectors, "tolist") else vectors


def _client():
    return chromadb.PersistentClient(
        path=str(config.CHROMA_DIR),
        settings=chromadb.config.Settings(anonymized_telemetry=False),
    )


def build_index(
    chunks: list[Chunk],
    corpus: str | None = None,
    variant: str = "default",
) -> int:
    """
    Embed every chunk and store it.

    `variant` lets you keep more than one index of the same corpus at the same
    time. In unit 2, when you compare two chunking strategies, index the second
    one as variant="v2" and you can query both instead of deleting the first
    and starting over.
    """
    name = config.collection_name(corpus, variant)
    client = _client()

    try:
        client.delete_collection(name)
    except Exception:
        pass

    collection = client.create_collection(
        name=name,
        # ⚠️ Do not remove. Chroma defaults to squared L2, and every distance
        # number in this course assumes cosine.
        metadata={"hnsw:space": "cosine"},
    )

    batch = 256
    for start in range(0, len(chunks), batch):
        window = chunks[start : start + batch]
        collection.add(
            ids=[f"{c.source}#{c.index}" for c in window],
            documents=[c.text for c in window],
            embeddings=embed([c.text for c in window]),
            metadatas=[
                {"source": c.source, "index": c.index, "produced_by": c.produced_by}
                for c in window
            ],
        )

    return len(chunks)


# Reciprocal rank fusion's constant, from the paper that introduced it
# (Cormack, Clarke & Büttcher, 2009). Deliberately not tuned: the only
# questions it could be tuned on are the test questions it is measured by.
RRF_K = 60

_keyword_indexes: dict[str, tuple] = {}


def _tokens(text: str) -> list[str]:
    """Lowercase words and numbers — the only preprocessing BM25 gets."""
    return re.findall(r"[a-z0-9]+", text.lower())


def _keyword_index(collection, name: str):
    """
    BM25 over the chunk texts already stored in the collection.

    Built once per process and then reused, like the embedding model: the first
    search pays for it and later ones don't. Rebuilt if the collection's size
    changes underneath it.
    """
    count = collection.count()
    cached = _keyword_indexes.get(name)
    if cached is None or cached[0] != count:
        from rank_bm25 import BM25Okapi

        stored = collection.get(include=["documents"])
        bm25 = BM25Okapi([_tokens(text) for text in stored["documents"]])
        cached = (count, stored["ids"], bm25)
        _keyword_indexes[name] = cached
    return cached[1], cached[2]


def _fuse(question: str, by_meaning: list[Result], collection, name: str) -> list[Result]:
    """
    Reciprocal rank fusion of the embedding ranking with a BM25 ranking.

    Each chunk scores 1/(RRF_K + its embedding rank), plus 1/(RRF_K + its BM25
    rank) if it shares any word with the question. Only ranks are used, never
    the raw scores, because cosine distance and BM25 are on scales that can't
    be compared. BM25 ranks only the chunks the embedding search returned, so
    a `source` filter applies to both halves. Ties keep embedding order.
    """
    ids, bm25 = _keyword_index(collection, name)
    scores = dict(zip(ids, bm25.get_scores(_tokens(question))))

    by_keyword = sorted(
        (r for r in by_meaning if scores.get(r.label, 0) > 0),
        key=lambda r: scores[r.label],
        reverse=True,
    )
    keyword_rank = {r.label: rank for rank, r in enumerate(by_keyword, 1)}

    def fused(ranked):
        rank, r = ranked
        score = 1 / (RRF_K + rank)
        if r.label in keyword_rank:
            score += 1 / (RRF_K + keyword_rank[r.label])
        return score

    return [r for _, r in sorted(enumerate(by_meaning, 1), key=fused, reverse=True)]


def search(
    question: str,
    top_k: int | None = None,
    corpus: str | None = None,
    variant: str = "default",
    source: str | None = None,
) -> list[Result]:
    """
    Retrieve the chunks that best answer a question.

    Returns the top_k best first, each with its real cosine distance. With
    config.HYBRID_SEARCH on, "best" is the fusion of the embedding ranking and
    a BM25 keyword ranking (see `_fuse`), so the order is no longer strictly
    nearest-first. With it off, this is the nearest-first embedding search that
    unit 2's "after" run log measured.

    `source` narrows the search to one document, by the filename `build_index`
    already stores in each chunk's metadata. Leave it as None — the default —
    and this makes exactly the query it always made. Note that `n_results` is
    still capped by the *unfiltered* collection size, so a filtered search
    legitimately returns fewer rows than top_k asked for; that is Chroma
    running out of matching chunks, not an error.
    """
    top_k = top_k or config.TOP_K
    name = config.collection_name(corpus, variant)

    try:
        collection = _client().get_collection(name)
    except Exception as exc:
        raise RuntimeError(
            f"No index called '{name}'. Run `python app.py index` first."
        ) from exc

    where = {"source": {"$eq": source}} if source is not None else None

    if not config.HYBRID_SEARCH:
        raw = collection.query(
            query_embeddings=embed([question]),
            n_results=min(top_k, collection.count()),
            where=where,
        )
        return _results(raw)

    # The embedding half of the fusion ranks every chunk, not just the top_k:
    # BM25 can only lift a chunk the embedding ranking has a place for. On a
    # corpus this size, asking Chroma for all of them costs next to nothing.
    raw = collection.query(
        query_embeddings=embed([question]),
        n_results=collection.count(),
        where=where,
    )
    return _fuse(question, _results(raw), collection, name)[:top_k]


def _results(raw) -> list[Result]:
    """Chroma's query response as Results, in the order Chroma returned them."""
    results: list[Result] = []
    for text, meta, distance in zip(
        raw["documents"][0], raw["metadatas"][0], raw["distances"][0]
    ):
        results.append(
            Result(
                text=text,
                source=str(meta.get("source", "unknown")),
                label=f"{meta.get('source', 'unknown')}#{meta.get('index', 0)}",
                distance=float(distance),
                produced_by=str(meta.get("produced_by", "unknown")),
            )
        )
    return results


def index_exists(corpus: str | None = None, variant: str = "default") -> bool:
    """Is there an index here to search, without searching it?

    `serve.py`'s health check asks this. It deliberately does not embed
    anything: loading the embedding model takes 80 MB and a few seconds, and a
    health check that heavy is a health check nobody can afford to call.
    """
    try:
        collection = _client().get_collection(config.collection_name(corpus, variant))
        return collection.count() > 0
    except Exception:
        return False


def reset():
    """Delete every index. Occasionally the fastest way out of a mess."""
    if config.CHROMA_DIR.exists():
        shutil.rmtree(config.CHROMA_DIR)
