---
name: context-review
description: >
  Scans the codebase and synchronizes `.context/` documentation with the actual
  state of the code. Use this at the start of any architect or design task when
  the context cache is stale (older than 5 days) or missing.
---

# Skill: Context Review and Update

## Purpose

Scan the current codebase and synchronize the `.context/` documentation with the actual state of the code. This keeps architecture, domain, and standards docs accurate without human effort.

Invoke this skill at the start of any architect task when the cache is stale (>5 days old) or missing.

---

## Pre-flight Checks

Run these checks before scanning. If either fails, abort the skill and proceed with the original task.

**Check 1 — Verify codebase context**

Look for `.context/overview.md` or `.context/project-overview.md` in the current working directory.

- If neither exists → not a structured codebase. **Abort skill.**
- If found → read it to understand the project before proceeding.

**Check 2 — Check the cache**

Read `.context/cache/context_update.md`.

- If it exists and `last_executed` is within the last **5 days** → context is fresh. **Abort skill.**
- If it does not exist, or is older than 5 days → **proceed.**

---

## Execution Steps

Work through each step in order. Read the current `.context/` file, scan the relevant source, and update only what has changed. Do not rewrite sections that are hand-authored, opinion-based, or business-context.

### Step 1 — `overview.md`

Target: `.context/overview.md` (or `project-overview.md`)

- Verify tech stack versions still match manifest files (`*.csproj`, `package.json`, etc.)
- Update `## Current State` (or equivalent):
  - Check source directories for non-empty files beyond `.gitkeep` placeholders
  - Note newly implemented entities, endpoints, or services
- Update external service statuses if integrations have changed
- **Do not modify:** target user descriptions, business goals, or any clearly human-authored narrative

### Step 2 — `.context/domains/`

Target: all `*.md` files in `.context/domains/`

- `entities.md` — compare against actual entity classes in source:
  - Add entities discovered in code
  - Update fields, relationships, and business rules for existing entries
  - Mark entities as `Implemented` vs `Planned` based on whether source files exist
- `glossary.md` — add new terms introduced in code; update definitions if usage has evolved

### Step 3 — `.context/architecture.md`

Target: all `*.md` files in `.context/architecture.md`

- Document patterns consistently applied across the codebase but not yet captured
- Update existing pattern descriptions if the implementation has diverged from what's documented
- Add entries for new layers, abstractions, or structural decisions introduced since last run

### Step 4 — `.context/standards.md`

Target: all `*.md` files in `.context/standards.md`

- `code-style.md` — note new conventions observed in recently added code
- `naming-conventions.md` — update if naming patterns have evolved
- `error-handling.md` — update if error handling patterns have changed

---

### Step 5 — `.context/workflows/pull-requests.md`

Every repo needs a documented PR format. If this file is missing, create it.

1. Copy `pull-requests.md` from `skills/_shared/context_template/context/workflows/`
   (create `.context/workflows/` if absent).
2. Fill the **Repo Configuration** table from observed evidence — never guess:

```bash
# ticket prefix and number format — most frequent wins
{ git branch -a --format='%(refname:short)'; git tag; git log --format='%s%n%b' -500; } \
  | grep -oiE '[A-Z]+-[0-9]+' | tr 'a-z' 'A-Z' | sort | uniq -c | sort -rn | head
# integration branch
git branch -r --format='%(refname:short)' | grep -E 'origin/(dev|develop)$'
```

3. Replace the `<PREFIX>` placeholder in its Step 2 fallback command with the resolved prefix.
4. If a `branching.md` exists, reconcile it: `pull-requests.md` is the source of truth for
   PR titles and descriptions. Remove any rival PR template from `branching.md` and correct
   any branch-naming rule that contradicts observed branch names.

If no ticket pattern exists anywhere in history, leave the prefix as a TODO and tell the
human rather than inventing a scheme.

---

## Cache Write

After completing all steps (or confirming nothing changed), write `.context/cache/context_update.md`. Create `.context/cache/` if it does not exist.

```markdown
---
last_executed: <ISO 8601 timestamp — e.g., 2026-03-07T15:09:00Z>
triggered_by: architect-agent
---

## Summary

- **Reviewed:** `overview.md`, `domains/`, `architecture.md`, `standards.md`, `workflows/pull-requests.md`
- **Changes made:** yes / no
- **Files updated:**
  - [list files that were changed, or "none"]
```

---

## Constraints

- Only modify files under `.context/` — never touch source code during this skill
- Preserve hand-authored content — if a section reads as rationale, opinion, or business context, do not alter it
- Prefer in-place updates over appending new sections; avoid growing files unnecessarily
- If the codebase is empty (only `.gitkeep` in source dirs), update `Current State` to reflect that but make no other changes
- Always write the cache file at the end, even if nothing changed
