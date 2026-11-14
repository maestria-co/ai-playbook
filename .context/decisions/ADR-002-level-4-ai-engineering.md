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

## What Level 4 means for a definitions repo

This repo ships Markdown — agents, skills, prompts — not a running
application. "Tests pass" has to be defined concretely or the target is
vacuous. Two kinds of oracle apply:

1. **Structural checks** — invariants over the artifacts themselves:
   frontmatter is valid and complete, skill references resolve to real
   directories, declared models exist, index tables in `CLAUDE.md` and
   `skills/GUIDE.md` match what is on disk, no stale agent names. This is
   what `scripts/validate.py` already does.
2. **Behavioral evals** — given a prompt, does the agent route, refuse,
   or produce the shape we expect? This is the part that does not exist yet
   and is the real work of reaching Level 4.

Structural checks catch "the artifact is malformed." Only behavioral evals
catch "the artifact is well-formed and wrong." Level 4 needs both.

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

## Open question: eval cost

⚠️ **Core value conflict: Free and Frugal** — behavioral evals invoke a model
per case, which is not free at any meaningful volume, and GitHub Actions
minutes are free only on public repos. Structural checks (phase 1) are free
and unaffected. Before any behavioral-eval work starts we must decide: run
them on a hard-capped budget, run them only on changed agents, run them
locally on demand rather than per push, or substitute assertions that need no
model call. This ADR does not decide it.

## Related

- `scripts/validate.py` — the existing structural oracle
- `.context/tasks/mje0008/plan.md` — gap assessment and sequencing
- `TRUE_NORTH.md` — Cruise Control, K.I.S.S., Free and Frugal, and their order
