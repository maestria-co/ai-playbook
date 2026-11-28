#!/usr/bin/env python3
"""
Structural validator for agent-defs repo.

Checks:
- All agents have required frontmatter keys (description, name, model)
- All agents declare a model from ALLOWED_MODELS
- All specialist agents have Behavior Tiers, Anti-Rationalization, Scope Guard, Constraints
- All skill references in agents resolve to real directories on disk
- No stale agent references (workspace-manager, monorepo-manager)
- Manager does not have 'codebase' in tools list
- GUIDE.md mentions all custom skills
- Index docs (CLAUDE.md, skills/GUIDE.md) cite no paths that have gone stale

Usage:
  python3 scripts/validate.py
  python3 scripts/validate.py --strict   # treat warnings as errors
"""

import os
import subprocess
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(REPO, "skills")
AGENTS_DIR = os.path.join(REPO, "agents")

# Skills installed from the skill kit — not owned by this repo, don't require GUIDE.md coverage
SKILLKIT_SKILLS = {
    "agent-file-review", "asana-story", "code-identifier", "commit-discipline",
    "dependency-management", "design-first", "initialize-monorepo", "initialize-repo",
    "initialize-workspace", "jira-story", "knowledge-graduation", "linear-story",
    "planning-tasks", "post-meeting", "researching-options", "start-worktree",
    "using-skills", "context-review",
}

# The only models agents may declare. This is the single source of truth —
# update it here when the fleet moves, and CI will flag any agent left behind.
ALLOWED_MODELS = {
    "claude-opus-5",
    "claude-sonnet-5",
    "claude-haiku-4-5-20251001",
}

# Hand-maintained index docs. Every repo-rooted file path they cite must
# resolve on disk, or a row has gone stale. This is the drift nothing caught
# before: a table row outlives the file it points at.
INDEX_DOCS = ["CLAUDE.md", os.path.join("skills", "GUIDE.md")]

# Files that ship twice: once for this repo to use, once inside the template
# `initialize-repo` installs into a consumer repo. Two copies drift, and the
# copy consumers get would be the one nobody ran — so the check that each pair
# is byte-identical runs in CI rather than relying on memory.
TEMPLATE = os.path.join("skills", "_shared", "context_template")
SHIPPED_PAIRS = [
    (
        os.path.join(".githooks", "commit-msg"),
        os.path.join(TEMPLATE, "githooks", "commit-msg"),
    ),
    (
        os.path.join("scripts", "check-context-layout.sh"),
        os.path.join(TEMPLATE, "scripts", "check-context-layout.sh"),
    ),
]

