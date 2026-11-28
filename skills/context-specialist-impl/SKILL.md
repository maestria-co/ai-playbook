---
name: context-specialist-impl
description: Internal backing skill for the @context-specialist agent. NOT for direct invocation. Covers tree-position detection and .context/ initialization for leaf, branch, and root nodes.
user-invocable: false
---

# Context Specialist Implementation

Backing skill for `@context-specialist`. Provides:
1. Tree-position detection from filesystem signals
2. Initialization process per position (leaf / branch / root)

---

## Section 1: Detect Tree Position

When the caller has not supplied an explicit `tree_position`, detect it from filesystem signals.

### context-specialist-impl: Step 1: ROOT check

Check for monorepo/workspace manifests at CWD. Any of these signals → position = `root`:

- `nx.json`, `turbo.json`, or `go.work` exists at CWD
- A `.sln` file exists at CWD
- A `*.code-workspace` file exists at CWD
- `package.json` at CWD contains a `"workspaces"` field
- `pom.xml` at CWD contains `<modules>` AND `src/` directory does NOT exist

### context-specialist-impl: Step 2: LEAF check

Any of these at CWD → position = `leaf`:

`package.json` (without `"workspaces"`), `go.mod`, `Cargo.toml`, `pyproject.toml`,
`requirements.txt`, `Gemfile`, `build.gradle`, `pom.xml` (with `src/`), `*.csproj`

### context-specialist-impl: Step 3: BRANCH check

No local manifest matched. Count subdirectories (depth 1) that contain any build manifest.
If **2 or more** subdirectories contain build manifests → position = `branch`.

### context-specialist-impl: Step 4: Fallback

No signals matched → default to `leaf`. Log a warning:

> "Tree position could not be determined from manifest signals — defaulting to leaf. Review the generated `.context/` for accuracy."

### Detection Summary

| Signal | Position |
|--------|---------|
| `nx.json`, `turbo.json`, `go.work`, `.sln` at CWD | root |
| `*.code-workspace` at CWD | root |
| `package.json` with `"workspaces"` | root |
| `pom.xml` with `<modules>` and no `src/` | root |
| `package.json` (no `workspaces`), `go.mod`, `*.csproj`, etc. at CWD | leaf |
| None of above, but 2+ subdirs contain build manifests | branch |
| No signals match | leaf (fallback + warning) |

---

## Section 2: Initialize Leaf Node

**For `tree_position: leaf`**, invoke the `initialize-repo` skill.
The full leaf initialization process lives there — do not duplicate it.

A leaf is a **project** node: the code lives here, so it takes the full
layout. `initialize-repo` declares `context_shape: project` in its
`overview.md`.

> Invoke skill: `initialize-repo`

---

## Section 3: Initialize Branch Node

**For `tree_position: branch`** — a grouping directory (e.g., `services/`, `apps/`) with sub-projects but no build manifest of its own.

### Branch `.context/` Structure

A branch is an **aggregate** node — it describes what its sub-projects share
and holds no code — so `overview.md` declares `context_shape: aggregate` and
the node takes the reduced layout.

```
.context/
├── META.md                     (copy from context_template — verbatim)
├── overview.md                 (context_shape: aggregate; what lives here, and the project map)
├── decisions/
│   ├── README.md               (ADR index)
│   └── ADR-NNN-<slug>.md       (decisions affecting 2+ sub-projects)
├── architecture/
│   ├── README.md               (entry point — agents read this)
│   └── patterns.md             (shared patterns used by 2+ sub-projects)
├── domains/
│   └── <domain>.md             (business/technical domains spanning 2+ sub-projects)
└── .gitignore                  (copy from context_template — verbatim)
```

No `workflows/` — a grouping directory is not a git repository, so it has no
PR format, branching strategy or CI of its own.

**Explicitly absent** at branch level:

| Omitted | Reason |
|---------|--------|
| `standards/` | Code style is per-leaf-project |
| `testing/` | Test infrastructure is per-leaf-project |
| `styling/` | Frontend conventions are per-leaf-project |
| `tasks/` | Tasks are tracked against specific projects |
| `retrospectives/` | Retrospectives belong to the project the work happened in |
| `workflows/` | PR format, branching and CI belong to the repository, not a directory inside it |

### Branch File Content Guide

**`overview.md`** — "what lives here and how do they relate?"
- `context_shape: aggregate` in the frontmatter
- 1–3 sentences on the group's shared purpose
- The **project map**, which is also the routing table `resolve-repo-context`
  reads. It lives here rather than in a separate `projects.md` because this
  table and that file were the same table:

```markdown
| Project Name | Path | Description | Primary Language/Stack |
|---|---|---|---|
| api-service | api-service/ | REST API for X | Node.js 20 |
```

- How sub-projects communicate (shared libraries, events, APIs) — omit if independent

**`decisions/`** — architectural decisions affecting 2+ sub-projects here, one
ADR per file plus a `README.md` index. A cross-project decision is an ADR with
a wider blast radius, not a different kind of artifact, so it is numbered and
cited the same way. Create the folder and its index even when there are no
cross-project decisions yet; it is where the first one goes.

**`architecture/README.md`** — the entry point agents read for this node, and a
short index of the files beside it.

**`architecture/patterns.md`** — cross-project patterns used by 2+ sub-projects (shared libraries, common middleware). Strictly cross-project only. Omit if sub-projects share nothing.

**`domains/<domain>.md`** — domain concepts spanning 2+ sub-projects only. Do not duplicate leaf domain files here.

### Branch Process

