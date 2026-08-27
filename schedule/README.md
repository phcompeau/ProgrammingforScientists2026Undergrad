# Semester schedule

`schedule.yaml` is the single source of truth for the 02-120 calendar: every class
meeting, what happens in it, what to complete before it, and what is due.

## Rebuilding the page

```
python3 build_schedule.py
```

That reads `schedule.yaml` plus `daily_challenges.yaml` and writes `../docs/index.html`,
which GitHub Pages serves. Commit and push, and the live page updates.

## Editing

- **A class meeting** is one entry under a week's `days:`. `kind:` is `lecture`,
  `recitation`, `exam`, `no-class`, or `deadline`.
- **Preparation** goes under `prepare:`. `kind: required` means complete it before that
  day, which is the default and the whole point of the "Complete before class" column.
  `kind: after` and `kind: reference` render with a tag and do not count toward the
  week's required-prep total.
- **Links** are keys into the `links:` block (`ca_conditionals`, `ch2_text`, ...) so a
  URL is written once. A full URL also works.
- **Due items** link to the homework autograder course unless given their own `url:`.
- **Watch times** in `minutes:` add up into each week header. They are video length; the
  page tells students to budget double.

## Daily challenges

`daily_challenges.yaml` is generated, not hand-edited. Cogniterra course 833 still carries
Fall 2025 dates; `import_daily_challenges.py` shifts them by 364 days, which preserves
every weekday and lands the fall break and Thanksgiving gaps correctly. Regenerate it
after 833 is re-dated to Fall 2026:

```
python3 import_daily_challenges.py > daily_challenges.yaml
```

Known drift until then: the challenges marked as exam and study days sit on 10/28 and
10/29, but Midterm 1 is Tuesday 10/27. The page suppresses those two labels rather than
point students at the wrong day.
