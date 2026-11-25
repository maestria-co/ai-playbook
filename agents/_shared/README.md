# Agent Definitions

This directory contains reusable, platform-agnostic AI agent definitions for software development teams. Each agent is a markdown file with a detailed system prompt, designed to be loaded into any AI assistant (GitHub Copilot, Claude, ChatGPT, etc.).

---

## What Are Agents?

An agent is an AI assistant operating under a specific role with clear responsibilities, constraints, and behaviors. Rather than using a single general-purpose AI for everything, agents give the AI a focused identity and set of rules — making outputs more consistent, predictable, and high-quality.

Think of agents like specialized team members:

- You wouldn't ask your QA engineer to design your database schema.
- You wouldn't ask your architect to write unit tests.
- Same principle applies here.

---

## Agent Roster

### Core Agents

| Agent          | File                  | One-Sentence Role                                                       |
| -------------- | --------------------- | ----------------------------------------------------------------------- |
| **Manager**    | `manager.agent.md`    | Orchestrates all agents, interfaces with the user, and tracks progress. |
| **Planner**    | `planner.agent.md`    | Breaks goals into concrete, ordered tasks with dependencies.            |
| **Researcher** | `researcher.agent.md` | Evaluates options, fills knowledge gaps, and produces research reports. |
| **Architect**  | `architect.agent.md`  | Makes system design and technology decisions, documents as ADRs.        |
| **Coder**      | `coder.agent.md`      | Implements features and fixes from clear specifications.                |
| **Tester**     | `tester.agent.md`     | Writes tests, validates implementations, reports coverage and bugs.     |
| **Reviewer**   | `reviewer.agent.md`   | Reviews code for correctness, quality, and standards compliance.        |

### Orchestration Agents

| Agent                 | File                         | One-Sentence Role                                                     |
| --------------------- | ---------------------------- | --------------------------------------------------------------------- |
| **Workspace-Manager** | `workspace-manager.agent.md` | Coordinates tasks across multiple projects in a multi-root workspace. |
| **Monorepo-Manager**  | `monorepo-manager.agent.md`  | Orchestrates tasks across sub-projects in a monorepo.                 |

### Specialized Support Agents

| Agent                  | File                          | One-Sentence Role                                                   |
| ---------------------- | ----------------------------- | ------------------------------------------------------------------- |
| **Dev-Support-Triage** | `dev-support-triage.agent.md` | Triages bug reports and support requests, routes to specialists.    |
| **Product-Manager**    | `product-manager.agent.md`    | Gathers and structures requirements into actionable specifications. |
| **Code-Researcher**    | `code-researcher.agent.md`    | Deep codebase analysis, pattern detection, and code archaeology.    |

---

## Workflow Overview

All user requests flow through the **Manager**. The Manager decides which specialists to invoke and in what order. For multi-project work, **Workspace-Manager** or **Monorepo-Manager** serves as the entry point and delegates to Manager instances per project.

```
User Request
    │
    ├── (multi-project) ──► Workspace-Manager / Monorepo-Manager
    │                              │
    │                              └──► Manager (per project)
    │
    ▼
 Manager  ◄──────────────────────────────────────────────────┐
    │                                                        │
    ├──► Product-Manager  (structure requirements)           │
    │                                                        │
    ├──► Planner          (decompose the work)               │
    │       └──► Researcher      (if unknowns exist)         │
    │                                                        │
    ├──► Code-Researcher  (understand existing code)         │
    │                                                        │
    ├──► Architect        (design decisions needed)          │
    │                                                        │
    ├──► Coder            (implementation)                   │
    │                                                        │
    ├──► Tester           (validation & quality)             │
    │                                                        │
    ├──► Reviewer         (code review)                      │
    │                                                        │
    ├──► Dev-Support-Triage (bug report triage)              │
    │                                                        │
    └──► Report back to Manager ─────────────────────────────┘
```

**Typical flow for a new feature:**

1. User describes the goal to **Manager**
2. **Manager** asks **Product-Manager** to structure requirements (if vague)
3. **Manager** asks **Planner** to break it down
4. **Planner** identifies unknowns → **Researcher** fills gaps
5. **Manager** asks **Architect** to review design decisions
6. **Manager** asks **Coder** to implement
7. **Coder** signals done → **Tester** validates
8. **Reviewer** checks code quality
9. **Manager** reports outcome to user

---

## How to Use These Agents

### Option A: Direct invocation (Copilot / Claude chat)

Paste the contents of an agent file at the start of your conversation as a system prompt, then proceed with your request.

```
[paste contents of agents/manager.md]

Hi, I need to add user authentication to my Express app.
```

### Option B: Reference in your project's copilot-instructions.md

Add a reference to these agents so Copilot knows they exist:

```markdown
# Agent Roles

This project uses a multi-agent system. See agents/ for role definitions.
When handling complex tasks, follow the workflow defined in agents/README.md.
```

### Option C: Invoke by role name

In a Copilot or Claude conversation, reference an agent by role:

```
Act as the Planner agent (see agents/planner.md) and break down this task: ...
```

---

## Shared Resources

All agents follow the rules in `_shared/`:

| File                          | Purpose                                           |
| ----------------------------- | ------------------------------------------------- |
| `_shared/conventions.md`      | Tone, format, tool-use rules shared by all agents |
| `_shared/handoff-protocol.md` | How agents hand work off to each other            |

---

## Context & Memory

Agents use the `.context/` directory to persist knowledge across sessions:

| Path | Purpose | Shape |
| --- | --- | --- |
| `.context/overview.md` | High-level project description, goals, tech stack | file |
| `.context/architecture.md` | System structure, layers, integrations | file → folder |
| `.context/standards.md` | Code style, naming, error handling | file → folder |
| `.context/testing.md` | Test framework, conventions, mocking | file → folder |
| `.context/decisions/` | Architecture Decision Records (ADRs) | always a folder |
| `.context/retrospectives/` | Rolling learning log — agents append, humans promote | folder, max 10 entries |
| `.context/tasks/` | One folder per task, each with `plan.md` | folder |
| `.context/workflows/` | PR format, branching, CI | folder |

**The layout rules are canonical in `skills/_shared/conventions.md`.** Do not
restate them here — read them there.

"file → folder" means it starts as a single file and is promoted to a folder
by `context-maintenance` once it passes 300 lines. **A promoted entry is read
at `<base>/README.md`, not `<base>.md`.** So resolve both before concluding a
repo documents nothing:

```bash
[ -f ".context/standards.md" ] && cat .context/standards.md \
  || cat .context/standards/README.md 2>/dev/null \
  || echo "no standards documented"
```

An absent context file is not "no conventions to follow" — it is a gap to
report.

**Before starting work**, agents should read `.context/overview.md` if it exists.  
**After significant decisions**, agents should write to `.context/decisions/`.  
**After completing tasks**, agents should append to the current retrospective log.

---

## Adding New Agents

When a new specialized role is needed:

1. Copy the structure from an existing agent file
2. Fill in all sections: Purpose, Triggers, Inputs, Outputs, Responsibilities, Handoffs, Constraints, Anti-patterns, Example
3. Add the agent to the roster table in this README
4. Update the workflow diagram if the agent changes the flow
5. Add a shared conventions reference in the agent's preamble

---

## Versioning

These agent definitions are version-controlled alongside your code. When you make significant changes to an agent's behavior:

- Update the agent file
- Note the change reason in the file's changelog section (bottom of each agent file)
- Append a retrospective entry explaining what changed and why
