# Pull Request Format

> **AI Instruction:** Follow this document whenever opening a pull request. It is the
> single source of truth for PR titles and descriptions. Where `branching.md` also shows
> a PR template, this file wins.

## Purpose

Give agents a deterministic procedure for producing a PR title and description from the
actual code changes, so every PR answers three questions in the same order: why the change
exists, what changed, and what the reviewer needs to watch out for.

---

## Repo Configuration

Each repo fills this in when copying this file. Everything below this block is portable.

| Setting | Value |
| --- | --- |
| Ticket prefix | <!-- TODO: e.g. `MAE` — derive from existing branch/commit history --> |
| Ticket number format | <!-- TODO: e.g. 4 digits, zero-padded (`MAE-0009`) --> |
| Default target branch | <!-- TODO: `main` or `dev` --> |
| Secondary integration branch | <!-- TODO: `dev` if the repo has one, otherwise _none_ --> |
| Tracker | <!-- TODO: Asana / Jira / Linear / GitHub Issues --> |

---

## Title Format

```
[TICKET-ID] Short imperative summary
```

**Rules:**
- Ticket ID in square brackets, uppercase, always first.
- Summary is imperative mood, no trailing period, aim for under 60 characters total.
- Summary describes the outcome, not the activity. `Cache OAuth2 tokens` beats `Changes for caching`.

**Good:**
```
[MAE-0009] Fix Kratos post-registration session hook
[MAE-0010] Inject business_id into Hydra JWT via consent session
```

**Bad:**
```
MAE-0009 fix stuff              → missing brackets, vague
[mae-9] Fixed the hook.         → wrong case, unpadded, past tense, trailing period
Fix Kratos hook                 → missing ticket ID
```

---

## Step 1 — Resolve the Target Branch

Never assume. Resolve in this order and stop at the first hit:

1. The base branch explicitly given in the request.
2. The branch the current branch was cut from:
   ```bash
   git merge-base --fork-point origin/main HEAD
   ```
3. If the repo has a `dev` branch, feature work targets `dev`; hotfixes target `main`:
   ```bash
   git branch -r --format='%(refname:short)' | grep -E 'origin/(dev|develop)$'
   ```
4. Otherwise `main`.

Confirm the resolved target with the human before opening the PR if steps 1–3 were all
ambiguous.

---

## Step 2 — Resolve the Ticket ID

Resolve in this order and stop at the first hit:

1. **Explicitly provided** in the request.
2. **Branch name** — matches the configured prefix, any case, with or without padding:
   ```bash
   git rev-parse --abbrev-ref HEAD | grep -oiE '[A-Z]+-[0-9]+'
   ```
   `feature/MAE-0009-configure-kratos-hydra` → `MAE-0009`
3. **Commit scopes on this branch** — the conventional-commit scope carries the ticket:
   ```bash
   git log origin/main..HEAD --format='%s' \
     | grep -oiE '\([A-Z]+-[0-9]+\)' | tr -d '()' | head -1
   ```
   `feat(MAE-0009): fix Kratos post-registration session hook` → `MAE-0009`
4. **Commit bodies** — `Refs MAE-0009`, `Closes MAE-0009`.
5. **No ticket found** — do not invent a number. Derive a provisional ID by taking the
   configured prefix and the next number above the highest ticket seen in branch and tag
   history, then flag it in the PR body as provisional and ask the human to confirm:
   ```bash
   { git branch -a --format='%(refname:short)'; git tag; git log --format='%s%n%b' -500; } \
     | grep -oiE '<PREFIX>-[0-9]+' | tr 'a-z' 'A-Z' | sort -u | tail -1
   ```
   Scan branches, tags **and** commit messages — tickets frequently appear only in a
   commit scope and never in a branch name.

Normalize whatever you find to the configured casing and padding: `mae-9` → `MAE-0009`.

---

## Step 3 — Read the Actual Changes

Build the description from the real diff against the resolved target branch, never from
memory of what you intended to do:

