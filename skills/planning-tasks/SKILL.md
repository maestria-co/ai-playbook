---
name: planning-tasks
description: >
  Breaks an ambiguous goal into an ordered, concrete, executable task list with
  acceptance criteria and dependencies. Use when: the goal has 3+ distinct steps,
  multiple areas of the codebase will be touched, or scope is unclear enough that
  wrong assumptions could waste significant effort. Do not use when: task is a
  single well-defined action or the user has already provided a step-by-step breakdown.
degree_of_freedom: medium
---

# Skill: Planning Tasks

## Purpose

Turn an ambiguous goal into an ordered list of concrete, executable tasks — each with
a clear input, output, and testable acceptance criteria. The plan becomes the shared
source of truth for implementation. Write it before writing code.

Do not invoke this pattern for a single well-defined task. If you already know exactly
what to do and how, start doing it. Planning is overhead; plan only when it reduces more
risk than it creates.

---

## Pre-flight Checks

**Check 1 — Understand the project context**

Read `.context/overview.md` if it exists.

- If it exists → read it before proceeding. Note the tech stack, current state, and constraints.
- If it does not exist → proceed, but note that your plan will lack full project context.

**Check 2 — Check for existing plans**

Check `.context/tasks/*/plan.md` for any existing plan for this feature or goal.

- If a plan exists and is recent → read it. Determine if this is an update or a new plan.
- If no plan exists → proceed to create one.

---

## Execution Steps

### Step 1 — Restate the Goal

Restate the goal in your own words. Include:
- What success looks like (done criteria)
- What is explicitly out of scope

If the goal is still unclear after restating, ask one focused question before proceeding.
State your assumption if you proceed without asking.

### Step 2 — Inventory Existing Work

Scan the relevant parts of the codebase and `.context/` files. Identify:
- What already exists that this feature builds on
- Existing patterns, naming conventions, and file structure to follow
- What could break if changed

Do not read files you do not need. Search specifically, not broadly.

### Step 3 — Identify Unknowns

List any questions that would block planning or execution. Separate them:

- **Blocks planning** → resolve now by marking as a research task or architecture task before implementation tasks
- **Blocks execution of step N** → include as a dependency in the task that needs it

Never assume unknowns away silently. State them explicitly in the plan.

### Step 4 — Write Tasks

Write each task using this format:

```
### Task N: [Verb + Noun] (S/M/L)
Depends on: Task N-1 | none
Input: [specific files or prior task outputs]
Output: [named file or artifact — be specific]
Acceptance criteria:
- [ ] [Testable condition — verifiable, not vague]
- [ ] [Another condition]
Scope out: [what this task explicitly does NOT include]
```

Rules for tasks:
- Use precise verbs: `create`, `validate`, `configure`, `migrate` — not `handle`, `manage`, `update`
- Size tasks S (< 1 hour), M (half day), L (full day). Split anything larger than L.
- One output per task. If a task has multiple outputs, split it.
- Acceptance criteria must be testable. "Works correctly" is not testable. "Returns 401 for missing token" is.

### Step 5 — Note Parallel Opportunities

Identify tasks that have no dependency on each other and can run in parallel.
Mark them explicitly: `(can run parallel with Task N)`.

### Step 6 — Save the Plan

Write the complete plan to `.context/tasks/<task-id>/plan.md`. If no tracker id
exists, generate one (`local-YYYY-MM-DD-<slug>`) and use it — the same rule
research reports follow. Use kebab-case for the slug:
`local-2026-11-25-oauth-implementation`, not `OAuth Implementation`.

The filename is always `plan.md`; the task id is what distinguishes one plan
from another. A plan is a task artifact, so it is pruned when its task folder
is — see `task-plan`, which owns the file's format.

---

## Output Format

```
Plan: [Feature name]

Saved: .context/tasks/<task-id>/plan.md
Tasks: N total (S: x, M: y, L: z)
Unknowns flagged: [description] | none
Parallel opportunities: Task N and Task M can run together | none
```

---

## Examples

<examples>

