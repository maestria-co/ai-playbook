# ADR-004: Use `claude plugin eval` Instead of Building an Eval Harness

**Date:** 2026-11-15
**Status:** Accepted, pending a spike
**Decided by:** mje0002
**Supersedes:** Partially supersedes ADR-003's assumption that we build the local suite

## Context

ADR-002 put behavioral evals at the centre of Level 4. ADR-003 decided they
run locally, on demand, and implicitly assumed we would build the runner.

We would not. `claude plugin eval` ships with the Claude Code CLI and does
the job already:

| Need | Flag |
|---|---|
| Pass/fail exit code | `--threshold <0..1>` — exits 1 if any case scores below it |
| Hard cost ceiling | `--max-cost-usd <usd>` — aborts at the cap, exit 2 |
| Machine-readable results | `--json [path]` |
| Cheap grading | `--judge-model` defaults to haiku |
| Repeat runs for flake | `--runs <n>`, default 3 |
| Does the skill even fire? | `--ablation with-without` scores with and without the plugin and reports the delta |
| Keep results private | `--no-publish` |

Cases live in `evals/**/case.yaml`, or `prompt.md` plus `graders/*.md`.

## Decision

Adopt `claude plugin eval` as the behavioral-eval runner. Do not build one.

Write cases under `evals/`. Run with `--threshold` and `--max-cost-usd` set,
and `--no-publish` by default.

## Rationale

**Off The Shelf.** Agent definitions are our product; a test runner for them
is not. This is a supporting need, and a managed one already exists in a
tool we run anyway.

**Free and Frugal.** `--max-cost-usd` turns ADR-003's weakest point into a
flag. We no longer have to trust ourselves to watch the spend — the runner
aborts at the ceiling and reports partial results.

**It answers the question we actually have.** `--ablation with-without`
scores the same cases with and without the plugin loaded and reports the
delta. That measures whether a skill changes behavior at all, which is the
real question about a 42-skill library nobody has ever measured. A
hand-built runner would not have given us that for free.

**K.I.S.S.** Zero new infrastructure. One command and a directory of cases.

## The spike this depends on

Status is "pending a spike" for one reason: **this repo is not a Claude Code
plugin.** It has no `plugin.json` and no `.claude-plugin/` directory — it is
a `.copilot`-compatible skills directory. The help text says a target may be
"a path, a plugin name, or a `plugin@marketplace` id" and that "installed
and skills-dir plugins both resolve," which suggests `skills/` is enough,
but we have not proven it.

Spike, time-boxed to one sitting:
1. Write one trivial eval case against one skill.
2. Run `claude plugin eval` against this repo's path with `--max-cost-usd 1`
   and `--no-publish`.
3. If it does not resolve, determine the smallest manifest that makes it
   resolve, and whether adding one breaks the `.copilot` compatibility this
   repo advertises in `CLAUDE.md`.

If the spike fails and a manifest would break Copilot compatibility, this
ADR is void and we reopen the build-vs-buy question. Record the outcome here
before any Phase 4 case-writing starts.

## Alternatives Considered

| Option | Why rejected |
|---|---|
| Build a bespoke runner | Violates Off The Shelf for a supporting need. Also means building cost capping, grading, and ablation ourselves — all of which already exist. |
| `/skill-doctor` only | Useful as a health report, but it is not a scored pass/fail gate and does not take a threshold. Complementary, not a substitute. |
| A third-party eval framework | More setup and another dependency, for a runner we already have installed. |

## Consequences

**Positive:**
- No eval infrastructure to build, run, or explain.
- Cost capping is a flag, not a discipline.
- Ablation gives us a measurement we did not know we could get: whether each
  of the 42 skills actually changes behavior.

**Negative / tradeoffs:**
- We depend on a CLI feature we do not control. If its interface changes,
  our gate changes with it.
- Cases are tied to Claude Code's eval format, so they are not portable to
  Copilot CLI — which this repo otherwise tries to stay compatible with.
  This is a real tension with the repo's stated cross-tool goal and is worth
  naming before writing many cases.
- Still model-calling, so still ADR-003's local on-demand tier. It does not
  become free, it becomes capped.

## Related

- `.context/decisions/ADR-002-level-4-ai-engineering.md` — why evals matter
- `.context/decisions/ADR-003-eval-cost.md` — the tier this runner sits in
- `.context/tasks/mje0008/plan.md` — Phase 4
