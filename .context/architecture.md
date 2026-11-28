# Architecture

This repository ships **definitions, not a running system**. Its artifacts are
Markdown files that other tools load as agent and skill definitions. There is
no server, no database, and no build output — which is why the only executable
code here is the validator and the installer.

---

## Layout

| Directory | Holds | Loaded by |
| --- | --- | --- |
| `agents/` | 11 `*.agent.md` role definitions | Copilot CLI / Claude Code at session start |
| `agents/_shared/` | Conventions and handoff protocol every agent follows | Referenced from each agent file |
| `skills/` | 43 skills, one folder each with a `SKILL.md` | On demand, by name |
| `skills/_shared/` | Cross-skill conventions and `context_template/` | Referenced from skills; template copied by `initialize-repo` |
| `recipes/` | End-to-end worked examples | Humans |
| `scripts/` | `validate.py`, hook scripts, task-state library | CI, git hooks |
| `.githooks/` | `commit-msg`, `pre-push` | git, once pointed at by `core.hooksPath` |
| `.context/` | This repo's own project context | Agents working in this repo |

---

## The two installation targets

`install.sh` copies this repo into one of two homes, translating agent
frontmatter for the target tool:

```
agent-defs/  ──┬── ./install.sh           ──►  ~/.copilot/   (GitHub Copilot)
               └── ./install.sh --claude  ──►  ~/.claude/    (Claude Code)
```

Installed files are **generated output**. Editing them is lost on the next
install — change the source here and reinstall.

Skills resolve from the installed location, which is why `find-context-template`
checks `~/.copilot/` then `~/.claude/` rather than assuming a repo path.

---

## How a task flows

```
Manager ──► reads .context/ ──► selects specialists ──► delegates
   │                                                      │
   │                        ┌─────────────────────────────┤
   │                        ▼                             ▼
   │                   Planner / Architect           Coder / Tester
   │                        │                             │
   └──◄── plan.md ◄─────────┴──────── Reviewer ◄──────────┘
             (.context/tasks/<ID>/plan.md — the handoff document)
```

`plan.md` is the durable boundary. It survives a context reset, so any agent
can resume cold. The format is defined by the `task-plan` skill.

---

## Verification boundary

Two oracles with different lifetimes, per
`.context/decisions/ADR-002-level-4-ai-engineering.md`:

| Oracle | Lifetime | Proves |
| --- | --- | --- |
| `scripts/validate.py` | standing | Nothing broke structurally |
| Per-task checks | one task | The right thing was built |

`validate.py` runs in CI and from `pre-push`. Per-task checks live beside their
task in `.context/tasks/<ID>/checks/`. See `.context/testing.md`.

---

## Consequences worth knowing

**Two hook systems exist by necessity.** Copilot CLI hooks live in
`.github/hooks/hooks.json` with `sessionStart` / `sessionEnd` / `postToolUse`
events; git hooks live in `.githooks/`. They are unrelated mechanisms. There
are deliberately **no** Claude Code hooks in `settings.json` — enforcement
belongs in CI, and a third hook system doing adjacent work in a third file
would astonish a newcomer.

**The index docs are hand-maintained.** `CLAUDE.md` and `skills/GUIDE.md` list
every skill and agent. Nothing generates them, so they rot — which is why
`validate.py` asserts every path they cite resolves on disk.

**The `commit-msg` hook is duplicated on purpose.** One copy for this repo in
`.githooks/`, one inside `context_template/` for consumer repos. `validate.py`
asserts the two are byte-identical.
