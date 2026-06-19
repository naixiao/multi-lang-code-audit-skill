#!/usr/bin/env python3
"""Minimal Codex skill validator for repository contributors."""

from __future__ import annotations

import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9-]{1,63}$")


def fail(message: str) -> int:
    print(f"Validation failed: {message}", file=sys.stderr)
    return 1


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            return None
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, body


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        return fail("usage: quick_validate.py <skill-folder>")

    skill_dir = Path(argv[1])
    skill_md = skill_dir / "SKILL.md"

    if not skill_dir.exists() or not skill_dir.is_dir():
        return fail(f"skill folder does not exist: {skill_dir}")
    if not skill_md.exists():
        return fail(f"missing SKILL.md: {skill_md}")

    text = skill_md.read_text(encoding="utf-8")
    parsed = parse_frontmatter(text)
    if parsed is None:
        return fail("SKILL.md must start with YAML frontmatter delimited by ---")

    metadata, body = parsed
    name = metadata.get("name", "")
    description = metadata.get("description", "")

    if not name:
        return fail("frontmatter missing required field: name")
    if not NAME_RE.fullmatch(name):
        return fail("name must use lowercase letters, digits, and hyphens only, max 63 chars")
    if name != skill_dir.name:
        return fail(f"name '{name}' must match skill folder '{skill_dir.name}'")
    if not description:
        return fail("frontmatter missing required field: description")
    if len(description) < 40:
        return fail("description is too short to be useful for skill discovery")
    if not body.strip():
        return fail("SKILL.md body is empty")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.exists() and not openai_yaml.read_text(encoding="utf-8").strip():
        return fail("agents/openai.yaml exists but is empty")

    print("Skill is valid!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
