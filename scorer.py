"""
The scorer `run_eval.py` looks for: `judge(question, expects, answer, results)`.

It measures criterion 1 in criteria.md — "the retrieved chunks include one that
contains the answer". Every `expects` in questions.py is a sentence or phrase
copied word for word from the corpus, so "contains the answer" can be checked
exactly: the `expects` text has to appear inside at least one retrieved chunk.
The pass/fail marks in the run log's Run columns are this verdict.
"""


def _normalize(text: str) -> str:
    """Lowercase, and collapse every run of whitespace to a single space.

    Chunk text keeps the corpus's paragraph breaks ("\\n\\n") while an
    `expects` string is typed on one line, so without this a match could fail
    on a line break rather than on the content.
    """
    return " ".join(text.lower().split())


def judge(question, expects, answer, results) -> bool:
    """True when some retrieved chunk contains `expects`.

    `answer` is deliberately unused. Criterion 1 is about retrieval; whether
    the generated answer names a source is criterion 2, counted separately
    from the answers in the run log. An empty `expects` is a fail, because
    nothing was decided in advance to look for.
    """
    wanted = _normalize(expects or "")
    if not wanted:
        return False
    return any(wanted in _normalize(r.text) for r in results or [])
