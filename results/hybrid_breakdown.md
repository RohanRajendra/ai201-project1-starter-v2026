# Hybrid search — what it ranked, and why

One-off evidence for the stretch section of the README. It calls the repo's own `store.py::search` with `config.HYBRID_SEARCH` off (embedding only, the `after` system) and on (hybrid, the `after2` system), and reads BM25's word weights from `store.py::_keyword_index`. Deterministic; no model calls. The script is listed at the bottom.

`RRF_K` = 60. A word's weight is BM25's IDF for it over the 122 chunks; rank_bm25 floors very common words at a small positive weight.

## Where each question's answer chunk ranks

An answer chunk is one containing the question's `expects` text, the same test as `scorer.py::judge`.

| Question | Answer chunk | Rank, embedding only | Rank, hybrid |
|---|---|---|---|
| When does a grade appeal go to the department? | `admin_grade_appeals.txt#0` | 1 | 1 |
| How to get an urgent health appointment? | `health_center.txt#0` | 1 | 1 |
| What are the assessments for Linear Algebra? | `course_math_220.txt#0` | 2 | 3 |
| When does Halden Hall close? | `dining_halden_hall.txt#0` | 3 | 4 |
| When does Halden Hall close? | `dining_halden_hall_followup.txt#1` | 1 | 1 |
| What is good about dining at the Atrium? | `dining_the_atrium.txt#0` | 4 | 3 |

## When does a grade appeal go to the department?

| Hybrid rank | Chunk | Cosine distance | Embedding rank | BM25 rank | Fused score | Question words it shares (weight) |
|---|---|---|---|---|---|---|
| 1 | `admin_grade_appeals.txt#0` | 0.2025 | 1 | 1 | 0.03279 | appeal (4.39), department (4.39), grade (3.88), does (3.53), go (2.09), a (0.90), the (0.90), to (0.90) |
| 2 | `transit_shuttle.txt#1` | 0.8006 | 25 | 2 | 0.02789 | when (3.53), a (0.90), the (0.90) |
| 3 | `course_stat_150.txt#1` | 0.7217 | 8 | 18 | 0.02753 | a (0.90), to (0.90), the (0.90) |
| 4 | `admin_withdrawal_deadline.txt#0` | 0.6504 | 3 | 28 | 0.02724 | a (0.90), to (0.90), the (0.90) |
| 5 | `dining_pellew_dining_hall_followup.txt#0` | 0.7823 | 17 | 11 | 0.02707 | go (2.09), a (0.90), to (0.90), the (0.90) |

Dropped from the embedding-only top 5: `admin_add_drop_deadline.txt#0` (0.6133, embedding rank 2, BM25 rank 46), `course_stat_150.txt#0` (0.6540, embedding rank 4, BM25 rank 94), `course_stat_150_exams.txt#0` (0.6731, embedding rank 5, BM25 rank 56).

## How to get an urgent health appointment?

| Hybrid rank | Chunk | Cosine distance | Embedding rank | BM25 rank | Fused score | Question words it shares (weight) |
|---|---|---|---|---|---|---|
| 1 | `health_center.txt#0` | 0.4552 | 1 | 1 | 0.03279 | health (4.39), appointment (4.39), urgent (4.39), to (0.90) |
| 2 | `dining_verrill_street_grill_followup.txt#1` | 0.7643 | 7 | 3 | 0.03080 | how (3.88) |
| 3 | `dining_verrill_street_grill.txt#0` | 0.7536 | 5 | 5 | 0.03077 | how (3.88), to (0.90) |
| 4 | `advising_registration.txt#0` | 0.7717 | 10 | 2 | 0.03041 | an (3.88), get (2.89) |
| 5 | `course_econ_101.txt#1` | 0.8004 | 13 | 4 | 0.02932 | get (2.89), to (0.90) |

Dropped from the embedding-only top 5: `dining_the_atrium_followup.txt#0` (0.7214, embedding rank 2, BM25 rank 24), `dining_the_atrium.txt#1` (0.7268, embedding rank 3, BM25 rank 32), `dining_the_atrium.txt#0` (0.7350, embedding rank 4, BM25 rank 71).

