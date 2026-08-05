# Programming for Scientists (02-120), Fall 2026

Code base for **02-120: Programming for Scientists** at Carnegie Mellon University, taught by [Phillip Compeau](https://compeau.cbd.cmu.edu).

Everything we write together in class lives here. Clone this repository at the start of the semester and pull from it regularly, because we will add to it every week.

## Getting the code

If you are new to Git, the easiest path is [GitHub Desktop](https://desktop.github.com):

1. Install GitHub Desktop and sign in.
2. Choose **File > Clone Repository > URL** and paste this repository's URL.
3. Each week, press **Fetch origin** and then **Pull** to get the newest code.

From the command line:

```bash
git clone https://github.com/phcompeau/ProgrammingforScientists2026Undergrad.git
cd ProgrammingforScientists2026Undergrad
git pull        # run this before each class to get new material
```

If you edited a file and `git pull` refuses to run, the fix is almost always to copy your edited file somewhere safe, discard the change, pull, and paste your work back. Ask a TA before doing anything more clever than that.

## What is in here

| Folder | What it holds |
| --- | --- |
| `Starter Code/` | The scaffolding we start from in class and the starter files for assignments. Each subfolder is one topic. |
| `Finished Code/` | Completed versions of our in-class code-alongs, posted after we build them together. |

`Finished Code/python/src/` is organized by topic (`variables`, `for_loops`, `functions`, `bst`, and so on) and `Finished Code/xtoy/` holds our X-TOY machine programs.

**A word about `Finished Code`.** These are the demos we build together in lecture, posted so you can review them. They are not solutions to your homework. Reading a finished program is not the same as being able to write one, and the exams test the second thing.

## Running the code

Most of the course is in Python 3. Programs that write images or animations do so into an `output/` folder next to the code. Those folders start empty on purpose: generated files are not tracked here, so what you find in `output/` is whatever your own program put there.

## Getting help

- **Esme**, our course AI assistant, is available for every assignment all semester. She will explain code, ask what output you expected, and help you find where your program went wrong.
- **Office hours** are the best place for anything that has you stuck for more than a few minutes. Please come; struggling in front of us is more useful than struggling alone.
- **Course homepage** on Canvas: <https://canvas.cmu.edu/courses/55141>

The AI policy for the course lives in the syllabus and is worth reading closely, because it changes partway through the semester.
