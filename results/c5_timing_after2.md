# Criterion 5 — retrieval timing (after2)

Criterion 5: for each of the five questions in `QUESTIONS`, `python app.py retrieve "<question>" --time` reports a median under 50ms across its 5 timed runs.

Produced by `python app.py retrieve "<question>" --time` (`app.py::_print_retrieval_timing`, which times `store.py::search`), for all five questions, in three separate passes. Every call is a fresh process. The medians tables are read off the timing lines above them by the capture step.

Measurement condition, fixed before the first pass and reused for every later label: the laptop as it is normally used — on battery, macOS Low Power Mode on, no apps closed for the run.

## Pass 1

- When: 2026-09-29 16:10:20
- Machine: Apple M4, 10 cores, macOS 26.6.2
- Power: Now drawing from 'Battery Power'; Low Power Mode on
- Load average (1/5/15 min): { 2.71 2.43 2.47 }

### When does a grade appeal go to the department?

```

Question: When does a grade appeal go to the department?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.2025     admin_grade_appeals.txt          On the grade appeals  A grade appeal starts with the...
2   0.8006     transit_shuttle.txt              The campus shuttle  It's free with a student ID. The...
3   0.7217     course_stat_150.txt              STAT 150 Applied Statistics  Expect 5 to 6 hours a w...
4   0.6504     admin_withdrawal_deadline.txt    On the withdrawal deadline  Withdrawal is a differen...
5   0.7823     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Adding to what people have s...

Gate: best distance 0.202 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 20.1 ms   median 21.5 ms   max 22.8 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### How to get an urgent health appointment?

```

Question: How to get an urgent health appointment?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4552     health_center.txt                The health centre  Walk-in hours are 8am to 11am; ev...
2   0.7643     dining_verrill_street_grill_followup.txt Re: Verrill Street Grill  Also worth saying: one reg...
3   0.7536     dining_verrill_street_grill.txt  Verrill Street Grill  I'm a junior and I've done thi...
4   0.7717     advising_registration.txt        Registration and your adviser  You need an adviser h...
5   0.8004     course_econ_101.txt              ECON 101 Introduction to Economics  The one piece of...

Gate: best distance 0.455 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 18.9 ms   median 19.8 ms   max 29.5 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### What are the assessments for Linear Algebra?

```

Question: What are the assessments for Linear Algebra?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4264     course_math_220_exams.txt        MATH 220 Linear Algebra — assessment  Two midterms a...
2   0.4934     course_math_220.txt              MATH 220 Linear Algebra  Expect 6 to 8 hours a week,...
3   0.4699     course_math_220.txt              MATH 220 Linear Algebra  I lived here my sophomore y...
4   0.6019     course_math_220_workload.txt     Workload for MATH 220 Linear Algebra  People keep as...
5   0.6397     course_cs_210_exams.txt          CS 210 Data Structures — assessment  Two midterms an...

Gate: best distance 0.426 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 19.2 ms   median 19.5 ms   max 21.3 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### When does Halden Hall close?

```

Question: When does Halden Hall close?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.2326     dining_halden_hall_followup.txt  Re: Halden Hall  Also worth saying: closes at 7:00pm...
2   0.4484     dining_halden_hall_followup.txt  Re: Halden Hall  Adding to what people have said abo...
3   0.2869     dining_halden_hall.txt           Halden Hall  Hours are 7:30am to 7:00pm weekdays, cl...
4   0.4428     dining_halden_hall.txt           Halden Hall  I lived here my sophomore year. Wait ti...
5   0.5573     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.233 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 18.9 ms   median 19.6 ms   max 20.8 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### What is good about dining at the Atrium?

