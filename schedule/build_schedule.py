"""Build the 02-120 master schedule page from schedule.yaml.

Usage:  python3 build_schedule.py [output.html] [--fragment]

Default output is ../docs/index.html, a complete HTML document for GitHub Pages.
Pass --fragment to emit the body only, for hosts that supply their own <head>.
"""

import datetime
import html
import sys
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
DEFAULT_OUT = HERE.parent / "docs" / "index.html"

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

KIND_LABELS = {
    "lecture": "Lecture",
    "recitation": "Recitation",
    "exam": "Exam",
    "no-class": "No class",
    "deadline": "Deadline",
}

PREP_LABELS = {
    "required": "",
    "after": "After class",
    "reference": "Optional",
}


def esc(text: str) -> str:
    """Escape a string for safe inclusion in HTML."""
    return html.escape(str(text), quote=True)


def resolve_url(raw: str, links: dict[str, str]) -> str:
    """Turn a link key from the YAML into a full URL, passing real URLs through."""
    if raw in links:
        return links[raw]
    return raw


def format_date(value: datetime.date) -> str:
    """Render a date as the short form used in the date rail, e.g. 'Tue 9/1'."""
    weekday = DAY_NAMES[value.weekday()]
    return f"{weekday} {value.month}/{value.day}"


def format_minutes(total: int) -> str:
    """Render a minute count as '48 min' or '2 hr 15 min'."""
    if total < 60:
        return f"{total} min"
    hours = total // 60
    minutes = total % 60
    if minutes == 0:
        return f"{hours} hr"
    return f"{hours} hr {minutes} min"


CHALLENGE_LABELS = {
    "reading": "reading",
    "weekend": "weekend",
    "study": "study day",
    "exam": "exam day",
    "challenge": "",
}


def exam_dates(data: dict[str, Any]) -> set[datetime.date]:
    """Every date the F26 schedule actually holds an exam, plus the day before."""
    dates: set[datetime.date] = set()
    for week in data["weeks"]:
        for day in week["days"]:
            if day["kind"] == "exam":
                dates.add(day["date"])
                dates.add(day["date"] - datetime.timedelta(days=1))
    return dates


