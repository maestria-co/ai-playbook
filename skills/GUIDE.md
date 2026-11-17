# Pattern Guide: When to Use Each Pattern

Quick reference for selecting and composing skills in `skills/`.

---

## Quick Selection

| If your task involves…                            | Use                           |
| ------------------------------------------------- | ----------------------------- |
| Setting up `.context/` for a new project          | `initialize-repo`             |
| Setting up `.context/` for a monorepo             | `initialize-monorepo`         |
| Bootstrapping all projects in a VS Code workspace | `initialize-workspace`        |
| Locating the context_template                     | `find-context-template`       |
| Loading project context at task start             | `context-loader`              |
| Updating `.context/` after a task                 | `context-maintenance`         |
| Writing or reviewing `.context/` docs for quality | `context-document-guidelines` |
| Syncing `.context/` docs with the codebase        | `context-review`              |
| Deciding which skill to use                       | `using-skills`                |
| Breaking a complex goal into ordered tasks        | `planning-tasks`              |
| Creating or updating a task plan.md               | `task-plan`                   |
| Deciding whether to design first or implement     | `design-first`                |
| Evaluating options or filling a knowledge gap     | `researching-options`         |
| Making a system design or technology decision     | `designing-systems`           |
| Writing or modifying code                         | `implementing-features`       |
| Writing or running tests                          | `writing-tests`               |
| Debugging a bug systematically                    | `systematic-debugging`        |
| Checking work before marking complete             | `verification-checklist`      |
| Making a git commit                               | `commit-discipline`           |
| Reflecting after completing a task                | `task-retrospective`          |
| Promoting patterns to reusable skills             | `knowledge-graduation`        |
| Creating, editing, or evaluating a skill          | `writing-skills`              |
| Evaluating an agent system for design issues      | `agent-evaluation`            |
| Reviewing code against quality standards          | `code-quality-rules`          |
| Resolving context root for a monorepo/workspace   | `resolve-repo-context`        |
| Formatting a spec as a Jira user story            | `jira-story`                  |
| Formatting a spec as an Asana task                | `asana-story`                 |
| Formatting a spec as a Linear issue               | `linear-story`                |
| Defining and structuring sprint goals             | `sprint-goals`                |
| Writing or improving an RFC document              | `rfc-format`                  |
| Refactoring an existing RFC for clarity           | `rfc-refactor`                |
| Capturing meeting decisions and action items      | `post-meeting`                |
| Generating release notes from git history         | `deployment-release-notes`    |
| Researching pre-deployment requirements           | `deployment-release-research` |
| Updating or auditing project dependencies         | `dependency-management`       |
| Locating code patterns in a large codebase        | `code-identifier`             |
| Executing the technical release process           | `tech-release-guide`          |
| Researching release readiness and blockers        | `tech-release-research`       |
| Assessing impact/risk before a code change        | `impact-assessor`             |
| Evaluating evidence quality before acting on it   | `evidence-analyzer`           |
| Finding and prioritizing technical debt / hacks   | `workaround-detector`         |
| Orchestrating full bug triage end-to-end          | `triage-orchestration`        |
| Triaging and routing incoming support tickets     | `support-triage`              |
| Upgrading a language, framework, or major dep     | `upgrade-repo`                |
| Setting up git worktrees for parallel work        | `start-worktree`              |
| Categorizing issues/tickets for a backlog         | `categorizer`                 |
| Assessing compute/carbon footprint of a change    | `ecological-impact`           |
| Querying and analyzing application logs           | `log-query`                   |
| Analyzing code paths, patterns, and usage         | `code-analysis`               |

---

## Skills vs. Agents: When to Use Each

**Skills** run in the current context window — no new window, no delegation:
- Use when the work is simple enough to complete within the current session
- Use when you need the output immediately as input to the next step
- Invoked by reading the SKILL.md and following it directly

**Agents** run in a separate context window via the task tool — full isolation:
- Use when the work is complex enough to benefit from a dedicated context (implementation, testing, deep research)
- Use when you want to keep the manager's context clean (long-running sub-tasks)
- Use when the sub-task has its own plan, files, and decisions
- Invoked via the `task` tool with `agent_type: "[AgentName]"`

