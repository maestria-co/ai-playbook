# AI Skill Kit

Reusable agents, skills, and prompts for AI-assisted software development. Structured as a `.copilot`-compatible customization kit.

Works with **GitHub Copilot**, **Claude Code**, and any AI assistant that accepts system prompts.

---

## Structure

```
agents/           # Agent definitions (*.agent.md)
skills/           # Composable skills (SKILL.md per folder)
                  #   _shared/context_template/ — .context/ template used by initialize-* skills
.context/         # Project context (decisions, retrospectives)
context_template/ # Template for generating .context/ in other projects
recipes/          # End-to-end workflow examples
build-guide/      # Build guide documentation
```

---

## Skills

19 skills organized into four categories:

### Infrastructure Skills

| Skill                 | When to use                                 | File                                  |
| --------------------- | ------------------------------------------- | ------------------------------------- |
| `initialize-repo`     | Set up `.context/` for a new project        | `skills/initialize-repo/SKILL.md`     |
| `context-loader`      | Load project context at task start          | `skills/context-loader/SKILL.md`      |
| `context-maintenance` | Update `.context/` after a task             | `skills/context-maintenance/SKILL.md` |
| `context-review`      | Full codebase scan to sync `.context/` docs | `skills/context-review/SKILL.md`      |
| `using-skills`        | Discover and select the right skill         | `skills/using-skills/SKILL.md`        |

### Planning & Design Skills

| Skill                 | When to use                                       | File                                  |
| --------------------- | ------------------------------------------------- | ------------------------------------- |
| `planning-tasks`      | Break a goal into ordered, dependency-aware tasks | `skills/planning-tasks/SKILL.md`      |
| `task-plan`           | Create/update canonical plan.md handoff documents | `skills/task-plan/SKILL.md`           |
| `design-first`        | Triage: design first or implement directly        | `skills/design-first/SKILL.md`        |
| `researching-options` | Evaluate libraries, approaches, or technologies   | `skills/researching-options/SKILL.md` |
| `designing-systems`   | Make an architecture decision and write an ADR    | `skills/designing-systems/SKILL.md`   |

### Implementation Skills

| Skill                   | When to use                               | File                                    |
| ----------------------- | ----------------------------------------- | --------------------------------------- |
| `implementing-features` | Write or modify code from a clear spec    | `skills/implementing-features/SKILL.md` |
| `writing-tests`         | Write and run tests for an implementation | `skills/writing-tests/SKILL.md`         |
| `systematic-debugging`  | Structured 4-phase debugging process      | `skills/systematic-debugging/SKILL.md`  |

### Discipline & Process Skills

| Skill                    | When to use                                   | File                                     |
| ------------------------ | --------------------------------------------- | ---------------------------------------- |
| `common-constraints`     | Universal agent rules (always active)         | `skills/common-constraints/SKILL.md`     |
| `verification-checklist` | Pre-completion verification with evidence     | `skills/verification-checklist/SKILL.md` |
| `testing-discipline`     | TDD practices and test quality standards      | `skills/testing-discipline/SKILL.md`     |
| `commit-discipline`      | Git commit conventions and branch management  | `skills/commit-discipline/SKILL.md`      |
| `task-retrospective`     | Structured reflection after completing tasks  | `skills/task-retrospective/SKILL.md`     |
| `knowledge-graduation`   | Promote validated patterns to reusable skills | `skills/knowledge-graduation/SKILL.md`   |
| `evaluate-skill`         | Evaluate a SKILL.md file for quality          | `skills/evaluate-skill/SKILL.md`         |

**Skill selection guide:** `skills/GUIDE.md`

### Skill Structure: Sidecar References Pattern

Some skills use a **sidecar references pattern** to keep the main SKILL.md concise (~150–200 lines) while preserving detailed content in organized reference files. This pattern improves readability for agents and humans alike.

**How it works:**
1. Main `SKILL.md` contains the core workflow, pre-flight checks, and execution steps
2. `references/` subdirectory contains focused files by use case:
   - `code-patterns.md` — Code examples and implementation patterns
   - `edge-cases.md` — Boundary conditions, gotchas, and how to handle them
   - `troubleshooting.md` — Common problems, diagnostics, and resolution steps

3. Cross-references in the main file point agents to reference files at natural decision points

**Example skills using this pattern:**
- `implementing-features` — See `references/code-patterns.md` for implementation examples
- `writing-tests` — See `references/code-patterns.md`, `edge-cases.md`, and `troubleshooting.md` for testing examples
- `agentic-evaluation` — See `references/output-template.md` for report structure

**Why this pattern:**
- ✅ Main files remain actionable without reading references
- ✅ Reference files are independently readable
- ✅ Agents can load context on-demand, reducing token overhead
- ✅ Natural decision points guide agents to supplementary details exactly when needed

---

## Agents

The **Manager** is the primary entry point for all multi-step development tasks. It reads project context, delegates to specialist agents, tracks progress, and enforces discipline constraints.

### Core Agents (10 total)

