"""
Build docs/cellular-automata.html for the 02-120 course site from the gallery
README in Finished Code, so the page and the README always list the same
automata and commands.

Usage (from schedule/): python3 build_automata_page.py ..
"""
import html
import re
import sys

BASE = "https://github.com/phcompeau/ProgrammingforScientists2026Undergrad"
FOLDER = BASE + "/tree/main/Finished%20Code/python/src/cellular_automata"
BLOB = BASE + "/blob/main/Finished%20Code/python/src/cellular_automata/"
RAW = "https://raw.githubusercontent.com/phcompeau/ProgrammingforScientists2026Undergrad/main/Finished%20Code/python/src/cellular_automata/"
README = "Finished Code/python/src/cellular_automata/README.md"
OUT = "docs/cellular-automata.html"

ENTRY = re.compile(
    r"\[!\[([a-z0-9_]+)\]\(videos/previews/[a-z0-9_]+\.gif\)\]\(videos/[a-z0-9_]+\.mp4\)\n\n"
    r"\*\*\[([^\]]+)\]\(videos/[a-z0-9_]+\.mp4\)\.\*\*(.*?)\n\n```\n(.*?)\n```",
    re.S,
)

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="02-120 Programming for Scientists, Fall 2026: every cellular automaton in the starter code, with the command that runs it.">
<title>Cellular Automata Gallery</title>
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
    --ink-2: #3A3F4A;
    --muted: #6B7280;
    --rule: #E3E6EC;
    --rule-strong: #CDD2DB;
    --blue: #1F5FAD;
    --red: #B01B2E;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--ground); color: var(--ink);
    font-family: "Source Sans 3", system-ui, sans-serif; font-size: 17px; line-height: 1.6;
  }
  .wrap { max-width: 1040px; margin: 0 auto; padding: 40px 16px 64px; }
  .narrow { max-width: 760px; }
  .back { font-size: 14px; }
  a { color: var(--blue); }
  h1 { font-family: Spectral, Georgia, serif; font-weight: 600; font-size: 38px; line-height: 1.15; margin: 18px 0 4px; }
  .sub { color: var(--muted); margin: 0 0 28px; }
  h2 { font-family: Spectral, Georgia, serif; font-weight: 600; font-size: 25px; margin: 44px 0 6px; }
  p { margin: 0 0 14px; color: var(--ink-2); }
  code {
    font-family: "IBM Plex Mono", monospace; font-size: 14px; color: var(--ink);
    background: var(--surface-2); border: 1px solid var(--rule); border-radius: 3px; padding: 1px 5px;
  }
  .box {
    margin: 28px 0 0; padding: 18px 20px; background: var(--surface);
    border: 1px solid var(--rule-strong); border-left: 3px solid var(--red); border-radius: 4px;
  }
  .box h2 { margin-top: 0; font-size: 21px; }
  .box ol { margin: 0; padding-left: 22px; color: var(--ink-2); }
  .box li { margin: 0 0 6px; }
  nav.toc { margin: 22px 0 0; font-size: 15px; color: var(--muted); }
  nav.toc a { margin-right: 14px; white-space: nowrap; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(300px, 100%), 1fr)); gap: 18px; margin-top: 14px; }
  .card {
    background: var(--surface); border: 1px solid var(--rule-strong); border-radius: 6px;
    padding: 14px; display: flex; flex-direction: column; min-width: 0;
  }
  .card .media { display: block; background: #3a3a3a; border-radius: 4px; overflow: hidden; aspect-ratio: 1 / 1; }
  .card .media img { width: 100%; height: 100%; object-fit: contain; display: block; }
  .card h3 { font-family: Spectral, Georgia, serif; font-weight: 600; font-size: 19px; margin: 12px 0 2px; }
  .card p { font-size: 15px; margin: 0 0 10px; }
  .cmd { position: relative; margin-top: auto; }
  .cmd pre {
    margin: 0; padding: 10px 12px; padding-right: 64px; background: var(--surface-2);
    border: 1px solid var(--rule); border-radius: 4px; white-space: pre-wrap; word-break: break-all;
    font-family: "IBM Plex Mono", monospace; font-size: 12.5px; line-height: 1.5; color: var(--ink);
  }
  .cmd button {
    position: absolute; top: 6px; right: 6px; font: 600 12px "Source Sans 3", sans-serif;
    border: 1px solid var(--rule-strong); background: var(--surface); color: var(--ink-2);
    border-radius: 4px; padding: 3px 8px; cursor: pointer;
  }
  .cmd button:hover { border-color: var(--blue); color: var(--blue); }
  .watch { font-size: 14px; margin-top: 8px; }
  footer { margin-top: 48px; font-size: 14px; color: var(--muted); }
</style>
</head>
<body>
<div class="wrap">
"""

INTRO = """  <a class="back" href="./">&larr; 02-120 semester map</a>
  <h1>Cellular Automata Gallery</h1>
  <p class="sub">02-120 Programming for Scientists, Fall 2026 &middot; Phillip Compeau</p>

  <div class="narrow">
  <p>Every automaton on this page runs on the engine that we built in class. From one to the next, the code does not change at all; only the rule file, the starting board, and the color map do. Each preview below is a short loop; click it to watch the full video.</p>

  <section class="box">
    <h2>Running one yourself</h2>
    <ol>
      <li>Open a terminal in your <code>python/src/cellular_automata</code> folder.</li>
      <li>Copy a command from below and run it (use <code>python</code> instead of <code>python3</code> on Windows).</li>
      <li>Your video appears in <code>output/</code>.</li>
    </ol>
    <p style="margin:12px 0 0">The arguments are, in order: neighborhood type, rule file, starting board, output file (without <code>.mp4</code>), cell width in pixels, number of generations, and an optional color map. If a run is slow, lower the cell width or the number of generations. Then try making your own: write a new board, or change a few lines of a rule file, and see what happens.</p>
  </section>
  </div>
"""

SCRIPT = """<script>
  var buttons = document.querySelectorAll(".cmd button");
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", function (event) {
      var button = event.currentTarget;
      var text = button.parentNode.querySelector("pre").textContent;
      try {
        navigator.clipboard.writeText(text).then(function () {
          button.textContent = "Copied";
          setTimeout(function () { button.textContent = "Copy"; }, 1500);
        });
      } catch (err) {
        button.textContent = "Select it";
      }
    });
  }
