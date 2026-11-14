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
4. ⬜ **Not done.** Make `validate.py` exit non-zero on drift between the
   `CLAUDE.md` / `skills/GUIDE.md` index tables and what is on disk. The
   indexes are hand maintained and nothing catches a stale row.

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

Step 3 is the one that changes agent behavior. Steps 1 and 2 only make it
possible.

### Phase 3 — Decide the eval-cost question
Blocked on the Free and Frugal conflict in ADR-002. Decide how behavioral
evals get paid for — hard budget cap, changed-agents-only, local-on-demand,
or model-free assertions — and record it as ADR-003.
**No Phase 4 work starts until this is decided.**

### Phase 4 — Behavioral evals
Structural checks catch a malformed artifact. Per-task checks catch an
undone task. Neither catches an artifact that is well-formed and wrong — an
agent that routes to the wrong specialist or skips a handoff.

Executable cases asserting an agent routes, refuses, or delegates as
intended. Assert on shape and routing, never exact wording. Start with the
Manager: highest leverage (see ADR-001), and its misrouting cascades to
every specialist.

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

1. ~~Is this repo public or private?~~ **Answered 2026-11-14: public.**
   Actions minutes are unlimited and free.
2. **Does `validate.py` own the model allowlist, or does it read it from a
   single source?** A hardcoded list rots again. It just did.
3. **Which agent after the Manager** gets evals first in Phase 4 — `coder`
   (most invoked) or `reviewer` (last line of defense before merge)?
4. **Who writes a task's per-task checks in Phase 2** — the planner when it
   writes the spec, or the coder when it does the work? The planner is the
   honest answer, because a coder writing its own passing condition is the
   same self-assessment problem one level up.
