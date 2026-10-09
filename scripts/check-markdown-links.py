#!/usr/bin/env python3
"""Fail if relative Markdown links do not resolve to files in this repo. """

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "ftp://", "#")


def should_skip(url: str) -> bool:
    stripped = url.strip()
    if not stripped:
        return True
    return stripped.startswith(SKIP_PREFIXES)


def iter_markdown_files() -> list[Path]:
    """Return all markdown files, skipping .git and "test_input" artefacts.

    The CI runner may contain helper / test artefacts under test_input/ that
    are not meant to be part of the documentation. Some of those may even have
    names that look like markdown files but are actually directories used for
    grouping test runs. To keep the link checker focused on real docs and avoid
    crashes like "IsADirectoryError" when a path segment is a directory, we
    explicitly skip anything under test_input/.
    """

    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        # Skip anything under .git or test_input directories.
        if ".git" in path.parts or "test_input" in path.parts:
            continue
        files.append(path)
    return files


def main() -> int:
    broken: list[str] = []
    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            raw = match.group(1).strip()
            if raw.startswith("<"):
                continue
            url = raw.split()[0].strip("<>")
            if should_skip(url):
                continue
            file_part = url.split("#", 1)[0]
            if not file_part:
                continue
            # Markdown links percent-encode spaces; decode before hitting the filesystem.
            target = (path.parent / unquote(file_part)).resolve()
            if not target.exists():
                rel = path.relative_to(ROOT).as_posix()
                broken.append(f"{rel} -> {url}")

    if broken:
        print("Broken relative Markdown links:")
        for item in broken:
            print(f"  {item}")
        return 1

    print("All relative Markdown links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
