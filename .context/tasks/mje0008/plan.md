# Implementation Plan: Move the Harness Toward Level 4

## Task

Define what Level 4 AI engineering means for this repo, assess the gap, and
sequence the changes that close it. Definition and assessment only — each
change below becomes its own branch and PR.

Definition lives in `.context/decisions/ADR-002-level-4-ai-engineering.md`.
That ADR's test governs this plan: a change counts as Level 4 progress only
if it adds or strengthens a pass/fail signal that runs without a human.

## Where we are: Level 2, wearing Level 3's clothes

| Level 4 requirement | Status | Evidence |
|---|---|---|
| Specs with acceptance criteria | **Partial** | `skills/task-plan/` produces criteria, but prose only, and the agent that did the work ticks its own boxes |
| Agents can build unattended | **Yes** | Manager + 10 specialists, delegation and handoff protocols exist |
| Automated pass/fail signal | **No** | `scripts/validate.py` exists but runs only by hand |
| Signal runs without a human | **No** | No `.github/workflows/` at all |
| Agents iterate until green | **No** | Nothing to iterate against |
| Behavioral evals of agents | **No** | `agent-evaluation` and `agentic-evaluation` are human-judgment rubrics, not executable |
| Lessons captured durably | **Partial** | `.context/retrospectives/` + `task-retrospective` + `knowledge-graduation` exist; graduation is manual and unprompted |

### The headline finding

On 2026-11-14, `python3 scripts/validate.py` on `main` exited **1**:

```
❌ 1 error:   [context-specialist.agent.md] Missing required section: ## Constraints
⚠️  11 warnings: model pinned to claude-sonnet-4.6, fleet is on sonnet-5 / opus-5
```

A correct validator, in the repo, failing on the default branch, unnoticed.
This is not a prompt-quality problem and no amount of better agent writing
fixes it. It is the absence of anything that runs.

The 11 warnings are the second half of the same lesson: the validator still
pins `claude-sonnet-4.6` while the fleet moved on. Unrun checks rot into
noise, then get ignored on purpose, then get deleted.

## Sequencing

Ordered by dependency. Each phase is a separate branch and PR.

**Revised 2026-11-14.** The old order put behavioral evals before per-task
acceptance checks. That was wrong twice over: the acceptance checks are the
clause that actually defines Level 4, and they are free, while the evals
cost money and are gated on an unmade decision. Old Phase 4 is now Phase 2.

### Phase 1 — Make the standing oracle real (free) — DONE
Branch `fix/validate-ci`, pushed 2026-11-14.
1. ✅ Fixed `context-specialist.agent.md`, which used `## Governing
   Constraints` where the other ten agents use `## Constraints`.
2. ✅ Replaced the hardcoded `claude-sonnet-4.6` pin with an
   `ALLOWED_MODELS` allowlist, raised from warning to error.
3. ✅ Added `.github/workflows/validate.yml` running `validate.py --strict`
   on push and PR. First automated pass/fail signal in the repo.
4. ✅ Added an index-drift check: every repo-rooted path cited in
   `CLAUDE.md` and `skills/GUIDE.md` must resolve. It immediately caught
   real rot — all three indexes cited `evaluate-skill`, a skill with no
   directory. Rows repointed to `writing-skills`.

Confirmed free: the repo is public, so Actions minutes are unlimited.

### Phase 2 — Per-task acceptance checks (free, no model calls)
The spec is the definition of done. `validate.py` is not and never will be:
it proves nothing broke, not that the right thing was built. See ADR-002,
"Two oracles, by lifetime."

1. Extend the `task-plan` acceptance-criteria format so each criterion
   carries a tier label — machine-checked or human-judged. Criteria that
   claim to be machine-checked must name the command that checks them.
2. Give a task a place to put its own checks, so a per-task check runs the
   same way the standing ones do. Keep the runner shared with
   `validate.py`; do not build a second test framework.
3. Change the completion path so an agent cannot tick a machine-checked box
   by self-assessment. The box is ticked by the exit code or not at all.
   This is the point of the phase — today `task-plan` says to tick when
   "verified with evidence," and the agent both produces and grades the
   evidence.
4. Add the graduation path: a per-task check that proves generally true
   moves into `validate.py` as a standing invariant.

