#!/usr/bin/env python3
"""Regenerate index.json, the OpenCode HTTP catalog for this repository.

Each root-level directory containing SKILL.md is one skill. The catalog lists
every file in that directory (relative paths) plus a version token derived from
their contents; OpenCode re-downloads a skill when its version changes.

Usage:
    python3 tools/sync_catalog.py           # write index.json
    python3 tools/sync_catalog.py --check   # fail if index.json is stale
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "index.json"
SKILL_ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
IGNORED_DIRS = {"__pycache__", "node_modules"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def skill_dirs() -> List[Path]:
    """Return root-level <skill-id>/ directories that contain SKILL.md."""
    found = []
    for child in sorted(ROOT.iterdir(), key=lambda path: path.name):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if (child / "SKILL.md").is_file():
            found.append(child)
    return found


def skill_files(directory: Path) -> List[Path]:
    """Return the files that belong to a skill, in stable order."""
    files = []
    for path in sorted(directory.rglob("*")):
        rel = path.relative_to(directory)
        if any(part in IGNORED_DIRS or part.startswith(".") for part in rel.parts):
            continue
        if path.is_dir() or not path.is_file():
            continue
        if path.suffix in IGNORED_SUFFIXES:
            continue
        files.append(path)
    return files


def build() -> Dict[str, List[Dict[str, object]]]:
    skills = []
    for directory in skill_dirs():
        name = directory.name
        if not SKILL_ID.match(name):
            raise SystemExit(
                f"invalid skill id {name!r}: use lowercase kebab-case "
                "(e.g. errepinet-cve-audit)"
            )
        digest = hashlib.sha256()
        files = []
        for path in skill_files(directory):
            rel = path.relative_to(directory).as_posix()
            files.append(rel)
            digest.update(rel.encode("utf-8"))
            digest.update(b"\0")
            digest.update(hashlib.sha256(path.read_bytes()).digest())
        skills.append(
            {
                "name": name,
                "version": digest.hexdigest()[:12],
                "files": files,
            }
        )
    return {"skills": skills}


def render(catalog: Dict[str, List[Dict[str, object]]]) -> str:
    return json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"


def main(argv: List[str]) -> int:
    catalog = build()
    if not catalog["skills"]:
        raise SystemExit(
            "no skills found: expected <skill-id>/SKILL.md at the repository root"
        )
    text = render(catalog)

    if "--check" in argv[1:]:
        current = CATALOG.read_text(encoding="utf-8") if CATALOG.is_file() else ""
        if current != text:
            print(
                "index.json is stale: run python3 tools/sync_catalog.py",
                file=sys.stderr,
            )
            return 1
        print(f"index.json is up to date ({len(catalog['skills'])} skills)")
        return 0

    CATALOG.write_text(text, encoding="utf-8")
    print(f"wrote {CATALOG.relative_to(ROOT)} ({len(catalog['skills'])} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
