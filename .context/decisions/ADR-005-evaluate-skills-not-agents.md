# ADR-005: Evaluate Skills First, by Ablation

**Date:** 2026-11-16
**Status:** Accepted
**Decided by:** mje0002
**Supersedes:** —

## Context

ADR-002 made behavioral evals central to Level 4. ADR-004 picked
`claude plugin eval` as the runner and the spike found it gated behind early
access. That left an unanswered question: **what are we evaluating — agents
or skills?**

## Decision

**Evaluate skills first.** Use `superpowers:writing-skills` as the method.
Run it by hand, using ablation, starting now.

## Rationale

### The repo answers it by what is missing

| Target | Count | Evaluation skills available |
|---|---|---|
| Agents | 11 | **Two** — `agent-evaluation` (system design, role overlap, routing) and `agentic-evaluation` (one `.agent.md` scored against best practice) |
| Skills | 42 | **None** |

Four times the surface area with no coverage at all. Skills are also where
the procedures live; an agent is largely a router plus constraints, and
ADR-001 already reasons about the highest-leverage one.

Nobody has ever measured whether any of the 42 skills changes behavior.

### The method is already installed

`superpowers:writing-skills` v7.0.0 is 681 lines of evaluation discipline,
not an authoring guide:

- The Iron Law, same as TDD
- RED-GREEN-REFACTOR for skills
- Testing all skill types
- Common rationalizations for skipping testing, including
  *"Academic review is enough" → Reading ≠ using. Test application scenarios.*
- Skill Discovery Optimization — whether the skill is even found
- A TDD-adapted checklist, one todo per item

### Its method is ablation done by hand

The checklist prescribes:

> RED: run scenarios **without** the skill, document baseline behavior verbatim
> GREEN: run scenarios **with** the skill, verify agents now comply

That is exactly what `claude plugin eval --ablation with-without` automates.

**This materially reduces the damage from ADR-004's block.** The gated tool
automates a method we can execute today. What we lose by not having it is
scoring, the `--max-cost-usd` ceiling, and repeatability — not the ability
to find out whether a skill works.

### It also supplies the evidence for ADR-002's central claim

ADR-002 argues a well-formed artifact can still be wrong, and that only
behavioral testing catches it. `superpowers:writing-skills` documents a real
instance: a description that summarized the workflow caused an agent to run
*one* review where the skill's own flowchart specified two. Changing only
the description wording fixed it.

A structural check would pass that skill. The ablation caught it.

## Consequences

**Positive:**
- Phase 4 has a free manual path instead of being blocked outright.
- No new tooling, no spend, nothing to build. Off The Shelf and Free and
  Frugal both satisfied by a skill already on the machine.
- Gives a first measurement target that is genuinely unknown: how many of
  the 42 skills change behavior at all. A skill that never fires is pure
  token cost.

**Negative / tradeoffs:**
- Manual ablation is slow and not repeatable on every push. It is a
  deliberate exercise, which is consistent with ADR-003's tier 2 but makes
  regression detection weak.
- Results are human-recorded, so they rot like any undated document. Each
  run needs its baseline captured verbatim, as the method requires.
- Evaluating agents is deferred, not cancelled. The two agent-eval skills
  stay as human-judgment rubrics.

## Related

- `.context/decisions/ADR-002-level-4-ai-engineering.md` — why behavior must be measured
- `.context/decisions/ADR-003-eval-cost.md` — the tier manual ablation sits in
- `.context/decisions/ADR-004-eval-harness.md` — the blocked runner this routes around
- `.context/decisions/ADR-006-rename-agent-eval-skills.md` — the naming fix this surfaced
