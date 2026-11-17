# ADR-002: Target Level 4 AI Engineering

**Date:** 2026-11-14
**Status:** Accepted
**Decided by:** mje0008
**Supersedes:** —

## Context

We need a shared definition of how far AI does the work here, so that
"improve the harness" stops being a matter of taste. We adopt this maturity
ladder:

| Level | Name | Who produces code | Who decides "done" |
|---|---|---|---|
| 0 | Spicy Autocomplete | Human writes all code; AI speeds up typing | Human |
| 1 | Coding Intern | Human hands off isolated tasks (a function, a unit test), then stitches | Human |
| 2 | Junior Developer / Pairing | AI works continuously across files; human is still primary producer, reads every line | Human |
| 3 | Developer as Manager | Human stops writing code, directs multiple agents, reviews PRs | Human |
| 4 | Developer as Product Manager | Human writes specs, edge cases, acceptance criteria; agents build, test, and iterate until specs pass | **Automated check** |
| 5 | The Dark Factory | Zero human code, zero human review; requirements and external behavioral tests feed an autonomous pipeline | Automated check |

Most teams stall at Level 2. This repo is at Level 2 with Level 3 ambitions:
it has a Manager orchestrator, specialist agents, and delegation protocols —
the *shape* of Level 3 — but the human is still the only thing that can tell
whether any of it worked.

## Decision

Target **Level 4** for this repo, and treat the gating constraint as the
**acceptance oracle**, not the quality of the prompts.

The ladder's levels 0–3 all end with a human deciding "done." Level 4 is the
first level where that judgment is delegated, because its defining clause —
agents "iterate in the background until the specs pass" — requires something
that can execute the specs and return pass/fail without a human present.

Therefore: **no agent, skill, or workflow change moves us toward Level 4
unless it adds or strengthens an automated pass/fail signal.** Better prompts
are Level 2 and 3 work. We will keep doing it, but we will not count it as
progress on this axis.

## Scope: two goals, and which one is the point

This repo is a kit. `install.sh` copies it to `~/.claude`, and
`initialize-repo` sets up `.context/` in other projects. Its value is what
it does to **other** repos. So "make the harness Level 4" splits in two, and
the split is easy to lose:

| | Goal | What it means |
|---|---|---|
| **A** | This repo develops *itself* at Level 4 | Agents build the harness's own Markdown against executable checks |
| **B** | This repo *enables* Level 4 in a consumer repo | A team installs the kit and can then spec a feature, have agents build it, and have them iterate until checks pass |

**B is the point. A is dogfooding.** A is worth doing — a kit that cannot
hold itself to its own standard is not credible, and it is where we learn
what the practice costs. But A is not a route to B, and progress on A must
not be reported as progress on B.

### Which work serves which

| Phase | Serves A | Serves B |
|---|---|---|
| 1 — `validate.py`, CI, index-drift, pre-push | Yes | **No** |
| 2 — per-task acceptance checks in `task-plan` | Yes | **Yes — this is what ships** |
| 2b — consumer repo readiness | No | **Yes** |
| 4 — evaluate the 42 skills | Yes | Yes |
| 5 — lessons loop | Yes | Partly |

The asymmetry to hold on to: **`validate.py` does not transfer.** It checks
agent and skill Markdown, and a consumer application repo has none. What
transfers is everything under `skills/`, because that is what gets
installed.

### Tests are necessary and not sufficient

An earlier draft of this ADR said the consumer's oracle is its own test
suite. That is wrong, and the error matters.

A green test suite proves that **the behaviors someone wrote tests for**
work. It says nothing about whether the spec was fulfilled. Three ways a
suite goes green on an unmet spec:

1. **Nothing tested AC 3.** The suite is green, the criterion was never
   implemented, and no one notices.
2. **Nothing maps AC 3 to a test.** Even at full coverage, no artifact says
   which check proves which criterion, so "all seven criteria are met" is
   not a statement anything can evaluate.
