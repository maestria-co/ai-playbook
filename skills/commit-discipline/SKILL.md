---
name: commit-discipline
description: >
  Git commit conventions and branch management standards. Use this skill whenever
  making commits, creating branches, reviewing commit history, or preparing code
  for a pull request. Also use when you notice messy commit history, unclear messages,
  or files that shouldn't be committed. If you're about to run `git commit`, consult
  this skill first.
---

# Skill: Commit Discipline

## Purpose

Consistent git practices make history readable, bisect usable, and collaboration smooth.
This skill defines commit message format, branch naming, atomicity rules, and what
should (and shouldn't) be committed.

### Enforcement

`scripts/git-hooks/commit-msg` rejects any message that doesn't match this format. Turn it on once per machine:

```
git config --global core.hooksPath <path-to-ai-playbook>/scripts/git-hooks
```

---

## Commit Message Format

Use Conventional Commits. Every commit message follows:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

### Types

| Type       | When to use                                         |
| ---------- | --------------------------------------------------- |
| `feat`     | New feature or capability                           |
| `fix`      | Bug fix                                             |
| `docs`     | Documentation only                                  |
| `refactor` | Code change that doesn't fix a bug or add a feature |
| `test`     | Adding or fixing tests                              |
| `chore`    | Build, config, tooling changes                      |
| `style`    | Formatting, whitespace (no logic change)            |
| `perf`     | Performance improvement                             |

### Scope

Optional. Use the module, component, or area affected:

- `feat(auth): add JWT token refresh`
- `fix(api): handle null response from payment gateway`
- `docs(readme): add setup instructions`

### Short Description

- Imperative mood: "add", "fix", "remove" — not "added", "fixes", "removed"
- Lowercase first letter
- No period at the end
- Max 72 characters

### Body (optional)

- Explain **why**, not what (the diff shows what)
- Wrap at 72 characters
- Separate from subject with a blank line

### Footer (optional)

- Reference issues: `Closes #123`, `Fixes #456`
- Breaking changes: `BREAKING CHANGE: removed legacy auth endpoint`

### Examples

```
feat(auth): add password reset flow

Users can now request a password reset via email. Tokens expire
after 24 hours. Rate limited to 3 requests per hour per email.

Closes #234
```

```
fix(api): handle null payment gateway response

The gateway returns null instead of an error object when the
service is degraded. Added null check with appropriate error message.

Fixes #567
```

---

## Branch Naming

### Format

```
<type>/[TASK-ID-]short-description
```

### Types

| Prefix      | When                  |
| ----------- | --------------------- |
| `feature/`  | New features          |
| `fix/`      | Bug fixes             |
| `refactor/` | Code restructuring    |
| `docs/`     | Documentation changes |
| `chore/`    | Tooling, config, CI   |

### Rules

- Use kebab-case: `feature/add-user-search`
- Include task ID if available: `feature/TASK-42-add-user-search`
- Keep it short but descriptive
- Branch from main/develop per project convention

### Detect Project Conventions

Before creating branches, check:

1. `.context/workflows/branching.md` — documented branch strategy
2. Recent git history: `git branch -a | head -20` — existing patterns
3. If no convention exists, use the format above

---

## Atomic Commits

### One Logical Change Per Commit

A commit should contain exactly one logical change. If you can describe it with "and"
in the commit message, it's probably two commits.

```
BAD:  "fix login bug and add user search feature"
GOOD: Two separate commits:
      "fix(auth): handle expired session token"
      "feat(search): add user search by email"
```

### What's "One Logical Change"?

- Moving a function + updating all callers = one commit (refactor)
- Adding a feature + its tests = one commit (feat)
- Fixing a bug + adding a regression test = one commit (fix)
- Fixing two unrelated bugs = two commits

### Staging Discipline

Use `git add -p` (patch mode) to stage specific hunks when a file has changes
for multiple logical units. Don't `git add .` and commit everything.

---

## What Not to Commit

### Never Commit

- **Credentials** — API keys, passwords, tokens, secrets
- **Build artifacts** — compiled output, `dist/`, `build/`, `node_modules/`
- **Temporary files** — `.DS_Store`, `*.swp`, IDE-specific files
- **Large binaries** — images over 1MB, videos, datasets (use Git LFS or external storage)
- **Environment files** — `.env` with real values (commit `.env.example` instead)

### Check Before Committing

```bash
# Review what you're about to commit
git diff --staged

# Check for accidentally staged files
git status

# Search for potential secrets
git diff --staged | grep -iE 'password|secret|api_key|token'
```

---

## Commit Frequency

### When to Commit

- After completing a logical unit of work
- Before switching to a different task
- Before making a risky change (commit the safe state first)
- At least once per work session

### When Not to Commit

- Code doesn't compile/build
- Tests are failing (unless the commit is specifically "add failing test for bug X")
- Changes are half-done and would break the build for others

---

## Project Convention Detection

Before making your first commit on a project:

1. Read `.context/workflows/branching.md` if it exists
2. Run `git log --oneline -20` to see existing message patterns
3. Check if the project uses Conventional Commits, Gitmoji, or custom format
4. **Follow the existing convention**, even if it differs from this skill's defaults

If the project has no established convention, use Conventional Commits as defined above.

---

## Constraints

- Never force-push to shared branches (main, develop)
- Never commit secrets — if you accidentally do, rotate the credentials immediately
- Follow project conventions over this skill's defaults when they differ
- Write commit messages in English unless the project explicitly uses another language
- Every commit on main/develop should leave the build in a passing state
