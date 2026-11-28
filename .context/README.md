# .context/

This directory is the persistent memory of the AI agent system. It stores project knowledge, architectural decisions, and learnings that agents read at the start of tasks and write to after completing significant work.

Unlike code, this directory captures the **why** behind decisions and the **what was learned** from doing the work.

---

## Structure

```
.context/
  README.md               ← This file: how the context system works
  overview.md     ← High-level project description (start here)
  decisions/
    README.md             ← ADR index and format guide
    ADR-001-*.md          ← Architecture Decision Records
  retrospectives/
    README.md             ← How the retro log works
    template.md           ← Template for new retro entries
    YYYY-MM-DD.md         ← Daily/weekly retro log entries
```

---

## State Management for Long Tasks

For tasks that span multiple sessions or long context windows, use structured state files alongside the `.context/` markdown:

| State type     | Format          | Location                   | Purpose                                              |
| -------------- | --------------- | -------------------------- | ---------------------------------------------------- |
| Task progress  | `progress.json` | `.context/`                | Machine-readable list of completed/pending steps     |
| Test tracking  | `tests.json`    | `.context/`                | Test results and coverage status per task            |
| Freeform notes | `YYYY-MM-DD.md` | `.context/retrospectives/` | General progress notes, blockers, decisions          |
| Code state     | git commits     | repo                       | What changed and when — always commit completed work |

**When context is about to clear:**

1. Write current progress to a state file
2. Commit completed work via git
3. Note the next step explicitly in the state file
4. A fresh context can read `git log --oneline`, the state file, and `overview.md` to resume exactly

**Starting from a fresh context:**

```
1. git log --oneline -10       # What was recently done
2. cat .context/overview.md  # Project facts
3. cat .context/progress.json  # Current task state (if exists)
4. cat .context/retrospectives/[latest].md  # Recent learnings
```

---

## How to Use This Directory

### Before Starting Work (pre-flight)

Read relevant context before beginning any non-trivial task:

- Always read `overview.md` for project-level context
- Read `decisions/` entries relevant to the area being worked in
- Skim recent `retrospectives/` entries for recent learnings
- Check `skills/GUIDE.md` to select the right skill for your task

### After Completing Work (write-back)

Write back to `.context/` when you:

- Make a significant architecture or design decision → `decisions/ADR-NNN-title.md`
- Complete a task with learnings worth preserving → `retrospectives/YYYY-MM-DD.md`
- Discover facts about the project that aren't documented → `overview.md`

### Selecting a Skill

Pick a skill from `skills/` based on what you're doing:

| Task type                               | Skill                   |
| --------------------------------------- | ----------------------- |
| Break a goal into ordered tasks         | `planning-tasks`        |
| Evaluate libraries, approaches, options | `researching-options`   |
| Make an architecture decision (ADR)     | `designing-systems`     |
| Write or modify code                    | `implementing-features` |
| Write or run tests                      | `writing-tests`         |
| Orchestrate 3+ skills                   | `coordinating-work`     |

See `skills/GUIDE.md` for the full selection guide and skill composition.

---

## The Learning Loop

```
Work is done
      │
      ▼
Append to retrospectives/YYYY-MM-DD.md
      │
      ▼
Human reviews retrospective entries periodically
      │
      ▼
Valuable learnings are promoted:
  - Skills → skills/ SKILL.md files
  - Decisions → decisions/ADR-NNN-*.md
  - Project facts → overview.md
      │
      ▼
Every future task starts more informed
```

This loop is how the system improves over time without requiring manual updates to every file.

---

## Rules

- **Never delete entries** from decisions/ or retrospectives/. Superseded ADRs are marked "Superseded" but kept.
- **Keep overview.md current.** It's the first thing read on every task.
- **Be specific in retro entries.** Vague entries ("things went well") have no learning value.
- **Humans promote, skills append.** Skills write raw learnings. Humans decide what gets elevated to permanent documentation.
