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
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks begin with their title line | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Retrieval median under 50 ms, per question | 5 of 5 | 0/5 | 0/5 | 0/5 | MISSED |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

**Where each row comes from.** Everything is committed in `results/`.

- **Rows 1–3** come from `results/run_2026-09-29_1408_before.md`, written by
  `python run_eval.py --label before`, which asks each question three separate
  times with caching off.
  - Row 1 counts the `pass` marks from `scorer.py::judge`. It checks whether
    the question's `expects` text, which I copied word for word from the
    corpus, appears in any chunk `store.py::search` returned.
  - Row 2 counts the answers that contain at least one corpus filename.
  - Row 3 is the gate's single pass. The same number goes in all three
    columns because retrieval and the gate give the same result every time.
- **Row 4** comes from `results/c4_chunks_before.md`: three separate runs of
  `python app.py chunks -n 5`, with each sampled chunk's first line checked
  against `head -n 1` of its source file.
- **Row 5** comes from `results/c5_timing_before.md`: three passes of
  `python app.py retrieve "<question>" --time` over all five questions,
  counting the medians under 50 ms.
  - Every pass ran on battery with macOS Low Power Mode on, which is how I
    normally use this laptop.
  - I fixed that condition before the first pass, and the after run uses it too.
- **Ranks behind row 1:** `results/c1_retrieve_before.md` has the full ranking
  for each question.

Rows 1, 3 and 4 come out the same in every column because nothing random
happens in retrieval, the gate or the `chunks` sample. Rows 2 and 5 are the
ones that could move. This was a real re-run, not a cache: the answer wording
changes from run to run, and the run made 15 model calls with none served
from cache.

`results/` also holds three logs from 2026-09-23 (`run_2026-09-23_2028.md`,
`run_2026-09-23_2039.md`, `run_2026-09-23_2100.md`). Earlier drafts of
`scorer.py` scored them while I was building it. Their pass/fail marks don't
measure criterion 1, so they are not this run log.

Today's first attempt stopped on a Gemini `503 UNAVAILABLE` (model
overloaded) at question 2, run 3, before `run_eval.py` wrote any file. The
log above is the complete re-run.

### Real output — criterion 1

The per-question table from `results/run_2026-09-29_1408_before.md`, written
by `run_eval.py::main`, with every mark from `scorer.py::judge`:

```text
| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| When does a grade appeal go to the department? | pass | pass | pass |
| How to get an urgent health appointment? | pass | pass | pass |
| What are the assessments for Linear Algebra? | pass | pass | pass |
| When does Halden Hall close? | pass | pass | pass |
| What is good about dining at the Atrium? | pass | pass | pass |
```

The closest of the five is the Atrium question.
- The chunk that holds the answer is `dining_the_atrium.txt#0`, which begins
  *"Transferred in last year…"* and contains *"genuinely good sandwiches
  restocked twice a day"*.
- It comes back at rank 4 of 5.
- This comes from `python app.py retrieve "What is good about dining at the
  Atrium?"` (`app.py::cmd_retrieve` → `store.py::search`), in
  `results/c1_retrieve_before.md`:

```text
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

### Real output — criterion 2

Run 1's five answers from `results/run_2026-09-29_1408_before.md`. Each is
generated by `generate.py::answer_from_chunks`, called from
`run_eval.py::run_once`.

**When does a grade appeal go to the department?** (run 1)

```text
A grade appeal goes to the department only after it has started with the instructor. 

Source: admin_grade_appeals.txt
```

**How to get an urgent health appointment?** (run 1)

```text
If something is urgent, you should go to the health centre at 8am and wait rather than booking. 

Source: health_center.txt
```

**What are the assessments for Linear Algebra?** (run 1)

```text
The assessments for Linear Algebra consist of two midterms and a cumulative final, which are curved to a B- median. 

