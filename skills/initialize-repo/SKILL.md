---
name: initialize-repo
description: >
  Automates the setup of `.context/` for a new project. Use this skill whenever
  someone mentions setting up a new repository, onboarding a project to the agent
  system, bootstrapping context, or when you detect a project has no `.context/`
  directory. Also use when someone says "initialize", "set up", or "configure" in
  relation to project context, or when installing the skill kit for the first time.
  Skip only when `.context/` already exists and is populated — in that case use
  `context-review` instead.
user-invocable: true
---

# Skill: Initialize Repository

## Purpose

Set up the `.context/` knowledge base for a project so that AI agents and developers
start every task informed. This skill runs once per repository. It detects the project's
characteristics, copies the context template, populates it with inferred details, and
configures AI tool integration files.

If `.context/` already exists with content, do not overwrite — use `context-review` instead.

---

## Pre-flight Checks

**Check 1 — Verify no existing context**

Look for `.context/overview.md` in the current working directory.

- If it exists and has content beyond placeholders → **Abort.** Report: "`.context/` already exists. Use `context-review` to update it."
- If it does not exist, or contains only `[PLACEHOLDER]` markers → proceed.

**Check 2 — Locate the skill kit template**

Find the `context_template/` directory using the **find-context-template** skill.

Detection approach (safe pattern):

```bash
template_dir=""
if [ -d ~/.copilot/skills/_shared/context_template/ ]; then
  template_dir=~/.copilot/skills/_shared/context_template
elif [ -d ~/.claude/skills/_shared/context_template/ ]; then
  template_dir=~/.claude/skills/_shared/context_template
fi
```

Check locations in order:

1. `~/.copilot/skills/_shared/context_template/` (Copilot install)
2. `~/.claude/skills/_shared/context_template/` (Claude Code install)
3. Ask the user for the path

- If found → note the path and verify it contains required files (see **find-context-template** skill)
- If not found → **fall back** to generating files from scratch using the structure in Step 2

**Security note:** Do not use nested command substitution like `$(realpath ...)` — use direct tilde expansion or `cd` + `pwd` for path resolution.

---

## Execution Steps

### Step 1 — Detect Project Characteristics

Scan the project to identify its stack. Check these files:

| File                                  | Detects                                            |
| ------------------------------------- | -------------------------------------------------- |
| `package.json`                        | Node.js — framework, test runner, key dependencies |
| `requirements.txt` / `pyproject.toml` | Python — framework, testing library                |
| `*.csproj` / `*.sln`                  | .NET — framework, target version                   |
| `pom.xml` / `build.gradle`            | Java/Kotlin — framework, build tool                |
| `Cargo.toml`                          | Rust — edition, key crates                         |
| `go.mod`                              | Go — module path, dependencies                     |

Also scan:

- **Top-level directory structure** — identify feature-based vs. layer-based organization
- **3–5 representative source files** — infer naming conventions, code style, error handling patterns
- **2–3 test files** — identify test framework, mocking approach, file naming pattern
- **`.github/workflows/`** or other CI config — identify CI/CD pipeline
- **Git history** — `git log --oneline -20` for recent activity; `git branch -a` for branching patterns

Record findings. These feed into Step 3.

### Step 2 — Create Directory Structure

Create the following directories:

```bash
mkdir -p .context/{decisions,retrospectives,tasks,workflows}
```

`workflows/` is always created — every repo needs a documented PR format (see Step 3a).
Add `branching.md` and `ci-cd.md` alongside it only if the project has non-obvious
workflows (complex branching, multi-step CI).
If the project has a rich domain with many entities or project-specific terminology, also create `.context/domains/`.

### Step 3 — Copy and Populate Files

**Universal files (copy verbatim from template):**

- `META.md`
- `decisions/index.md`
- `decisions/ADR-001-example-decision.md`
- `retrospectives/README.md`

### Step 3a — Populate `workflows/pull-requests.md`

Copy `workflows/pull-requests.md` from the template, then fill in its **Repo Configuration**
table from observed evidence. Do not guess — derive each value:

| Setting | How to derive |
| --- | --- |
| Ticket prefix | Most frequent `[A-Z]+-[0-9]+` token across branches, tags and commit subjects. If none exists, ask the human rather than inventing one. |
| Ticket number format | Digit count and zero-padding of the matches found above (`MAE-0009` → 4 digits, zero-padded). |
| Default target branch | `dev`/`develop` if present on the remote, else `main`. |
| Secondary integration branch | `dev` if it exists and is not already the default, else _none_. |
| Tracker | From repo config, README, or ask the human. |

