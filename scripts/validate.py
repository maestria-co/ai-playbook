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

# The commit-msg hook ships twice: once for this repo, once inside the template
# `initialize-repo` installs into a consumer repo. Two copies drift, so the
# check that they are byte-identical runs in CI rather than relying on memory.
HOOK_COPIES = [
    os.path.join(".githooks", "commit-msg"),
    os.path.join("skills", "_shared", "context_template", "githooks", "commit-msg"),
]

# `.context/` layout, per the table in context_template/context/META.md. A flat
# file is promoted
# to a folder of the same name at 300 lines, and a promoted entry is read at
# <base>/README.md. Six Maestria repos grew six different shapes because nothing
# checked. These three rules are the ones worth enforcing.
PROMOTABLE = ["standards", "testing", "architecture"]
PROMOTE_AT_LINES = 300
MAX_RETROSPECTIVE_ENTRIES = 10

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

    # The two commit-msg copies must stay byte-identical
    hook_paths = [os.path.join(REPO, h) for h in HOOK_COPIES]
    missing = [h for h, p in zip(HOOK_COPIES, hook_paths) if not os.path.isfile(p)]
    if missing:
        for h in missing:
            errors.append(f"[githooks] Required hook copy not found: {h}")
    else:
        bodies = [open(p, "rb").read() for p in hook_paths]
        if bodies[0] != bodies[1]:
            errors.append(
                "[githooks] commit-msg copies have drifted: "
                f"{HOOK_COPIES[0]} != {HOOK_COPIES[1]}"
            )
        for h, p in zip(HOOK_COPIES, hook_paths):
            if not os.access(p, os.X_OK):
                errors.append(f"[githooks] Hook is not executable: {h}")

    # .context/ layout conventions
    ctx = os.path.join(REPO, ".context")
    if os.path.isdir(ctx):
        # overview.md is the one canonical name. This is the bug that opened
        # PR #35: this repo called it project-overview.md, so a guard looking
        # for overview.md found nothing and reported "proceed" against six
        # ADRs. The rename is only a one-time cleanup unless something keeps
        # it renamed.
        if not os.path.isfile(os.path.join(ctx, "overview.md")):
            errors.append("[.context] Missing required file: overview.md")
        if os.path.isfile(os.path.join(ctx, "project-overview.md")):
            errors.append(
                "[.context] project-overview.md is drift — rename to "
                "overview.md"
            )

        # META.md is the layout spec itself, and workflows/ holds the PR
        # format every repo needs. Both are "always created" per the spec, and
        # neither was asserted — so this repo shipped the convention without
        # following it. A spec the defining repo does not satisfy is a weak
        # spec. domains/ stays unchecked: it is conditional by design.
        for required in ("META.md", os.path.join("workflows", "pull-requests.md")):
            if not os.path.isfile(os.path.join(ctx, required)):
                errors.append(f"[.context] Missing required file: {required}")

        # decisions/ and retrospectives/ are always folders, never files.
        #
        # Collapsing either into one file destroys what makes it work: an ADR
        # is immutable, numbered and cited by number, and a retrospective is
        # one dated entry per task. Absence is an error too — a check that
        # only validates the shape of an entry that exists passes silently on
        # the repo that has no entry at all.
        #
        # Severity is deliberately asymmetric against the promotable entries
        # below, which are warnings: these two must exist before the first
        # entry is written, while standards/testing/architecture are docs a
        # repo can legitimately not have written yet. Do not flatten them to
        # match each other in either direction. (--strict collapses the
        # distinction in CI, which is the point: a warning is a nudge locally
        # and a gate on the default branch.)
        for base, unit in (
            ("decisions", "one ADR per file"),
            ("retrospectives", "one dated entry per file"),
        ):
            if os.path.isfile(os.path.join(ctx, base + ".md")):
                errors.append(
                    f"[.context] {base} must be a folder, not {base}.md — "
                    f"{unit}"
                )
            if not os.path.isdir(os.path.join(ctx, base)):
                errors.append(
                    f"[.context] Missing required folder: {base}/"
                )

        # Each promotable entry must exist in exactly one shape
        for base in PROMOTABLE:
            flat = os.path.join(ctx, base + ".md")
            folder = os.path.join(ctx, base)
            has_flat, has_folder = os.path.isfile(flat), os.path.isdir(folder)
            if has_flat and has_folder:
                errors.append(
                    f"[.context] {base} exists as both {base}.md and {base}/ — "
                    "pick one shape"
                )
            elif has_folder and not os.path.isfile(
                os.path.join(folder, "README.md")
            ):
                errors.append(
                    f"[.context] {base}/ has no README.md — a promoted entry "
                    "needs an entry point, since agents no longer find "
                    f"{base}.md"
                )
            elif has_flat:
                n = sum(1 for _ in open(flat, encoding="utf-8"))
                if n > PROMOTE_AT_LINES:
                    warnings.append(
                        f"[.context] {base}.md is {n} lines (over "
                        f"{PROMOTE_AT_LINES}) — promote it to {base}/ via "
                        "context-maintenance"
                    )
            elif not has_folder:
                warnings.append(f"[.context] Missing {base}.md")

        # retrospectives/ caps at 10 entries, excluding scaffolding.
        #
        # os.listdir counts top-level *.md only, so entries archived into
        # retrospectives/archive/ do not count toward the cap. That is the
        # stated remedy for going over, not an accident of the
        # implementation — context-maintenance names the same path. Keep the
        # two in step.
        retro = os.path.join(ctx, "retrospectives")
        if os.path.isdir(retro):
            entries = [
                f for f in os.listdir(retro)
                if f.endswith(".md") and f not in ("README.md", "template.md")
            ]
            if len(entries) > MAX_RETROSPECTIVE_ENTRIES:
                errors.append(
                    f"[.context] retrospectives/ has {len(entries)} entries, "
                    f"max {MAX_RETROSPECTIVE_ENTRIES} — promote the lessons "
                    "and archive them"
                )

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