Source: `course_math_220.txt` (also mentioned in `course_math_220_exams.txt`)
```

**When does Halden Hall close?** (run 1)

```text
Halden Hall closes at 7:00pm, according to *dining_halden_hall.txt* and *dining_halden_hall_followup.txt*.
```

**What is good about dining at the Atrium?** (run 1)

```text
The Atrium features genuinely good sandwiches that are restocked twice a day, and it has no queue because it uses grab-and-go refrigerated cases. 

Source: `dining_the_atrium.txt`
```

### Real output — criterion 3

From `results/run_2026-09-29_1408_before.md`, written by
`run_eval.py::check_out_of_scope`:

```text
Produced by `run_eval.py::check_out_of_scope`, cutoff 0.65. Refused 5 of 5.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.923 | refused |
| Who won the 1994 World Cup? | 0.886 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.848 | refused |
| How do I write a for loop in Rust? | 0.877 | refused |
```

### Real output — criterion 4

Pass 1 of `python app.py chunks -n 5` (`app.py::cmd_chunks` →
`chunker.py::split_documents`), from `results/c4_chunks_before.md`:

```text
122 chunks total. Showing 5, spread across the corpus.

Paste these into your README under Sample Chunks. The rubric asks
for the source file and the function that produced them — both are
printed for you below.

======================================================================
Chunk 1  |  source: admin_add_drop_deadline.txt#0  |  produced by: chunker.py::split_documents
======================================================================
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.

======================================================================
Chunk 2  |  source: course_cs_210_workload.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Workload for CS 210 Data Structures

People keep asking so: 8 to 10 hours a week outside class. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.

======================================================================
Chunk 3  |  source: course_phys_130_workload.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.

======================================================================
Chunk 4  |  source: dining_the_ridgeway_cafe_followup.txt#1  |  produced by: chunker.py::split_documents
======================================================================
Re: The Ridgeway Café

Also worth saying: seating is tight; about 40 seats for a building of 900. Nobody tells you this at orientation.

======================================================================
Chunk 5  |  source: housing_morrow_house_laundry.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Laundry in Morrow House

Machines take $1.50 wash, $1.25 dry, coin or card. There are eight washers and six dryers for the building, which is the wrong ratio and means the dryers back up on Sunday evenings.
```

| Chunk | Chunk's first line | `head -n 1` of its source file | Same? |
|---|---|---|---|
| `admin_add_drop_deadline.txt#0` | On the add/drop deadline | On the add/drop deadline | yes |
| `course_cs_210_workload.txt#0` | Workload for CS 210 Data Structures | Workload for CS 210 Data Structures | yes |
| `course_phys_130_workload.txt#0` | Workload for PHYS 130 Mechanics | Workload for PHYS 130 Mechanics | yes |
| `dining_the_ridgeway_cafe_followup.txt#1` | Re: The Ridgeway Café | Re: The Ridgeway Café | yes |
| `housing_morrow_house_laundry.txt#0` | Laundry in Morrow House | Laundry in Morrow House | yes |

Passes 2 and 3 printed the same five chunks, because `cmd_chunks` samples by
stride, not at random.

### Real output — criterion 5

Pass 1, first question, from `results/c5_timing_before.md`. The timing lines
are printed by `app.py::_print_retrieval_timing`, which times
`store.py::search`:

```text
Retrieval timing, 5 runs after one discarded warm-up:
  min 69.7 ms   median 85.2 ms   max 93.5 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.
```

All fifteen medians, read off the timing lines in the same file:

