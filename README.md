# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

Name: Rohan Rajendra. Corpus: Campus Life

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

This is a question-answering system over `campus_life`, a corpus of 88 short
posts written by students about one university — dining halls, residence halls,
course workloads and assessments, and administrative processes like grade
appeals and the add/drop deadline. You ask a question in plain English; it
finds the handful of passages most likely to hold the answer, then has a
language model write a short answer from those passages and name the file each
fact came from.

It is built for the questions the official site doesn't answer plainly: *When
does Halden Hall close? What are the assessments for Linear Algebra? How do I
get an urgent health appointment?* Ask it something the documents don't cover
and it tells you it doesn't have enough information instead of guessing — a
distance cutoff refuses clearly unrelated questions before they ever reach the
model, and the model is instructed to answer only from the text it was given.

## Chunking Strategy

**Chunk size:** pack paragraphs until a chunk reaches 180 characters; hard cap 450
**Overlap:** 0

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

Result: 122 chunks from 88 documents, 235 characters on average, shortest 103,
longest 397. The starter produced 88 chunks — one per document — at 800/120.

**What I noticed reading the documents.** Every one of the 88 posts in
`campus_life` has the same shape: a title line, a blank line, then one to four
body paragraphs. They are short — 309 characters at the median, 549 at the
longest — so the starter's 800-character window never cut anything at all. That
is not a bug, but it is not right either, because the paragraphs inside a post
are separate sub-topics. The Atrium post is a review paragraph and then an
hours-and-cost paragraph. The health centre post is walk-in care and then
counselling. Asked "what are the Atrium's hours," a single 400-character chunk
makes me match the review text too.

**Why the title gets prefixed.** Splitting on paragraphs alone breaks the
second half. On its own, `Hours are 7:30am to 7:00pm weekdays, closed Sundays.
Costs one meal swipe, or $10.00 cash.` never says which dining hall it means,
so it can't match a question about Halden Hall. Since the first line of every
document is its title, each chunk gets that title prepended. That is what makes
splitting safe here, and it's what criterion 4 in `criteria.md` is asking for.

**Why 180 and not one chunk per paragraph.** One paragraph per chunk gives 183
chunks, but 26 of this corpus's paragraphs are under 80 characters — things like
`Expect 4 hours a week outside class.` Titles average 28 characters and run to
47, so prefixing one onto a 72-character paragraph makes the title roughly half
the chunk, diluting the part that makes it distinct and pushing same-document
chunks toward identical embeddings. Packing to 180 brings titles down to about
12% of the average chunk.

The cost of that floor is real and I'd rather record it than hide it:
`health_center.txt`'s first paragraph is 173 characters, just under the line, so
counselling got packed in with walk-in hours instead of splitting. One of the
two topics I used to justify splitting didn't actually split. At a floor of 150
it would have. I kept 180 because the dilution problem affects 26 chunks and
this one affects one, but it is a genuine trade-off, not a free choice.

**Why overlap is 0.** Overlap repairs a specific injury: a fixed-size window
cutting a sentence in half so neither half retrieves. My cuts land on paragraph
breaks, so no sentence is ever severed and there is nothing to stitch back
together. The context-carrying that overlap usually does is done by the title
prefix instead. Adding it would also duplicate text across chunks, and on a
corpus this small two near-identical embeddings can take two of the five top-k
slots for one answer.

**About the 450 cap.** It never fired. The longest body paragraph in the corpus
is 373 characters, so `_split_long` returned its input unchanged every time. I
kept it as a guard so that adding a longer document later can't silently
produce one enormous chunk, but on this corpus it is inactive, and the longest
chunk (397) is a paragraph plus its title, not a capped one.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_cs_210_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for CS 210 Data Structures

People keep asking so: 8 to 10 hours a week outside class. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 3** — source: `course_phys_130_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_the_ridgeway_cafe_followup.txt#1` — produced by: `chunker.py::split_documents`

```
Re: The Ridgeway Café

Also worth saying: seating is tight; about 40 seats for a building of 900. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_morrow_house_laundry.txt#0` — produced by: `chunker.py::split_documents`

```
Laundry in Morrow House

Machines take $1.50 wash, $1.25 dry, coin or card. There are eight washers and six dryers for the building, which is the wrong ratio and means the dryers back up on Sunday evenings.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**
What is good about dining at the Atrium?

**Answer:**

```
According to `dining_the_atrium.txt`, what is good about dining at The Atrium is that it features genuinely good sandwiches that are restocked twice a day, and there is no queue because it is all grab-and-go refrigerated cases.