```

Question: What is good about dining at the Atrium?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4324     dining_the_atrium_followup.txt   Re: The Atrium  Adding to what people have said abou...
2   0.5275     dining_the_atrium_followup.txt   Re: The Atrium  Also worth saying: picked clean by 1...
3   0.5311     dining_the_atrium.txt            The Atrium  Transferred in last year, so take this w...
4   0.5978     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Adding to what people have s...
5   0.5412     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.432 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 19.3 ms   median 20.7 ms   max 22.0 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### Medians — pass 1

| Question | Median (ms) | Under 50 ms? |
|---|---|---|
| When does a grade appeal go to the department? | 21.5 | yes |
| How to get an urgent health appointment? | 19.8 | yes |
| What are the assessments for Linear Algebra? | 19.5 | yes |
| When does Halden Hall close? | 19.6 | yes |
| What is good about dining at the Atrium? | 20.7 | yes |

**Pass 1: 5 of 5 under 50 ms.**

## Pass 2

- When: 2026-09-29 16:10:27
- Machine: Apple M4, 10 cores, macOS 26.6.2
- Power: Now drawing from 'Battery Power'; Low Power Mode on
- Load average (1/5/15 min): { 2.57 2.41 2.46 }

### When does a grade appeal go to the department?

```

Question: When does a grade appeal go to the department?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.2025     admin_grade_appeals.txt          On the grade appeals  A grade appeal starts with the...
2   0.8006     transit_shuttle.txt              The campus shuttle  It's free with a student ID. The...
3   0.7217     course_stat_150.txt              STAT 150 Applied Statistics  Expect 5 to 6 hours a w...
4   0.6504     admin_withdrawal_deadline.txt    On the withdrawal deadline  Withdrawal is a differen...
5   0.7823     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Adding to what people have s...

Gate: best distance 0.202 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 19.0 ms   median 20.1 ms   max 20.9 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### How to get an urgent health appointment?

```

Question: How to get an urgent health appointment?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4552     health_center.txt                The health centre  Walk-in hours are 8am to 11am; ev...
2   0.7643     dining_verrill_street_grill_followup.txt Re: Verrill Street Grill  Also worth saying: one reg...
3   0.7536     dining_verrill_street_grill.txt  Verrill Street Grill  I'm a junior and I've done thi...
4   0.7717     advising_registration.txt        Registration and your adviser  You need an adviser h...
5   0.8004     course_econ_101.txt              ECON 101 Introduction to Economics  The one piece of...

Gate: best distance 0.455 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 19.0 ms   median 19.9 ms   max 20.7 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### What are the assessments for Linear Algebra?

```

Question: What are the assessments for Linear Algebra?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4264     course_math_220_exams.txt        MATH 220 Linear Algebra — assessment  Two midterms a...
2   0.4934     course_math_220.txt              MATH 220 Linear Algebra  Expect 6 to 8 hours a week,...
3   0.4699     course_math_220.txt              MATH 220 Linear Algebra  I lived here my sophomore y...
4   0.6019     course_math_220_workload.txt     Workload for MATH 220 Linear Algebra  People keep as...
5   0.6397     course_cs_210_exams.txt          CS 210 Data Structures — assessment  Two midterms an...

Gate: best distance 0.426 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 19.3 ms   median 20.4 ms   max 21.1 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### When does Halden Hall close?

```

Question: When does Halden Hall close?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.2326     dining_halden_hall_followup.txt  Re: Halden Hall  Also worth saying: closes at 7:00pm...
2   0.4484     dining_halden_hall_followup.txt  Re: Halden Hall  Adding to what people have said abo...
3   0.2869     dining_halden_hall.txt           Halden Hall  Hours are 7:30am to 7:00pm weekdays, cl...
4   0.4428     dining_halden_hall.txt           Halden Hall  I lived here my sophomore year. Wait ti...
5   0.5573     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.233 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 21.4 ms   median 22.5 ms   max 27.4 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### What is good about dining at the Atrium?

```

Question: What is good about dining at the Atrium?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4324     dining_the_atrium_followup.txt   Re: The Atrium  Adding to what people have said abou...
2   0.5275     dining_the_atrium_followup.txt   Re: The Atrium  Also worth saying: picked clean by 1...
3   0.5311     dining_the_atrium.txt            The Atrium  Transferred in last year, so take this w...
4   0.5978     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Adding to what people have s...
5   0.5412     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.432 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 19.0 ms   median 19.7 ms   max 20.2 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### Medians — pass 2

| Question | Median (ms) | Under 50 ms? |
|---|---|---|
| When does a grade appeal go to the department? | 20.1 | yes |
| How to get an urgent health appointment? | 19.9 | yes |
| What are the assessments for Linear Algebra? | 20.4 | yes |
| When does Halden Hall close? | 22.5 | yes |
| What is good about dining at the Atrium? | 19.7 | yes |

