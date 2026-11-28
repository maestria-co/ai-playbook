---
name: task-plan
description: >
  Defines the canonical plan.md format used as a handoff document between agents
  and across context boundaries. Use this skill whenever creating a new task plan,
  resuming work on a task with an existing plan, updating an in-progress plan, or
  when writing a plan that another agent (or yourself after context reset) needs to
  pick up cold. If a task has 3+ steps or spans multiple sessions, you need a plan.md
  and this skill tells you the format.
user-invocable: false
---

# Skill: Task Plan

## Purpose

`plan.md` is a **handoff document** — it contains enough context for any agent
(or the same agent after a context clear) to resume work without re-reading the
entire codebase. It is not a progress tracker or a to-do list.

This skill defines the canonical format and rules for maintaining plan files.

---

## Canonical Format

Every `plan.md` lives in `.context/tasks/[TASK-ID]/plan.md` and follows this structure:

```markdown
# [TASK-ID]: [Short Title]

## Branch

`feature/TASK-ID-short-description`

## Objective

One paragraph. What are we building and why?

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Decisions

Key decisions made during planning or implementation.

- **Decision:** [What was decided]
  **Rationale:** [Why]

## Key Files

Files central to this task — helps the next agent load context fast.

- `path/to/file.ts` — [role in this task]
- `path/to/other.ts` — [role in this task]

## Task Breakdown

Ordered steps to complete the work.

1. [x] Step 1 — completed description
2. [ ] Step 2 — in progress description ← CURRENT
3. [ ] Step 3 — upcoming description

## Progress Log

Reverse-chronological entries. One per work session.

- **[Date/Session]:** What was accomplished, what's next

## Blockers

- [Blocker description] — [status: investigating / escalated / resolved]
```

---

## Section Guidance

### Objective

- One paragraph max
- Include the "why" — not just the "what"
- Should be understandable without additional context

### Acceptance Criteria

- Checkboxes (`- [ ]` / `- [x]`)
- Each criterion is independently verifiable
- Written from the user's perspective when possible
- Updated to `[x]` only when verified with evidence

### Decisions

- Record as you go — don't wait until the end
- Include rationale, not just the choice
- Reference ADRs in `.context/decisions/` for major decisions

### Key Files

- List only files actively touched or read for this task
- Update as the task reveals new files
- Remove files that turn out to be irrelevant

### Task Breakdown

- Ordered — dependencies flow top to bottom
- Mark current step with `← CURRENT`
- Check off completed steps with `[x]`
- Each step should be completable in one work session

### Progress Log

- Reverse chronological (newest first)
- Brief — 2–3 sentences per entry
- Always include "what's next" to guide resumption
- Write an entry at the end of every work session

### Blockers

- Only list actual blockers — not risks or concerns
- Include status so the next agent knows what's actionable
- Remove resolved blockers (or move to Decisions if the resolution was a decision)

---

## When to Create a Plan

| Situation                         | Create plan?                          |
| --------------------------------- | ------------------------------------- |
| Multi-step feature (3+ steps)     | Yes                                   |
| Bug fix requiring investigation   | Yes — helps track debugging progress  |
| Simple one-file change            | No — overkill                         |
| Refactoring across multiple files | Yes                                   |
| Research task                     | No — use `.context/tasks/[task-id]/research/` instead |

---

## When to Update a Plan

Update the plan whenever:

- A step is completed → check it off, add progress log entry
- A decision is made → add to Decisions section
- A new file becomes relevant → add to Key Files
- A blocker is found → add to Blockers
- Work session ends → add progress log entry with "what's next"

---

## Freshness Gate

Before continuing work on any step, verify the plan reflects current reality:

1. Read the **Task Breakdown** — does the current step match what you're about to do?
2. Read the **Progress Log** — does it accurately reflect what's been done?
3. Read **Decisions** — were any decisions made that aren't recorded?

**If the plan is stale** (e.g., steps were skipped, scope changed, a decision was made without recording it):
- Update the plan first — mark completed steps `[x]`, add decisions, update `← CURRENT`
- Only then proceed with the next step

**Rule:** A plan that doesn't match current state is worse than no plan — it actively misleads
the next agent. Fix it before using it.

---

## Cold Resume Protocol

When resuming a task from a plan:

1. Read the plan's **Objective** and **Acceptance Criteria** — understand the goal
2. Read the **Task Breakdown** — find the `← CURRENT` marker
3. Read the **Progress Log** (latest entry) — understand where things left off
4. Read the **Key Files** — load relevant code context
5. Check **Blockers** — address any before proceeding
6. Continue from the current step

---

## Constraints

- Plan files live only in `.context/tasks/[TASK-ID]/plan.md`
- Never delete a plan for an in-progress task
- Always update the progress log before ending a work session
- Keep the plan concise — if any section exceeds 30 lines, it needs pruning
- The plan is the source of truth for task state — not chat history

---

## Plan.md Template Structure

For tasks that span multiple sessions or involve frequent agent handoffs, use this
4-section template to keep active work visible and completed work out of the way.
Agents read **Active Task** and **Next Up** to resume — they skip **Completed Tasks**
by default.

```markdown
## Active Task

**Step:** [Current step name]
**Status:** In Progress

[1–3 sentences: what you are doing right now and any critical context for this step]

## Next Up

1. [Next step] — brief description
2. [Step after that] — brief description
3. [Further step] — brief description

## Blocked / Waiting

- [Blocker description] — [status] — waiting on [who/what]

_(Empty if no active blockers)_

<details>
<summary>Completed Tasks</summary>

- [x] [Step name] — [brief outcome or note]
- [x] [Step name] — [brief outcome or note]

</details>
```

### Section Guidance

**Active Task** — The current in-progress step. An agent must be able to pick up
work from this section alone. Keep it to 3–5 lines. Update it whenever the active
step changes.

**Next Up** — The ordered backlog of upcoming steps. Gives sequencing context
without requiring the full plan breakdown. Move a step here from Completed Tasks
when it finishes; promote it to Active Task when it starts.

**Blocked / Waiting** — Anything preventing progress. Leave empty if unblocked.
One line per blocker with a status note and who/what it depends on.

**Completed Tasks** — Historical record wrapped in a `<details>` block. Agents
skip this section during routine session starts. Read it only when historical
context is needed — for example, debugging a regression or understanding a past
decision.

### When to Use This Template

| Situation                                    | Use 4-section template? |
| -------------------------------------------- | ----------------------- |
| Task spans 3+ work sessions                  | Yes                     |
| Task Breakdown has 5+ steps                  | Yes                     |
| Multiple agents handing off work             | Yes                     |
| Short task, single session                   | No — standard format    |
| Simple bug fix or one-file change            | No — standard format    |

### Example

See `.context/tasks/MKT-0003/example-plan.md` for a realistic demonstration of
this template in use.