**Rule of thumb:** If the next step after this work requires the full output to be in
your context (e.g., reading a report before making a decision), use a skill. If the
sub-task is fire-and-verify (you check results, not process them inline), use an agent.

### Internal Skills (not user-invocable)

These skills are loaded by agents on demand. Do not invoke them directly.

| If your task involves…                                       | Internal skill                        |
| ------------------------------------------------------------ | ------------------------------------- |
| Investigating scope (unclear task, unknown approach)         | `task-plan-phase-investigation`       |
| Making architectural decisions as primary task work          | `task-plan-phase-architecture`        |
| Writing code when plan is ready                              | `task-plan-phase-implementation`      |
| Running tests as primary task concern                        | `task-plan-phase-testing`             |
| Closing a task (review, context updates, retro)              | `task-plan-phase-completion`          |
| Detecting tree position + initializing branch/root `.context/` | `context-specialist-impl`          |

---

## When to Use One Pattern vs. Compose Multiple

**Use a single pattern directly** for most tasks. The overhead of composing multiple
patterns is only justified when outputs from one pattern are required inputs for another.

**Compose patterns when:**

- Planning → Implementation → Tests (outputs chain: plan feeds implementation, implementation feeds tests)
- Research → Design → Implementation (research informs a design decision that informs code)
- A task has 3+ truly distinct steps that can't be collapsed

**Do not compose when:**

- You're just doing one thing (implement a feature, write a test)
- Two patterns are independent (research and test-writing for separate features)
- Two patterns already handle the task without orchestration overhead

---

## Pattern Pairs (Common Compositions)

### Design → Implement

```
designing-systems   →   implementing-features
```

Use when you need to decide _how_ to build something before building it.
The ADR produced by `designing-systems` is the spec for `implementing-features`.

### Implement → Test

```
implementing-features   →   writing-tests
```

The most common composition. Use after every non-trivial implementation.

### Plan → Implement → Test

```
planning-tasks   →   implementing-features   →   writing-tests
```

For features with 3+ steps. The plan breaks it down; each task gets its own
`implementing-features` + `writing-tests` cycle.

### Research → Design

```
researching-options   →   designing-systems
```

Use when a design decision requires technical evidence before the decision can be made.
Research produces a recommendation; `designing-systems` turns it into a documented ADR.

### Full Stack (complex feature)

```
planning-tasks
  → researching-options   (for unknowns flagged in plan)
  → designing-systems     (for architecture decisions)
  → implementing-features (per task in plan)
  → writing-tests         (per implementation)
```

---

## Pattern Summaries

### `initialize-repo`

- **Input:** A project repository without `.context/`
- **Output:** Populated `.context/` directory with project-specific details
- **When NOT to use:** `.context/` already exists
- **Degree of freedom:** Medium

### `context-loader`

- **Input:** A task to start or resume
- **Output:** Relevant context loaded into the agent's working memory
- **When NOT to use:** Trivial tasks, one-line changes
- **Degree of freedom:** Low

### `context-maintenance`

- **Input:** Completed task with new learnings
- **Output:** Updated `.context/` files, promoted retrospective items
- **When NOT to use:** Full codebase scan (use `context-review` instead)
- **Degree of freedom:** Low

### `using-skills`

- **Input:** Uncertain which skill to use
- **Output:** Selected skill(s) with invocation plan
- **When NOT to use:** You already know which skill to use
- **Degree of freedom:** Low

### `planning-tasks`

- **Input:** Ambiguous goal
- **Output:** `.context/plans/[feature].md` — ordered task list with acceptance criteria
- **When NOT to use:** Single well-defined task, or user already provided a breakdown
- **Degree of freedom:** Medium

### `task-plan`

- **Input:** Task that needs a plan.md handoff document
- **Output:** `.context/tasks/[TASK-ID]/plan.md` in canonical format
- **When NOT to use:** Simple one-file changes, research tasks
- **Degree of freedom:** Low

### `design-first`

- **Input:** New task (before implementation starts)
- **Output:** Decision: design first or implement directly
- **When NOT to use:** Task type is obvious (clear bug fix or clear design need)
- **Degree of freedom:** Low

### `researching-options`

- **Input:** A specific technical question
- **Output:** `.context/research/[topic].md` — recommendation with evidence
- **When NOT to use:** Obvious answers, business/product decisions
- **Degree of freedom:** High

