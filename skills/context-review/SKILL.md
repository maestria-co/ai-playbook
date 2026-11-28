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

Look for `.context/overview.md` in the current working directory.

- If it does not exist → not a structured codebase. **Abort skill.**
- If found → read it to understand the project before proceeding.

**Check 2 — Check the cache**

Read `.context/cache/context_update.md`.

- If it exists and `last_executed` is within the last **5 days** → context is fresh. **Abort skill.**
- If it does not exist, or is older than 5 days → **proceed.**

---

## Execution Steps

Work through each step in order. Read the current `.context/` file, scan the relevant source, and update only what has changed. Do not rewrite sections that are hand-authored, opinion-based, or business-context.

### Step 0 — Structural conformance

Content accuracy is pointless if an agent cannot find the file. Run the
layout check before reconciling anything:

```bash
./scripts/check-context-layout.sh
```

It asserts `.context/` matches the spec in `.context/META.md` section 2 —
required files present, `decisions/` as a folder, each promotable entry in
exactly one shape, promoted folders carrying a `README.md`, and at a project
node `retrospectives/` as a folder under its cap. Exit 1 means at least one
`ERROR:`.

**First, settle the context shape.** The checker's rule set depends on
`context_shape` in `overview.md`, and this skill is the migration path for
every node that predates the key. Read it; if it is absent, decide which it is
and **write it** before fixing anything else, because the findings you are
about to act on depend on it:

| Evidence | Shape |
|---|---|
| Code at this node — a build manifest, source tree, or test suite | `project` |
| No code of its own; subdirectories are the projects. A monorepo root, a grouping directory like `services/`, a workspace root | `aggregate` |

When the evidence is genuinely mixed — a repo root holding both its own code
and sub-projects — it is a `project`. The reduced aggregate layout drops
`standards.md` and `testing.md`, and a node with code needs both.

An absent key already behaves as `project`, so writing `project` changes no
behavior and is still worth doing: it is the difference between a node that
declares what it is and one that is assumed. Writing `aggregate` is the case
that matters — it is what stops the findings below from being wrong.

If the script is absent, the repo predates it — copy it from the template at
`<template_dir>/scripts/check-context-layout.sh` and run it.

**Fix the mechanical findings. Report the rest.**

| Finding | Action |
|---|---|
| `missing required file: META.md` | Copy from `<template_dir>/context/META.md`. Pure copy, no placeholders |
| `missing required file: workflows/pull-requests.md` | Copy from the template, then fill the Repo Configuration block from evidence — see `initialize-repo` Step 3a |
| `<base>/ has no README.md` | Write one: a short index linking each file already in that folder |
| `missing <base>.md` | Create it as part of the step for that file below |
| `<base> at an aggregate node` | **Report.** The entry does not belong at this shape, but deleting documentation is never mechanical — the content may need moving to a project node first |
| `unrecognized context_shape` | Fix the typo. Valid values are `project` and `aggregate`; nothing else |
| `<base>.md is NNN lines (over 300)` | Hand to `context-maintenance` — promotion is its job, not this skill's |
| `project-overview.md is drift` | Rename to `overview.md` and update every reference |
| `exists as both <base>.md and <base>/` | **Report.** Deciding which content wins needs a human |
| `decisions.md is drift` | **Report.** See below |
| `retrospectives.md is drift` | **Report.** See below |
| `retrospectives/ has N entries` | Hand to `context-maintenance` — it owns promotion and archiving |

**Never split a collapsed `decisions.md` or `retrospectives.md` automatically.**
Both need judgment this skill does not have: where one ADR ends and the next
begins, what number each should carry, which retrospective entry belongs to
which task. Guessing produces ADRs with invented numbers that other documents
then cite. Report it as a migration the human has to drive:

```
decisions.md found (N decisions, M lines). Spec requires decisions/ with one
ADR per file. This needs a human: ADR numbers are cited by other documents,
so the split cannot be guessed.
```

Then re-run the checker. A shape written in this step changes which findings
apply, so the first run's output is stale the moment you write the key — and
acting on a stale list is how an aggregate node acquires the `standards.md`
the spec says it must not have.

Do not write the cache file as fresh while an unreported ERROR stands — a
structurally broken `.context/` reviewed for content is worse than one that
reports itself broken, because the cache then suppresses the next review for
five days.

### Step 1 — `overview.md`

Target: `.context/overview.md`

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

- **Structural conformance:** pass / N errors reported
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
- Always write the cache file at the end, even if nothing changed — except while an unresolved structural ERROR stands, which must be reported rather than cached over
- Never split a collapsed `decisions.md` or `retrospectives.md` — report it as a human-driven migration
