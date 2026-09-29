# Criterion 1 support — retrieval ranks (after)

Produced by `python app.py retrieve "<question>"` (`app.py::cmd_retrieve` → `store.py::search`), once per question in `QUESTIONS`. Retrieval is deterministic, so one pass is the whole measurement. The three run values for criterion 1 are the `scorer.py::judge` marks in the `run_eval.py` log.

- When: 2026-09-29 15:31:22
- Machine: Apple M4, 10 cores, macOS 26.6.2
- Power: Now drawing from 'Battery Power'; Low Power Mode on
- Load average (1/5/15 min): { 4.36 5.97 4.90 }

## When does a grade appeal go to the department?

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

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

## How to get an urgent health appointment?

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

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

## What are the assessments for Linear Algebra?

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

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

## When does Halden Hall close?

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

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

## What is good about dining at the Atrium?

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

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```