### `designing-systems`

- **Input:** A design question or technology choice
- **Output:** `.context/decisions/ADR-NNN-title.md` — documented decision
- **When NOT to use:** Implementation details within an already-decided approach
- **Degree of freedom:** Medium

### `implementing-features`

- **Input:** Clear spec with acceptance criteria
- **Output:** Source code changes
- **When NOT to use:** Unclear spec, undecided architecture, no acceptance criteria
- **Degree of freedom:** Low

### `writing-tests`

- **Input:** Implemented code + spec
- **Output:** Test files with coverage report
- **When NOT to use:** Code not yet implemented
- **Degree of freedom:** Medium

### `systematic-debugging`

- **Input:** Bug report or unexpected behavior
- **Output:** Root-cause fix + regression test + verification evidence
- **When NOT to use:** Simple typo or config error (just fix it)
- **Degree of freedom:** Medium

### `verification-checklist`

- **Input:** Completed implementation (before reporting done)
- **Output:** Verification summary with evidence
- **When NOT to use:** Never skip entirely — use Quick Check minimum
- **Degree of freedom:** Low

### `commit-discipline`

- **Input:** Code changes ready to commit
- **Output:** Well-structured git commits with conventional messages
- **When NOT to use:** Generated commits (CI, bots)
- **Degree of freedom:** Low

### `task-retrospective`

- **Input:** Completed task
- **Output:** Entry in `.context/retrospectives/` with promotion items
- **When NOT to use:** Trivial one-line changes
- **Degree of freedom:** Medium

### `knowledge-graduation`

- **Input:** `.context/` patterns ready for promotion
- **Output:** New skill in `skills/` + updated GUIDE.md
- **When NOT to use:** Patterns that haven't met all 4 graduation criteria
- **Degree of freedom:** Medium

---

## Choosing by Task Type

| Task type                                   | Recommended pattern(s)                                                        |
| ------------------------------------------- | ----------------------------------------------------------------------------- |
| "Set up this new repo for AI agents"        | `initialize-repo`                                                             |
| "Set up our monorepo for AI agents"         | `initialize-monorepo`                                                         |
| "Set up all projects in this workspace"     | `initialize-workspace`                                                        |
| "Build this feature" (simple)               | `implementing-features` → `writing-tests`                                     |
| "Build this feature" (complex)              | `planning-tasks` → `implementing-features` × N → `writing-tests` × N          |
| "Fix this bug"                              | `systematic-debugging` → `writing-tests` (add regression test)                |
| "Triage this incident end-to-end"           | `triage-orchestration`                                                        |
| "Process these support tickets"             | `support-triage` → `triage-orchestration` (for bugs)                          |
| "Should we use library X or Y?"             | `researching-options`                                                         |
| "How should we design this system?"         | `designing-systems`                                                           |
| "What should we build next?"                | `planning-tasks`                                                              |
| "Refactor this module"                      | `planning-tasks` (if non-trivial) → `implementing-features` → `writing-tests` |
| "Upgrade our Node/Python/framework version" | `upgrade-repo`                                                                |
| "Update our dependencies"                   | `dependency-management`                                                       |
| "What breaks if I change X?"                | `impact-assessor`                                                             |
| "Find the tech debt in this codebase"       | `workaround-detector`                                                         |
| "Write a Jira story for this feature"       | `jira-story`                                                                  |
| "Write an Asana task for this feature"      | `asana-story`                                                                 |
| "Write a Linear issue for this feature"     | `linear-story`                                                                |
| "Write an RFC for this proposal"            | `rfc-format`                                                                  |
| "Is our `.context/` up to date?"            | `context-review`                                                              |
| "Review this SKILL.md file"                 | `writing-skills`                                                              |
| "This task needs architecture planning"     | `design-first` → `designing-systems` → `implementing-features`                |
| "I just finished a task"                    | `task-retrospective` → `context-maintenance`                                  |
| "Promote our best practices to skills"      | `knowledge-graduation`                                                        |

---

## Shared Conventions

All skills follow the conventions in `skills/_shared/conventions.md`:

- XML tag structure for structured output
- One-question clarity rule
- Self-verify before completing
- Stopping conditions and check-in format
- Context window management
- Anti-patterns

---

## Files Written by Each Pattern

