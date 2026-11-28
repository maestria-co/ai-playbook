# Setup Prompt for .context/

> Generate project-specific context files that give AI agents the information they need to work effectively in your codebase.

## Before You Run

- [ ] You are in the root directory of your project (not the skill kit repo)
- [ ] The project has at least some existing source files to scan
- [ ] The skill kit is installed (`install.sh` or `install.ps1` has been run)
- [ ] You have write access to the repository

## How to Use

Copy the prompt below and paste it into **Claude Code** (terminal, agent mode) or **VS Code Copilot** (agent mode). It works verbatim in both tools and generates populated `.context/` files tailored to your codebase.

## Setup Prompt

```
You are setting up the `.context/` memory system for this project. Complete all steps without stopping.

## Step 1 — Scan the Project

Read the following to understand the project:
- `package.json` / `requirements.txt` / `Cargo.toml` / `go.mod` (whichever exists) — detect language, framework, key libraries, test framework
- The top-level directory structure (`ls` or equivalent)
- 3-5 representative source files from the main application logic
- 2-3 existing test files
- Any existing `README.md`

From this scan, identify:
- Primary language and version
- Web framework (if any)
- Database and ORM/query library (if any)
- Test framework and how tests are run
- Directory structure pattern (feature-based? layer-based? monorepo?)
- Key third-party dependencies worth documenting
- Actual file paths to use as examples (e.g., a real service file, a real test file)

## Step 2 — Create Directory Structure

Create the following directories if they don't exist:

```
.context/
.context/decisions/
.context/retrospectives/
.context/tasks/
```

If the project has workflows that aren't obvious (complex branching, multi-step CI, etc.), also create `.context/workflows/`.
If the project has a rich domain with many entities, also create `.context/domains/`.

## Step 3 — Copy Universal Files Verbatim

These files are universal (not project-specific). Copy them from the installed skill kit template:

- Copy `~/.copilot/skills/_shared/context_template/context/META.md` → `.context/META.md`
- Copy `~/.copilot/skills/_shared/context_template/context/decisions/README.md` → `.context/decisions/README.md`
- Copy `~/.copilot/skills/_shared/context_template/context/decisions/ADR-001-example-decision.md` → `.context/decisions/ADR-001-example-decision.md`
- Copy `~/.copilot/skills/_shared/context_template/context/retrospectives/README.md` → `.context/retrospectives/README.md`

> Claude Code users: replace `~/.copilot` with `~/.claude` in the paths above.

## Step 4 — Generate Project-Specific Files

For each file below, generate project-specific content based on Step 1. Replace every placeholder with actual content. Use real file paths from this codebase as examples — never generic ones.

| File | What to put in it | Don't duplicate |
|---|---|---|
| `.context/overview.md` | Project purpose, tech stack, key dependencies, current phase. Leave `<!-- TODO: [reason] -->` for anything you cannot determine. | — |
| `.context/architecture.md` | System structure: layers, data flow, key integrations, where things run. Keep it structural — not decisions, not code style. | Don't repeat the tech stack from `overview.md` |
| `.context/standards.md` | Code style, naming conventions, error handling, structural patterns. Read 3+ source files to infer real patterns. Use real file names as examples. | Don't describe what the code does — that's `architecture.md` |
| `.context/testing.md` | Test framework, how to run tests, file naming, mocking approach. Read 2–3 real test files. | Don't duplicate test file paths already in `standards.md` |
| `.context/decisions/ADR-001-example-decision.md` | Replace the example with 1–2 real architectural choices already visible in the codebase. Keep the ADR format exactly. | Don't re-document patterns already in `standards.md` or structure already in `architecture.md` |

## Step 5 — Update AI Configuration Files

**For Claude Code — create or update `CLAUDE.md`:**
If `CLAUDE.md` does **not** exist, copy it from the template:
```
~/.claude/skills/_shared/context_template/CLAUDE.md → CLAUDE.md
```
Then update the `[Project Name]` placeholder with the actual project name and the brief description.

If `CLAUDE.md` **already exists**, add the following block at the top (do not remove existing content):
```
## Project Context

See @.context/overview.md for project overview and tech stack.
See @.context/architecture.md for system structure, layers, and integrations.
See @.context/standards.md for coding conventions and patterns.
See @.context/testing.md for test framework and patterns.
See @.context/decisions/ for architectural decision records (ADRs).
```

**For VS Code GitHub Copilot — create or update `.github/copilot-instructions.md`:**
Create `.github/` if it doesn't exist. Create or update `.github/copilot-instructions.md`:
```
## Project Context

Read `.context/overview.md` for project overview and tech stack before starting any task.
Read `.context/architecture.md` for system structure and integration points.
Read `.context/standards.md` for coding conventions and patterns.
Read `.context/testing.md` for test framework and patterns.
Read `.context/decisions/README.md` for architectural decision records.

Reference specific context files in your prompts with `#` (e.g., `#.context/overview.md`).
```

**If the skill kit is installed**, also add to both files:
```
## Pattern System

Reusable task patterns are in `skills/`. Select a pattern by task type:

- planning-tasks: break a goal into ordered steps
- researching-options: evaluate libraries or approaches
- designing-systems: architecture decisions and ADRs
- implementing-features: write or modify code
- writing-tests: write and run tests
- coordinating-work: orchestrate multi-pattern workflows
  See `skills/GUIDE.md` for the full selection guide.
```

## Step 6 — Final Review Request

After creating all files:
1. List every file created and any sections left as `<!-- TODO -->`
2. Ask the user to review `.context/overview.md` and fill in: business goals, external links, compliance constraints, and current development phase — these cannot be inferred from code alone.

Do not stop before completing all 6 steps.
```