Sources retrieved: dining_pellew_dining_hall_followup.txt, dining_the_atrium.txt, dining_the_atrium_followup.txt
```

Three sources are listed but the answer cites one, and that is the grounding
working rather than two citations going missing. "Sources retrieved" is the
whole top-k set handed to the model; `GROUNDING_INSTRUCTION` then asks it to
name the file each fact actually came from. Here every fact came from
`dining_the_atrium.txt`, so that is the only file named. Criterion 2 asks that
an answer name at least one source, and a retrieved chunk that contributed
nothing is not a source.

**My relevance cutoff:** 0.65

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
| When does a grade appeal go to the department? | Yes | 0.2025 |
| When does Halden Hall close? | Yes | 0.2326 |
| What is good about dining at the Atrium? | Yes | 0.4126 |
| What are the assessments for Linear Algebra? | Yes | 0.4264 |
| How to get an urgent health appointment? | Yes | 0.4552 |
| What is the capital of Mongolia? | No | 0.8246 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8477 |
| How do I write a for loop in Rust? | No | 0.8768 |
| Who won the 1994 World Cup? | No | 0.8859 |
| How do I change the oil in a diesel engine? | No | 0.9231 |

**The two groups.** In-corpus questions run 0.2025 to 0.4552. Off-topic ones run
0.8246 to 0.9231. Nothing lands in between, so the gap is 0.455 to 0.825 —
0.369 wide, which is larger than the entire spread of either group. I put the
cutoff at its midpoint, 0.65 (0.640 rounded), leaving about 0.19 of headroom in
each direction. Measured at 0.65, all five in-corpus questions are answered and
all five off-topic ones are refused.

I did not pick a number closer to either group. With a gap this wide, no value
between 0.46 and 0.82 changes the result on these ten questions, so the choice
is really about questions I haven't asked yet — and the midpoint is the value
that degrades most slowly whether an unseen real question scores worse than
0.455 or an unseen off-topic one scores better than 0.825.

**What the cutoff cannot do.** The five `OUT_OF_SCOPE` questions are from a
different world entirely, which makes them easy and makes the gap look better
than it is. I tried six off-topic questions that share the corpus's subject
matter instead, and they land at 0.404 to 0.608 — overlapping the in-corpus
range completely:

| Off-topic but topically adjacent | Best distance |
|---|---|
| What are the dining hall hours at Stanford? | 0.4043 |
| Which residence hall has the best gym? | 0.4781 |
| What time does the campus bookstore close? | 0.5039 |
| What is the workload for CHEM 101? | 0.5350 |
| How much does a meal plan cost at community college? | 0.5541 |
| How do I appeal a parking ticket in Boston? | 0.6084 |

"What are the dining hall hours at Stanford?" scores 0.4043 — closer than three
of my five real questions. No cutoff can separate these: catching Stanford at
0.40 would mean refusing four of my five real questions. The gate measures
topical similarity, and these questions genuinely are on-topic; they are just
about the wrong institution.

This is what the second layer is for, and it works. Asked the Stanford question,
the system retrieves Atrium and Halden Hall chunks, passes the gate, and the
grounding instruction still produces: *"there is no mention of dining hall hours
at 'Stanford'... Therefore, I do not have enough information to answer about
Stanford."* Same for CHEM 101. I left `GROUNDING_INSTRUCTION` unchanged because
I tested the case that would justify tightening it and it held.

**Top-k is 5**, unchanged, and the Atrium question is why. Its answer-bearing
chunk (`dining_the_atrium.txt#0`) comes back at rank 4, behind two chunks from
the follow-up post. At top-k 3 that question would fail criterion 1, taking me
from 5 of 5 to 4 of 5. Worth noting that top-k does not affect the gate at all:
`gate.check` compares the single best distance, so top-k only changes how much
context the model sees.

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1. Getting Claude to measure my corpus, then building the chunker.** I'd read through documents in the corpus and had a rough sense that
they were short and structured, but I couldn't turn that into numbers. So
before any code, I asked Claude to characterise all 88 documents. It reported
back: every single one opens with a title line, a blank line, and then one to
four body paragraphs; there are 183 body paragraphs with a median length of 112
characters and a maximum of 373; 26 of them are under 80 characters; and titles
average 28 characters.

I had Claude simulate each option against the real corpus before I committed to
one, so I was choosing between measured outcomes (183 vs 122 vs 92 chunks) rather
than guesses. I also deliberated setting the overlap to 0, because
that read as skipping a parameter. I asked it to build the alternative rather
than defend its answer; the one-sentence-carryover version added 2,649 duplicated
characters and pushed sandwich-restocking text into the Atrium's hours chunk. So
I kept 0, for a reason I could state.

