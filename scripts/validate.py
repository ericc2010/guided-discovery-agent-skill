#!/usr/bin/env python3
"""Repository checks that the Agent Skills reference validator (skills-ref) does not cover.

skills-ref checks the frontmatter and naming rules. This script checks:
  - SKILL.md stays inside the spec's size guidance (< 500 lines, < ~5000 tokens)
  - metadata.version is semver and has a matching CHANGELOG.md entry
  - required repository files exist
  - relative Markdown links resolve

Standard library only. Usage: python3 scripts/validate.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "guided-discovery"
SKILL = SKILL_DIR / "SKILL.md"
REQUIRED = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "skills/guided-discovery/SKILL.md",
    "examples/software-architecture.md",
    "examples/product-design.md",
    "examples/business-strategy.md",
    "tests/behavior-scenarios.md",
]
MAX_LINES = 500
MAX_TOKENS = 5000  # spec guidance for the SKILL.md body
DESC_MAX = 1024

errors = []


def fail(msg):
    errors.append(msg)


for rel in REQUIRED:
    if not (ROOT / rel).is_file():
        fail(f"missing required file: {rel}")

if SKILL.is_file():
    text = SKILL.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        fail("SKILL.md: frontmatter block not found")
    else:
        front, body = match.groups()
        lines = text.count("\n") + 1
        if lines >= MAX_LINES:
            fail(f"SKILL.md: {lines} lines, spec recommends under {MAX_LINES}")
        # Rough estimate: ~4 characters per token for English prose.
        tokens = len(body) // 4
        if tokens >= MAX_TOKENS:
            fail(f"SKILL.md body: ~{tokens} tokens, spec recommends under {MAX_TOKENS}")

        desc = re.search(r"^description:\s*(.+)$", front, re.M)
        if desc and len(desc.group(1).strip()) > DESC_MAX:
            fail(f"description is {len(desc.group(1))} chars, max {DESC_MAX}")

        version = re.search(r'^\s+version:\s*"?([^"\n]+)"?\s*$', front, re.M)
        if not version:
            fail("SKILL.md: metadata.version not set")
        else:
            v = version.group(1).strip()
            if not re.fullmatch(r"\d+\.\d+\.\d+", v):
                fail(f"metadata.version '{v}' is not semver (X.Y.Z)")
            changelog = ROOT / "CHANGELOG.md"
            if changelog.is_file() and f"## [{v}]" not in changelog.read_text(encoding="utf-8"):
                fail(f"CHANGELOG.md has no '## [{v}]' entry for metadata.version")
        print(f"SKILL.md: {lines} lines, ~{tokens} body tokens")

link_re = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
for md in ROOT.rglob("*.md"):
    if any(part.startswith(".") and part != ".github" for part in md.relative_to(ROOT).parts):
        continue
    for target in link_re.findall(md.read_text(encoding="utf-8")):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        path = (md.parent / target.split("#")[0]).resolve()
        if not path.exists():
            fail(f"{md.relative_to(ROOT)}: broken link -> {target}")

if errors:
    print("FAILED")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("OK: repository checks passed")
