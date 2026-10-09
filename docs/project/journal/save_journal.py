"""Copy this project's Claude Code session logs into journal/.

02-120 build journal hook. Claude Code runs this at the start and end of every
session in this folder. It copies every session log that Claude Code keeps for
this folder, so sessions from before you set this up are included too.
You can also run it by hand: python save_journal.py
"""

import json
import os
import re
import shutil
import sys
from pathlib import Path


def project_dir() -> Path:
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_dir:
        return Path(env_dir)
    return Path(__file__).resolve().parent.parent.parent


def read_hook_input() -> dict:
    if sys.stdin is None or sys.stdin.isatty():
        return {}
    try:
        return json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}


def log_folder(hook_input: dict, project: Path) -> Path:
    transcript_path = hook_input.get("transcript_path")
    if transcript_path:
        return Path(transcript_path).expanduser().parent
    slug = re.sub(r"[^A-Za-z0-9]", "-", str(project.resolve()))
    return Path.home() / ".claude" / "projects" / slug


def main() -> None:
    project = project_dir()
    source = log_folder(read_hook_input(), project)
    if not source.is_dir():
        print(f"save_journal: no Claude Code logs found at {source}", file=sys.stderr)
        return
    journal = project / "journal"
    journal.mkdir(exist_ok=True)
    copied_count = 0
    for log_file in sorted(source.glob("*.jsonl")):
        destination = journal / log_file.name
        if destination.exists() and destination.stat().st_size == log_file.stat().st_size:
            continue
        shutil.copy2(log_file, destination)
        copied_count += 1
    print(f"save_journal: {copied_count} session log(s) updated in {journal}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # a journal problem must never block a Claude Code session
        print(f"save_journal: {error}", file=sys.stderr)
