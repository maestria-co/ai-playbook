---
name: context-maintenance
description: >
  Keeps `.context/` documentation accurate and current. Use this skill after
  completing any non-trivial task, when you've learned something new about the
  project, when promoting lessons from retrospectives, when pruning stale task
  folders, or when you notice documentation that's outdated or duplicated. If you
  just finished a task and learned something worth preserving, this is the right
  skill — even if the user doesn't explicitly ask. For full codebase-level syncs,
  use `context-review` instead.
---

# Skill: Context Maintenance

## Purpose

Keep `.context/` accurate without letting it rot or bloat. This skill covers the
ongoing maintenance tasks: promoting retrospective insights, pruning stale content,
deciding when to update vs. create, and avoiding duplication.

Use `context-review` for full codebase scans. Use this skill for incremental updates
after individual tasks.

---

## Retrospective Promotion Workflow

Lessons logged in `.context/retrospectives/` should graduate to permanent docs. This prevents
the retrospective from becoming an unread graveyard.

### Process

1. Open `retrospectives/`
2. Find entries with unchecked `[ ]` promotion items
3. For each unchecked item:
   - Read the target file (e.g., `standards.md`)
   - Add the lesson in the appropriate section — don't just append; integrate it
   - Check the box: `[x]`
4. Entries older than 4 weeks with all items checked → archive or delete

### Promotion Decision

| Lesson type                    | Promote to                                     |
| ------------------------------ | ---------------------------------------------- |
| Coding pattern or anti-pattern | `standards.md` or `standards.md`               |
| Naming discovery               | `standards.md`                                 |
| Test strategy or mock pattern  | `testing.md` or `testing.md`                   |
| Architecture insight           | `architecture.md`                              |
| Domain knowledge               | `domains/entities.md` or `domains/glossary.md` |
| Process improvement            | `workflows/` appropriate file                  |
| Decision rationale             | `decisions/index.md` (as a new ADR)            |

---

## When to Update vs. Create

| Situation                               | Action                                                    |
| --------------------------------------- | --------------------------------------------------------- |
| New information about an existing topic | **Update** the existing file                              |
| Existing file is wrong or outdated      | **Update** — replace the stale content                    |
| Completely new topic area               | **Create** a new file in the appropriate subdirectory     |
| Information exists in multiple places   | **Consolidate** into a single file and remove duplicates  |
| A pattern applies to only one area      | **Update** the area-specific file, don't create a new one |

**Rule of thumb:** If you're tempted to create a new file, first check if the content
belongs in an existing one. Fewer, richer files beats many sparse ones.

---

## Task Folder Management

Task folders in `.context/tasks/[TASK-ID]/` are ephemeral by default.

### Lifecycle

1. **Active tasks:** Keep all artifacts (brief, plan, research, decisions)
2. **Completed tasks (< 2 weeks):** Keep — lessons may not yet be promoted
3. **Completed tasks (2–4 weeks):** Promote remaining lessons, then delete the folder
4. **Completed tasks (> 4 weeks):** Delete unless the task contains a reference design

### Pruning Triggers

Delete or archive a task folder when **any** of these are true:

- **Age:** Completed task folder older than 4 weeks
- **Scope drift:** Folder content no longer reflects what the task actually became (scope changed significantly mid-task and the plan was never updated)
- **Orphaned:** Task was abandoned with no retrospective and no active branch

### Pruning Process

```bash
# Find task folders older than 4 weeks
find .context/tasks/ -name "plan.md" -mtime +28 -exec dirname {} \;
```

For each old or drifted folder:

1. Check if retrospective was written and lessons promoted
2. If yes → delete the folder
3. If no → write the retrospective first, promote lessons, then delete

---

## Quality Checks

Run these periodically (or after every 3–5 tasks):

### Check 1 — Staleness

- Read `overview.md` — does the tech stack still match manifest files?
- Read `standards.md` — do conventions match recently-written code?
- If stale → update the specific sections

### Check 2 — Duplication

- Search for the same information in multiple files
- If found → consolidate into the canonical location, remove duplicates

### Check 3 — Drift

- Read `architecture.md` — do documented patterns match actual code?
- If code has diverged → either update the doc (if the code is correct) or flag the code (if the doc is correct)
- If a `.context/tasks/` folder has scope-drifted (plan describes a different task than what was built) → apply pruning trigger above

### Check 4 — Bloat and shape

The layout rules live in `skills/_shared/conventions.md`. This check is where
they get enforced. Both thresholds are numbers, not judgment calls.

**Promote a flat file to a folder at 300 lines.** Applies to `standards.md`,
`testing.md`, and `architecture.md`:

```bash
for base in standards testing architecture; do
  f=".context/$base.md"
  [ -f "$f" ] && n=$(wc -l < "$f") && [ "$n" -gt 300 ] && echo "$base.md: $n lines — promote"
done
```

To promote `standards.md`:

1. `mkdir .context/standards/`
2. Split by top-level section into `standards/naming.md`,
   `standards/errors.md`, and so on
3. Write `standards/README.md` as the entry point — a short index linking each
   file, because that is the path agents read once the flat file is gone
4. `git rm .context/standards.md`

Never promote below the threshold. A 120-line file split into four 30-line
files is harder to read, not easier.

**`decisions/` stays a folder.** If you find a `decisions.md`, that is drift —
split it into one file per ADR. Never the reverse.

**Cap `retrospectives/` at 10 entries**, excluding `README.md` and
`template.md`:

```bash
ls .context/retrospectives/*.md 2>/dev/null \
  | grep -v -E '/(README|template)\.md$' | wc -l
```

Over 10: promote the lessons per the Retrospective Promotion Workflow above,
then move the promoted entries into `retrospectives/archive/`:

```bash
mkdir -p .context/retrospectives/archive/
git mv .context/retrospectives/<entry>.md .context/retrospectives/archive/
```

`validate.py` counts top-level `*.md` only, so an archived entry stops
counting against the cap. Use this exact path — a sibling folder or a rename
leaves CI red, and deleting instead loses the entry.

Archive only what has been promoted. The constraint against deleting
unpromoted retrospectives still holds, so if all 10 are unpromoted, promote
first and archive second. Going over the cap is a hard CI error, so this is
the remedy to reach for, not a judgment call.

---

## Constraints

- Do not touch source code during maintenance — only `.context/` files
- Do not delete retrospective entries that haven't been promoted yet
- Do not add generic advice — only project-specific knowledge belongs in `.context/`
- Preserve hand-authored content (business context, rationale) — only update factual details
- When in doubt about whether to update or create, update