1. Scan depth 1–2 for build manifests to discover sub-projects
2. Read each sub-project's `.context/overview.md` first sentence (if it exists); otherwise scan build manifest + README first paragraph
3. Invoke `find-context-template` to locate `$TEMPLATE_DIR`; copy `META.md` and `.gitignore` verbatim
4. Generate `overview.md` — `context_shape: aggregate`, group purpose, and the project map from the sub-projects discovered in step 1
5. Create `decisions/` with a `README.md` index; add ADRs only for decisions that are actually identifiable
6. Generate `architecture/README.md`, plus `patterns.md` only if 2+ sub-projects share patterns
7. Generate `domains/<domain>.md` only for concepts spanning 2+ sub-projects
8. Run the layout checker against this node — `scripts/check-context-layout.sh <path>/.context` — and fix what it reports before committing
9. Commit all created files

---

## Section 4: Initialize Root Node

**For `tree_position: root`** — top-level of a monorepo or workspace.

**Do not modify sub-project `.context/` folders.** Root context covers what is shared across projects — not what is specific to any one project.

### Root `.context/` Structure

A root is an **aggregate** node, so `overview.md` declares
`context_shape: aggregate` and the node takes the reduced layout. A monorepo
root *is* the git repository, so unlike a branch node it does carry
`workflows/` — including the required `pull-requests.md`. A workspace root is
a folder of repositories and carries none.

```
.context/
├── META.md                           (copy from context_template — verbatim)
├── overview.md                       (context_shape: aggregate; what this is, how areas relate, the area map)
├── decisions/
│   ├── README.md                     (ADR index)
│   └── ADR-NNN-<slug>.md             (decisions affecting 2+ areas)
├── architecture/
│   ├── README.md                     (entry point — agents read this)
│   └── patterns.md                   (cross-area patterns and shared abstractions)
├── domains/
│   └── <domain>.md                   (domains spanning 2+ areas)
└── workflows/                        (monorepo root only — a workspace root has no .git)
    ├── pull-requests.md              (required; copy from template and fill)
    ├── ci-cd.md                      (root-level pipeline and deployment)
    ├── branching.md                  (branching strategy and merge process)
    └── commit-conventions.md         (detected from git log)
```

No `standards.md`, `testing.md`, `retrospectives/` or `tasks/` — all four
belong to the areas themselves.

### Root Initialization Process

**Step A — Read sub-project context**: Before generating anything, read each area's `.context/overview.md` first sentence. Record primary stack and any shared libraries mentioned.

**Step B — Build the area map**: Derive names from each area's `overview.md` first sentence; fall back to build manifest + README. Paths relative to repo root. Include every area — omit none. This map goes into `overview.md` in Step D, not a separate `projects.md`: the area table and the overview's area table were the same table, and `resolve-repo-context` reads it from `overview.md`.

```markdown
| Project Name | Path | Description | Primary Language/Stack |
|---|---|---|---|
| api | services/api | REST API gateway | Node.js 20 |
```

**Step C — Scan root infrastructure**: Check for CI/CD files (`.github/workflows/`, `Jenkinsfile`, `azure-pipelines.yml`), IaC (`terraform/`, `cdk/`), shared scripts (`Makefile`, `scripts/`), monorepo build coordinators (`nx.json`, `turbo.json`, `go.work`, `Directory.Build.props`).

**Step D — Generate `overview.md`**: Declare `context_shape: aggregate` in the frontmatter. What the monorepo is, how areas relate, shared libraries and event buses, cross-cutting concepts, and the area map from Step B. Reference area paths — do not duplicate area content.

**Step E — Create `decisions/`**: One ADR per file plus a `README.md` index, the same shape a project node uses — a cross-area decision is an ADR with a wider blast radius, not a different artifact. Candidates: shared auth libraries, locked framework versions, patterns not used and why. Create the folder and index even when no cross-area decision is identifiable yet; it is where the first one goes.

**Step F — Generate `architecture/README.md` and `patterns.md`**: `README.md` is the entry point agents read for a promoted folder, and indexes what sits beside it. `patterns.md` holds cross-area patterns only — how services communicate, shared packages used by 2+ areas, module dependency graph.

**Step G — Generate `domains/` files**: One file per domain spanning 2+ areas. Format mirrors leaf domain files. Skip domains internal to a single area.

**Step H — Generate `workflows/ci-cd.md`**: CI system, pipeline stages, deployment environments, manual gates, per-area divergences.

**Step I — Generate `workflows/branching.md`**: Detect from `git branch -r` and `git log`. Primary integration branch(es), feature branch naming with real examples, merge strategy.

**Step J — Generate `workflows/commit-conventions.md`**: Detect from `git log --oneline -50`. Format pattern with 3–5 real examples from the log.

**Step K — Copy infrastructure files**: Invoke `find-context-template` for `$TEMPLATE_DIR`; copy `META.md` and `.gitignore` verbatim. At a monorepo root also copy `workflows/pull-requests.md` and fill its Repo Configuration table, per `initialize-repo` Step 3a. Do **not** copy a `retrospectives.md` — the template has never shipped one, and an aggregate node holds no retrospectives.

**Step L — Verify and commit**: Run `scripts/check-context-layout.sh <root>/.context` and fix what it reports — a node this skill just built should pass, so a finding is a bug in this run. Then flag any remaining content gaps as "needs attention" and commit with a message following repo conventions.

### Root Content Quality Standard

Root context is **cross-project and infrastructure-level**. Reference area paths rather than duplicating area content.

| Shallow (bad) | Thorough (good) |
|---|---|
| "Areas communicate via REST" | Table: which service calls which, shared client libraries, auth method |
| "Uses GitHub Actions" | Pipeline stages, triggers, deploy environments, manual gates |
| "Monorepo with multiple services" | An area map in `overview.md` with paths, descriptions and stacks, plus cross-area ADRs in `decisions/` |