3. **The agent wrote passing tests for the wrong thing.** Tests the agent
   authored and graded are the self-assessment problem wearing a green tick.

So Level 4 needs three layers, not one:

| Layer | Answers | Who provides it |
|---|---|---|
| Tests | "Does this behavior work?" | The consumer repo |
| AC → check mapping | "Which check proves which criterion?" | The spec, written by the planner |
| **Spec completeness evaluator** | "Is every criterion accounted for, and did every machine-checked one pass?" | The kit |

The third layer is the thing that actually decides done. Tests are an input
to it, not a substitute for it. And it is the layer that does not exist
anywhere today — not here, and not in a consumer repo.

Note what the evaluator must refuse to do: report green when a criterion has
no check. A criterion with no check is an **unknown**, and an unknown is not
a pass. It must also report the human-judged criteria separately rather than
quietly omitting them, or it produces a false green — "5 of 7 verified, 2
await review" is the honest output, and "all tests passed" is not.

### A repo with no runnable test command still cannot do Level 4

That remains true. There is nothing for the mapping to point at, so the loop
cannot close no matter how good the spec is.

`context_template/context/testing.md` has a `Run tests:` placeholder, so the
foundation half-exists. But nothing requires it to be filled in, and no
agent treats it as a gate — `initialize-repo` will finish happily on a repo
with no working test command, leaving a consumer that is structurally
incapable of the thing the kit promises. Phase 2b closes that.

## What "the specs pass" means here

This repo ships Markdown — agents, skills, prompts — not a running
application. The Level 4 clause "iterate until the specs pass" has to be
defined concretely or the target is vacuous.

### Two oracles, by lifetime

The spec is the definition of done. A standing validator is not, and the two
must not be confused.

| | Standing invariants | Per-task acceptance checks |
|---|---|---|
| Question answered | "Did I break the repo?" | "Did I build the thing asked for?" |
| Scope | Every branch, every task | This task only |
| Changes per task | Never | Always |
| Lifetime | Permanent | Dies with the task |
| Today | `scripts/validate.py` | `plan.md` prose checkboxes |

`validate.py` is a regression guard. It can prove an agent damaged nothing.
It can never prove the agent did what was asked: a branch that implements
the wrong feature flawlessly passes it green. Only the per-task checks,
derived from the spec, close that gap.

### Why the per-task half does not work today

`skills/task-plan/SKILL.md` defines acceptance criteria as checkboxes that
are "independently verifiable" and "updated to `[x]` only when verified with
evidence." Both are prose aspirations. In practice the agent that did the
work also decides the box is ticked — worker and judge are the same party.

This is the exact failure `skills/common-constraints/` exists to prevent,
and it attempts the prevention with more prose. A rule instructing an agent
not to rationalize is itself available to be rationalized past. A
self-assessment problem is not fixable with better instructions to the self.
It is fixable only by moving the judgment outside the agent.

### Criteria need a tier label

Not every criterion can execute. Taking the criteria from
`.context/tasks/mje0008/plan.md` as a worked example:

| Criterion | Mechanizable |
|---|---|
| Ladder recorded with the repo's current position | Yes — file exists, table has six levels, states a position |
| Core value conflicts surfaced, not buried | Yes — contains `Core value conflict:`, and not only in the final section |
| Phases sized to one PR each | Weak — file-count proxy at best |
| Level 4 given a non-vacuous meaning | No — judgment |

So each criterion is labelled machine-checked or human-judged. The agent
iterates unattended against the machine-checked ones. The human reviews only
the judged ones.

This is the real payoff, and it is worth stating plainly: Level 4 is not
"no human review" — that is Level 5. It is that the review queue shrinks to
the few items that need a brain, because everything mechanical was proven
before it arrived.

### Behavioral evals are a third thing

Structural checks catch "the artifact is malformed." Per-task checks catch
"the task was not done." Neither catches "the artifact is well-formed and
wrong" — an agent that routes to the wrong specialist, or skips a handoff.
That needs behavioral evals: given a prompt, does the agent route, refuse,
or produce the expected shape? These are standing like `validate.py`, but
assert on agent behavior rather than on files. They do not exist yet.