| Agent      | File                         | Description                                      |
| ---------- | ---------------------------- | ------------------------------------------------ |
| Manager    | `agents/manager.agent.md`    | Orchestrates workflows, delegates to specialists |
| Planner    | `agents/planner.agent.md`    | Task decomposition and planning                  |
| Researcher | `agents/researcher.agent.md` | Technology evaluation and research               |
| Architect  | `agents/architect.agent.md`  | System design and architecture decisions         |
| Coder      | `agents/coder.agent.md`      | Code implementation from specs                   |
| Tester     | `agents/tester.agent.md`     | Test writing and execution                       |
| Reviewer   | `agents/reviewer.agent.md`   | Code review for correctness and quality          |

### Specialized Support Agents

| Agent           | File                              | Description                     |
| --------------- | --------------------------------- | ------------------------------- |
| Product-Manager | `agents/product-manager.agent.md` | Requirements and specifications |
| Code-Researcher | `agents/code-researcher.agent.md` | Deep codebase analysis          |

All agents follow: [`agents/_shared/conventions.md`](agents/_shared/conventions.md)
Handoff protocol: [`agents/_shared/handoff-protocol.md`](agents/_shared/handoff-protocol.md)

---

## Installation

Copy all skills and agents into your AI tool's config folder:

**macOS / Linux — GitHub Copilot**

```bash
./install.sh
```

**macOS / Linux — Claude Code**

```bash
./install.sh --claude
```

**Windows — GitHub Copilot**

```powershell
.\install.ps1
```

**Windows — Claude Code**

```powershell
.\install.ps1 -Claude
```

Re-run after any `git pull` to pick up updates. The `--claude` / `-Claude` flag installs to `~/.claude/skills/` and `~/.claude/agents/`, then automatically updates your `~/.claude/CLAUDE.md` with a skills reference table so Claude Code knows what's available.

### Agent frontmatter is translated on install

Agent definitions are authored once in a tool-neutral vocabulary. `install.sh --claude`
rewrites `tools:` and `model:` into Claude Code's names as it installs:

| Authored token | Claude Code tools |
| --- | --- |
| `agent` | `Agent` |
| `read` | `Read` |
| `edit` | `Edit`, `Write` |
| `search` | `Grep`, `Glob` |
| `execute` | `Bash` |
| `web` | `WebFetch`, `WebSearch` |
| `skill` | `Skill` |
| `*` | `*` |

`model:` has its dots converted to dashes (`claude-sonnet-4.5` → `claude-sonnet-4-5`).
An unrecognized token is passed through unchanged with a warning rather than dropped.

> **Never hand-edit the installed files in `~/.claude/agents/`.** Every install overwrites
> them. Edit the agent in this repo and re-run the installer.

---

## Task Tracking with Hooks

Agent-defs now includes **global task tracking** using a hybrid architecture.

### Setup

Run once to install hooks:

```bash
./setup-hooks.sh    # Linux/macOS
```

```powershell
.\setup-hooks.ps1   # Windows
```

### How It Works

1. **Manager reads state:** Step 0 loads `~/.copilot/active-tasks.json` and checks for task ID mentions
2. **Hooks write state:** Update timestamps on session start/end, auto-register new tasks, auto-archive old tasks
3. **Mention task ID anywhere:** Manager auto-resumes that task
4. **No interruptions:** Manager never blocks your workflow unless you explicitly ask
5. **Auto-cleanup:** Tasks inactive for 7+ days automatically archive via sessionEnd hook

### Task Lifecycle

- **Create:** `@manager [request]` → Manager creates task folder + registers globally
- **Update:** Every plan.md update → `last_active` timestamp refreshed
- **Complete:** `@manager wrap up` → Task archived + retrospective written
- **Resume:** Mention task ID in any request → Auto-checkout + load plan.md

### Commands

- `@manager show active` — List active tasks
- `@manager complete TASK-ID` — Mark done without resuming
- `@manager wrap up` — Complete current task

---

## Quick Start

See [`QUICK_START.md`](QUICK_START.md) for copy-paste prompt templates for each skill.

**Basic pattern:**

```
Use the [skill-name] skill.

<task>[what you want to do]</task>
<context>
Stack: [language/framework]
Relevant files: [paths]
Constraints: [any limits]
</context>
```

---

## Workflow Recipes

End-to-end examples for common development tasks:

| Recipe                       | Skills used                                                  | File                          |
| ---------------------------- | ------------------------------------------------------------ | ----------------------------- |
| Simple bug fix               | `implementing-features` + `writing-tests`                    | `recipes/simple-task.md`      |
| Multi-file feature           | `planning-tasks` + `implementing-features` + `writing-tests` | `recipes/complex-task.md`     |
| Architecture decision        | `researching-options` + `designing-systems`                  | `recipes/design-task.md`      |
| Full feature (OAuth example) | All 5 core skills                                            | `recipes/feature-workflow.md` |

---

## Troubleshooting

Pattern output too vague? Wrong scope? Test blocked? See [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

---

## Key Principles

- **Simplicity first** — add complexity only when it demonstrably improves outcomes
- **Context awareness** — write state to `.context/` before context clears; use git as checkpoints
- **Human checkpoints** — stop and check in after 3–5 major actions or before irreversible changes
- **Verify before done** — check each acceptance criterion explicitly before signaling completion
