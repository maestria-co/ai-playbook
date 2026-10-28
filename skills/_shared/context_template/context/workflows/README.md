# workflows/

Development workflows, branching strategy, and CI/CD documentation.

## What belongs here

- **Task execution workflow** — how to pick the right pattern for a task and execute it
- **Pull request format** — PR title convention and description structure (required in every repo)
- **Git branching strategy** — branch naming, lifecycle, commit messages
- **CI/CD pipeline** — what runs in CI, how to replicate locally, deployment process

## Files

| File                        | Purpose                                                           |
| --------------------------- | ----------------------------------------------------------------- |
| `task-workflow-template.md` | Decision tree for choosing the right workflow pattern per task    |
| `pull-requests.md`          | **Source of truth for PR titles and descriptions**                |
| `branching.md`              | Branch naming, commit message format                              |
| `ci-cd.md`                  | Pipeline overview, local replication commands, deployment process |

## When to update

- The PR title format or ticket convention changes
- The branching strategy changes
- CI/CD pipeline steps are added or modified
- A new workflow pattern is established
- Deployment process or environment changes