</script>
"""


def inline(text: str) -> str:
    escaped = html.escape(text.strip(), quote=False)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def main() -> None:
    root = sys.argv[1]
    text = open(root + "/" + README).read()
    body = text[text.index("## Game of Life"):]
    sections: list[str] = []
    toc: list[str] = []
    count = 0
    for block in re.split(r"\n## ", "\n" + body)[1:]:
        lines = block.split("\n")
        title = lines[0].strip()
        rest = "\n".join(lines[1:])
        intro = rest[:rest.find("[![")].strip()
        toc.append(f'<a href="#{slug(title)}">{html.escape(title)}</a>')
        parts: list[str] = [f'  <h2 id="{slug(title)}">{html.escape(title)}</h2>']
        if intro != "":
            parts.append(f'  <p class="narrow">{inline(intro)}</p>')
        parts.append('  <div class="grid">')
        for m in ENTRY.finditer(rest):
            name, card_title, desc, cmd = m.groups()
            video = BLOB + "videos/" + name + ".mp4"
            gif = RAW + "videos/previews/" + name + ".gif"
            parts.append(
                '    <div class="card">\n'
                f'      <a class="media" href="{video}"><img src="{gif}" alt="{html.escape(card_title)}" loading="lazy"></a>\n'
                f'      <h3>{html.escape(card_title)}</h3>\n'
                f'      <p>{inline(desc)}</p>\n'
                f'      <div class="cmd"><pre>{html.escape(cmd)}</pre><button type="button">Copy</button></div>\n'
                f'      <div class="watch"><a href="{video}">Watch the full video</a></div>\n'
                '    </div>'
            )
            count += 1
        parts.append("  </div>")
        sections.append("\n".join(parts))
    page = (HEAD + INTRO
            + '  <nav class="toc">' + " ".join(toc) + "</nav>\n"
            + "\n".join(sections)
            + f'\n  <footer>All {count} videos, with their commands, are also in the <a href="{FOLDER}">course repository</a>.</footer>\n'
            + "</div>\n" + SCRIPT + "</body>\n</html>\n")
    open(root + "/" + OUT, "w").write(page)
    print(f"wrote {OUT}: {count} automata, {len(page)} chars, em dashes {page.count(chr(0x2014))}")


if __name__ == "__main__":
    main()