| Question | Pass 1 | Pass 2 | Pass 3 |
|---|---|---|---|
| When does a grade appeal go to the department? | 85.2 ms | 81.8 ms | 82.8 ms |
| How to get an urgent health appointment? | 82.9 ms | 64.7 ms | 84.1 ms |
| What are the assessments for Linear Algebra? | 86.5 ms | 81.4 ms | 85.3 ms |
| When does Halden Hall close? | 92.3 ms | 82.3 ms | 81.2 ms |
| What is good about dining at the Atrium? | 84.1 ms | 83.4 ms | 82.3 ms |
| **Under 50 ms** | **0 of 5** | **0 of 5** | **0 of 5** |

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer (target: at least 4 of 5) | MET | Every run found the answer in the retrieved chunks for all 5 questions, one more than the target needs. The margin is thinner than 5/5 looks: the Atrium question passes only because its answer chunk comes back at rank 4 of the 5 retrieved. |
| 2 | Every answer names a source (target: 5 of 5) | MET | The target allows no misses, so one unsourced answer in any run would have made this MISSED. All 15 answers (5 questions × 3 runs) name at least one corpus file. |
| 3 | Gate stops out-of-corpus questions (target: 5 of 5) | MET | The gate refused all 5 `OUT_OF_SCOPE` questions. The nearest sits at 0.825 against a 0.65 cutoff, and the gate gives the same answer every time, so rerunning can't move this number. |
| 4 | Sampled chunks begin with their title line (target: 5 of 5) | MET | In each of the three runs, all 5 sampled chunks start with exactly the first line of their source file. The three runs are the same five chunks, because the sample is taken by stride. |
| 5 | Retrieval median under 50 ms, per question (target: 5 of 5) | MISSED | None of the 15 medians came in under 50 ms, so the target failed in every run, not just once. It isn't close: the fastest median was 64.7 ms and the other fourteen ran 81.2–92.3 ms. |

**Arguing the other side.** Before settling these, I argued each one the
opposite way. Three of those arguments are worth writing down. None of them
changes a verdict.

- **Criterion 3 as MISSED.** The criterion says the gate stops "a question my
  documents clearly don't cover". My five `OUT_OF_SCOPE` questions come from a
  different world entirely.
  - In unit 1 I found off-topic questions that share the corpus's subject
    matter and get *through* the gate. "What are the dining hall hours at
    Stanford?" scores 0.404, well under 0.65.
  - Read that broadly, the gate does not stop every question my documents
    don't cover.
  - It stays MET because the target counts five tries, those five are the
    `OUT_OF_SCOPE` questions, and the run log measures exactly them. But it
    means this criterion only ever asked about the easy case.
- **Criterion 5 as MET.** Every pass ran on battery with Low Power Mode on,
  which slows the CPU, so the same code might clear 50 ms plugged in.
  - It stays MISSED because I fixed that condition before measuring, and the
    criterion doesn't name any other.
  - Switching to whichever condition passes after seeing the numbers would
    be lowering the target by another route.
- **Criterion 4 couldn't have come out any other way.** `split_documents`
  puts the title at the top of every chunk of every document that has one,
  and all 88 documents do.
  - I checked all 122 chunks, not just the 5 sampled: every one starts with
    its file's first line.
  - So MET is right, but this criterion checks what the chunker's code
    guarantees, not something the corpus could get wrong.

I revised no criterion. Each one produced a number I could check the same
way every time, so none turned out to be unmeasurable. Criteria 3 and 4 being
easy to pass is a problem with where I set the bar, not with the measurement,
so I come back to it under "What I'd Do Differently".

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

One criterion missed: **criterion 5**, retrieval under 50 ms. The other four
were MET, so this is the only diagnosis.

### Criterion 5: stage 3, embedding

**Where the time goes.** I timed `store.search()` and the three steps inside
it, all in the same loop iteration so they saw the same machine load. That was
50 iterations per question, done twice. The condition was the same as the run
log: battery, Low Power Mode on. The data is section A of
`results/c5_diagnosis.md`:

| Step inside `store.search()` | Median across both runs |
|---|---|
| Open the Chroma client and collection | 3.3–3.5 ms |
| **Embed the question** (`store.embed`) | **76.4–84.9 ms** |
| Count + nearest-neighbour lookup | 4.6–5.0 ms |
| Whole `store.search()` | 83.9–94.1 ms |

Embedding the question is 90–91% of the time, for every question in both
runs. The retrieval stage itself, the lookup over 122 vectors, takes under
5 ms. Even if the lookup took no time at all, criterion 5 would still miss.
The problem is in stage 3.