def challenges_in_week(week: dict[str, Any], challenges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Every daily challenge whose date falls inside one week."""
    inside: list[dict[str, Any]] = []
    for item in challenges:
        if week["start"] <= item["date"] <= week["end"] + datetime.timedelta(days=2):
            inside.append(item)
    return inside


def render_challenges(week: dict[str, Any], challenges: list[dict[str, Any]],
                      exams: set[datetime.date], daily: str) -> str:
    """Render one week's daily-challenge strip."""
    inside = challenges_in_week(week, challenges)
    if not inside:
        return ""
    chips: list[str] = []
    for item in inside:
        kind = item["kind"]
        if kind in ("exam", "study") and item["date"] not in exams:
            kind = "challenge"
        label = CHALLENGE_LABELS[kind]
        suffix = ""
        if label:
            suffix = f'<span class="chiptag">{esc(label)}</span>'
        chips.append(
            f'<span class="chip chip-{kind}">{esc(format_date(item["date"]))}{suffix}</span>'
        )
    return f"""
      <div class="strip">
        <a class="striplabel striplink" href="{esc(daily)}" target="_blank" rel="noopener">Daily challenges &rsaquo;</a>
        <div class="chips">{"".join(chips)}</div>
      </div>"""


def render_prepare(day: dict[str, Any], links: dict[str, str]) -> str:
    """Render the 'Prepare first' cell for one day."""
    items = day.get("prepare", [])
    if not items:
        return '<span class="none">&middot;</span>'
    pieces: list[str] = []
    previous_kind = ""
    for item in items:
        kind = item.get("kind", "required")
        label = PREP_LABELS[kind]
        if kind == previous_kind:
            label = ""
        previous_kind = kind
        text = esc(item["text"])
        if "url" in item:
            target = esc(resolve_url(item["url"], links))
            body = f'<a href="{target}" target="_blank" rel="noopener">{text}</a>'
        else:
            body = text
        badge = ""
        if "minutes" in item:
            badge = f'<span class="mins">{esc(format_minutes(item["minutes"]))}</span>'
        note = ""
        if "note" in item:
            note = f'<span class="prepnote">{esc(item["note"])}</span>'
        tag = ""
        if label:
            tag = f'<span class="tag tag-{kind}">{esc(label)}</span>'
        pieces.append(f'<li class="prep prep-{kind}">{tag}{body}{badge}{note}</li>')
    return '<ul class="preplist">' + "".join(pieces) + "</ul>"


def render_due(day: dict[str, Any], homework: str) -> str:
    """Render the 'Due' cell for one day."""
    items = day.get("due", [])
    if not items:
        return '<span class="none">&middot;</span>'
    pieces: list[str] = []
    for item in items:
        text = esc(item["text"])
        target = esc(item.get("url", homework))
        body = f'<a href="{target}" target="_blank" rel="noopener">{text}</a>'
        classes = "due"
        if item.get("flag"):
            classes = "due due-flag"
        pieces.append(f'<li class="{classes}">{body}</li>')
    return '<ul class="duelist">' + "".join(pieces) + "</ul>"


def render_class(day: dict[str, Any]) -> str:
    """Render the 'In class' cell for one day."""
    kind = day["kind"]
    if kind == "deadline":
        return '<span class="none">&middot;</span>'
    title = esc(day.get("title", ""))
    chip = ""
    if day.get("tbd"):
        chip = '<span class="tbd">to be confirmed</span>'
    detail = ""
    if day.get("detail"):
        detail = f'<div class="detail">{esc(day["detail"])}</div>'
    return f'<div class="ctitle">{title}{chip}</div>{detail}'


def render_day(day: dict[str, Any], course: dict[str, Any], links: dict[str, str]) -> str:
    """Render one dated row."""
    when = day["date"]
    kind = day["kind"]
    kind_label = KIND_LABELS[kind]
    return f"""
      <div class="row row-{kind}" data-date="{when.isoformat()}">
        <div class="cell cell-date">
          <span class="date">{esc(format_date(when))}</span>
          <span class="kind">{esc(kind_label)}</span>
        </div>
        <div class="cell cell-class"><span class="colhead">In class</span>{render_class(day)}</div>
        <div class="cell cell-prep"><span class="colhead">Before class</span>{render_prepare(day, links)}</div>
        <div class="cell cell-due"><span class="colhead">Due</span>{render_due(day, course["homework"])}</div>
      </div>"""


def render_week(week: dict[str, Any], course: dict[str, Any], links: dict[str, str],
                challenges: list[dict[str, Any]], exams: set[datetime.date]) -> str:
    """Render one week band with its header and rows."""
    note = ""
    if week.get("note"):
        note = f'<p class="wnote">{esc(week["note"])}</p>'
    rows: list[str] = []
    for day in week["days"]:
        rows.append(render_day(day, course, links))
    return f"""
    <section class="week" data-start="{week['start'].isoformat()}" data-end="{week['end'].isoformat()}">
      <header class="whead">
        <div class="wleft">
          <span class="wlabel">{esc(week['label'])}</span>
          <h2 class="wtitle">{esc(week['title'])}</h2>
        </div>
      </header>
      {note}
      {render_challenges(week, challenges, exams, course["daily"])}
      <div class="rows">
        <div class="row rowhead">
          <div class="cell">Date</div>
          <div class="cell">In class</div>
          <div class="cell">Complete before class</div>
          <div class="cell">Due</div>
        </div>{"".join(rows)}</div>
    </section>"""


def render_page(data: dict[str, Any]) -> str:
    """Render the whole schedule page."""
    course = data["course"]
    links = data["links"]
    challenges = data.get("daily_challenges", [])
    exams = exam_dates(data)
    weeks: list[str] = []
    for week in data["weeks"]:
        weeks.append(render_week(week, course, links, challenges, exams))
    stamp = datetime.date.today().strftime("%B %-d, %Y")
    return PAGE.replace("{{WEEKS}}", "".join(weeks)) \
               .replace("{{NUMBER}}", esc(course["number"])) \
               .replace("{{TITLE}}", esc(course["title"])) \
               .replace("{{TERM}}", esc(course["term"])) \
               .replace("{{LECTURE}}", esc(course["lecture_time"])) \
               .replace("{{RECITATION}}", esc(course["recitation_time"])) \
               .replace("{{NOTE}}", esc(course["note"])) \
               .replace("{{CANVAS}}", esc(course["canvas"])) \
               .replace("{{ED}}", esc(course["ed"])) \
               .replace("{{HOMEWORK}}", esc(course["homework"])) \
               .replace("{{DAILY}}", esc(course["daily"])) \
               .replace("{{REPO}}", esc(course["repo"])) \
               .replace("{{STAMP}}", esc(stamp))


PAGE = r"""<title>02-120 Semester Map</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
  :root {
    color-scheme: light;
    --ground: #F7F8FA;
    --surface: #FFFFFF;
    --surface-2: #F1F3F7;
    --ink: #171A20;
    --ink-2: #39414F;
    --muted: #5C6472;
    --rule: #DFE3E9;
    --rule-strong: #C6CDD8;
    --blue: #1F5F8B;
    --blue-soft: #E7EFF6;
    --red: #B01B2E;
    --red-soft: #FBEAEC;
    --now: #FFF8E4;
    --now-edge: #E0B348;
    --shadow: 0 1px 2px rgba(23, 26, 32, .05);
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--ground);
    color: var(--ink);
    font-family: "Source Sans 3", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 16px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
  }
  a { color: var(--blue); text-decoration-thickness: 1px; text-underline-offset: 2px; }
  a:hover { text-decoration-thickness: 2px; }
  a:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; border-radius: 2px; }

  .wrap { max-width: 1800px; margin: 0 auto; padding: 0 clamp(20px, 3vw, 44px) 96px; }

  /* ---------- masthead ---------- */
  .mast { padding: 34px 0 28px; border-bottom: 2px solid var(--ink); }
  .brand {
    display: flex; align-items: center; justify-content: space-between;
    gap: 24px; margin: 0 0 30px;
  }
  .brand img { display: block; width: auto; }
  .brand .scs { height: 44px; }
  .brand .cbd { height: 40px; }
  h1 {
    font-family: Spectral, Georgia, serif;
    font-weight: 600; font-size: clamp(32px, 5vw, 46px); line-height: 1.1;
    margin: 0 0 8px; text-wrap: balance; letter-spacing: -.01em;
  }
  .term {
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: 13px; letter-spacing: .14em; text-transform: uppercase; color: var(--muted);
    margin: 0 0 14px;
  }
  .meets {
    display: flex; flex-wrap: wrap; gap: 6px 22px;
    font-size: 15px; color: var(--ink-2); margin-bottom: 20px;
  }
  .meets span { display: inline-flex; gap: 8px; }
  .meets b { font-weight: 600; color: var(--muted); font-size: 13px;
             font-family: "IBM Plex Mono", monospace; letter-spacing: .06em; text-transform: uppercase; }
  .quick { display: flex; flex-wrap: wrap; gap: 8px; }
  .quick a {
    display: inline-block; padding: 6px 13px; border: 1px solid var(--rule-strong);
    border-radius: 999px; background: var(--surface); color: var(--ink-2);
    font-size: 14px; text-decoration: none; box-shadow: var(--shadow);
  }
  .quick a:hover { border-color: var(--blue); color: var(--blue); }
  .quick a.jump { border-color: var(--now-edge); background: var(--now); color: var(--ink); }

  .legend {
    display: flex; flex-wrap: wrap; gap: 6px 18px; padding: 26px 0 30px;
    border-bottom: 1px solid var(--rule); margin-bottom: 8px;
    font-size: 13px; color: var(--muted);
  }
  .legend span { display: inline-flex; align-items: center; gap: 7px; }
  .swatch { width: 14px; height: 3px; border-radius: 2px; display: inline-block; }

  /* ---------- weeks ---------- */
  .week { padding: 34px 0 8px; border-bottom: 1px solid var(--rule); }
  .week.now {
    background: var(--now);
    margin: 0 -18px; padding: 34px 18px 12px;
    border-radius: 6px; border-bottom-color: var(--now-edge);
  }
  .whead {
    display: flex; align-items: baseline; justify-content: space-between;
    gap: 16px; flex-wrap: wrap; margin-bottom: 14px;
  }
  .wleft { display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; }
  .wlabel {
    font-family: "IBM Plex Mono", monospace; font-size: 12px; font-weight: 500;
    letter-spacing: .12em; text-transform: uppercase; color: var(--surface);
    background: var(--ink); padding: 4px 9px; border-radius: 3px;
  }
  .week.now .wlabel { background: var(--red); }
  .wtitle {
    font-family: Spectral, Georgia, serif; font-weight: 600; font-size: 24px;
    margin: 0; letter-spacing: -.005em;
  }
  .wnote {
    margin: 0 0 14px; padding: 10px 14px; background: var(--surface-2);
    border-left: 3px solid var(--rule-strong); border-radius: 0 4px 4px 0;
    font-size: 14.5px; color: var(--ink-2); max-width: 88ch;
  }
  .nowpill {
    font-family: "IBM Plex Mono", monospace; font-size: 11px; letter-spacing: .12em;
    text-transform: uppercase; color: var(--red); border: 1px solid var(--red);
    padding: 3px 8px; border-radius: 999px;
  }

  .strip {
    display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap;
    margin: 0 0 14px; padding: 9px 12px;
    background: var(--surface); border: 1px solid var(--rule); border-radius: 5px;
  }
  .striplabel {
    font-family: "IBM Plex Mono", monospace; font-size: 10.5px; letter-spacing: .12em;
    text-transform: uppercase; color: var(--muted); white-space: nowrap;
  }
  .chips { display: flex; flex-wrap: wrap; gap: 6px; }
  .chip {
    display: inline-flex; align-items: baseline; gap: 5px;
    font-family: "IBM Plex Mono", monospace; font-size: 12px; font-variant-numeric: tabular-nums;
    padding: 3px 8px; border: 1px solid var(--rule-strong); border-radius: 3px;
    color: var(--ink-2); text-decoration: none; background: var(--ground);
  }
  .striplink { color: var(--blue); text-decoration: none; }
  .striplink:hover { text-decoration: underline; }
  .chip-weekend { border-style: dashed; }
  .chip-exam, .chip-study { border-color: var(--red); color: var(--red); background: var(--red-soft); }
  .chiptag {
    font-size: 9.5px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted);
  }
  .chip-exam .chiptag, .chip-study .chiptag { color: var(--red); }

  /* ---------- rows ---------- */
  .rows { display: flex; flex-direction: column; gap: 1px; background: var(--rule); border-radius: 5px; overflow: hidden; }
  .row {
    display: grid; grid-template-columns: 132px minmax(0, 1.25fr) minmax(0, 1.9fr) minmax(0, 0.8fr);
    gap: 20px; padding: 15px 16px 15px 13px;
    background: var(--surface); border-left: 3px solid transparent;
  }
  .row-lecture { border-left-color: var(--rule-strong); }
  .row-recitation { border-left-color: var(--blue); }
  .row-exam { border-left-color: var(--red); background: var(--red-soft); }
  .row-deadline { border-left-color: var(--red); }
  .row-no-class { border-left-color: transparent; background: var(--surface-2); }
  .row-no-class .ctitle { color: var(--muted); font-style: italic; }

  .rowhead {
    background: var(--surface-2); border-left-color: var(--rule);
    padding-top: 7px; padding-bottom: 7px;
  }
  .rowhead .cell {
    font-family: "IBM Plex Mono", monospace; font-size: 10.5px; letter-spacing: .12em;
    text-transform: uppercase; color: var(--muted);
  }
  .cell-date { display: flex; flex-direction: column; gap: 3px; }
  .date {
    font-family: "IBM Plex Mono", monospace; font-size: 15px; font-weight: 500;
    font-variant-numeric: tabular-nums; color: var(--ink);
  }
  .kind {
    font-family: "IBM Plex Mono", monospace; font-size: 10.5px; letter-spacing: .1em;
    text-transform: uppercase; color: var(--muted);
  }
  .row-exam .kind, .row-deadline .kind { color: var(--red); }

  .colhead { display: none; }
  .ctitle { font-weight: 600; font-size: 15.5px; }
  .detail { color: var(--muted); font-size: 14.5px; margin-top: 3px; max-width: 60ch; }
  .none { color: var(--rule-strong); }

  ul.preplist, ul.duelist { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 7px; }
  .prep, .due { font-size: 14.5px; line-height: 1.42; max-width: 72ch; }
  .prep-reference, .prep-after { color: var(--muted); }
  .tag {
    font-family: "IBM Plex Mono", monospace; font-size: 9.5px; letter-spacing: .1em;
    text-transform: uppercase; padding: 2px 6px; border-radius: 3px;
    background: var(--surface-2); color: var(--muted); margin-right: 7px;
    border: 1px solid var(--rule); vertical-align: 1px;
  }
  .prepnote { display: block; color: var(--muted); font-size: 13.5px; margin-top: 2px; }
  .mins {
    font-family: "IBM Plex Mono", monospace; font-size: 12px; color: var(--muted);
    font-variant-numeric: tabular-nums; margin-left: 7px; white-space: nowrap;
  }
  .due { color: var(--red); font-weight: 600; }
  .due a { color: var(--red); }
  .due-flag { font-weight: 600; }
  .tbd {
    font-family: "IBM Plex Mono", monospace; font-size: 10px; letter-spacing: .08em;
    text-transform: uppercase; color: var(--muted); border: 1px dashed var(--rule-strong);
    padding: 2px 6px; border-radius: 3px; margin-left: 9px; vertical-align: 2px; font-weight: 400;
  }

  footer {
    padding: 34px 0 0; color: var(--muted); font-size: 13.5px;
    display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap;
  }
  footer .stamp { font-family: "IBM Plex Mono", monospace; font-variant-numeric: tabular-nums; }

  @media (max-width: 920px) {
    .brand { gap: 16px; }
    .brand .scs { height: 32px; }
    .brand .cbd { height: 29px; }
    .row { grid-template-columns: 1fr; gap: 10px; padding: 16px 14px 18px 13px; }
    .cell-date { flex-direction: row; align-items: baseline; gap: 10px; }
    .colhead {
      display: block; font-family: "IBM Plex Mono", monospace; font-size: 10px;
      letter-spacing: .12em; text-transform: uppercase; color: var(--muted); margin-bottom: 4px;
    }
    .cell-class .colhead { display: none; }
    .cell-prep:has(.none), .cell-due:has(.none) { display: none; }
    .rowhead { display: none; }
    .whead { flex-direction: column; align-items: flex-start; gap: 8px; }
  }
</style>

<div class="wrap">
  <header class="mast">
    <div class="brand">
      <img class="scs" src="assets/cmu-scs.png" alt="Carnegie Mellon University School of Computer Science">
      <img class="cbd" src="assets/cbd.png" alt="Computational Biology Department">
    </div>
    <h1>{{NUMBER}} {{TITLE}}</h1>
    <p class="term">{{TERM}}</p>
    <div class="meets">
      <span><b>Lecture</b>{{LECTURE}}</span>
      <span><b>Recitation</b>{{RECITATION}}</span>
    </div>
    <nav class="quick">
      <a class="jump" href="#now" id="jumpnow">Jump to this week</a>
      <a href="{{CANVAS}}" target="_blank" rel="noopener">Canvas</a>
      <a href="{{ED}}" target="_blank" rel="noopener">Ed Discussion</a>
      <a href="{{HOMEWORK}}" target="_blank" rel="noopener">Homework autograders</a>
      <a href="{{DAILY}}" target="_blank" rel="noopener">Daily challenges</a>
      <a href="https://programmingforlovers.com" target="_blank" rel="noopener">Code alongs</a>
      <a href="{{REPO}}" target="_blank" rel="noopener">Course code</a>
    </nav>
  </header>

  <div class="legend">
    <span><i class="swatch" style="background:var(--rule-strong)"></i>Lecture</span>
    <span><i class="swatch" style="background:var(--blue)"></i>Recitation</span>
    <span><i class="swatch" style="background:var(--red)"></i>Exam or deadline</span>
    <span>{{NOTE}}</span>
  </div>

  {{WEEKS}}

  <footer>
    <span>Recitation topics beyond Sorting II are announced closer to the date. Items marked <em>to be confirmed</em> are not yet final, and daily-challenge dates are provisional.</span>
    <span class="stamp">Updated {{STAMP}}</span>
  </footer>
</div>

<script>
  (function () {
    var today = new Date();
    var iso = today.getFullYear() + "-" +
              String(today.getMonth() + 1).padStart(2, "0") + "-" +
              String(today.getDate()).padStart(2, "0");
    var weeks = document.querySelectorAll(".week");
    var current = null;
    for (var i = 0; i < weeks.length; i++) {
      var week = weeks[i];
      var start = week.getAttribute("data-start");
      var end = week.getAttribute("data-end");
      if (iso > end) {
        week.classList.add("past");
      } else if (iso >= start && iso <= end) {
        week.classList.add("now");
        current = week;
      }
    }
    if (current === null) {
      for (var j = 0; j < weeks.length; j++) {
        if (!weeks[j].classList.contains("past")) { current = weeks[j]; break; }
      }
    }
    if (current) {
      current.id = "now";
      var head = current.querySelector(".wleft");
      var pill = document.createElement("span");
      pill.className = "nowpill";
      pill.textContent = current.classList.contains("now") ? "this week" : "up next";
      head.appendChild(pill);
    } else {
      document.getElementById("jumpnow").style.display = "none";
    }
  })();
</script>
"""


DOCUMENT_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="02-120 Programming for Scientists, Fall 2026: the semester day by day.">
<link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20viewBox%3D%270%200%20100%20100%27%3E%3Ctext%20y%3D%27.9em%27%20font-size%3D%2790%27%3E%26%23128197%3B%3C%2Ftext%3E%3C%2Fsvg%3E">
"""


def main() -> None:
    """Read the YAML and write the HTML page."""
    data = yaml.safe_load((HERE / "schedule.yaml").read_text())
    challenge_file = HERE / "daily_challenges.yaml"
    if challenge_file.exists():
        data.update(yaml.safe_load(challenge_file.read_text()))
    arguments = []
    for value in sys.argv[1:]:
        if value != "--fragment":
            arguments.append(value)
    fragment = "--fragment" in sys.argv
    if arguments:
        out = Path(arguments[0])
    else:
        out = DEFAULT_OUT
    body = render_page(data)
    if fragment:
        page = body
    else:
        head, rest = body.split("</style>", 1)
        page = DOCUMENT_HEAD + head + "</style>\n</head>\n<body>" + rest + "\n</body>\n</html>\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    print(f"wrote {out}" + (" (fragment)" if fragment else " (full document)"))


main()