**Pass 2: 5 of 5 under 50 ms.**

## Pass 3

- When: 2026-09-29 16:10:34
- Machine: Apple M4, 10 cores, macOS 26.6.2
- Power: Now drawing from 'Battery Power'; Low Power Mode on
- Load average (1/5/15 min): { 3.01 2.51 2.50 }

### When does a grade appeal go to the department?

```

Question: When does a grade appeal go to the department?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.2025     admin_grade_appeals.txt          On the grade appeals  A grade appeal starts with the...
2   0.8006     transit_shuttle.txt              The campus shuttle  It's free with a student ID. The...
3   0.7217     course_stat_150.txt              STAT 150 Applied Statistics  Expect 5 to 6 hours a w...
4   0.6504     admin_withdrawal_deadline.txt    On the withdrawal deadline  Withdrawal is a differen...
5   0.7823     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Adding to what people have s...

Gate: best distance 0.202 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 19.9 ms   median 20.9 ms   max 21.8 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### How to get an urgent health appointment?

```

Question: How to get an urgent health appointment?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4552     health_center.txt                The health centre  Walk-in hours are 8am to 11am; ev...
2   0.7643     dining_verrill_street_grill_followup.txt Re: Verrill Street Grill  Also worth saying: one reg...
3   0.7536     dining_verrill_street_grill.txt  Verrill Street Grill  I'm a junior and I've done thi...
4   0.7717     advising_registration.txt        Registration and your adviser  You need an adviser h...
5   0.8004     course_econ_101.txt              ECON 101 Introduction to Economics  The one piece of...

Gate: best distance 0.455 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 18.8 ms   median 20.0 ms   max 21.1 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### What are the assessments for Linear Algebra?

```

Question: What are the assessments for Linear Algebra?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4264     course_math_220_exams.txt        MATH 220 Linear Algebra — assessment  Two midterms a...
2   0.4934     course_math_220.txt              MATH 220 Linear Algebra  Expect 6 to 8 hours a week,...
3   0.4699     course_math_220.txt              MATH 220 Linear Algebra  I lived here my sophomore y...
4   0.6019     course_math_220_workload.txt     Workload for MATH 220 Linear Algebra  People keep as...
5   0.6397     course_cs_210_exams.txt          CS 210 Data Structures — assessment  Two midterms an...

Gate: best distance 0.426 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 20.0 ms   median 21.7 ms   max 23.0 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### When does Halden Hall close?

```

Question: When does Halden Hall close?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.2326     dining_halden_hall_followup.txt  Re: Halden Hall  Also worth saying: closes at 7:00pm...
2   0.4484     dining_halden_hall_followup.txt  Re: Halden Hall  Adding to what people have said abo...
3   0.2869     dining_halden_hall.txt           Halden Hall  Hours are 7:30am to 7:00pm weekdays, cl...
4   0.4428     dining_halden_hall.txt           Halden Hall  I lived here my sophomore year. Wait ti...
5   0.5573     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.233 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 19.1 ms   median 20.5 ms   max 21.2 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### What is good about dining at the Atrium?

```

Question: What is good about dining at the Atrium?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4324     dining_the_atrium_followup.txt   Re: The Atrium  Adding to what people have said abou...
2   0.5275     dining_the_atrium_followup.txt   Re: The Atrium  Also worth saying: picked clean by 1...
3   0.5311     dining_the_atrium.txt            The Atrium  Transferred in last year, so take this w...
4   0.5978     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Adding to what people have s...
5   0.5412     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.432 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 18.8 ms   median 20.8 ms   max 23.0 ms
  This times store.search() alone: embedding the question, then the
  Chroma lookup. It EXCLUDES process start-up, loading the embedding
  model, and the generation call — none of which happen again once
  the process is warm.

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

### Medians — pass 3

| Question | Median (ms) | Under 50 ms? |
|---|---|---|
| When does a grade appeal go to the department? | 20.9 | yes |
| How to get an urgent health appointment? | 20.0 | yes |
| What are the assessments for Linear Algebra? | 21.7 | yes |
| When does Halden Hall close? | 20.5 | yes |
| What is good about dining at the Atrium? | 20.8 | yes |

**Pass 3: 5 of 5 under 50 ms.**
