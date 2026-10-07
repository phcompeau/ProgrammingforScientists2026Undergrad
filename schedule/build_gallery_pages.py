"""
Build the gallery pages of the 02-120 course site from the gallery READMEs in
Finished Code, so each page and its README always list the same runs and
commands:
    docs/cellular-automata.html  from  Finished Code/python/src/cellular_automata/README.md
    docs/gravity.html            from  Finished Code/python/src/gravity/README.md

The page plays web copies of the videos from docs/gallery/<name>/ (GitHub serves
the repository's MP4s as downloads, so they cannot play in a page); each card
still links to the original on GitHub.

Usage (from schedule/): python3 build_gallery_pages.py ..
"""
import html
import re
import sys

BASE = "https://github.com/phcompeau/ProgrammingforScientists2026Undergrad"

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
<meta name="description" content="@@DESC@@">
<title>@@TITLE@@</title>
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
  .card .media { display: block; background: @@MEDIA_BG@@; border-radius: 4px; overflow: hidden; aspect-ratio: 1 / 1; }
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
  .media { cursor: zoom-in; }
  .watch a { cursor: pointer; }
  .lightbox {
    position: fixed; inset: 0; z-index: 10; display: none; align-items: center; justify-content: center;
    background: rgba(10, 12, 16, 0.88); padding: 16px;
  }
  .lightbox.open { display: flex; }
  .lightbox figure { margin: 0; max-width: min(92vw, 92vh); width: 100%; }
  .lightbox video { width: 100%; max-height: 84vh; display: block; background: #000; border-radius: 6px; }
  .lightbox figcaption { color: #E9ECF2; font-size: 15px; margin-top: 10px; text-align: center; }
  .lightbox figcaption a { color: #9EC3F5; }
  .lightbox .close {
    position: absolute; top: 12px; right: 16px; font: 600 30px/1 "Source Sans 3", sans-serif;
    color: #fff; background: none; border: 0; cursor: pointer; padding: 6px 10px;
  }
</style>
</head>
<body>
<div class="wrap">
"""

AUTOMATA_INTRO = """  <a class="back" href="./">&larr; 02-120 semester map</a>
  <h1>Cellular Automata Gallery</h1>
  <p class="sub">02-120 Programming for Scientists, Fall 2026 &middot; Phillip Compeau</p>

  <div class="narrow">
  <p>Every automaton on this page runs on the engine that we built in class. From one to the next, the code does not change at all; only the rule file, the starting board, and the color map do. Each preview below is a short loop; click it to play the full video.</p>

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

GRAVITY_INTRO = """  <a class="back" href="./">&larr; 02-120 semester map</a>
  <h1>Gravity Simulator Gallery</h1>
  <p class="sub">02-120 Programming for Scientists, Fall 2026 &middot; Phillip Compeau</p>

  <div class="narrow">
  <p>Every video on this page comes from the gravity simulator that we built in class. The physics engine never changes; only the starting universe in <code>data/</code> and the command-line arguments do. Each preview below is a short loop; click it to play the full video. On this page, the trails are drawn thicker than in your own videos (and the three-body videos are zoomed in) so that they show up well on the web.</p>

  <section class="box">
    <h2>Running one yourself</h2>
    <ol>
      <li>Open a terminal in your <code>python/src/gravity</code> folder.</li>
      <li>Copy a command from below and run it (use <code>python</code> instead of <code>python3</code> on Windows).</li>
      <li>Your video appears in <code>output/</code>, named after the scenario, so a new run of the same scenario replaces the old video.</li>
    </ol>
    <p style="margin:12px 0 0">The arguments are, in order: the scenario (a file in <code>data/</code>, without <code>.txt</code>), the number of generations, the time step in seconds, the canvas width in pixels, and the drawing frequency (we draw one frame every this many generations). Then try your own experiments: change the gravitational constant, a mass, or a starting velocity in a data file, and see what happens.</p>
  </section>
  </div>
"""

SCRIPT = """<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Video player">
  <button class="close" type="button" aria-label="Close">&times;</button>
  <figure>
    <video controls playsinline loop></video>
    <figcaption></figcaption>
  </figure>
</div>
<script>
  var box = document.getElementById("lightbox");
  var player = box.querySelector("video");
  var caption = box.querySelector("figcaption");
  function openVideo(event) {
    event.preventDefault();
    var link = event.currentTarget;
    player.src = link.getAttribute("data-video");
    caption.innerHTML = "";
    var title = document.createElement("span");
    title.textContent = link.getAttribute("data-title") + " \u00b7 ";
    var source = document.createElement("a");
    source.href = link.getAttribute("href");
    source.textContent = "original on GitHub";
    caption.appendChild(title);
    caption.appendChild(source);
    box.classList.add("open");
    var playing = player.play();
    if (playing !== undefined) { playing.catch(function () {}); }
  }
  function closeVideo() {
    box.classList.remove("open");
    player.pause();
    player.removeAttribute("src");
    player.load();
  }
  var openers = document.querySelectorAll("[data-video]");
  for (var k = 0; k < openers.length; k++) {
    openers[k].addEventListener("click", openVideo);
  }
  box.querySelector(".close").addEventListener("click", closeVideo);
  box.addEventListener("click", function (event) { if (event.target === box) { closeVideo(); } });
  document.addEventListener("keydown", function (event) { if (event.key === "Escape") { closeVideo(); } });
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


GALLERIES: list[dict[str, str]] = [
    {
        "folder": "Finished Code/python/src/cellular_automata",
        "out": "docs/cellular-automata.html",
        "title": "Cellular Automata Gallery",
        "description": "02-120 Programming for Scientists, Fall 2026: every cellular automaton in the starter code, with the command that runs it.",
        "first_section": "## Game of Life",
        "media_bg": "#3a3a3a",
        "intro": AUTOMATA_INTRO,
        "web": "gallery/automata",
    },
    {
        "folder": "Finished Code/python/src/gravity",
        "out": "docs/gravity.html",
        "title": "Gravity Simulator Gallery",
        "description": "02-120 Programming for Scientists, Fall 2026: Jupiter's moons and three-body orbits from our gravity simulator, with the command that runs each one.",
        "first_section": "## Jupiter's moons",
        "media_bg": "#000000",
        "intro": GRAVITY_INTRO,
        "web": "gallery/gravity",
    },
]


def inline(text: str) -> str:
    escaped = html.escape(text.strip(), quote=False)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def build_page(root: str, gallery: dict[str, str]) -> None:
    folder_path = gallery["folder"].replace(" ", "%20")
    folder_url = BASE + "/tree/main/" + folder_path
    blob = BASE + "/blob/main/" + folder_path + "/"
    web = gallery["web"] + "/"
    text = open(root + "/" + gallery["folder"] + "/README.md").read()
    body = text[text.index(gallery["first_section"]):]
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
            original = blob + "videos/" + name + ".mp4"
            video = web + name + ".mp4"
            gif = web + "previews/" + name + ".gif"
            opener = f'href="{original}" data-video="{video}" data-title="{html.escape(card_title)}"'
            parts.append(
                '    <div class="card">\n'
                f'      <a class="media" {opener}><img src="{gif}" alt="{html.escape(card_title)}" loading="lazy"></a>\n'
                f'      <h3>{html.escape(card_title)}</h3>\n'
                f'      <p>{inline(desc)}</p>\n'
                f'      <div class="cmd"><pre>{html.escape(cmd)}</pre><button type="button">Copy</button></div>\n'
                f'      <div class="watch"><a {opener}>Watch the full video</a></div>\n'
                '    </div>'
            )
            count += 1
        parts.append("  </div>")
        sections.append("\n".join(parts))
    head = HEAD.replace("@@DESC@@", gallery["description"]).replace("@@TITLE@@", gallery["title"])
    head = head.replace("@@MEDIA_BG@@", gallery["media_bg"])
    page = (head + gallery["intro"]
            + '  <nav class="toc">' + " ".join(toc) + "</nav>\n"
            + "\n".join(sections)
            + f'\n  <footer>All {count} videos, with their commands, are also in the <a href="{folder_url}">course repository</a>.</footer>\n'
            + "</div>\n" + SCRIPT + "</body>\n</html>\n")
    open(root + "/" + gallery["out"], "w").write(page)
    print(f"wrote {gallery['out']}: {count} videos, {len(page)} chars, em dashes {page.count(chr(0x2014))}")


def main() -> None:
    root = sys.argv[1]
    for gallery in GALLERIES:
        build_page(root, gallery)


if __name__ == "__main__":
    main()
