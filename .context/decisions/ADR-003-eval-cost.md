# ADR-003: How Agent Evals Get Paid For

**Date:** 2026-11-14
**Status:** Accepted
**Decided by:** mje0002
**Supersedes:** —

## Context

ADR-002 targets Level 4 and left one question open: behavioral evals invoke
a model per case, which is not free at volume. That conflict with the **Free
and Frugal** core value gated all Phase 4 work.

## Decision

Two tiers, split by whether a check needs a model.

| Tier | Needs a model | Where it runs | When |
|---|---|---|---|
| Model-free assertions | No | CI, via `validate.py` | Every push and PR |
| Behavioral evals | Yes | Locally, on demand | When a person chooses |

Model-free assertions are the default. Write a check without a model call
wherever one is possible. Behavioral evals are reserved for what genuinely
cannot be asserted statically, and they never run in CI.

## Rationale

This costs nothing on either axis. CI stays free because nothing there calls
a model, and the repo is public so Actions minutes are unlimited. The evals
that do call a model run on an existing subscription, at a volume a person
controls, with no per-push multiplier.

It also puts the gate in the right place. A push happens dozens of times a
day; an eval run is a deliberate act before a merge or a release.

## The limitation this accepts

Stated plainly, because it is easy to lose: **a model-free assertion cannot
verify behavior.** It can only verify what an agent *declares*.

A static check can prove that `manager.agent.md` names `@coder` in its
routing table and that `agents/coder.agent.md` exists. It cannot prove that
the Manager actually routes a coding task to `@coder` when asked. Only a
model call shows that.

So the two tiers are not interchangeable, and the cheap tier is not a
substitute for the expensive one. The split is about *when* the expensive
tier runs, not about avoiding it. If the local suite is never run, Phase 4
is not done regardless of how many static assertions pass.

Guard against that: the local eval suite needs a single documented command
and a recorded last-run date, so "we have not run it in two months" is
visible rather than assumed.

## Alternatives Considered

| Option | Why rejected |
|---|---|
| Hard budget cap in CI | Still spends money, and a cap that trips turns a red build into a billing question. |
| Evals only on changed agents | Cheaper than all-on-push but still per-push spend, and an agent's behavior depends on agents it delegates to, so "changed" is not a clean boundary. |
| Model-free assertions only | Free, but cannot verify behavior at all. Would let us declare Level 4 while testing nothing an agent actually does. |

## Consequences

**Positive:**
- No new spend. Satisfies Free and Frugal with no stated conflict.
- CI stays fast, because no CI step waits on a model.
- Forces the useful discipline of asking "can this be checked statically?"
  before reaching for a model call.

**Negative / tradeoffs:**
- Behavioral regressions are caught late — at a human-triggered run rather
  than on the push that caused them.
- An on-demand suite rots if nobody demands it. This is the same failure as
  the unrun `validate.py` that motivated ADR-002, one level up. The recorded
  last-run date is the mitigation, and it is a weak one.
- **Cruise Control gave way here.** Cruise Control ranks second and wants
  automation end to end; a human-triggered suite is a manual step. It is
  accepted because the alternative spends money on every push, and because
  a person monitoring the automation is the role Cruise Control assigns to
  people. Revisit if a free hosted option appears.

## Related

- `.context/decisions/ADR-002-level-4-ai-engineering.md` — the open question this closes
- `.context/tasks/mje0008/plan.md` — Phase 4
- `TRUE_NORTH.md` — Free and Frugal, Cruise Control, and their order