| Pattern                       | Writes to                                                    |
| ----------------------------- | ------------------------------------------------------------ |
| `initialize-repo`             | `.context/` directory (full setup)                           |
| `initialize-monorepo`         | `.context/` root + `packages/[name]/.context/`               |
| `initialize-workspace`        | `.context/` per project + workspace-level overview           |
| `find-context-template`       | Nothing (search and report only)                             |
| `context-loader`              | Nothing (read-only)                                          |
| `context-maintenance`         | `.context/` documentation files                              |
| `context-document-guidelines` | Nothing (quality standards reference)                        |
| `using-skills`                | Nothing (routing only)                                       |
| `planning-tasks`              | `.context/plans/`                                            |
| `task-plan`                   | `.context/tasks/[TASK-ID]/plan.md`                           |
| `design-first`                | Nothing (triage decision) or lightweight design in `plan.md` |
| `researching-options`         | `.context/research/`                                         |
| `designing-systems`           | `.context/decisions/`                                        |
| `implementing-features`       | Source code files                                            |
| `writing-tests`               | Test files                                                   |
| `systematic-debugging`        | Source code (fix) + test files (regression)                  |
| `verification-checklist`      | Nothing (verification summary in chat)                       |
| `commit-discipline`           | Git commits                                                  |
| `task-retrospective`          | `.context/retrospectives/`                                   |
| `knowledge-graduation`        | `skills/[new-skill]/SKILL.md` + `GUIDE.md`                   |
| `context-review`              | `.context/` documentation files                              |
| `common-constraints`          | Nothing (behavioral constraints, always active)              |
| `testing-discipline`          | Nothing (quality standards, referenced during testing)       |
| `jira-story`                  | Jira story markdown (`.context/tasks/[ID]/story.md`)         |
| `asana-story`                 | Asana task markdown (`.context/tasks/[ID]/story.md`)         |
| `linear-story`                | Linear issue markdown (`.context/tasks/[ID]/story.md`)       |
| `sprint-goals`                | Sprint planning doc (in chat or file)                        |
| `rfc-format`                  | RFC document (in chat or file)                               |
| `rfc-refactor`                | Updated RFC document                                         |
| `post-meeting`                | Meeting notes doc (in chat or file)                          |
| `deployment-release-notes`    | Release notes entry                                          |
| `deployment-release-research` | Pre-deployment research report                               |
| `dependency-management`       | Updated manifest + lock files; git commits per dep           |
| `code-identifier`             | Nothing (search and report only)                             |
| `tech-release-guide`          | Nothing (procedural guidance; outputs git tags, commits)     |
| `tech-release-research`       | Release readiness report                                     |
| `impact-assessor`             | Impact assessment report (in chat)                           |
| `evidence-analyzer`           | Evidence quality assessment (in chat)                        |
| `workaround-detector`         | Workaround report; optionally tickets/`.context/` notes      |
| `categorizer`                 | Categorized issue table (in chat or file)                    |
| `support-triage`              | Triage report; routed tickets                                |
| `upgrade-repo`                | Updated manifests + source code; git commits                 |
| `start-worktree`              | Git worktree directory                                       |
| `categorizer`                 | Categorized issue table (in chat or file)                    |
| `ecological-impact`           | Impact report (in chat)                                      |
| `log-query`                   | Findings summary (in chat)                                   |
| `code-analysis`               | Analysis report (in chat or `.context/`)                     |
| `writing-skills`              | `skills/[new-skill]/SKILL.md` (guidance; actual write is manual) |
| `agent-evaluation`            | Evaluation report (in chat)                                  |
| `code-quality-rules`          | Nothing (quality standards reference — loaded by reviewer)   |
| `resolve-repo-context`        | Nothing (returns structured JSON; run as explore sub-agent)  |
| `task-plan-phase-investigation` | `plan.md` (investigation checklist + two-step seed)        |
| `task-plan-phase-architecture` | `plan.md` Decisions section                                 |
| `task-plan-phase-implementation` | Source code (via @coder); updates `plan.md` progress      |
| `task-plan-phase-testing`     | Test files (via @tester); updates `plan.md` progress         |
| `task-plan-phase-completion`  | `.context/retrospectives/` + context updates (via retro)     |
| `context-specialist-impl`     | `.context/` directory (branch or root initialization)        |