```bash
TARGET=main   # from Step 1
git fetch origin "$TARGET"
git log  "origin/$TARGET...HEAD" --format='%s%n%b'   # intent, per commit
git diff "origin/$TARGET...HEAD" --stat              # blast radius
git diff "origin/$TARGET...HEAD"                     # the actual change
```

Use three dots (`...`). Two dots includes commits that landed on the target after you
branched, which inflates the PR description with other people's work.

---

## Step 4 — Write the Description

```markdown
## Why

[1-3 sentences. The problem, not the solution. What was broken, missing, or blocked —
and the user- or system-level consequence. Link the ticket.]

## Summary of Changes

- [Change grouped by behavior or subsystem, not by file.]
- [Each bullet names the real path(s) it touches.]
- [Omit noise: lockfiles, formatting-only churn, generated output.]

## Reviewer Notes

[Only what the diff does not make obvious. Delete any heading below that does not apply —
an empty section is worse than no section.]

**Needs close review:** [Specific files or logic where a subtle mistake would be costly.]

**Deliberate decisions:** [Choices a reviewer might otherwise flag, and why.]

**Out of scope:** [Related problems intentionally left alone, with the follow-up ticket.]

**Risk / rollout:** [Migrations, config or secret changes, breaking API changes,
ordering requirements for deploy.]

**Verification:** [What was actually run and what the result was. State plainly if a
check was skipped.]
```

### Section Rules

- **Why** comes first and is never skipped. A PR without a stated reason cannot be reviewed,
  only read.
- **Summary of Changes** groups by behavior. Ten bullets that restate the file list are
  worth less than three that explain the change.
- **Reviewer Notes** is where honesty lives. If tests fail, say so here with the output. If
  something is untested, say that. Do not report work as verified when it is not.

---

## Worked Example

Illustrative only — replace with a real PR from this repo once one exists.
Branch `feature/MAE-0009-configure-kratos-hydra` → `main`:

```markdown
[MAE-0009] Fix Kratos post-registration session hook

## Why

New users completing registration were left without a session, so the app bounced them
back to login immediately after signup. Kratos was not issuing a session on the
post-registration hook, and the default return URL pointed at a route that no longer
exists. Refs MAE-0009.

## Summary of Changes

- Enable the `session` hook on the Kratos post-registration flow so signup issues a
  session directly (`kratos/kratos.yml`).
- Repoint the default return URL at the app's post-signup landing route
  (`kratos/kratos.yml`, `src/config/urls.ts`).
- Document the Hydra M2M client credentials the flow depends on (`docs/hydra-setup.md`).

## Reviewer Notes

**Needs close review:** the hook ordering in `kratos.yml` — the session hook must run
after `profile`, or the identity traits are not yet persisted when the session is minted.

**Deliberate decisions:** kept the return URL in config rather than deriving it from the
request origin, so a spoofed `Origin` header cannot redirect new users off-domain.

**Risk / rollout:** requires the Kratos container to be restarted to pick up `kratos.yml`.
No database migration.

**Verification:** full registration flow driven end-to-end in Playwright against the local
compose stack — signup now lands authenticated on the dashboard. Logout path retested and
still terminates the Hydra session.
```

---

## Pitfalls

- **Using `git diff main...HEAD` without fetching first.** A stale `origin/main` silently
  produces a wrong diff and a description full of changes you did not make.
- **Two dots instead of three.** Pulls in unrelated commits from the target branch.
- **Inventing a ticket number.** If Step 2 reaches the fallback, label it provisional and
  ask. A wrong ticket ID is harder to clean up than a missing one.
- **Describing intent instead of the diff.** Write the PR from what the code actually does
  after the final commit, not from the plan you started with.
- **Keeping empty Reviewer Notes headings.** Delete what does not apply.
- **Conflicting template in `branching.md`.** That file carries an older PR template; this
  document supersedes it.

---

## Related Files

- `.context/workflows/branching.md` — branch naming and merge strategy
- `.context/workflows/ci-cd.md` — checks that must pass before merge