## What are the assessments for Linear Algebra?

| Hybrid rank | Chunk | Cosine distance | Embedding rank | BM25 rank | Fused score | Question words it shares (weight) |
|---|---|---|---|---|---|---|
| 1 | `course_math_220_exams.txt#0` | 0.4264 | 1 | 1 | 0.03279 | algebra (3.27), linear (3.27), are (0.94), the (0.90) |
| 2 | `course_math_220.txt#1` | 0.4934 | 3 | 2 | 0.03200 | algebra (3.27), linear (3.27), are (0.94), the (0.90) |
| 3 | `course_math_220.txt#0` | 0.4699 | 2 | 4 | 0.03175 | linear (3.27), algebra (3.27), for (0.75) |
| 4 | `course_math_220_workload.txt#0` | 0.6019 | 4 | 3 | 0.03150 | linear (3.27), algebra (3.27), the (0.90), for (0.75) |
| 5 | `course_cs_210_exams.txt#0` | 0.6397 | 8 | 33 | 0.02546 | are (0.94), the (0.90) |

Dropped from the embedding-only top 5: `course_engl_205_exams.txt#0` (0.6117, embedding rank 5, BM25 rank 41).

## When does Halden Hall close?

| Hybrid rank | Chunk | Cosine distance | Embedding rank | BM25 rank | Fused score | Question words it shares (weight) |
|---|---|---|---|---|---|---|
| 1 | `dining_halden_hall_followup.txt#1` | 0.2326 | 1 | 2 | 0.03252 | halden (3.27), hall (1.80) |
| 2 | `dining_halden_hall_followup.txt#0` | 0.4484 | 4 | 1 | 0.03202 | halden (3.27), hall (1.80) |
| 3 | `dining_halden_hall.txt#1` | 0.2869 | 2 | 3 | 0.03200 | halden (3.27), hall (1.80) |
| 4 | `dining_halden_hall.txt#0` | 0.4428 | 3 | 4 | 0.03150 | halden (3.27), hall (1.80) |
| 5 | `dining_pellew_dining_hall_followup.txt#1` | 0.5573 | 5 | 11 | 0.02947 | hall (1.80) |

Dropped from the embedding-only top 5: none.

## What is good about dining at the Atrium?

| Hybrid rank | Chunk | Cosine distance | Embedding rank | BM25 rank | Fused score | Question words it shares (weight) |
|---|---|---|---|---|---|---|
| 1 | `dining_the_atrium_followup.txt#0` | 0.4324 | 2 | 2 | 0.03226 | atrium (3.27), about (1.15), what (0.98), the (0.90) |
| 2 | `dining_the_atrium_followup.txt#1` | 0.5275 | 3 | 5 | 0.03126 | atrium (3.27), at (1.61), the (0.90) |
| 3 | `dining_the_atrium.txt#0` | 0.5311 | 4 | 4 | 0.03125 | atrium (3.27), good (2.60), is (0.90), the (0.90) |
| 4 | `dining_pellew_dining_hall_followup.txt#0` | 0.5978 | 9 | 1 | 0.03089 | dining (3.06), at (1.61), about (1.15), what (0.98), the (0.90) |
| 5 | `dining_pellew_dining_hall_followup.txt#1` | 0.5412 | 5 | 7 | 0.03031 | dining (3.06), at (1.61), the (0.90) |

Dropped from the embedding-only top 5: `dining_the_atrium.txt#1` (0.4126, embedding rank 1, BM25 rank 14).

## The script