**2. Simulating the different retrieval distances for a bunch of test questions.** To zero in on the cutoff point. I set a bunch of sample questions, both on topic and off topic, and ran some simulations with different cutoffs to land at a midpoint value of 0.65, Claude was useful in creating the questions and running different simulations of the cutoff point. I kept
0.65, because no cutoff separates "this campus's dining" from "some campus's
dining," but updated the section to highlight the current limitations and why the
grounding instruction layer should be able to catch it.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

## Stretch Features

Declared here before any of them was built. All three are additive: no existing
command's output changes, and `serve.py`, `run_eval.py` and `ask_pipeline` are
untouched.

**1. Metadata filtering on retrieval.** `build_index` already writes a `source`
field into Chroma's metadata and nothing in the repo ever queries it. I want a
`--source FILENAME` flag on `python app.py retrieve` that narrows the search to
one document. The reason is a problem I already measured, three sections up: the
Atrium question's answer-bearing chunk (`dining_the_atrium.txt#0`) comes back at
rank 4, behind two chunks from the follow-up post. I want to find out whether
filtering by source fixes a ranking problem I documented before I knew this
feature existed.

**2. A second embedding model.** Re-index the same corpus with
`all-mpnet-base-v2` (768-dimensional) alongside the bundled MiniLM
(384-dimensional), keep both indexes side by side rather than replacing one with
the other, and re-run the same ten questions from my distance table on each. The
question I actually want answered is whether 0.65 still separates in-corpus from
off-topic on a model it was never calibrated against.

**3. Conversational memory.** A `python app.py chat` command that carries the
previous turn, so a follow-up like *"when does it close?"* — a question with no
subject in it at all — resolves against the question before it. The hard part is
not storing the history. It is that a bare pronoun question embeds badly against
the corpus and gets refused by the 0.65 gate before the model ever runs, so the
follow-up has to be rewritten into a self-contained query *before* retrieval.

### Result 1 — metadata filtering on retrieval

**What I built.** `store.search` takes an optional `source=`, which becomes a
Chroma `where` filter on the metadata `build_index` was already writing and
nothing was reading. `python app.py retrieve` exposes it as `--source FILENAME`.
With no `--source` the query is the one it always made, so `serve.py`,
`run_eval.py` and `ask_pipeline` are untouched.

**Before** — `python app.py retrieve "What is good about dining at the Atrium?"`

```
Question: What is good about dining at the Atrium?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4126     dining_the_atrium.txt            The Atrium  Hours are 8:00am to 6:00pm weekdays. Cos...
2   0.4324     dining_the_atrium_followup.txt   Re: The Atrium  Adding to what people have said abou...
3   0.5275     dining_the_atrium_followup.txt   Re: The Atrium  Also worth saying: picked clean by 1...
4   0.5311     dining_the_atrium.txt            The Atrium  Transferred in last year, so take this w...
5   0.5412     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.413 is under the 0.65 cutoff
```

**After** — the same question with `--source dining_the_atrium.txt`

```
Question: What is good about dining at the Atrium?
Filtered to source: dining_the_atrium.txt

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4126     dining_the_atrium.txt            The Atrium  Hours are 8:00am to 6:00pm weekdays. Cos...
2   0.5311     dining_the_atrium.txt            The Atrium  Transferred in last year, so take this w...

Gate: best distance 0.413 is under the 0.65 cutoff
```

**What changed, and what didn't.** The answer-bearing chunk here is
`dining_the_atrium.txt#0` — the one beginning *"Transferred in last year"*, which
holds *"genuinely good sandwiches restocked twice a day"*. That is the chunk my
Sample Answer section above records at **rank 4**, behind the hours chunk and two
chunks from the follow-up post. Filtering drops the two follow-up chunks and
moves it from **rank 4 of 5 to rank 2 of 2**, which is the difference between
missing and surviving a top-k of 3.

It did **not** fix the ranking itself, and that is the more useful result. Inside
`dining_the_atrium.txt`, the hours chunk (`#0` is the review, `#1` the hours) is
*still* closer to the question at 0.4126 than the sandwiches chunk at 0.5311 —
on a question asking what is *good* about the Atrium. Both chunks carry the same
`The Atrium` title prefix, so the title contributes equally to both and the
ranking turns on the body; "hours" and "costs one meal swipe" apparently sit
closer to the question's embedding than "worth going for" does. Metadata
filtering narrows *which documents* are eligible; it has no opinion about which
chunk inside them answers the question.

The honest scope of this feature: it fixes the case where the right document is
known and competing documents are crowding it out. It is not a relevance fix,
and I only know that because I had the rank-4 measurement written down before I
built it.

