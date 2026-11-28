---
name: initialize-monorepo
description: >
  Bootstrap .context/ for a monorepo with multiple packages or services. Use when
  setting up the agent system for a monorepo — triggered by "initialize this monorepo",
  "set up context for our monorepo", "we have a packages/ directory and need context
  docs", "our Nx/Turborepo/Lerna workspace needs bootstrapping", or any time a
  multi-package repo has no .context/ and needs to be onboarded. Creates both a
  root-level overview and per-package context directories.
user-invocable: true
---

# Skill: Initialize Monorepo

## Purpose

Bootstrap `.context/` for a monorepo by creating both a root-level overview and per-package
context directories. This skill extends `initialize-repo` to handle repositories with multiple
packages or services that need coordinated but separate documentation. Prevents the common
mistake of merging all package context into a single jumbled document.

---

## Pre-Flight Checks

Run these checks from the `initialize-repo` skill first:

- [ ] Check for existing `.context/` directory (warn if exists, don't overwrite)
- [ ] Locate context_template directory (`~/.copilot/skills/_shared/context_template/` or `~/.claude/skills/_shared/context_template/`)
- [ ] Verify git repository root
- [ ] Confirm write permissions

**Stop if any check fails** — resolve issues before proceeding.

---

## Phase 1: Detect Monorepo Structure

### Detection Strategies by Tool

| Build Tool               | Detection Method                               | Output                     |
| ------------------------ | ---------------------------------------------- | -------------------------- |
| npm/yarn/pnpm workspaces | Read `workspaces` field in root `package.json` | List of glob patterns      |
| Nx                       | Read `nx.json` and `project.json` files        | List of project paths      |
| Turborepo                | Read `turbo.json` and workspace config         | List of package paths      |
| Lerna                    | Read `lerna.json` packages field               | List of glob patterns      |
| Maven                    | Read parent `pom.xml` modules                  | List of module directories |
| Gradle                   | Read `settings.gradle` include statements      | List of project paths      |

### Steps

1. **Identify the monorepo tool** — Check for config files in the repository root
2. **List all packages/services** — Extract package locations from the config
3. **Resolve globs** — If using patterns like `packages/*`, expand to actual directories
4. **Read package metadata** — For each package, extract:
   - Package name
   - Package purpose (from README, package.json description, or pom.xml)
   - Entry points (main files, public APIs)

### Output

```markdown
## Detected Monorepo Structure

Tool: [npm workspaces / Nx / Maven / etc.]
Packages found: [N]

| Package Path    | Name      | Purpose              |
| --------------- | --------- | -------------------- |
| packages/ui-lib | @acme/ui  | Shared UI components |
| packages/api    | @acme/api | REST API service     |
| apps/web        | @acme/web | Main web application |
```

---

## Phase 2: Build Dependency Graph

### Goal

Understand which packages depend on which others to document relationships and build order.

### Detection Methods

| Language              | Method                                      | Command                                |
| --------------------- | ------------------------------------------- | -------------------------------------- |
| JavaScript/TypeScript | Read `dependencies` in package.json         | `npm list --all --json` or parse files |
| Java (Maven)          | Read `<dependencies>` in pom.xml            | `mvn dependency:tree`                  |
| Java (Gradle)         | Read `dependencies` block                   | `gradle dependencies`                  |
| Python                | Read `requirements.txt` or `pyproject.toml` | Parse dependencies                     |

### Steps

1. **Extract dependencies for each package** — Read from package manifests
2. **Filter for internal dependencies** — Keep only dependencies on other packages in this repo
3. **Build directed graph** — Create edges from consumer → dependency
4. **Calculate build order** — Topologically sort the graph

### Output

```markdown
## Package Dependencies

### Dependency Graph

[package-a] → [shared-lib]
[package-b] → [shared-lib]
[app] → [package-a], [package-b]

### Build Order

1. [shared-lib]
2. [package-a], [package-b] (parallel)
3. [app]
```

---

## Phase 3: Create Root-Level Context

### Root `.context/overview.md`

The root is an **aggregate** node: it describes what the packages share, not
code of its own. Declare that in the frontmatter, because the layout checker
reads it to pick its rule set — and an absent key means `project`, which would
have the root asked for `standards.md`, `testing.md`, `retrospectives/` and
`tasks/` it is not supposed to have.

Template:

````markdown
---
context_shape: aggregate
---

# [Monorepo Name] Overview

## Repository Type

Monorepo containing [N] packages/services

## Build Tool

[npm workspaces / Nx / Maven / etc.]

## Package Directory

| Package | Purpose        | Consumers     |
| ------- | -------------- | ------------- |
| [name]  | [what it does] | [who uses it] |

## Tech Stack

- [Language/framework for each type of package]
- [Build tool]
- [Testing frameworks]
- [CI/CD platform]

## Getting Started

```bash
# Clone and install
git clone [repo-url]
cd [repo-name]
[install command]

# Build all packages
[build command]

# Run tests
[test command]
```
````

## Cross-Package Development

- How to link packages locally
- How to test changes across multiple packages
- How to version and release

````

### Root `.context/architecture.md` (Monorepo section)

Add a "Package Structure" section to the root `architecture.md` documenting the dependency relationships discovered in Phase 2, with a diagram if helpful.

### Root `.context/workflows/monorepo-workflow.md`

```markdown
# Monorepo Workflow

## Building
- **Individual package**: [command to build one package]
- **All packages**: [command to build all]
- **Changed packages only**: [command if supported]

## Testing
- **Individual package**: [command]
- **All packages**: [command]
- **Affected tests only**: [command if supported]

## Releasing
- [Versioning strategy — independent vs. fixed]
- [Release process — manual vs. automated]
- [Changelog generation]

## Common Tasks
- Adding a new package: [steps]
- Moving code between packages: [steps]
- Deprecating a package: [steps]
````

---

## Phase 4: Create Per-Package Context

For each package/service:

### Package `.context/overview.md`

A package **is** a project node — the code lives here — so it takes the full
layout and the default shape. The key is written out rather than left implicit
so the contrast with the root is visible in the file itself.

Template:

````markdown
---
context_shape: project
---

# [Package Name]

## Purpose

[What this package does, why it exists]

## Public Interface

- Entry point: [main file or module]
- Exports: [key functions/classes/components]
- API surface: [list or link to API docs]

## Consumers

- [Other packages that depend on this one]
- [External systems if a service]

## Development

```bash
# Run package tests
[command]

# Run package locally (if a service)
[command]

# Build package
[command]
```
````

## Dependencies

- Internal: [other packages in this repo]
- External: [key external dependencies]

## Special Considerations

[Any package-specific quirks, performance notes, security considerations]

````

### Package `.context/domains/` (optional)

Create domain documents only if this package has significant domain knowledge not shared
across the monorepo. If domain knowledge applies to multiple packages, put it in the root
`.context/domains/` instead.

### Skip Generated Packages

Do not create context documentation for:
- Packages containing only generated code
- Build artifacts directories
- Node_modules or vendor directories

---

## Phase 5: Configure AI Tools

### Root `CLAUDE.md` or `.github/copilot-instructions.md`

Template addition:

```markdown
## Monorepo Structure

This is a monorepo containing [N] packages. Context documentation is organized as:

- **Root context** (`.context/` at repo root): Monorepo-wide architecture, workflows, decisions
- **Package context** (`packages/[name]/.context/`): Package-specific details — uses the same flat-file structure (`overview.md`, `standards.md`, `testing.md`, `architecture.md`)

When working on a specific package, consult both the root context and the package-specific context.

### Package Index
[List packages with one-line descriptions]

### Build Commands
- Build all: `[command]`
- Test all: `[command]`
- Build single package: `[command]`
````

### Per-Package Instructions (Optional)

Package-level `CLAUDE.md` files are optional — root instructions are the primary entry point.
Only add per-package instructions if the package has unique conventions that override root conventions.

---

## Phase 6: Verification

### Checklist

- [ ] Root `.context/overview.md` exists and lists all packages
- [ ] Root `.context/architecture.md` has a "Package Structure" section documenting package relationships
- [ ] Root `.context/workflows/monorepo-workflow.md` explains build/test/release
- [ ] Each non-generated package has `.context/overview.md`
- [ ] Root `CLAUDE.md` or `.github/copilot-instructions.md` points to context directories
- [ ] All required files from `initialize-repo` checklist exist at root
- [ ] No context files created for generated-only packages
- [ ] Dependency graph matches actual package.json/pom.xml/build.gradle

### Verification Commands

```bash
# List all context directories created
find . -name ".context" -type d

# Verify context files exist
ls -la .context/
ls -la packages/*/.context/ 2>/dev/null
```

---

## Output Format

```markdown
## Monorepo Initialization Complete

### Root Context

- `.context/overview.md` — [N] packages documented
- `.context/architecture.md` — package relationships and dependency graph documented
- `.context/workflows/monorepo-workflow.md` — build/test/release documented

### Package Context

- `packages/[name]/.context/overview.md` — [repeated for each package]

### AI Tool Configuration

- `CLAUDE.md` — configured with monorepo structure

### Build Order

[shared-lib] → [package-a] → [app]

### Next Steps

1. Review generated context for accuracy
2. Fill in any [TODO] placeholders
3. Add domain-specific documentation to `.context/domains/` as needed (optional — only for complex domains)
4. Commit context documentation to version control
```

---

## Constraints

- **Never merge multiple packages' domain knowledge into a single .context/ file** — keep them
  separate. Root overview describes relationships; package overviews describe the package itself.
- **Do not generate context for packages containing only generated code** — these add noise.
- **Root context is the source of truth for relationships** — package context describes only
  that package, not its relationships.
- **Follow all constraints from initialize-repo skill** — this skill extends it.
- **Do not create circular references** — if package A depends on package B, B cannot depend on A.
- **Verify all build commands actually work** — don't document commands that fail.