```python
"""How hybrid search ranked each question's top 5, and why. One-off evidence.

    python hybrid_breakdown.py <output.md>

Not part of the system and changes nothing in it: it calls the repo's own
`store` functions with config.HYBRID_SEARCH on and off. Deterministic, no model
calls. The listing of this script is appended to the output file.
"""

import sys
from pathlib import Path

REPO = "/Users/adri/scripts/projects/codepath/ai-prep/ai201-project1-starter-v2026"
sys.path.insert(0, REPO)

import config  # noqa: E402
import questions as qs  # noqa: E402
import scorer  # noqa: E402
import store  # noqa: E402

out = []
say = out.append

name = config.collection_name()
col = store._client().get_collection(name)
ids, bm25 = store._keyword_index(col, name)
scores_for = lambda q: dict(zip(ids, bm25.get_scores(store._tokens(q))))  # noqa: E731
text_of = dict(zip(ids, col.get(ids=ids, include=["documents"])["documents"]))


def ranked(hybrid, q, k=None):
    config.HYBRID_SEARCH = hybrid
    try:
        return store.search(q, top_k=k)
    finally:
        config.HYBRID_SEARCH = True


say("# Hybrid search — what it ranked, and why")
say("")
say("One-off evidence for the stretch section of the README. It calls the repo's "
    "own `store.py::search` with `config.HYBRID_SEARCH` off (embedding only, the "
    "`after` system) and on (hybrid, the `after2` system), and reads BM25's word "
    "weights from `store.py::_keyword_index`. Deterministic; no model calls. "
    "The script is listed at the bottom.")
say("")
say(f"`RRF_K` = {store.RRF_K}. A word's weight is BM25's IDF for it over the "
    f"{len(ids)} chunks; rank_bm25 floors very common words at a small positive "
    "weight.")
say("")

say("## Where each question's answer chunk ranks")
say("")
say("An answer chunk is one containing the question's `expects` text, the same test "
    "as `scorer.py::judge`.")
say("")
say("| Question | Answer chunk | Rank, embedding only | Rank, hybrid |")
say("|---|---|---|---|")
for item in qs.answered():
    q, want = item["question"], scorer._normalize(item["expects"])
    vec, hyb = ranked(False, q), ranked(True, q)
    hits = sorted({r.label for r in vec + hyb if want in scorer._normalize(r.text)})
    for label in hits:
        rv = next((i for i, r in enumerate(vec, 1) if r.label == label), "not in top 5")
        rh = next((i for i, r in enumerate(hyb, 1) if r.label == label), "not in top 5")
        say(f"| {q} | `{label}` | {rv} | {rh} |")
say("")

for item in qs.answered():
    q = item["question"]
    full = ranked(False, q, k=col.count())
    vrank = {r.label: i for i, r in enumerate(full, 1)}
    s = scores_for(q)
    matched = sorted((r for r in full if s.get(r.label, 0) > 0), key=lambda r: s[r.label], reverse=True)
    brank = {r.label: i for i, r in enumerate(matched, 1)}
    qt = store._tokens(q)
    say(f"## {q}")
    say("")
    say("| Hybrid rank | Chunk | Cosine distance | Embedding rank | BM25 rank | Fused score | Question words it shares (weight) |")
    say("|---|---|---|---|---|---|---|")
    for i, r in enumerate(ranked(True, q), 1):
        fused = 1 / (store.RRF_K + vrank[r.label]) + (1 / (store.RRF_K + brank[r.label]) if r.label in brank else 0)
        words = sorted({t for t in qt if t in store._tokens(text_of[r.label])}, key=lambda t: -bm25.idf.get(t, 0))
        shared = ", ".join(f"{t} ({bm25.idf.get(t, 0):.2f})" for t in words) or "none"
        say(f"| {i} | `{r.label}` | {r.distance:.4f} | {vrank[r.label]} | {brank.get(r.label, '—')} | {fused:.5f} | {shared} |")
    dropped = [r for r in ranked(False, q) if r.label not in {x.label for x in ranked(True, q)}]
    say("")
    say("Dropped from the embedding-only top 5: " + (", ".join(
        f"`{r.label}` ({r.distance:.4f}, embedding rank {vrank[r.label]}, BM25 rank {brank.get(r.label, '—')})"
        for r in dropped) or "none") + ".")
    say("")

say("## The script")
say("")
Path(sys.argv[1]).write_text(
    "\n".join(out + ["```python", Path(__file__).read_text().rstrip(), "```", ""]),
    encoding="utf-8",
)
print(f"wrote {sys.argv[1]}")
```