<example>
<scenario>Breaking down an OAuth 2.0 feature with multiple components</scenario>
<input>
<task>Add OAuth 2.0 authentication to the existing Express API. Support Google and GitHub.</task>
<context>
- App currently uses session-based auth with express-session
- Existing models in src/models/ using Sequelize ORM
- See .context/decisions/ADR-003-auth-strategy.md for prior auth decisions
- Must not break existing session-based auth for internal routes
</context>
</input>
<output>
Plan: OAuth 2.0 Authentication

### Task 1: Research refresh token rotation approach (S)
Depends on: none
Input: .context/decisions/ADR-003-auth-strategy.md, current auth middleware
Output: .context/tasks/MAE-0031/research/oauth-refresh-tokens.md
Acceptance criteria:
- [ ] At least 2 approaches compared
- [ ] Recommendation made with security rationale
Scope out: Implementation — research only

### Task 2: Create OAuthProvider model and migration (M)
Depends on: Task 1
Input: .context/tasks/MAE-0031/research/oauth-refresh-tokens.md, src/models/User.js (style reference)
Output: src/models/OAuthProvider.js, db/migrations/YYYYMMDD-create-oauth-provider.js
Acceptance criteria:
- [ ] Model includes userId foreign key referencing users table
- [ ] Includes timestamps (createdAt, updatedAt)
- [ ] Migration runs without errors on a clean DB
Scope out: Tests (Task 4), Google/GitHub OAuth flow (Task 3)

### Task 3: Implement Google OAuth flow (L)
Depends on: Task 2
Input: OAuthProvider model, .context/decisions/ADR-003-auth-strategy.md
Output: src/routes/auth/google.js, src/middleware/oauth.js
Acceptance criteria:
- [ ] Google OAuth login redirects correctly
- [ ] Token stored in OAuthProvider on success
- [ ] Existing session auth routes unaffected
Scope out: GitHub OAuth (Task 5), tests (Task 4)

Tasks: 5 total (S: 1, M: 2, L: 2)
Unknowns flagged: refresh token strategy — blocked until Task 1 research complete
Parallel: Task 4 (tests) and Task 5 (GitHub) can run parallel after Task 3
</output>
</example>

<example>
<scenario>Planning a database migration with risk of data loss</scenario>
<input>
<task>Rename the `user_name` column to `username` across the entire application.</task>
<context>
- PostgreSQL database, ~50k rows in users table
- Column referenced in 12 files (found via grep)
- Production deployment happens Friday
</context>
</input>
<output>
Plan: Rename user_name to username

### Task 1: Audit all references to user_name (S)
Depends on: none
Input: codebase grep results
Output: .context/tasks/local-2026-11-25-username-migration/plan.md (list of all files + line numbers)
Acceptance criteria:
- [ ] Every reference to user_name documented
- [ ] Each reference categorized: SQL query, ORM, test, API response
Scope out: Any changes — audit only

### Task 2: Write zero-downtime migration (M)
Depends on: Task 1
Input: audit document
Output: db/migrations/YYYYMMDD-rename-user-name.js
Acceptance criteria:
- [ ] Migration adds username column, copies data, drops user_name
- [ ] Rollback migration restores original state
- [ ] Tested on staging with production-size dataset
Scope out: Code changes (Task 3)

Tasks: 3 total (S: 1, M: 1, M: 1)
Unknowns flagged: zero-downtime strategy for column rename — resolve in Task 2
</output>
</example>

<example>
<scenario>Simple feature that does NOT need this pattern</scenario>
<input>
<task>Add a `last_login` timestamp field to the User model.</task>
</input>
<output>
This task is a single well-defined action. Do not plan — implement directly using
the implementing-features pattern.

If you want to note it: "Add last_login (timestamp, nullable) to User model and
migration. Update login handler to set it on successful auth."
</output>
</example>

</examples>

---

## Constraints

- Do not write implementation code — pseudocode in task notes is acceptable
- Do not make architecture decisions — flag design questions as a separate `designing-systems` task
- Do not assume unknowns away — state them explicitly and create tasks to resolve them
- Do not over-plan: a 20-task plan for a 3-hour feature adds overhead that slows execution
- Do not under-plan: missing tasks surface as surprises mid-execution
- Write plans to `.context/tasks/<task-id>/plan.md` — do not deliver plans only in chat
- If goal is unclear after one clarifying question, state your assumption and proceed