The filter is close to free. Timing the Chroma lookup alone over the same 122
chunks, unfiltered runs at a 4.4ms median and `where source=...` at 5.0ms — a
metadata `$eq` on a collection this small costs about half a millisecond.

### Result 2 — a second embedding model

**What I built.** `config.EMBEDDING_MODEL` now reads
`os.getenv("AI201_EMBEDDING_MODEL", "all-MiniLM-L6-v2")`, matching how `CORPUS`
and `MODEL` already work either side of it. That one line is the whole code
change: `store._sentence_transformer`, the `--variant` flag and
`config.collection_name` were all already in the starter. With the variable
unset, nothing about the system changes.

```
pip install 'sentence-transformers>=3.4,<3.5'
AI201_EMBEDDING_MODEL=all-mpnet-base-v2 python app.py --variant mpnet index
AI201_EMBEDDING_MODEL=all-mpnet-base-v2 python app.py --variant mpnet retrieve "<q>"
```

`--variant mpnet` puts the second index in its own collection, so both models
stay queryable and the MiniLM numbers above remain reproducible.
`requirements.txt` is deliberately untouched — the starter excludes
`sentence-transformers` on purpose, since it pulls PyTorch.

**The same ten questions, both models.** Best distance per question, MiniLM
(384-dimensional) against `all-mpnet-base-v2` (768-dimensional):

| Question | In corpus? | MiniLM | mpnet | Δ |
|---|---|---|---|---|
| When does a grade appeal go to the department? | Yes | 0.2025 | 0.1868 | −0.0156 |
| When does Halden Hall close? | Yes | 0.2326 | 0.2450 | +0.0124 |
| What is good about dining at the Atrium? | Yes | 0.4126 | 0.3484 | −0.0642 |
| What are the assessments for Linear Algebra? | Yes | 0.4264 | 0.4055 | −0.0210 |
| How to get an urgent health appointment? | Yes | 0.4552 | 0.4930 | +0.0378 |
| What is the capital of Mongolia? | No | 0.8246 | 0.8134 | −0.0112 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8477 | 0.8515 | +0.0038 |
| How do I write a for loop in Rust? | No | 0.8768 | 0.7987 | −0.0781 |
| Who won the 1994 World Cup? | No | 0.8859 | 0.9135 | +0.0276 |
| How do I change the oil in a diesel engine? | No | 0.9231 | 0.8477 | −0.0754 |

**Which direction things moved.** The separation got *worse*, not better. The
worst in-corpus question moved out from 0.4552 to 0.4930 and the closest
off-topic one moved in from 0.8246 to 0.7987, so the gap narrowed from **0.3694
to 0.3057** — about 17% of the headroom gone. Nothing crossed, though: at 0.65,
both models still answer 5 of 5 in-corpus questions and refuse 5 of 5 off-topic
ones.

**Does 0.65 transfer?** I expected it not to, because a different model means a
different distance scale and the number was calibrated against MiniLM. It does,
and by a closer margin than I would have guessed: computing the midpoint of
mpnet's own gap the same way I computed 0.65 gives **0.6459**. The cutoff I
already had is within 0.005 of the one I would have derived from scratch. That
is a coincidence rather than a law — both models are cosine-normalised
sentence encoders trained on overlapping data, so their scales are similar —
but on this corpus the threshold survives the swap.

**Where mpnet is actually worse.** The interesting failure is in the
topically-adjacent questions from my cutoff section — the ones no threshold can
separate:

| Off-topic but topically adjacent | MiniLM | mpnet | Δ |
|---|---|---|---|
| What are the dining hall hours at Stanford? | 0.4043 | 0.3906 | −0.0137 |
| Which residence hall has the best gym? | 0.4781 | 0.4761 | −0.0020 |
| What time does the campus bookstore close? | 0.5039 | 0.4795 | −0.0244 |
| **What is the workload for CHEM 101?** | **0.5350** | **0.3704** | **−0.1646** |
| How much does a meal plan cost at community college? | 0.5541 | 0.5299 | −0.0242 |
| How do I appeal a parking ticket in Boston? | 0.6084 | 0.6865 | +0.0781 |

CHEM 101 is the one that matters. My corpus has no CHEM 101 document. Under
MiniLM it sat at 0.5350 — further away than every one of my five real questions,
whose worst was 0.4552, so it fell outside the in-corpus range entirely. Under
mpnet it drops to 0.3704, which lands it *inside* that range: closer than two of
my five real questions (0.4055 and 0.4930) and sitting between the Atrium
question at 0.3484 and Linear Algebra at 0.4055. mpnet has learned the *shape* of
"workload for a course code" well enough that it matches my workload documents
strongly whether or not the specific course exists. A better embedding
model made the confusable case more confusable, because being better at topical
similarity is exactly the wrong skill for telling *this* campus from any campus.
The parking-ticket question moved the other way and now sits above 0.65, so
mpnet would refuse it where MiniLM did not.

