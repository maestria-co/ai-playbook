# Quick Start — Agentless Patterns

Get work done immediately. Pick your task type and use the pattern directly.

---

## I want to...

### Break a goal into tasks
**Pattern:** `planning-tasks`

```
Use the planning-tasks skill.

<task>Break this goal into an ordered, dependency-aware task list: [GOAL]</task>
<context>
Project: [brief description]
Stack: [language/framework]
Existing relevant code: [files or none]
Constraints: [deadline, scope limits, or none]
</context>
```

Expected output: ordered task list with S/M/L estimates, flagged unknowns, parallel tasks identified.
Saved to: `.context/tasks/[ID]/plan.md`

---

### Evaluate a library, tool, or approach
**Pattern:** `researching-options`

```
Use the researching-options skill.

<task>Which [library/tool/approach] should we use for [PROBLEM]?</task>
<context>
Project type: [description]
Stack: [language/framework]
Key constraints: [performance, license, bundle size, etc.]
Options already considered: [list or none]
</context>
```

Expected output: one recommendation with rationale, honest tradeoffs, confidence level.
Saved to: `.context/tasks/[ID]/research.md`

---

### Make an architecture decision
**Pattern:** `designing-systems`

```
Use the designing-systems skill.

<task>Decide [DECISION TO MAKE]</task>
<context>
Project: [description]
Relevant constraints: [scale, team size, existing tech]
Options in play: [list or "evaluate"]
Reversibility: [one-way or two-way door]
</context>
```

Expected output: ADR with decision, rationale, rejected alternatives, consequences.
Saved to: `.context/decisions/ADR-NNN-[title].md`

---

### Implement a feature or fix
**Pattern:** `implementing-features`

```
Use the implementing-features skill.

<task>[WHAT NEEDS TO BE DONE]</task>
<context>
Spec or acceptance criteria:
- [ ] [criterion 1]
- [ ] [criterion 2]
Relevant files: [list]
Patterns to follow: [reference or none]
</context>
```

Expected output: implementation with self-review diff summary, acceptance criteria verified.

---

### Write or run tests
**Pattern:** `writing-tests`

```
Use the writing-tests skill.

<task>Write tests for [FILE OR COMPONENT]</task>
<context>
Implementation file(s): [paths]
Test framework: [jest/pytest/etc.]
Coverage target: [% or "standard"]
Special cases to cover: [auth, concurrency, etc. or none]
</context>
```

Expected output: passing tests with coverage report, or blocked report with specific blocker.

---

### Orchestrate a multi-step workflow
**Pattern:** `coordinating-work`

> Use this only when you have 3+ interdependent patterns. For 1-2 patterns, chain them directly.

```
Use the coordinating-work skill.

<task>[HIGH-LEVEL GOAL]</task>
<context>
Scope: [what's in, what's out]
Key constraints: [timeline, breaking-change rules, etc.]
</context>
```

Expected output: sequenced pattern plan with delegation templates for each step.

---

## Common Combinations

| Goal | Patterns (in order) |
|---|---|
| Add a feature | `planning-tasks` → `implementing-features` × N → `writing-tests` |
| Add a feature with unknowns | `researching-options` → `designing-systems` → `planning-tasks` → `implementing-features` → `writing-tests` |
| Fix a bug | `implementing-features` → `writing-tests` |
| Evaluate and decide | `researching-options` → `designing-systems` |
| Refactor | `designing-systems` (decide scope) → `implementing-features` × N → `writing-tests` |

---

## Where Output Goes

| Output type | File location |
|---|---|
| Task plan | `.context/tasks/[ID]/plan.md` |
| Research report | `.context/tasks/[ID]/research.md` |
| Architecture decision | `.context/decisions/ADR-NNN-[title].md` |
| Implementation | Source code (git committed) |
| Test results | Test files + brief summary |
| Lessons learned | `.context/retrospectives/YYYY-MM-DD.md` |

---

## First Time? Try This

1. **Read** `.context/overview.md` — 2 minutes
2. **Create** `.context/tasks/[TASK-ID]/brief.md` — write the goal + acceptance criteria
3. **Pick** a pattern from the table above
4. **Paste** the template, fill in the `<context>` block, run it
5. **Write** a retrospective entry when done

That's the full loop. No routing, no Manager, no orchestration needed.
