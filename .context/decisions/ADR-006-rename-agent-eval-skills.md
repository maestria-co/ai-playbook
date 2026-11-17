# ADR-006: Rename the Two Agent-Evaluation Skills

**Date:** 2026-11-16
**Status:** Accepted
**Decided by:** mje0002
**Supersedes:** —

## Context

Two skills in this repo have near-identical names and different jobs:

| Directory | H1 | What it actually does |
|---|---|---|
| `agent-evaluation` | "Agent System Evaluation" | Audits the agent *system* — role overlap, responsibility leakage, orchestrator routing clarity |
| `agentic-evaluation` | "Agent Evaluation" | Scores one `.agent.md` *file* against best practice and proposes rewrites |

Neither the directory names nor the headings disambiguate them. "Agent
Evaluation" is the heading of the file-level skill, while the system-level
skill is the one named `agent-evaluation`. A newcomer asked to review an
agent file cannot guess which to open, and has a better than even chance of
opening the wrong one.

## Decision

Rename:

- `agent-evaluation` → **`agent-system-audit`**
- `agentic-evaluation` → **`agent-file-review`**

Update the H1 of each to match its directory.

## Rationale

This is a direct Least Astonishment violation, and `TRUE_NORTH.md` uses
naming as that principle's worked example: "Structure, layout, and names
must make the right place obvious and the wrong place unlikely. If a
reasonable person would be surprised by where something lives, what it is
called, or what it does, change the design — not the explanation."

The distinction that matters to a reader is **system versus single file**,
so the names should carry it. "Agentic" versus "agent" carries nothing: it
reads as a stylistic variant, not a scope boundary.

TRUE_NORTH also says: "When you touch code that already surprises its
reader this way, rename it as part of the change and say so in the PR."
ADR-005 touched this area, so the rename happens now rather than being
logged as debt.

## Alternatives Considered

| Option | Why rejected |
|---|---|
| Leave them and document the difference | Explaining a confusing name is the thing the principle explicitly forbids. |
| Merge into one skill | They have genuinely different inputs (a system vs a file) and outputs. Merging would produce one skill with two modes, which is worse. |
| Rename only `agentic-evaluation` | Fixes half of it. `agent-evaluation` would still read as the generic one while being the narrower system-level audit. |

## Consequences

**Positive:**
- The right skill is guessable from its name.
- `scripts/validate.py` enforces that references resolve, so a missed
  reference fails CI rather than rotting.

**Negative / tradeoffs:**
- Breaks any external reference to the old names, including the user's
  global `~/.claude/CLAUDE.md` skill table.
- **`install.sh` copies additively and never deletes.** Re-running it after
  this rename installs the new directories but leaves
  `~/.claude/skills/agent-evaluation/` and
  `~/.claude/skills/agentic-evaluation/` behind as orphans, and both old and
  new will be listed. The old directories must be removed by hand once, or
  `install.sh` needs a prune step. This is a real gap in the installer,
  recorded here because the rename is what exposes it.

## Related

- `TRUE_NORTH.md` — Least Astonishment and its naming guidance
- `.context/decisions/ADR-005-evaluate-skills-not-agents.md` — surfaced this
- `install.sh` — the additive-copy gap this exposes
