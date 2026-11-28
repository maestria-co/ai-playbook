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

| Check | Severity | Failure mode it catches |
| --- | --- | --- |
| Required frontmatter (`name`, `description`, `model`) | error | An agent the harness cannot load |
| `model` is in `ALLOWED_MODELS` | error | A model pin that outlived the fleet |
| Required sections per agent tier | error | A specialist missing `## Constraints` |
| Skill references resolve to real directories | error | A cited skill with no folder |
| No stale agent references | error | A rename that missed a caller |
| No `codebase` tool in a tools list | error | A tool grant contradicting the no-raw-source rule |
| `GUIDE.md` exists | error | The routing table gone missing |
| Custom skill is mentioned in `GUIDE.md` | warning | A skill nothing routes to |
| Index-doc paths resolve | error | A table row that outlived its file |
| Shipped file pairs exist, are byte-identical and executable | error | The copy consumers get drifting from the one we run |
| `.context/` layout | error / warning | **Delegated** — see below |

## What `scripts/check-context-layout.sh` asserts

`validate.py` does not reimplement these. It shells out to the checker and
parses its `ERROR:` / `WARN:` lines, so there is one implementation of the
layout rules and consumers run the same file we do. CI also runs it
standalone, because its CLI contract is what `context-review` depends on.

| Check | Severity | Failure mode it catches |
| --- | --- | --- |
| `.context/` exists at all | error | Running the checker against an unstructured repo |
| `overview.md` exists | error | The entry point agents read on every task |
| No `project-overview.md` | error | A relapse of the drift that opened PR #35 |
| `META.md` exists | error | The layout spec missing from the repo that defines it |
| `workflows/pull-requests.md` exists | error | The PR format every repo needs, absent |
| `decisions`/`retrospectives` are folders, not `.md` files | error | ADR numbers and dated entries collapsed into one file |
| `decisions/`/`retrospectives/` exist | error | A repo with nowhere to record a decision |
| Promotable entry exists in exactly one shape | error | `standards.md` and `standards/` both present, agents reading one |
| Promoted folder has a `README.md` | error | A promotion that removed the path agents read |
| Flat file over 300 lines | warning | A file past the promotion threshold |
| Promotable entry absent entirely | warning | Conventions nobody wrote down |
| `retrospectives/` over 10 entries | error | A log nobody prunes |

**This table is itself the drift class it describes.** Nothing pairs a row
with the check it summarizes — the Index-doc check verifies that backticked
*paths* resolve, which cannot catch a row describing behavior the script no
longer has. It was already stale once: the five `.context/` layout checks
landed without rows, in the same commit as a table claiming to list what the
script asserts. If you add or remove a check, edit this table in the same
commit.

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
