"""
Stage 2 of the pipeline: splitting documents into chunks.

`split_documents` is title-prefixed paragraph packing, written for campus_life
in Milestone 3. It groups a document's paragraphs into blocks of at least
CHUNK_MIN_CHARS and prefixes each block with the document's title line, so
every chunk says what it is about.

The starter's strategy is still here as `fallback_split`: fixed-size character
windows with overlap, paying no attention to where sentences or paragraphs end.
On this corpus it never cut anything — 88 documents came out as 88 chunks,
because nothing in campus_life reaches 800 characters. Keeping it makes the
before/after comparison in unit 2 possible.

Note that `fallback_split` reads CHUNK_SIZE and CHUNK_OVERLAP, which Milestone 3
repurposed to 450 and 0. To reproduce the starter's original behaviour, call
`fallback_split(documents, chunk_size=800, overlap=120)` explicitly.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _title_and_body(text: str) -> tuple[str | None, list[str]]:
    """
    Separate a document's title line from its body paragraphs.

    Every document in campus_life opens with a short title on its own line,
    then a blank line, then the body. `ingest.clean_text` has already collapsed
    paragraph breaks to exactly one blank line, so splitting on "\\n\\n" is
    enough. If the first block doesn't look like a title, treat the whole
    document as body rather than silently eating a real paragraph.
    """
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    if not blocks:
        return None, []

    looks_like_title = "\n" not in blocks[0] and len(blocks[0]) < 80
    if looks_like_title and len(blocks) > 1:
        return blocks[0], blocks[1:]
    return None, blocks


def _pack(paragraphs: list[str]) -> list[str]:
    """
    Group paragraphs into blocks of at least CHUNK_MIN_CHARS.

    One paragraph per chunk would be the obvious move, but 26 of this corpus's
    183 paragraphs are under 80 characters ("Expect 4 hours a week outside
    class."). Once the title is prefixed, the title would be nearly half the
    text of those chunks and would drown out the part that makes them distinct.
    """
    blocks: list[str] = []
    buffer: list[str] = []

    for paragraph in paragraphs:
        buffer.append(paragraph)
        if sum(len(p) for p in buffer) >= config.CHUNK_MIN_CHARS:
            blocks.append("\n\n".join(buffer))
            buffer = []

    if buffer:
        tail = "\n\n".join(buffer)
        # A short leftover rides along with the previous block instead of
        # becoming a chunk too thin to stand up on its own.
        if blocks and len(tail) < config.CHUNK_MIN_CHARS // 2:
            blocks[-1] = f"{blocks[-1]}\n\n{tail}"
        else:
            blocks.append(tail)

    return blocks


def _split_long(text: str) -> list[str]:
    """
    Break a block longer than CHUNK_SIZE on sentence boundaries.

    A guard, not an active parameter: the longest body paragraph in campus_life
    is 373 characters, so this never fires on the corpus as it stands. It is
    here so that adding a longer document later can't silently produce one
    enormous chunk.
    """
    if len(text) <= config.CHUNK_SIZE:
        return [text]

    pieces: list[str] = []
    current = ""
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if current and len(current) + len(sentence) + 1 > config.CHUNK_SIZE:
            pieces.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        pieces.append(current)

    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks, one topic at a time, each labelled.

    The starter's fixed 800-character window never cut anything here — nothing
    in campus_life is that long, so 88 documents came out as 88 chunks. But a
    post usually holds more than one thought: the Atrium post is a review and
    then an hours-and-cost note, and the health centre post is walk-in care and
    then counselling. Those should be separate chunks.

    Splitting on paragraphs alone breaks them, though. "Hours are 8:00am to
    6:00pm weekdays" never says which building it means, so on its own it
    matches nothing useful. Every document's first line is its title, so each
    chunk gets that title prepended. That is what lets the split be safe.

    Overlap is 0. Overlap exists to repair a sentence cut in half by a
    fixed-size window; cuts here land on paragraph breaks, so there is nothing
    to stitch back together, and duplicating text would only put near-identical
    embeddings in front of the same query.
    """
    chunks: list[Chunk] = []

    for doc in documents:
        title, paragraphs = _title_and_body(doc.text)

        blocks = _pack(paragraphs) if paragraphs else []
        if not blocks:
            # A title with no body, or a document that survived cleaning as a
            # single line. Keep it whole rather than dropping it.
            blocks = [doc.text.strip()]
            title = None

        index = 0
        for block in blocks:
            for piece in _split_long(block):
                text = f"{title}\n\n{piece}" if title else piece
                chunks.append(
                    Chunk(
                        text=text,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
