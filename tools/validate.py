#!/usr/bin/env python3
"""Validate every Claude-Blue skill against the repo's structure and PRINCIPLES.md.

Usage:
    python tools/validate.py                # validate the repo this script lives in
    python tools/validate.py --strict       # treat warnings as errors
    python tools/validate.py --sync-references  # refresh skills' copies of tools/references first

Exit code 0 when there are no errors, 1 otherwise. When run inside GitHub
Actions, problems are also printed as annotations so they appear on the PR.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "Skills"
README = ROOT / "README.md"
SHARED_REFS = ROOT / "tools" / "references"

CATEGORIES = {"soc", "detection", "ir", "intel", "hardening", "identity", "cloud", "people"}
NAME_RE = re.compile(r"^defensive-[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED_WORDS = ("claude", "anthropic")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_LINES = 500

# Sections every skill must have, and why (shown in the error message).
REQUIRED_SECTIONS = {
    "## Human authority": "PRINCIPLES 1 & 3: say what Claude does and does not do",
    "## Learning mode": "PRINCIPLES 4: support 'coach me'",
    "## Pitfalls": "list where models and people go wrong on this task",
}
HANDOFF_MARKER = "YOUR CALL"  # PRINCIPLES 1: hand the decision back


class Report:
    def __init__(self) -> None:
        self.errors: list[tuple[Path, str]] = []
        self.warnings: list[tuple[Path, str]] = []

    def error(self, path: Path, msg: str) -> None:
        self.errors.append((path, msg))

    def warn(self, path: Path, msg: str) -> None:
        self.warnings.append((path, msg))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_frontmatter(text: str, path: Path, report: Report) -> dict | None:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not match:
        report.error(path, "missing YAML frontmatter delimited by '---' lines at the top of the file")
        return None
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        where = f" (line {mark.line + 1}, column {mark.column + 1})" if mark else ""
        problem = getattr(exc, "problem", None) or str(exc).splitlines()[0]
        report.error(path, f"frontmatter is not valid YAML: {problem}{where}")
        return None
    if not isinstance(data, dict):
        report.error(path, "frontmatter must be a YAML mapping")
        return None
    return data


def section_body(text: str, heading: str) -> str:
    """Return the text under a '## ' heading, up to the next '## ' heading."""
    start = text.find(heading)
    if start == -1:
        return ""
    rest = text[start + len(heading):]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def check_skill(skill_md: Path, report: Report) -> str | None:
    folder = skill_md.parent
    category_dir = folder.parent.name
    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text, skill_md, report)
    if fm is None:
        return None

    # --- name ---
    name = fm.get("name")
    if not isinstance(name, str) or not name:
        report.error(skill_md, "frontmatter 'name' is missing")
    else:
        if name != folder.name:
            report.error(skill_md, f"name '{name}' must match its folder name '{folder.name}'")
        if not NAME_RE.match(name):
            report.error(skill_md, f"name '{name}' must be lowercase kebab-case starting with 'defensive-'")
        if len(name) > MAX_NAME:
            report.error(skill_md, f"name is {len(name)} characters; maximum is {MAX_NAME}")
        for word in RESERVED_WORDS:
            if word in name:
                report.error(skill_md, f"name must not contain the reserved word '{word}'")

    # --- description ---
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        report.error(skill_md, "frontmatter 'description' is missing")
    else:
        if len(desc) > MAX_DESCRIPTION:
            report.error(skill_md, f"description is {len(desc)} characters; maximum is {MAX_DESCRIPTION}")
        if "<" in desc or ">" in desc:
            report.error(skill_md, "description must not contain angle brackets")
        if "use when" not in desc.lower():
            report.warn(skill_md, "description should include 'Use when …' triggers so Claude knows when to load it")

    # --- license & metadata ---
    if fm.get("license") != "MIT":
        report.warn(skill_md, "license should be 'MIT' to match the repo")
    meta = fm.get("metadata")
    if not isinstance(meta, dict):
        report.error(skill_md, "frontmatter 'metadata' mapping is missing")
    else:
        category = meta.get("category")
        if category not in CATEGORIES:
            report.error(skill_md, f"metadata.category '{category}' must be one of: {', '.join(sorted(CATEGORIES))}")
        elif category != category_dir:
            report.error(skill_md, f"metadata.category '{category}' must match its folder Skills/{category_dir}/")
        if not meta.get("human_role"):
            report.error(skill_md, "metadata.human_role is missing (PRINCIPLES 1: who owns the decision?)")
        for key, value in meta.items():
            if not isinstance(value, str):
                report.error(skill_md, f"metadata.{key} must be a plain string (lists and numbers break claude.ai uploads); "
                                       f"write e.g. \"T1059, T1027\"")

    # --- frontmatter keys that claude.ai uploads accept ---
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    for key in fm:
        if key not in allowed:
            report.error(skill_md, f"frontmatter key '{key}' is not portable (claude.ai accepts: {', '.join(sorted(allowed))})")

    check_references(folder, text, report)

    # --- principles: required sections ---
    for heading, why in REQUIRED_SECTIONS.items():
        if not re.search(rf"^{re.escape(heading)}\s*$", text, re.M):
            report.error(skill_md, f"missing section '{heading}' ({why})")

    authority = section_body(text, "## Human authority").lower()
    if authority and "does not" not in authority:
        report.error(skill_md, "'## Human authority' must state what Claude does not do")

    if HANDOFF_MARKER not in text:
        report.error(skill_md, f"output never hands the decision back — add a '{HANDOFF_MARKER}' step (PRINCIPLES 1)")

    # --- softer checks ---
    if not re.search(r"^## References\s*$", text, re.M):
        report.warn(skill_md, "no '## References' section; add authoritative sources where they exist")
    lines = text.count("\n") + 1
    if lines > MAX_LINES:
        report.warn(skill_md, f"SKILL.md is {lines} lines; keep it under {MAX_LINES} and move detail to reference files")

    return name if isinstance(name, str) else None


def check_references(folder: Path, text: str, report: Report) -> None:
    """Linked reference files exist; reference files are linked; master copies match."""
    skill_md = folder / "SKILL.md"
    linked = set(re.findall(r"\]\((references/[^)#\s]+)\)", text))
    for link in sorted(linked):
        if not (folder / link).is_file():
            report.error(skill_md, f"links to '{link}', which does not exist in the skill folder")
    ref_dir = folder / "references"
    if ref_dir.is_dir():
        for ref in sorted(ref_dir.rglob("*")):
            if not ref.is_file():
                continue
            local = ref.relative_to(folder).as_posix()
            if local not in linked:
                report.warn(ref, "reference file is never linked from SKILL.md, so Claude won't know to read it")
            shared = SHARED_REFS / ref.relative_to(ref_dir)
            if shared.is_file() and shared.read_bytes() != ref.read_bytes():
                report.error(ref, f"differs from tools/references/{shared.name}; "
                                  f"edit the master copy, then run: python tools/validate.py --sync-references")


def sync_references() -> int:
    """Copy every master reference over the skills' copies of it."""
    updated = 0
    for shared in SHARED_REFS.rglob("*") if SHARED_REFS.is_dir() else []:
        if not shared.is_file():
            continue
        relative = shared.relative_to(SHARED_REFS)
        for copy in SKILLS_DIR.glob(f"*/*/references/{relative.as_posix()}"):
            if copy.read_bytes() != shared.read_bytes():
                shutil.copyfile(shared, copy)
                print(f"synced  {rel(copy)}")
                updated += 1
    return updated