# A backticked path ending in .md / .py / .sh
PATH_REF = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|py|sh))`")

# Illustrative paths in prose, not real references.
PLACEHOLDER_MARKERS = ("NNN", "TASK-ID", "[", "<")

REQUIRED_FRONTMATTER = ["description", "name", "model"]
REQUIRED_SECTIONS_SPECIALIST = [
    "## Behavior Tiers",
    "## Anti-Rationalization",
    "## Scope Guard",
    "## Constraints",
]
STALE_AGENT_REFS = ["workspace-manager", "monorepo-manager"]

STRICT = "--strict" in sys.argv


def collect_skills():
    skills = set()
    for entry in os.listdir(SKILLS_DIR):
        if os.path.isfile(os.path.join(SKILLS_DIR, entry, "SKILL.md")):
            skills.add(entry)
    return skills


def validate():
    errors = []
    warnings = []

    real_skills = collect_skills()
    agent_files = sorted(f for f in os.listdir(AGENTS_DIR) if f.endswith(".agent.md"))

    for fname in agent_files:
        path = os.path.join(AGENTS_DIR, fname)
        content = open(path).read()
        is_manager = fname == "manager.agent.md"

        # Frontmatter
        for key in REQUIRED_FRONTMATTER:
            if not re.search(rf"^{key}:", content, re.MULTILINE):
                errors.append(f"[{fname}] Missing frontmatter key: {key}")

        # Model version
        m = re.search(r"^model:\s*(.+)", content, re.MULTILINE)
        if m:
            model = m.group(1).strip()
            if model not in ALLOWED_MODELS:
                errors.append(
                    f"[{fname}] Model not in allowlist: {model} "
                    f"(allowed: {', '.join(sorted(ALLOWED_MODELS))})"
                )

        # Required sections (all agents except manager)
        if not is_manager:
            for section in REQUIRED_SECTIONS_SPECIALIST:
                if section not in content:
                    errors.append(f"[{fname}] Missing required section: {section}")

        # Skill references
        for ref in re.findall(r"skills/([^/\s]+)/SKILL\.md", content):
            if ref not in real_skills:
                errors.append(f"[{fname}] Broken skill ref: skills/{ref}/SKILL.md (not on disk)")

        # Stale agent references
        for stale in STALE_AGENT_REFS:
            if stale in content:
                errors.append(f"[{fname}] Stale agent reference found: '{stale}'")

        # Manager-specific checks
        if is_manager:
            if '"codebase"' in content:
                errors.append(f"[{fname}] 'codebase' tool in tools list contradicts no-raw-source rule")

    # GUIDE.md coverage for custom skills
    guide_path = os.path.join(SKILLS_DIR, "GUIDE.md")
    if os.path.isfile(guide_path):
        guide_content = open(guide_path).read()
        for skill in real_skills:
            if skill.startswith("_") or skill in SKILLKIT_SKILLS:
                continue
            if skill not in guide_content:
                warnings.append(f"[GUIDE.md] Custom skill not mentioned: {skill}")
    else:
        errors.append("[GUIDE.md] File not found")

    # Index-doc drift: every repo-rooted path cited must exist
    for doc in INDEX_DOCS:
        doc_path = os.path.join(REPO, doc)
        if not os.path.isfile(doc_path):
            errors.append(f"[{doc}] Index doc not found")
            continue
        for ref in sorted(set(PATH_REF.findall(open(doc_path).read()))):
            # Bare filenames are relative prose mentions, not references.
            if "/" not in ref:
                continue
            if any(mark in ref for mark in PLACEHOLDER_MARKERS):
                continue
            if not os.path.exists(os.path.join(REPO, ref)):
                errors.append(f"[{doc}] Stale reference, path does not exist: {ref}")

    # Every shipped pair must stay byte-identical and executable
    for rel_a, rel_b in SHIPPED_PAIRS:
        name = os.path.basename(rel_a)
        paths = [os.path.join(REPO, rel_a), os.path.join(REPO, rel_b)]
        missing = [r for r, p in zip((rel_a, rel_b), paths) if not os.path.isfile(p)]
        if missing:
            for r in missing:
                errors.append(f"[shipped] Required copy not found: {r}")
            continue
        if open(paths[0], "rb").read() != open(paths[1], "rb").read():
            errors.append(
                f"[shipped] {name} copies have drifted: {rel_a} != {rel_b}"
            )
        for r, p in zip((rel_a, rel_b), paths):
            if not os.access(p, os.X_OK):
                errors.append(f"[shipped] Not executable: {r}")

    # .context/ layout — delegated, not reimplemented.
    #
    # The rules are identical for every repo, so there is one implementation:
    # scripts/check-context-layout.sh, which also ships in the template and is
    # what `context-review` runs in a consumer repo. Two copies of these rules
    # would drift, and the copy consumers get would be the one nobody tested.
    layout = os.path.join(REPO, "scripts", "check-context-layout.sh")
    if not os.path.isfile(layout):
        errors.append("[.context] scripts/check-context-layout.sh not found")
    else:
        proc = subprocess.run(
            [layout, os.path.join(REPO, ".context")],
            capture_output=True, text=True,
        )
        for line in proc.stdout.splitlines():
            if line.startswith("ERROR: "):
                errors.append(f"[.context] {line[7:]}")
            elif line.startswith("WARN: "):
                warnings.append(f"[.context] {line[6:]}")

    return errors, warnings


def main():
    errors, warnings = validate()

    if errors:
        print(f"❌ {len(errors)} error(s) found:\n")
        for e in errors:
            print(f"  {e}")
    else:
        print("✅ No errors")

    if warnings:
        print(f"\n⚠️  {len(warnings)} warning(s):\n")
        for w in warnings:
            print(f"  {w}")
    else:
        print("✅ No warnings")

    if errors or (STRICT and warnings):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
