# Criterion 4 — sampled chunks (after2)

Criterion 4: all 5 of 5 chunks sampled by `python app.py chunks -n 5` begin with their source document's title line, checked by comparing each chunk's first line with the first line of its file in `corpora/campus_life/documents/`.

Produced by `python app.py chunks -n 5` (`app.py::cmd_chunks` → `chunker.py::split_documents`), run three separate times. The "First-line check" tables are added by the capture step: each chunk's first line next to `head -n 1` of its source file.

## Pass 1

- When: 2026-09-29 16:10:49
- Machine: Apple M4, 10 cores, macOS 26.6.2
- Power: Now drawing from 'Battery Power'; Low Power Mode on
- Load average (1/5/15 min): { 2.99 2.53 2.50 }

```
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

For each one, ask: could someone answer a question using only this,
without reading what came before or after?
```

### First-line check — pass 1

| Chunk | Source | Chunk's first line | `head -n 1` of source file | Same? |
|---|---|---|---|---|
| 1 | `admin_add_drop_deadline.txt#0` | On the add/drop deadline | On the add/drop deadline | yes |
| 2 | `course_cs_210_workload.txt#0` | Workload for CS 210 Data Structures | Workload for CS 210 Data Structures | yes |
| 3 | `course_phys_130_workload.txt#0` | Workload for PHYS 130 Mechanics | Workload for PHYS 130 Mechanics | yes |
| 4 | `dining_the_ridgeway_cafe_followup.txt#1` | Re: The Ridgeway Café | Re: The Ridgeway Café | yes |
| 5 | `housing_morrow_house_laundry.txt#0` | Laundry in Morrow House | Laundry in Morrow House | yes |

**Pass 1: 5 of 5 begin with their title line.**

## Pass 2

- When: 2026-09-29 16:10:49
- Machine: Apple M4, 10 cores, macOS 26.6.2
- Power: Now drawing from 'Battery Power'; Low Power Mode on
- Load average (1/5/15 min): { 2.99 2.53 2.50 }

```
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

For each one, ask: could someone answer a question using only this,
without reading what came before or after?
```

### First-line check — pass 2

| Chunk | Source | Chunk's first line | `head -n 1` of source file | Same? |
|---|---|---|---|---|
| 1 | `admin_add_drop_deadline.txt#0` | On the add/drop deadline | On the add/drop deadline | yes |
| 2 | `course_cs_210_workload.txt#0` | Workload for CS 210 Data Structures | Workload for CS 210 Data Structures | yes |
| 3 | `course_phys_130_workload.txt#0` | Workload for PHYS 130 Mechanics | Workload for PHYS 130 Mechanics | yes |
| 4 | `dining_the_ridgeway_cafe_followup.txt#1` | Re: The Ridgeway Café | Re: The Ridgeway Café | yes |
| 5 | `housing_morrow_house_laundry.txt#0` | Laundry in Morrow House | Laundry in Morrow House | yes |

**Pass 2: 5 of 5 begin with their title line.**

## Pass 3

- When: 2026-09-29 16:10:49
- Machine: Apple M4, 10 cores, macOS 26.6.2
- Power: Now drawing from 'Battery Power'; Low Power Mode on
- Load average (1/5/15 min): { 2.99 2.53 2.50 }

```
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

For each one, ask: could someone answer a question using only this,
without reading what came before or after?
```

### First-line check — pass 3

| Chunk | Source | Chunk's first line | `head -n 1` of source file | Same? |
|---|---|---|---|---|
| 1 | `admin_add_drop_deadline.txt#0` | On the add/drop deadline | On the add/drop deadline | yes |
| 2 | `course_cs_210_workload.txt#0` | Workload for CS 210 Data Structures | Workload for CS 210 Data Structures | yes |
| 3 | `course_phys_130_workload.txt#0` | Workload for PHYS 130 Mechanics | Workload for PHYS 130 Mechanics | yes |
| 4 | `dining_the_ridgeway_cafe_followup.txt#1` | Re: The Ridgeway Café | Re: The Ridgeway Café | yes |
| 5 | `housing_morrow_house_laundry.txt#0` | Laundry in Morrow House | Laundry in Morrow House | yes |

**Pass 3: 5 of 5 begin with their title line.**