**Decided 2026-11-14: the planner writes a task's checks, not the coder.**
A coder that writes its own passing condition reproduces the
self-assessment problem one level up. This raises the bar on `@planner` and
on `skills/task-plan/` — writing a spec precise enough to be mechanically
checked is the real work that Level 4 names when it calls the human a
product manager.

Step 3 is the one that changes agent behavior. Steps 1 and 2 only make it
possible.

### Phase 3 — Decide the eval-cost question — DONE
Resolved in `.context/decisions/ADR-003-eval-cost.md`. Two tiers:
model-free assertions run in CI on every push; behavioral evals that need a
model run locally, on demand. No new spend, and Phase 4 is unblocked.

Carry forward the limitation ADR-003 records: a model-free assertion
verifies what an agent *declares*, never what it *does*. The cheap tier
does not substitute for the expensive one.

### Phase 4 — Behavioral evals
Structural checks catch a malformed artifact. Per-task checks catch an
undone task. Neither catches an artifact that is well-formed and wrong — an
agent that routes to the wrong specialist or skips a handoff.

Executable cases asserting an agent routes, refuses, or delegates as
intended. Assert on shape and routing, never exact wording.

**Order decided 2026-11-14:** `manager`, then `coder`, then `reviewer`.
Manager first because its misrouting cascades to every specialist (see
ADR-001). Then `coder` as the most-invoked agent, then `reviewer` as the
last check before a merge.

Split each agent's cases by tier per ADR-003: whatever can be asserted
without a model goes into `validate.py` and runs in CI; the rest goes in the
local on-demand suite. That suite needs one documented command and a
recorded last-run date, or it rots exactly as `validate.py` did.

### Phase 5 — Close the lessons loop
`task-retrospective` and `knowledge-graduation` both exist and both wait for
a human who remembers to invoke them. Trigger graduation on a schedule or a
task-count threshold, and have it open a PR rather than ask.

Note the dependency: Phase 2 step 4 makes checks graduate. This phase makes
documented lessons graduate. Same mechanism, two artifact types — build the
second on the first rather than separately.

## Guardrails: what is already here

Worth stating so Phase 4 does not rebuild it. `skills/common-constraints/`,
`verification-checklist`, and the per-agent Anti-Rationalization and Scope
Guard tables are a real guardrail layer. The gap is not that guardrails are
missing — it is that **nothing verifies the guardrails are working.** Every
one of them is an instruction the agent may or may not follow, with no
measurement. That is precisely what Phase 4 tests.

## Acceptance criteria for this task

- [x] Maturity ladder recorded with the repo's current position
- [x] Level 4 given a concrete, non-vacuous meaning for a definitions repo
- [x] Gating constraint identified and evidenced
- [x] Phases sequenced by dependency, each sized to one PR
- [x] Core value conflicts surfaced, not buried (Free and Frugal, K.I.S.S.)
- [x] Phase 1 scope confirmed with mje0002 and implemented on `fix/validate-ci`
- [ ] Phase 1 step 4 (index-drift check) decided: do now or defer

## Open questions

All six questions from the first pass are answered. Recorded 2026-11-14.

1. ~~Public or private?~~ **Public.** Actions minutes unlimited and free.
2. ~~Does `validate.py` own the model allowlist?~~ **It owns it**, as a named
   `ALLOWED_MODELS` constant at the top of the file. Still a hardcoded list,
   so it can still rot — but it now rots visibly, as a CI error rather than
   a warning nobody reads.
3. ~~Index-drift check now or later?~~ **Now.** Done, Phase 1 step 4.
4. ~~Who writes a task's per-task checks?~~ **The planner.** See Phase 2.
5. ~~How do evals get paid for?~~ **Two tiers.** See ADR-003.
6. ~~Which agent after the Manager?~~ **`coder`, then `reviewer`.** See Phase 4.

### New, from the Phase 1 work

7. **Does "evaluate a SKILL.md file" need its own skill?** All three index
   docs pointed at `evaluate-skill`, which does not exist. The rows now
   point at `writing-skills`, which covers skill quality and hardening but
   does not advertise evaluation. If evaluation deserves a dedicated skill,
   the rows are wrong and should point at it instead.
8. **Who owns the local eval suite's last-run date?** ADR-003 relies on it
   to stop the suite rotting, and calls the mitigation weak. A person
   checking a date is the kind of manual step Cruise Control dislikes.
