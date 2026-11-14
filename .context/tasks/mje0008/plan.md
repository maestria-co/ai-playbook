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
| Specs with acceptance criteria | **Partial** | `skills/task-plan/` and `planning-tasks` produce criteria, but prose only — nothing consumes them |
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

### Phase 1 — Make the existing oracle real (free, no model calls)
1. Fix the `context-specialist.agent.md` missing `## Constraints` section so
   `main` is green.
2. Un-rot `validate.py`: replace the hardcoded `claude-sonnet-4.6` pin with
   the set of models the fleet actually uses, so warnings mean something.
3. Add `.github/workflows/validate.yml` running `validate.py --strict` on
   push and PR. This is the first automated pass/fail signal in the repo and
   the minimum bar for Cruise Control.
4. Make `validate.py` exit non-zero on drift between `CLAUDE.md` /
   `skills/GUIDE.md` index tables and what is on disk — the indexes are hand
   maintained today and nothing catches a stale row.

Phase 1 is entirely free: no model calls, and Actions minutes are free for
public repos. If this repo is private, confirm the free-tier minute budget
before step 3.

### Phase 2 — Decide the eval-cost question
Blocked on the Free and Frugal conflict recorded in ADR-002. Decide how
behavioral evals get paid for — hard budget cap, changed-agents-only,
local-on-demand, or model-free assertions — and record it as ADR-003.
**No Phase 3 work starts until this is decided.**

### Phase 3 — Behavioral evals
Executable cases that assert an agent routes, refuses, or delegates as
intended. Assert on shape and routing, never exact wording. Start with the
Manager: it is the highest-leverage agent (see ADR-001) and its
misrouting cascades to every specialist.

### Phase 4 — Specs that machines consume
Give `task-plan` acceptance criteria a machine-readable form so an agent can
check its own work against them and loop until green. This is the clause
that actually defines Level 4. It depends on Phase 1 and 3 existing first —
a spec format with no runner is more unrun ceremony.

### Phase 5 — Close the lessons loop
`task-retrospective` and `knowledge-graduation` both exist and both wait to
be invoked by a human who remembers. Trigger graduation automatically on a
schedule or a task-count threshold, and have it open a PR rather than ask.

## Guardrails: what is already here

Worth stating so Phase 3 does not rebuild it. `skills/common-constraints/`,
`verification-checklist`, and the per-agent Anti-Rationalization and Scope
Guard tables are a real guardrail layer. The gap is not that guardrails are
missing — it is that **nothing verifies the guardrails are working.** Every
one of them is an instruction the agent may or may not follow, with no
measurement. That is precisely what Phase 3 tests.

## Acceptance criteria for this task

- [x] Maturity ladder recorded with the repo's current position
- [x] Level 4 given a concrete, non-vacuous meaning for a definitions repo
- [x] Gating constraint identified and evidenced
- [x] Phases sequenced by dependency, each sized to one PR
- [x] Core value conflicts surfaced, not buried (Free and Frugal, K.I.S.S.)
- [ ] Phase 1 scope confirmed with mje0002 before any implementation branch

## Open questions

1. **Is this repo public or private?** Decides whether Actions minutes are
   free and therefore whether Phase 1 step 3 is free.
2. **Does `validate.py` own the model allowlist, or does it read it from a
   single source?** A hardcoded list rots again. It just did.
3. **Which agent after the Manager** gets evals first in Phase 3 — `coder`
   (most invoked) or `reviewer` (last line of defense before merge)?
