# Git Branching Strategy

> **Purpose:** Document how branches are named, managed, and merged. Consistent branching makes CI predictable and the git history readable.

---

## Branch Naming Convention

[PLACEHOLDER — document the naming pattern for feature, fix, and chore branches]

**Convention in this project:**

| Type | Pattern | Example |
|---|---|---|
| Feature | `feat/TICKET-NNN-short-description` | `feat/AUTH-42-add-oauth-login` |
| Bug fix | `fix/TICKET-NNN-short-description` | `fix/AUTH-67-expired-token-error` |
| Chore | `chore/short-description` | `chore/update-dependencies` |
| Release | `release/vX.Y.Z` | `release/v1.4.0` |
| Hotfix | `hotfix/short-description` | `hotfix/stripe-webhook-failure` |

Use `kebab-case` for the description. Keep it under 5 words. Always include the ticket number for feat/fix branches.

---

## Main Branches

[PLACEHOLDER — document the permanent branches and their purpose]

| Branch | Purpose | Who can push? |
|---|---|---|
| `main` | Production-ready code. Deploys to production on merge. | Nobody directly — PR only |
| `develop` | Integration branch. Deploys to staging on merge. | Nobody directly — PR only |

---

## Branch Lifecycle

1. **Create** from `develop` (or `main` for hotfixes)
2. **Develop** on the branch — commit early, commit often
3. **Open PR** against `develop` — follow `pull-requests.md` for title and description
4. **Pass CI** — all checks must be green before review
5. **Get approval** — at least 1 reviewer approval required
6. **Merge** via squash merge — keeps history clean
7. **Delete** the branch after merge — GitHub does this automatically if configured

---

## Commit Message Format

[PLACEHOLDER — document the commit message convention]

**Convention:** Conventional Commits (`type(scope): description`)

```
feat(auth): add GitHub OAuth login
fix(auth): handle expired JWT tokens correctly
chore(deps): update vitest to 1.6.0
docs(context): add session entity to domains/entities.md
```

Types: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`, `perf`

Keep the subject line under 72 characters. Add a body if the *why* isn't obvious.

---

## PR Rules

> PR **title and description format** live in `pull-requests.md` — that file is the
> source of truth. Do not add a competing PR template here.

[PLACEHOLDER — document what's required for a PR to be merged]

- At least **1 approval** from a team member (not the author)
- All **CI checks must pass**: lint, unit tests, integration tests, type check
- **Linked ticket** — PR description must reference the ticket number
- **No force pushes** to `develop` or `main`
- **Squash merge** only — no merge commits, no rebase-and-merge
