---
name: implementing-features
description: >
  Implements a feature, bug fix, or refactor from a clear specification. Use when:
  the task has clear acceptance criteria, a bug is diagnosed and the fix is understood,
  or code needs refactoring with a clear goal. Do not use when: the spec is unclear,
  an architecture decision still needs to be made, or the task needs to be broken into
  multiple steps first.
degree_of_freedom: low
---

# Skill: Implementing Features

## Purpose

Write the minimum correct code that satisfies the spec and matches existing patterns.
Read before you write. Implement minimally. Verify before declaring done.

Do not invoke this pattern if the spec is unclear or acceptance criteria are missing.
Use `planning-tasks` to define the task first, or ask one clarifying question.

---

## Pre-flight Checks

**Check 1 — Confirm the spec is complete**

Read the task specification. Verify it includes:
- What to build (feature/fix/refactor description)
- Acceptance criteria (testable conditions that define "done")
- Output location (which files to create or modify)

- If any of these is missing → ask one focused question to resolve the most critical gap.
  Do not start implementation until you can verify completion.
- If spec is complete → proceed.

**Check 2 — Read before writing**

Read in this order before writing a single line of code:

1. The spec and acceptance criteria
2. Existing code in the area being changed (patterns, naming, error handling)
3. `.context/decisions/` ADRs relevant to this area

**Apply content-aware reading strategies:**
- If reading JSON config → use jq to query specific fields
- If reading code → grep for exports/functions first, then view_range for relevant sections
- If checking logs → filter for errors/warnings with grep before requesting full logs
- See `context-loader` skill for complete content-aware patterns

- If an ADR constrains this implementation → follow it. Do not contradict ADRs silently.
- If you discover a conflict between the spec and an existing ADR → stop and surface it.

**Refer to `references/code-patterns.md` for real-world examples** of model implementation, bug fixing, and spec clarification patterns.

---

## Execution Steps

### Step 1 — Restate the Acceptance Criteria

Write out each acceptance criterion before touching code. This is your "definition of done."
You will check each criterion explicitly before completing this pattern.

### Step 2 — Identify the Scope

Determine exactly which files will change. List them before starting.

If you find that implementing the spec requires changing code significantly outside your
listed scope → stop. Surface this as a scope change before proceeding.

### Step 3 — Implement Minimally

Write the smallest change that satisfies the spec:
- Match existing naming conventions, error handling patterns, and code style
- No speculative refactors ("while I'm here I'll also...")
- No unasked features (YAGNI)
- One concern per function
- Follow SOLID, and extract shared code on the third copy, not the second (`applying-design-principles`)
- Inject dependencies; avoid global state — untestable code will fail in `writing-tests`

For bugs: fix the root cause, not just the symptom. State what the root cause was.

**See `references/code-patterns.md` for detailed examples of common patterns** (new models, bug fixes, spec clarification).

### Step 4 — Verify

Run the build. Confirm it compiles and passes lint.

- If build fails → fix before moving on. Do not hand off failing code.
- If you cannot run the build → note this explicitly in the output.

### Step 5 — Self-Review

Read your own diff as if you were reviewing someone else's work. Check:

- [ ] Every acceptance criterion is met
- [ ] No regressions introduced in adjacent code
- [ ] No secrets, tokens, or credentials committed
- [ ] Error paths handled explicitly (no silent swallows)
- [ ] No dead code (commented-out blocks, unused imports)

If any check fails → fix it before completing.

---

## Output Format

```
Implemented: [Task name]

Files changed:
- [path] — [what changed and why, if non-obvious]

Acceptance criteria:
- [x] [criterion — verified]
- [x] [criterion — verified]

Key decisions:
- [Any non-obvious choice made and why]
- [ADR followed: ADR-NNN if applicable]

Suggested next: writing-tests (verify implementation with tests)
```

---

## Constraints

- Do not modify code outside the defined task scope without explicit approval
- Do not make architecture decisions — if one is needed, stop and use `designing-systems`
- Do not signal completion without verifying all acceptance criteria
- Do not commit secrets — use environment variables
- Do not silently swallow errors — every failure path must handle failure explicitly
- Write testable code — inject dependencies, avoid global state
- Scope: reads and writes source code files; reads `.context/decisions/`
