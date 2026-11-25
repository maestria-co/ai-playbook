# Testing

How this repository verifies itself. There is no application code here — the
artifacts are Markdown agent and skill definitions — so "tests" means
structural validation of those files.

---

## Running the checks

```bash
python3 scripts/validate.py            # warnings allowed
python3 scripts/validate.py --strict   # warnings are errors — what CI runs
```

Pure stdlib, no dependencies, no install step. Exit 0 means pass.

| Where it runs | When | Blocking |
| --- | --- | --- |
| `.github/workflows/validate.yml` | every push and pull request | yes |
| `.githooks/pre-push` | before a local push | yes, bypass with `--no-verify` |

The hook and CI deliberately run the identical command. If they drift, a push
passes locally and fails remotely, and people stop trusting the hook.

Local hooks need pointing at once per clone:

```bash
git config --local core.hooksPath .githooks
```

---

## What `scripts/validate.py` asserts

| Check | Failure mode it catches |
| --- | --- |
| Required frontmatter (`name`, `description`, `model`) | An agent the harness cannot load |
| `model` is in `ALLOWED_MODELS` | A model pin that outlived the fleet |
| Required sections per agent tier | A specialist missing `## Constraints` |
| Skill references resolve to real directories | A cited skill with no folder |
| Index-doc paths resolve | A table row that outlived its file |
| `commit-msg` hook copies are byte-identical | The two shipped copies drifting apart |

---

## Adding a check

Put standing invariants — true for every file, every commit — in
`scripts/validate.py` beside the existing ones. Keep it stdlib-only so CI
needs no setup step.

Per-task checks are different: they live with their task in
`.context/tasks/<ID>/checks/` and are promoted to `scripts/checks/` only when a
second task reaches for one. See `.context/tasks/mje0008/plan.md`.

---

## The failure mode to design against

A check that passes by finding nothing is worse than no check, because it
reports green. Observed four times in this repo and its tooling:

| Case | What happened |
| --- | --- |
| `claude plugin eval` | Gated behind early access, exits 0 |
| `jest -t "<typo>"` | 91 tests skipped, nothing run, exits 0 |
| `core.hooksPath` → missing dir | git silently runs no hooks |
| `initialize-repo` pre-flight | Looked for one filename, found nothing, reported "proceed" |

When adding a check, assert that it did something — a count, a parsed result —
not merely that it failed to fail.