**The mechanism.** `store.embed` uses the MiniLM build that Chroma bundles
(chromadb's `ONNXMiniLM_L6_V2`, created in `store.py::_OnnxEmbedder`). Two of
its settings make a 9-to-12-token question cost far more than it needs to:

1. **Every question is padded to 256 tokens.** Chroma's tokenizer calls
   `enable_padding(length=256)`. My questions are 9 to 12 tokens long, so the
   model processes 21 to 28 times as many positions as the question has.
2. **Chroma gives ONNX Runtime every provider it has, and on this Mac the
   first is CoreML.** The session runs with `['CoreMLExecutionProvider',
   'AzureExecutionProvider', 'CPUExecutionProvider']`. Chroma's own source
   comments that CoreML "doesn't fit this model".

Section B of the same file times one forward pass of the model four ways for
each question:

| One forward pass (median across both runs) | Padded to 256 | At the question's real length |
|---|---|---|
| Providers as Chroma sets them (CoreML first) | 98.9–113.6 ms | 22.2–26.0 ms |
| CPU provider only | 24.6–28.7 ms | 2.3–3.0 ms |

The four variants run against each other in the same loop, so they compete for
the same cores. Compare figures within this table rather than against the one
above.

Starting from the setup as it ships, removing either setting cuts a forward
pass by about 4×, and removing both cuts it by about 40×. Neither setting
changes the result. For every one of my five questions, the final vector is
the same padded or unpadded, and on CoreML or CPU: cosine similarity 1.000000,
because Chroma's mean pooling ignores the padded positions. All the extra time
buys nothing.

**The pattern.** All five questions miss by almost the same amount. Their
medians in the run log run 81–92 ms apart from a single 64.7, and the
embedding share is 90–91% for every one of them. That fits the mechanism: the
cost doesn't depend on what I ask, because every question is padded to the
same 256 tokens and sent through the same provider. It is one problem, not
five.

**What this corrects from unit 1.** My unit 1 README guessed that the ONNX
build "runs single-threaded on the CPU". That is wrong. During a padded
forward pass the process uses 4.65–4.98 CPU-seconds per wall-clock second
(section C), so about five cores are busy. The slowdown doesn't come from too
little parallelism. It comes from 21–28 times more positions than the
question needs, run on a provider that suits this model badly.

The padding probably also explains why mpnet came out faster than MiniLM in
unit 1. sentence-transformers pads a batch only to its longest input, so a
single question runs at its own length. I haven't measured that part.

## The Improvement

**What I changed:** One argument, in `store.py::_OnnxEmbedder`:

```python
# before
self._ef = ONNXMiniLM_L6_V2()
# after
self._ef = ONNXMiniLM_L6_V2(preferred_providers=["CPUExecutionProvider"])
```

ONNX Runtime now runs MiniLM on its plain CPU provider. Before, it used the
provider list Chroma picks when left alone, which puts CoreML first on this
Mac. Nothing else changed: the model, chunks, index, top-k, gate and prompt
are all the same. I didn't rebuild the index, because the vectors come out
identical either way (cosine 1.000000 in the diagnosis). All five best
distances are still 0.2025, 0.4552, 0.4264, 0.2326 and 0.4126.

**Why I picked it:** It removes the second cause in my criterion 5 diagnosis.
Left to choose, Chroma runs the embedding on the CoreML provider, and that
alone makes each question's forward pass about 4× slower than the CPU
provider, for an identical vector.

The diagnosis found two causes, and the milestone asks for one change. I
picked this one over removing the 256-token padding because it's a
documented constructor argument. Removing the padding would mean overriding
Chroma's tokenizer (a cached internal property), which a Chroma upgrade
could quietly undo.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

**What I expected, written before the after run.**
- Section B of `results/c5_diagnosis.md` puts a padded forward pass at
  24.6–28.7 ms on the CPU provider, against 98.9–113.6 ms as shipped.
- Add the client (about 3 ms) and the lookup (about 5 ms), and each
  question's median should land around 32–38 ms. That's under 50, but not by
  a wide margin.
- Before choosing, I tried both candidate fixes in a throwaway script without
  touching the repo, and it pointed the same way.

**Why it might not work.**
- **The 256-token padding is still there.** On the CPU provider it still
  makes each forward pass about 10× longer than the question needs
  (24.6–28.7 ms padded, 2.3–3.0 ms unpadded, section B). A load spike could
  eat the margin.
- **It's tuned to a specific device that is running the tests.** On hardware where CoreML suits this model,
  forcing the CPU could be the slower choice.

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks begin with their title line | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Retrieval median under 50 ms, per question | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Where each row comes from.** The commands and counting are the same as the
before log. The files are labelled `after`:

- **Rows 1–3:** `results/run_2026-09-29_1530_after.md`, from 15 real model
  calls with none served from cache.
- **Row 4:** `results/c4_chunks_after.md`.
- **Row 5:** `results/c5_timing_after.md`, in the same condition as before:
  battery, Low Power Mode on, no apps closed.
- **Ranks behind row 1:** `results/c1_retrieve_after.md`.

The machine was busier this time: the load average during the timing passes
was 4.3–4.8, against 1.6–2.4 for the before log.

Real output for criterion 5 from pass 1, first question, in
`results/c5_timing_after.md`. It's printed by
`app.py::_print_retrieval_timing`, timing `store.py::search`:

```text
Retrieval timing, 5 runs after one discarded warm-up:
  min 17.4 ms   median 18.3 ms   max 18.9 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.
```

**Did it help?** Yes. Criterion 5 went from MISSED to MET, and nothing else
moved.

| Question | Before: pass 1 / 2 / 3 | After: pass 1 / 2 / 3 |
|---|---|---|
| When does a grade appeal go to the department? | 85.2 / 81.8 / 82.8 ms | 18.3 / 19.0 / 17.9 ms |
| How to get an urgent health appointment? | 82.9 / 64.7 / 84.1 ms | 17.1 / 21.2 / 16.9 ms |
| What are the assessments for Linear Algebra? | 86.5 / 81.4 / 85.3 ms | 17.2 / 18.2 / 18.4 ms |
| When does Halden Hall close? | 92.3 / 82.3 / 81.2 ms | 17.7 / 18.6 / 20.3 ms |
| What is good about dining at the Atrium? | 84.1 / 83.4 / 82.3 ms | 17.7 / 17.6 / 18.1 ms |
| **Under 50 ms** | **0 / 0 / 0 of 5** | **5 / 5 / 5 of 5** |

- **Criterion 5 went from 0 of 5 in every pass to 5 of 5 in every pass.**
  - The fifteen medians fell from 64.7–92.3 ms to 16.9–21.2 ms, about a
    fifth of what they were (4.5× faster on average).
  - The slowest median after the change, 21.2 ms, is well under the line.
- **Criteria 1–4 didn't move.**
  - `results/c1_retrieve_after.md` matches `results/c1_retrieve_before.md`
    line for line: same chunks, same order, same distances.
  - The five chunks sampled for criterion 4 are also identical.
  - Criterion 2 still has a source in all 15 answers.
- **How I know it was the change.** Same five questions, same commands, same
  power condition, and the one argument in `store.py` is the only system
  difference between the two logs. The after run also had the harder
  conditions (higher load) and was faster anyway.

**Against my prediction.** I expected 32–38 ms and got 16.9–21.2 ms, so my
estimate was too pessimistic. The reason is my own method:
- Section B of the diagnosis timed the four variants against each other in
  one loop, so every CPU pass ran straight after a CoreML pass.
- I noted there that its figures shouldn't be compared with anything outside
  that table, and then I built my prediction from them anyway.
- In `retrieve --time`, the CPU session runs on its own.

**What the two risks turned into.**
- **A load spike eating the margin** didn't happen. The after run had the
  heavier load and still stayed under 22 ms.
- **The fix being tuned to this device** is still untested. I have run it
  only on this laptop.

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## Stretch: A Second Improvement — Hybrid Search

**Declared on 2026-09-29, before any of it was built or tried.** I'm
committing this section first. The code and its run log come in later
commits.

**What I'm adding.** Keyword search alongside the embedding search, inside
`store.py::search`:

- **BM25** (`rank-bm25`, already in `requirements.txt`) over the same 122 chunk
  texts the Chroma collection stores.
- **Reciprocal rank fusion** to combine the two rankings.
  - Each chunk scores `1/(60 + its embedding rank) + 1/(60 + its BM25 rank)`,
    and the top 5 go to the model.
  - A chunk that shares no word with the question gets no BM25 term.
  - 60 is the standard constant from the paper that introduced reciprocal
    rank fusion. I'm not tuning it.
- **Real cosine distances on every returned chunk**, so the relevance gate
  still compares the same kind of number against 0.65.
- **A switch, `AI201_HYBRID=0`**, which brings back the vector-only search the
  after run measured, so that log stays reproducible.

**Why rank fusion rather than a weighted score.** These are the factors I
weighed before choosing. It's reasoning, not measurement: I haven't run
either method.

| Factor | Reciprocal rank fusion (chosen) | Weighted score fusion |
|---|---|---|
| What it computes | `1/(60 + embedding rank) + 1/(60 + BM25 rank)`. Only the order within each list counts. | Both scores rescaled to 0–1 for each question (for example, min-max), then `α × embedding + (1 − α) × BM25`. |
| Settings to choose | One constant, k = 60, the published default. | The weight α and the rescaling method, both normally tuned. |
| Data needed to set them | None. | Labelled questions. The only ones I have are my five test questions, and tuning on them would be fitting the test. |
| Mismatched scales (cosine distance runs 0–2; BM25 is unbounded and changes with every question) | Never compared, because only ranks are used. | Must be reconciled for each question, so the same α weighs keywords differently from one question to the next. |
| The size of a lead | Lost. A chunk far ahead counts the same as one barely ahead. The grade-appeal answer sits at 0.2025 and the next chunk at 0.6133. | Kept. A big semantic or keyword lead stays big. |
| Rare words in this corpus ("Atrium" in 2 of 88 documents, "dining" in 4, "good" in 8) | A strong keyword match can move a chunk by at most 1/61 ≈ 0.016, so its effect has a ceiling. | After rescaling, the few chunks that share a rare word take most of the BM25 range. That could lift the Atrium answer further, and it could lift the Pellew "dining" posts just as hard. |
| A question that shares no word with any chunk | BM25 adds nothing, and the result is the embedding ranking. | Min-max rescaling divides by zero and needs a special case. |
| Criteria 2–5 | **3 can't get worse:** the gate reads the best real distance among the 5 returned, and that can never be lower than the best overall. **4 is untouched:** chunking doesn't change. **2** depends on which chunks reach the model. **5** pays for one BM25 pass. | Same, plus a few arithmetic steps for the rescaling. |
| Where it's known to do well | As an untuned default across very different datasets. That's the finding of the 2009 paper that introduced it (Cormack, Clarke and Büttcher). | With α tuned on labelled questions. A 2023 comparison (Bruch, Gai and Ingber) found it then beats rank fusion. |

Both are defensible. Weighted fusion might even move the Atrium chunk
further, because it keeps the size of BM25's lead for a chunk that matches
two rare words.

I chose rank fusion because it's the one I can run honestly with what I have.
- It needs no tuning. Any α I picked would come from my five test questions,
  and choosing it after seeing their results is exactly the loosening this
  unit warns against.
- It also caps how far one rare-word match can move a chunk, and on this
  corpus that's the risk I worry about most.

A fair test of weighted fusion needs a separate set of labelled questions to
tune α on. I don't have one, so it stays a follow-up rather than part of this
measurement.

**Why this, and what it's meant to fix.** After the first improvement nothing
is missed, so this targets the thinnest margin left in my run logs.
- Criterion 1's Atrium question passes only because its answer chunk
  (`dining_the_atrium.txt#0`, *"genuinely good sandwiches restocked twice a
  day"*) comes back at **rank 4 of 5**, behind the hours chunk and two
  follow-up chunks.
- Two of the question's words point straight at that chunk.
  - "Atrium" appears in only 2 of the 88 documents.
  - "good" appears in 8 documents, and among the Atrium's posts only in the
    answer chunk.
- The milestone says hybrid search helps "when your questions contain names,
  numbers, or exact terms that semantic search glides past". "Good" next to
  "Atrium" is that kind of term.

**How I'll judge it, decided now.**
- **It helped** if the Atrium answer chunk moves above rank 4 and no other
  question's answer chunk drops out of the top 5.
- **Evidence:** the `app.py retrieve` ranks for all five questions, plus a
  third run log, labelled `after2`, with all five criteria, three runs each,
  in the same condition as the other two.

**What could go wrong, predicted before building.**
- **"dining" pulls in the wrong posts.** The word is in 4 documents, and none
  of them is the Atrium's: the two Pellew Dining Hall posts, the
  dining-dollars post and a jobs post. BM25 could lift those into the top 5.
- **The follow-up post rises instead of the answer.** It repeats "The Atrium"
  and "what people have said about", so it shares more of the question's
  words than the answer chunk does.
- **Another question loses its answer.** Fusion could push a correct
  embedding hit out of the top 5, which would cost criterion 1.
- **The gate sees a worse best distance.** If fusion drops the embedding's
  closest chunk, the gate's best distance goes up. For an in-corpus question
  that could mean a refusal.
- **Criterion 5 pays for the extra scoring.** It should be a few milliseconds
  against a 50 ms line, but I'll measure it rather than assume.

*Everything below was added after the build. The declaration above is
unchanged.*

### Run Log — After 2 (hybrid search)

The code is in `store.py` (`search`, `_fuse`, `_keyword_index`, `_tokens`) and
`config.py` (`HYBRID_SEARCH`). It's built exactly as declared above, with
nothing tuned after seeing results.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks begin with their title line | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Retrieval median under 50 ms, per question | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Where each row comes from.** The commands, counting and condition are the
same as the other two logs. The files are labelled `after2`:

- **Rows 1–3:** `results/run_2026-09-29_1610_after2.md`, from 15 real model
  calls with none served from cache.
- **Row 4:** `results/c4_chunks_after2.md`.
- **Row 5:** `results/c5_timing_after2.md`, on battery with Low Power Mode on,
  load average 2.6–3.0.
- **Ranks behind row 1:** `results/c1_retrieve_after2.md`.

Real output: the Atrium question with hybrid search on, from
`python app.py retrieve "What is good about dining at the Atrium?"`
(`app.py::cmd_retrieve` → `store.py::search` → `store.py::_fuse`), in
`results/c1_retrieve_after2.md`. The rows are now in fused order, so the
distances no longer rise down the column.

```text
Question: What is good about dining at the Atrium?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4324     dining_the_atrium_followup.txt   Re: The Atrium  Adding to what people have said abou...
2   0.5275     dining_the_atrium_followup.txt   Re: The Atrium  Also worth saying: picked clean by 1...
3   0.5311     dining_the_atrium.txt            The Atrium  Transferred in last year, so take this w...
4   0.5978     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Adding to what people have s...
5   0.5412     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.432 is under the 0.65 cutoff
```

**Did it help?** Yes, by the test I set before building. But only narrowly,
and at a price.

The test was whether the Atrium answer chunk moves above rank 4 while no other
answer chunk drops out of the top 5. Here's where each question's answer chunk
ranked with the embedding only (the after log) and with hybrid search
(after2):

| Question | Answer chunk | Rank, embedding only | Rank, hybrid |
|---|---|---|---|
| When does a grade appeal go to the department? | `admin_grade_appeals.txt#0` | 1 | 1 |
| How to get an urgent health appointment? | `health_center.txt#0` | 1 | 1 |
| What are the assessments for Linear Algebra? | `course_math_220.txt#0` | 2 | 3 |
| When does Halden Hall close? | `dining_halden_hall_followup.txt#1` (also `dining_halden_hall.txt#0`) | 1 (and 3) | 1 (and 4) |
| What is good about dining at the Atrium? | `dining_the_atrium.txt#0` | **4** | **3** |

- **The test passes.** The Atrium answer moved from rank 4 to rank 3, and
  every answer chunk stayed in the top 5.
  - The margin that mattered closed: with a top-3 cutoff, the embedding-only
    search finds 4 of 5 answers and the hybrid finds all 5.
- **But not for the reason I predicted.** I expected BM25 to reward "good"
  and lift the answer chunk. It didn't.
  - By keywords alone, the answer chunk ranks only 4th. First is a Pellew
    follow-up chunk, which shares "dining", "at", "about" and "what".
  - The answer moved up because the chunk above it fell away. The Atrium's
    hours chunk, the embedding's first, shares only "atrium" and "the" with
    the question. It ranks 14th by keywords and dropped out of the top 5.
  - The ranks, keyword ranks, word weights and fused scores behind this
    section are in `results/hybrid_breakdown.md`, which lists the script that
    produced them.
- **Every criterion is still MET.** Criterion 5 paid about 2 ms: medians went
  from 16.9–21.2 ms (after) to 19.5–22.5 ms (after2), even though the load
  was lower this time (2.6–3.0 against 4.3–4.8).

**How the risks I predicted before building turned out.** Three of the five
came true.

- **The follow-up post rose instead of the answer:** came true. The Atrium
  follow-up's two chunks are now ranks 1 and 2. One shares "atrium", "about"
  and "what" with the question, and the other "atrium" and "at". The answer
  chunk shares "atrium" and "good".
- **"dining" pulled in the wrong posts:** came true. Both Pellew Dining Hall
  follow-up chunks are now in the Atrium top 5, at ranks 4 and 5.
- **The gate sees a worse best distance:** came true, but harmlessly.
  - Fusion dropped the Atrium's hours chunk, which was the embedding's
    closest at 0.4126, so the best distance the gate sees rose to 0.4324.
    That's still far under 0.65.
  - Two out-of-corpus questions moved the same way. Mongolia went from 0.825
    to 0.826 and the diesel engine from 0.923 to 0.934, and both are still
    refused.
- **Another question loses its answer:** didn't happen. But two answer
  chunks slipped a place: Linear Algebra from 2 to 3, and Halden's second
  answer chunk from 3 to 4.
- **Criterion 5 pays for the extra scoring:** came true, at about 2 ms, as
  above.

**The side effect I didn't predict.** BM25 treats question words as keywords,
because in this corpus they're rare.
- The posts are statements, so "when", "how", "get" and "an" appear in few
  chunks and get high weights: 3.53 for "when" and 3.88 for "how" and "an",
  against 0.90 for "the".
- That pulled chunks with nothing to do with the question into the context.
  - The grade-appeal top 5 now includes `transit_shuttle.txt#1` at rank 2.
    The embedding ranks it 25th (distance 0.8006), but BM25 ranks it 2nd
    because it shares "when", along with "the" and "a".
  - The health top 5 now includes `advising_registration.txt#0` (0.7717,
    sharing "an" and "get").
- The answers didn't suffer: all 15 are still correct and sourced. The
  grounding instruction and the rank-1 chunk carried them. But the model is
  now given more irrelevant text than before.

**Is it worth keeping?** It's on in the committed system, and by my own test
it earned that: one real rank gain where the margin was thinnest, and no
criterion lost. Put plainly, it helped the question it was aimed at and added
noise everywhere else.

The obvious next step is keeping question words out of BM25's input with a
stopword list. I haven't done it. It would be a third change, and I'd be
tuning it on the same five questions.

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