**One ranking improvement.** On the Atrium question, the answer-bearing chunk
`dining_the_atrium.txt#0` moves from **rank 4 under MiniLM to rank 3 under
mpnet** — still behind the hours chunk, but inside a top-k of 3 without needing
the `--source` filter.

**The unexpected result: mpnet is faster.** Three paired runs of
`retrieve ... --time` on the same machine, same minute:

| Run | MiniLM (384d, ONNX) | mpnet (768d, PyTorch) |
|---|---|---|
| 1 | 170.5 ms | 59.5 ms |
| 2 | 177.5 ms | 47.7 ms |
| 3 | 193.2 ms | 42.1 ms |

Twice the vector width, three to four times faster. The vector width is not what
is being measured: the Chroma lookup is a few milliseconds either way, and almost all of
this is the query embedding. MiniLM arrives as an ONNX build that runs
single-threaded on the CPU, while `sentence-transformers` loads mpnet through
PyTorch, which uses the machine's accelerated multi-threaded backend. The
*runtime* dominates the *model*. Absolute numbers here are higher than the ones
in criterion 5 because the machine was under load; the ratio held across all
three paired runs regardless.

That is a finding I would not have got from reading model cards, and it points
at the real lever for criterion 5: the fix for retrieval latency is the
inference runtime, not a smaller model.

### Result 3 — conversational memory

**What I built.** `python app.py chat`. Turn 1 goes to the existing
`ask_pipeline` unchanged. From turn 2 on, the previous question and the new
follow-up go to the model first, with an instruction to rewrite the follow-up so
it stands on its own; that rewritten string is what gets retrieved on and
prompted with. `ask_pipeline`, `generate.py` and `serve.py` are untouched, and
`store.py` is untouched *by this feature* — the whole of it is `cmd_chat` plus
one helper in `app.py`. (`store.py` does change elsewhere in this submission, for
the metadata filter above.)

**The two-turn exchange**, pasted as run:

```
> What is good about dining at the Atrium?
  (best distance 0.413, cutoff 0.65)

According to `dining_the_atrium.txt`, what is good about dining at The Atrium is that it features genuinely good sandwiches that are restocked twice a day, and there is no queue because it is all grab-and-go refrigerated cases.

Sources retrieved: dining_pellew_dining_hall_followup.txt, dining_the_atrium.txt, dining_the_atrium_followup.txt

> When does it close?
  (resolved to: When does the Atrium close?)
  (best distance 0.387, cutoff 0.65)

The Atrium is open from 8:00 am to 6:00 pm on weekdays (dining_the_atrium.txt).

Sources retrieved: dining_halden_hall_followup.txt, dining_the_atrium.txt, dining_the_atrium_followup.txt
```

Turn 2 contains no subject at all. *"When does it close?"* cannot be answered by
any system that has not seen turn 1, because the string does not say what "it"
is — the information needed to answer it is not in the question.

**The contrast that proves the memory is doing the work.** Asked cold, in a
fresh process with no turn 1, the same question is *not refused*:

```
$ python app.py ask "When does it close?"
  (best distance 0.424, cutoff 0.65)

Halden Hall closes at 7:00pm (Source: `dining_halden_hall.txt` and `dining_halden_hall_followup.txt`).
```

It answers confidently about the wrong dining hall. I had expected the relevance
gate to catch this one — a pronoun question carries almost no topical signal, so
I assumed it would land beyond the 0.65 cutoff and be refused. It doesn't: it
lands at 0.424, because "close" on its own is a strong match against a corpus
full of closing times. The gate has no way to know the question is
under-specified rather than off-topic; it measures distance, and this question
is genuinely close to something. So the failure mode here is not a refusal I
could have spotted — it is a fluent, sourced, wrong answer, which is the harder
kind to catch.

**What is carried, and what deliberately is not.** Only the previous *question*
travels forward, never the previous answer. Carrying the answer would push a
whole paragraph of prose into the string that gets embedded, and retrieval would
start drifting toward whatever that paragraph happened to mention rather than
what was asked. The rewritten question is what gets stored for the next turn, so
a third turn still resolves — *"How much does it cost?"* became *"How much does
the Atrium cost?"* — while only ever one turn of history is held.

**What it costs.** One extra model call per follow-up turn, on top of the answer
call. Turn 1 costs what it always did.

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 5 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 5 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
