# Criterion 5 — retrieval timing (after)

Criterion 5: for each of the five questions in `QUESTIONS`, `python app.py retrieve "<question>" --time` reports a median under 50ms across its 5 timed runs.

Produced by `python app.py retrieve "<question>" --time` (`app.py::_print_retrieval_timing`, which times `store.py::search`), for all five questions, in three separate passes. Every call is a fresh process. The medians tables are read off the timing lines above them by the capture step.

Measurement condition, fixed before the first pass and reused for every later label: the laptop as it is normally used — on battery, macOS Low Power Mode on, no apps closed for the run.

## Pass 1

- When: 2026-09-29 15:30:59
- Machine: Apple M4, 10 cores, macOS 26.6.2
- Power: Now drawing from 'Battery Power'; Low Power Mode on
- Load average (1/5/15 min): { 4.80 6.19 4.94 }

### When does a grade appeal go to the department?

```

Question: When does a grade appeal go to the department?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.2025     admin_grade_appeals.txt          On the grade appeals  A grade appeal starts with the...
2   0.6133     admin_add_drop_deadline.txt      On the add/drop deadline  You can add a course throu...
3   0.6504     admin_withdrawal_deadline.txt    On the withdrawal deadline  Withdrawal is a differen...
4   0.6540     course_stat_150.txt              STAT 150 Applied Statistics  Transferred in last yea...
5   0.6731     course_stat_150_exams.txt        STAT 150 Applied Statistics — assessment  Three equa...

Gate: best distance 0.202 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 17.4 ms   median 18.3 ms   max 18.9 ms
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
2   0.7214     dining_the_atrium_followup.txt   Re: The Atrium  Adding to what people have said abou...
3   0.7268     dining_the_atrium.txt            The Atrium  Hours are 8:00am to 6:00pm weekdays. Cos...
4   0.7350     dining_the_atrium.txt            The Atrium  Transferred in last year, so take this w...
5   0.7536     dining_verrill_street_grill.txt  Verrill Street Grill  I'm a junior and I've done thi...

Gate: best distance 0.455 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 16.8 ms   median 17.1 ms   max 18.0 ms
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
2   0.4699     course_math_220.txt              MATH 220 Linear Algebra  I lived here my sophomore y...
3   0.4934     course_math_220.txt              MATH 220 Linear Algebra  Expect 6 to 8 hours a week,...
4   0.6019     course_math_220_workload.txt     Workload for MATH 220 Linear Algebra  People keep as...
5   0.6117     course_engl_205_exams.txt        ENGL 205 Writing for the Sciences — assessment  No e...

Gate: best distance 0.426 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 16.6 ms   median 17.2 ms   max 18.8 ms
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
2   0.2869     dining_halden_hall.txt           Halden Hall  Hours are 7:30am to 7:00pm weekdays, cl...
3   0.4428     dining_halden_hall.txt           Halden Hall  I lived here my sophomore year. Wait ti...
4   0.4484     dining_halden_hall_followup.txt  Re: Halden Hall  Adding to what people have said abo...
5   0.5573     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.233 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 16.9 ms   median 17.7 ms   max 18.8 ms
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
1   0.4126     dining_the_atrium.txt            The Atrium  Hours are 8:00am to 6:00pm weekdays. Cos...
2   0.4324     dining_the_atrium_followup.txt   Re: The Atrium  Adding to what people have said abou...
3   0.5275     dining_the_atrium_followup.txt   Re: The Atrium  Also worth saying: picked clean by 1...
4   0.5311     dining_the_atrium.txt            The Atrium  Transferred in last year, so take this w...
5   0.5412     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.413 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 17.0 ms   median 17.7 ms   max 19.6 ms
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
| When does a grade appeal go to the department? | 18.3 | yes |
| How to get an urgent health appointment? | 17.1 | yes |
| What are the assessments for Linear Algebra? | 17.2 | yes |
| When does Halden Hall close? | 17.7 | yes |
| What is good about dining at the Atrium? | 17.7 | yes |

**Pass 1: 5 of 5 under 50 ms.**

## Pass 2

- When: 2026-09-29 15:31:07
- Machine: Apple M4, 10 cores, macOS 26.6.2
- Power: Now drawing from 'Battery Power'; Low Power Mode on
- Load average (1/5/15 min): { 4.66 6.14 4.93 }

### When does a grade appeal go to the department?

```

Question: When does a grade appeal go to the department?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.2025     admin_grade_appeals.txt          On the grade appeals  A grade appeal starts with the...
2   0.6133     admin_add_drop_deadline.txt      On the add/drop deadline  You can add a course throu...
3   0.6504     admin_withdrawal_deadline.txt    On the withdrawal deadline  Withdrawal is a differen...
4   0.6540     course_stat_150.txt              STAT 150 Applied Statistics  Transferred in last yea...
5   0.6731     course_stat_150_exams.txt        STAT 150 Applied Statistics — assessment  Three equa...

Gate: best distance 0.202 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 18.2 ms   median 19.0 ms   max 22.8 ms
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
2   0.7214     dining_the_atrium_followup.txt   Re: The Atrium  Adding to what people have said abou...
3   0.7268     dining_the_atrium.txt            The Atrium  Hours are 8:00am to 6:00pm weekdays. Cos...
4   0.7350     dining_the_atrium.txt            The Atrium  Transferred in last year, so take this w...
5   0.7536     dining_verrill_street_grill.txt  Verrill Street Grill  I'm a junior and I've done thi...