### How the halves connect

Because this repo ships files, most per-task criteria are assertions about
files — the same shape `validate.py` already evaluates. Same runner,
different lifetime. That gives a pipeline: a per-task check that proves
generally true graduates into `validate.py` as a permanent invariant.

That is `skills/knowledge-graduation/` applied to checks instead of docs.
The harness already has the concept; it is pointed at the wrong artifact.

## Rationale

The evidence that the oracle is the binding constraint, not prompt quality:
on 2026-11-14, `python3 scripts/validate.py` on `main` exited 1 with a real
error (`context-specialist.agent.md` missing its `## Constraints` section)
and 11 warnings. The validator existed, was correct, and was never run,
because nothing runs it. The repo had a working oracle and still could not
tell it was broken.

Note also that the 11 warnings are the validator being stale — it pins
`claude-sonnet-4.6` while the fleet has moved to `claude-sonnet-5` and
`claude-opus-5`. An oracle nobody runs rots into noise, which is why
"run it automatically" and "write more checks" are the same project.

This also resolves a standing conflict with the **Cruise Control** core
value, which ranks second and requires automation end to end with people
monitoring and correcting it. A validator invoked only by hand is a manual
step kept manual for simplicity — exactly the trade True North forbids:
K.I.S.S. ranks last and does not justify dropping automation.

## Alternatives Considered

| Option | Why rejected |
|---|---|
| Target Level 3 instead | We already have Level 3's structure. Its ceiling is human PR review throughput, which is the bottleneck we are trying to remove. |
| Target Level 5 | Requires trusting an unmonitored pipeline to ship. Violates Cruise Control's "people monitor and correct the automation," and we have no oracle at all yet. |
| Improve agent prompts and measure by feel | This is what we have been doing. It produced a repo whose own validator fails on `main` undetected. |
| Buy an off-the-shelf agent-eval product | Revisit when free tiers are evaluated. Agent definitions are our product, so their tests are product tests, not a supporting need — Off The Shelf does not force a purchase here. |

## Consequences

**Positive:**
- "Does this move us to Level 4?" becomes an answerable question with a
  mechanical test: does it add a pass/fail signal that runs without a human?
- Specs and acceptance criteria get a consumer, so writing them stops being
  ceremony.
- Satisfies Cruise Control, which the current manual-validator state violates.

**Negative / tradeoffs:**
- Adds moving parts — CI workflow, eval harness, fixtures — against K.I.S.S.
  Accepted deliberately: K.I.S.S. ranks last, and Cruise Control ranks second.
- Behavioral evals of a non-deterministic agent are themselves flaky. They
  need to assert on routing and shape, not on exact wording.
- Running evals calls a model, which costs money. **Free and Frugal conflict —
  see below.** No eval work proceeds until the cost question is answered.

## Open question: eval cost — RESOLVED

**Closed 2026-11-14 by ADR-003**, which splits checks into a free model-free
tier in CI and a local on-demand tier for anything needing a model. The
conflict below is recorded as it stood.

⚠️ **Core value conflict: Free and Frugal** — behavioral evals invoke a model
per case, which is not free at any meaningful volume, and GitHub Actions
minutes are free only on public repos. Structural and per-task checks (phases 1 and 2) are free
and unaffected. Before any behavioral-eval work starts we must decide: run
them on a hard-capped budget, run them only on changed agents, run them
locally on demand rather than per push, or substitute assertions that need no
model call. This ADR does not decide it.

## Related

- `scripts/validate.py` — the existing structural oracle
- `.context/tasks/mje0008/plan.md` — gap assessment and sequencing
- `.context/decisions/ADR-003-eval-cost.md` — closes the eval-cost question
- `TRUE_NORTH.md` — Cruise Control, K.I.S.S., Free and Frugal, and their order
