# .context/ Maintenance Guide

This file tells you (human or AI agent) how to maintain the `.context/` directory so it stays useful and doesn't rot.

---

## 1. Purpose

`.context/` is the shared memory store for this project. It holds the things that would take a new engineer (or a fresh AI context window) hours to reconstruct from reading the code: non-obvious decisions, established patterns, discovered pitfalls, and domain terminology.

Without it, every agent starts from zero. With it, every agent starts informed.

---

## 2. Separation of Concerns

**This table is the canonical layout spec.** It is the one list of what
belongs in `.context/` and what shape each entry takes. Do not restate it
elsewhere — link here.

| File | Role | Shape | Characteristics |
|---|---|---|---|
| `CLAUDE.md` / `copilot-instructions.md` | Entry point — project facts + context imports | file | Under 80 lines. Changes rarely. Agent reads on every task. |
| `.context/META.md` | This file — what belongs where | file | The layout spec. Ships with the template. |
| `.context/README.md` | Orientation — what this directory is and how it is used | file | **Optional** — not shipped in the template. Write one if newcomers need the tour; nothing requires or checks it. |
| `.context/overview.md` | What the project is | **always a file** | Tech stack, purpose, current phase. Never `project-overview.md`. |
| `.context/architecture.md` | How the system is structured | file → folder | Layers, data flow, integrations. Not decisions, not code style. |
| `.context/standards.md` | How to write code here | file → folder | Style, naming, error handling, patterns. |
| `.context/testing.md` | How to test here | file → folder | Framework, file conventions, mocking. |
| `.context/decisions/` | Why key choices were made | **always a folder** | One ADR per file. Grows over time. |
| `.context/retrospectives/` | Lessons learned per task | folder | Dated files, **max 10**; archive the rest to `retrospectives/archive/`. |
| `.context/tasks/` | Per-task work artifacts | folder | One folder per task. Research reports live in `tasks/<id>/research/`. |
| `.context/workflows/` | PR format, branching, CI | folder | Always created. `pull-requests.md` is required. |
| `.context/domains/` | Entities, glossary, domain rules | folder | **Conditional** — only for a repo with a rich domain or its own vocabulary. |

**Conditional** and **Optional** entries are never required: nothing fails
when `domains/` or `README.md` is absent. No check rejects an entry this table
does not list either, which is why a file sitting in `.context/` needs a row
here rather than being left to inference — "is this allowed?" should be
answerable from the spec, not from whether a checker happens to complain.

### Shapes

**`file → folder`** means it starts as a single file and is promoted by
`context-maintenance` once it passes **300 lines**. A promoted entry is read at
`<base>/README.md`, so `standards.md` becomes `standards/README.md` plus
`standards/naming.md` and friends. Promote on the threshold, never on taste —
splitting a 120-line file into four 30-line files is harder to read, not
easier.

**`always a file`** / **`always a folder`** do not change. `decisions/` is a
folder because an ADR is immutable once accepted and cited by number;
collapsing them into one `decisions.md` destroys both properties. `overview.md`
is one fixed name because tooling looks for it — a repo that calls it
`project-overview.md` reads as uninitialized.

Keep `CLAUDE.md` short by keeping detail here. If `CLAUDE.md` grows past 80 lines, promote content to `.context/`.

---

## 3. When to Update

Update `.context/` when any of the following happens:

1. **A new pattern is established** — in code review, PR feedback, or architectural discussion
2. **A standard evolves** — old pattern replaced with new one; update the file, don't just add
3. **Architecture changes** — new service, new layer, new integration
4. **A recurring bug is fixed** — document the root cause and fix so it doesn't recur
5. **A new domain entity or term is introduced** — update `domains/entities.md` and `domains/glossary.md`
6. **A workflow changes** — CI steps, branching rules, deployment process
7. **Context was recovered from scratch and something was missing** — whatever you had to re-derive belongs here

---

## 4. What Belongs Here

**High value — add this:**
- Non-obvious decisions with rationale (why we chose X over Y)
- Patterns discovered through painful refactors
- Recurring bug fixes with root cause
- Test strategies for tricky areas (auth, async, third-party mocks)
- Business rules that aren't obvious from the code

**Low value — don't add this:**
- Things immediately obvious from reading the code
- Things covered in official library or framework documentation
- One-off notes that are only relevant for a single PR

---

## 5. Retrospective Promotion

`retrospectives/` holds individual files per task (`YYYY-MM-DD-TASK-ID.md`). Lessons in them should be promoted to the appropriate subdirectory file during weekly review.

**Process:**
1. Open any file in `retrospectives/` with unchecked `[ ]` promotion items
2. Copy the lesson into the referenced file (e.g., `standards/error-handling.md`)
3. Check the box: `[x]`
4. Files older than 4 weeks with all items checked can be archived or deleted

---

## 6. Context Recovery

When resuming after a context reset, follow these steps in order:

1. Read `overview.md` — get oriented to the project
2. Run `git log --oneline -10` — see what's been done recently
3. Read the latest file in `retrospectives/` — see what the last task uncovered
4. Read `architecture.md` and `standards.md` — refresh on how code is structured
5. Read any in-progress task files in `tasks/[TASK-ID]/` — see what was being worked on

Do not start implementing until you've completed all 4 steps.

---

## 7. Maintenance Schedule

| Cadence | Action |
|---|---|
| After each task | Add a retrospective entry to `retrospectives.md` |
| Weekly | Promote checked-off lessons from retrospectives to subdirectory files |
| Monthly | Prune stale content — remove anything that no longer reflects how the project works |
