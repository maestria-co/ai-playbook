---
name: initialize-workspace
description: >
  Bootstrap agent context for every project in a VS Code multi-root workspace. Use when
  setting up the agent system across a multi-project workspace, when someone says "initialize
  all projects in this workspace", "set up agent context for all our repos", or "I have a
  .code-workspace file and need to get all projects bootstrapped". Runs initialize-repo (or
  upgrade-repo) per project and generates workspace-level cross-project context.
user-invocable: true
---

# Skill: Initialize Workspace

## Purpose

Run initialize-repo (or upgrade-repo if .context/ exists) across all projects in
a VS Code multi-root workspace, then generate workspace-level cross-project context.
This skill enables the agent system to understand multi-project relationships, shared
dependencies, and cross-project workflows.

---

## Phase 1: Locate Workspace File

Find the `.code-workspace` file (search current dir and one level up) and parse
its `folders` array to get project paths.

For each folder, classify as:

- **Project** — has source code (`src/`, `lib/`, `package.json`, etc.) → initialize context
- **Resource** — docs, config, or shared assets only → document in overview, skip init
- **Submodule** — git submodule → initialize independently

---

## Phase 2: Branch Guard

For each git repository, if the current branch is `main`, `master`, `production`,
or `release/*`, create a `context-bootstrap-[date]` branch before making any changes.
Never commit context files directly to protected branches.

---

## Phase 3: Initialize Each Project

For each classified project folder:

```
Has .context/?
  No  → Apply initialize-repo skill
  Yes → Apply upgrade-repo skill (update context, not code)
```

Each project must be initialized in isolation — don't let one project's context
influence another's. Each gets its own `.context/overview.md`, `.context/standards.md`, `.context/architecture.md`, etc.

---

## Phase 4: Generate Workspace Overview

Create `.context/overview.md` at the **workspace root** (not inside any
project folder). This is the workspace-level entry point for cross-project
tasks.

The name is `overview.md`, same as every other node — the path already says
which node it is, so a `workspace-` prefix earns nothing and costs a lot. A
second overview filename means Check 1 in `initialize-repo` looks for
`.context/overview.md`, finds nothing at an already-initialized workspace
root, and reports "proceed". That is exactly the bug this convention exists to
prevent, one level up. `initialize-monorepo` and `context-specialist-impl`
both already use `overview.md` for a root node.

A workspace root is an **aggregate** node — it describes a set of
repositories and holds no code — so it declares the shape and takes the
reduced layout: no `standards.md`, `testing.md`, `retrospectives/` or
`tasks/`, all of which belong to the repositories themselves.

It is also not a git repository, so it needs no `workflows/pull-requests.md`.
The checker tests for a `.git` beside `.context/` rather than asking, which
means each project in the workspace is still required to document its own PR
format and the workspace root is not.

```markdown
---
context_shape: aggregate
---

# Workspace Overview

**Workspace:** [workspace-name]
**Generated:** [date]

## Projects

| Name        | Tech Stack        | Purpose       | Entry Point     |
| ----------- | ----------------- | ------------- | --------------- |
| [project-1] | [Node.js, React]  | [Frontend]    | `src/index.tsx` |
| [project-2] | [Python, FastAPI] | [Backend API] | `app/main.py`   |

## Cross-Project Dependencies

### [project-1] → [project-2]

- **Type:** API contract
- **Interface:** REST HTTP
- **Files:** `frontend/src/api/` → `backend/app/routes/`

## Shared Resources

- [ESLint config, Docker Compose, shared type library, etc.]

## Development Workflow

[How to start all services, run tests across projects, build order]

## Agent Entry Point

For tasks spanning multiple projects, use the **Manager** agent — it will coordinate
across projects as needed.

## Maintenance

Update this file when projects are added, dependencies change, or workflows change.
```

---

## Phase 5: Document Cross-Project Relationships

Discover relationships by scanning imports, API calls, and shared configs:

| Type             | Description                              |
| ---------------- | ---------------------------------------- |
| Shared Library   | One project imports code from another    |
| API Contract     | Projects communicate via HTTP/RPC        |
| Event Bus        | Projects communicate via message queue   |
| Shared Config    | Common ESLint, TypeScript, Docker config |
| Build Dependency | One project must build before another    |

For each discovered relationship, document: type, direction, interface, and specific files.

---

## Checklist

**Pre-init:**

- [ ] Workspace file found and parsed
- [ ] Each folder classified (project vs. resource)

**Per project:**

- [ ] Branch guard applied if on protected branch
- [ ] `.context/` initialized or upgraded
- [ ] No cross-contamination between projects

**Workspace-level:**

- [ ] `overview.md` created at workspace root
- [ ] All projects listed with tech stacks
- [ ] Cross-project dependencies documented

---

## Output Summary

```markdown
# Workspace Initialization Complete

## Workspace: [workspace-name]

| Project     | Status                       | Branch                   |
| ----------- | ---------------------------- | ------------------------ |
| [project-1] | ✅ Initialized               | context-bootstrap-[date] |
| [project-2] | ✅ Upgraded                  | context-bootstrap-[date] |
| [docs]      | ⏭️ Skipped (resource folder) | —                        |

**Workspace overview:** `.context/overview.md`

**Next steps:**

1. Review and commit context changes in each project
2. Use the **Manager** agent for cross-project tasks```

---

## Constraints

- Each project initialized independently — no cross-pollination of context
- Workspace overview lives at workspace root, not inside any project
- Never commit directly to main/master — always use a branch
- Only document relationships that can be verified in actual code
- Skip resource folders (docs, assets) — only source projects get `.context/`