```bash
# ticket prefix and format
{ git branch -a --format='%(refname:short)'; git tag; git log --format='%s%n%b' -500; } \
  | grep -oiE '[A-Z]+-[0-9]+' | tr 'a-z' 'A-Z' | sort | uniq -c | sort -rn | head
# integration branch
git branch -r --format='%(refname:short)' | grep -E 'origin/(dev|develop)$'
```

Also replace the `<PREFIX>` placeholder in the Step 2 fallback command with the resolved
prefix, and swap the illustrative worked example for a real PR from this repo if one exists.

**Project-specific files (generate from Step 1 scan):**

| File                                    | Generation approach                                                                                                         | Don't duplicate                                                                |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `overview.md`                           | Infer from manifest + directory structure. Leave `<!-- TODO -->` for unknowable fields (business goals, compliance).        | —                                                                              |
| `architecture.md`                       | System structure: layers, data flow, key integrations, where it runs. Structural — not code style, not decisions.           | Don't repeat tech stack from `overview.md`                                     |
| `standards.md`                          | Code style, naming conventions, error handling, structural patterns. Read 3+ source files. Use real file names as examples. | Don't describe what the code does — that's `architecture.md`                   |
| `testing.md`                            | Test framework, how to run tests, file naming, mocking approach. Read 2–3 real test files.                                  | Don't duplicate file paths already in `standards.md`                           |
| `decisions/ADR-001-example-decision.md` | Replace the example with 1–2 real architectural choices visible in the codebase. Keep the ADR format exactly.               | Don't re-document patterns in `standards.md` or structure in `architecture.md` |

### Step 4 — Configure AI Tool Integration

**For Claude Code — create or update `CLAUDE.md`:**

If `CLAUDE.md` does not exist, copy it from the template:

```
~/.copilot/skills/_shared/context_template/CLAUDE.md → CLAUDE.md
```

Then fill in the `[Project Name]` and brief description placeholders.

If `CLAUDE.md` already exists, add at the top (preserve existing content):

```markdown
## Project Context

See @.context/overview.md for project overview and tech stack.
See @.context/architecture.md for system structure, layers, and integrations.
See @.context/standards.md for coding conventions and patterns.
See @.context/testing.md for test framework and patterns.
See @.context/decisions/ for architectural decision records (ADRs).
```

**For VS Code Copilot — create or update `.github/copilot-instructions.md`:**

```markdown
## Project Context

Read `.context/overview.md` for project overview and tech stack before starting any task.
Read `.context/architecture.md` for system structure and integration points.
Read `.context/standards.md` for coding conventions and patterns.
Read `.context/testing.md` for test framework and patterns.
Read `.context/decisions/index.md` for architectural decision records.
```

### Step 5 — Verification

Confirm all required files exist and are non-empty:

```bash
for f in .context/META.md .context/overview.md .context/architecture.md \
         .context/standards.md .context/testing.md \
         .context/decisions/index.md .context/retrospectives/README.md; do
  [ -s "$f" ] && echo "✅ $f" || echo "❌ $f — missing or empty"
done
```

**Quality bar:** Before finishing, apply the **context-document-guidelines** skill to each
generated file. Each file must pass the quality checklist (specific to this project, contains
real file paths, explains rationale, not generic boilerplate). Files that only contain
placeholder text should be flagged for human completion rather than left as misleading stubs.

---

## Output Format

```
Initialized: .context/ for [project name]

Tech stack detected: [language, framework, test runner]
Files created: [count]
Files with TODOs: [count] — these need human input

Next steps:
1. Review .context/overview.md — fill in business goals, external links, compliance
2. Commit .context/ to version control
3. Tell your team — link to META.md
```

---

## Constraints

- Never overwrite existing `.context/` files that have content beyond placeholders
- Use real file paths from the codebase in examples — never generic ones
- Leave `<!-- TODO: [reason] -->` for anything that cannot be inferred from code
- Do not invent business rules — only document what's visible in the code
- Do not modify source code during this skill — only `.context/`, `CLAUDE.md`, and `copilot-instructions.md`