Gate: best distance 0.455 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 18.2 ms   median 21.2 ms   max 23.5 ms
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
2   0.4699     course_math_220.txt              MATH 220 Linear Algebra  I lived here my sophomore y...
3   0.4934     course_math_220.txt              MATH 220 Linear Algebra  Expect 6 to 8 hours a week,...
4   0.6019     course_math_220_workload.txt     Workload for MATH 220 Linear Algebra  People keep as...
5   0.6117     course_engl_205_exams.txt        ENGL 205 Writing for the Sciences — assessment  No e...

Gate: best distance 0.426 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 17.1 ms   median 18.2 ms   max 18.4 ms
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
2   0.2869     dining_halden_hall.txt           Halden Hall  Hours are 7:30am to 7:00pm weekdays, cl...
3   0.4428     dining_halden_hall.txt           Halden Hall  I lived here my sophomore year. Wait ti...
4   0.4484     dining_halden_hall_followup.txt  Re: Halden Hall  Adding to what people have said abo...
5   0.5573     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.233 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 17.9 ms   median 18.6 ms   max 18.7 ms
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
1   0.4126     dining_the_atrium.txt            The Atrium  Hours are 8:00am to 6:00pm weekdays. Cos...
2   0.4324     dining_the_atrium_followup.txt   Re: The Atrium  Adding to what people have said abou...
3   0.5275     dining_the_atrium_followup.txt   Re: The Atrium  Also worth saying: picked clean by 1...
4   0.5311     dining_the_atrium.txt            The Atrium  Transferred in last year, so take this w...
5   0.5412     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.413 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 17.2 ms   median 17.6 ms   max 18.4 ms
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
| When does a grade appeal go to the department? | 19.0 | yes |
| How to get an urgent health appointment? | 21.2 | yes |
| What are the assessments for Linear Algebra? | 18.2 | yes |
| When does Halden Hall close? | 18.6 | yes |
| What is good about dining at the Atrium? | 17.6 | yes |

**Pass 2: 5 of 5 under 50 ms.**

## Pass 3

- When: 2026-09-29 15:31:14
- Machine: Apple M4, 10 cores, macOS 26.6.2
- Power: Now drawing from 'Battery Power'; Low Power Mode on
- Load average (1/5/15 min): { 4.33 6.02 4.90 }

### When does a grade appeal go to the department?

```

Question: When does a grade appeal go to the department?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.2025     admin_grade_appeals.txt          On the grade appeals  A grade appeal starts with the...
2   0.6133     admin_add_drop_deadline.txt      On the add/drop deadline  You can add a course throu...
3   0.6504     admin_withdrawal_deadline.txt    On the withdrawal deadline  Withdrawal is a differen...
4   0.6540     course_stat_150.txt              STAT 150 Applied Statistics  Transferred in last yea...
5   0.6731     course_stat_150_exams.txt        STAT 150 Applied Statistics — assessment  Three equa...

Gate: best distance 0.202 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 16.6 ms   median 17.9 ms   max 18.5 ms
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
2   0.7214     dining_the_atrium_followup.txt   Re: The Atrium  Adding to what people have said abou...
3   0.7268     dining_the_atrium.txt            The Atrium  Hours are 8:00am to 6:00pm weekdays. Cos...
4   0.7350     dining_the_atrium.txt            The Atrium  Transferred in last year, so take this w...
5   0.7536     dining_verrill_street_grill.txt  Verrill Street Grill  I'm a junior and I've done thi...

Gate: best distance 0.455 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 16.5 ms   median 16.9 ms   max 18.6 ms
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
2   0.4699     course_math_220.txt              MATH 220 Linear Algebra  I lived here my sophomore y...
3   0.4934     course_math_220.txt              MATH 220 Linear Algebra  Expect 6 to 8 hours a week,...
4   0.6019     course_math_220_workload.txt     Workload for MATH 220 Linear Algebra  People keep as...
5   0.6117     course_engl_205_exams.txt        ENGL 205 Writing for the Sciences — assessment  No e...

Gate: best distance 0.426 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 17.6 ms   median 18.4 ms   max 18.5 ms
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
2   0.2869     dining_halden_hall.txt           Halden Hall  Hours are 7:30am to 7:00pm weekdays, cl...
3   0.4428     dining_halden_hall.txt           Halden Hall  I lived here my sophomore year. Wait ti...
4   0.4484     dining_halden_hall_followup.txt  Re: Halden Hall  Adding to what people have said abo...
5   0.5573     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.233 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 20.1 ms   median 20.3 ms   max 21.3 ms
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
1   0.4126     dining_the_atrium.txt            The Atrium  Hours are 8:00am to 6:00pm weekdays. Cos...
2   0.4324     dining_the_atrium_followup.txt   Re: The Atrium  Adding to what people have said abou...
3   0.5275     dining_the_atrium_followup.txt   Re: The Atrium  Also worth saying: picked clean by 1...
4   0.5311     dining_the_atrium.txt            The Atrium  Transferred in last year, so take this w...
5   0.5412     dining_pellew_dining_hall_followup.txt Re: Pellew Dining Hall  Also worth saying: the furth...

Gate: best distance 0.413 is under the 0.65 cutoff

Retrieval timing, 5 runs after one discarded warm-up:
  min 16.8 ms   median 18.1 ms   max 24.5 ms
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
| When does a grade appeal go to the department? | 17.9 | yes |
| How to get an urgent health appointment? | 16.9 | yes |
| What are the assessments for Linear Algebra? | 18.4 | yes |
| When does Halden Hall close? | 20.3 | yes |
| What is good about dining at the Atrium? | 18.1 | yes |

**Pass 3: 5 of 5 under 50 ms.**