def check_readme(names: list[str], report: Report) -> None:
    if not README.exists():
        report.error(README, "README.md is missing")
        return
    text = README.read_text(encoding="utf-8")
    for name in names:
        if f"`{name}`" not in text:
            report.error(README, f"skill '{name}' is not listed in the README skill index")
    badge = re.search(r"skills-(\d+)-", text)
    if badge and int(badge.group(1)) != len(names):
        report.error(README, f"README badge says {badge.group(1)} skills but the repo has {len(names)}")


def annotation(text: str) -> str:
    """Escape text for a GitHub Actions workflow command."""
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def emit(report: Report, strict: bool) -> int:
    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    for level, items in (("error", report.errors), ("warning", report.warnings)):
        for path, msg in items:
            print(f"{level.upper():7s} {rel(path)}: {msg}")
            if in_actions:
                print(f"::{level} file={rel(path)}::{annotation(msg)}")
    failed = bool(report.errors) or (strict and bool(report.warnings))
    print(f"\n{len(report.errors)} error(s), {len(report.warnings)} warning(s)"
          + (" — warnings treated as errors (--strict)" if strict and report.warnings else ""))
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--sync-references", action="store_true",
                        help="copy tools/references files over the skills' copies before validating")
    args = parser.parse_args()

    if args.sync_references:
        print(f"Synced {sync_references()} file(s) from tools/references/\n")

    report = Report()
    if not SKILLS_DIR.is_dir():
        report.error(ROOT, "Skills/ directory not found")
        return emit(report, args.strict)

    for entry in sorted(SKILLS_DIR.iterdir()):
        if entry.is_dir() and entry.name not in CATEGORIES:
            report.error(entry, f"unknown category folder; allowed: {', '.join(sorted(CATEGORIES))}")

    names: list[str] = []
    for folder in sorted(p for p in SKILLS_DIR.glob("*/*") if p.is_dir()):
        skill_md = folder / "SKILL.md"
        if not skill_md.exists():
            report.error(folder, "skill folder has no SKILL.md")
            continue
        name = check_skill(skill_md, report)
        if name:
            names.append(name)

    for dup in sorted({n for n in names if names.count(n) > 1}):
        report.error(SKILLS_DIR, f"duplicate skill name '{dup}'")

    check_readme(names, report)
    print(f"Checked {len(names)} skill(s) in {rel(SKILLS_DIR)}/\n")
    return emit(report, args.strict)


if __name__ == "__main__":
    sys.exit(main())
