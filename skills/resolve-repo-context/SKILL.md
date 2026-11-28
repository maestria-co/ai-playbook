---
name: resolve-repo-context
description: Use when a manager agent needs to determine the correct context root for a task and the repo type is not a plain project — workspaces, monorepos, and multi-module repos all require this resolution before delegating to sub-agents.
user-invocable: false
---

# Resolve Repo Context

## Overview

**This skill maps a task description to the correct sub-project root, context path, and skills directory before any implementation work begins.** It detects repository topology from filesystem signals, matches the task to the right sub-project, and returns a structured result.

Run this skill as an isolated **explore sub-agent** — never inline in the manager's main context.

## When to Use

- Manager has identified the repo as a `monorepo`, `workspace`, or `multi-module` layout
- Manager needs to know which `.context/`, `copilot-instructions.md`, and project root govern the task

---

## Inputs

Passed via prompt from the manager:

| Field | Required | Description |
|-------|----------|-------------|
| `cwd` | Yes | Absolute path where the manager agent is running |
| `task_description` | Yes | Natural language description of the task |

---

## resolve-repo-context: Step 1: Detect Repo Type

Inspect the filesystem at `cwd` to determine `repo_type`:

| Signal | Repo type |
|--------|-----------|
| `nx.json`, `turbo.json`, `go.work` present | `monorepo` |
| `*.code-workspace` file present | `workspace` |
| `package.json` with `"workspaces"` field | `monorepo` |
| Root `pom.xml` with `<modules>` and no `src/` | `multi-module` |
| Any single build manifest (`package.json`, `go.mod`, `*.csproj`, etc.) | `project` |
| No manifest found | `project` (fallback) |

If `repo_type` is `project`: return immediately with `root = cwd`. This skill is unnecessary for plain project repos.

## resolve-repo-context: Step 2: Discover Sub-Projects

For `monorepo`, `workspace`, or `multi-module` repos, scan for sub-projects:

- Parse workspace configuration files (`*.code-workspace`, root `package.json#workspaces`, `nx.json`)
- Find build manifests (`package.json`, `go.mod`, `Cargo.toml`, `*.csproj`, `pom.xml`) in immediate subdirectories
- Collect each sub-project: `{ name, root }` — `name` from the manifest's name field or directory name

## resolve-repo-context: Step 3: Match Task to Sub-Project

Match the task description to a sub-project using these signals in priority order. Stop at the first confident match.

**Priority 1 — Explicit path or file reference in task description**
- If the task mentions a file path or directory name that maps unambiguously to one sub-project: use it
- Ambiguous or absent → fall through to Priority 2

**Priority 2 — Domain or module keyword in task description**
- Scan for sub-project names, package names, or domain keywords in the task text
- Validate the candidate against the topology before accepting

**Priority 3 — Filesystem fallback**
- If Priorities 1 and 2 are inconclusive, inspect the full topology
- If the task plausibly touches multiple sub-projects: set `scope: cross-project` and resolve root to git root or lowest common ancestor

## resolve-repo-context: Step 4: Return Structured Result

Return exactly this schema:

```json
{
  "repo_type": "monorepo | workspace | multi-module | project",
  "resolved_context": {
    "scope": "sub-project | repo-root | cross-project",
    "root": "/absolute/path",
    "git_root": "/absolute/path",
    "instructions": "/absolute/path/.github/copilot-instructions.md",
    "context": "/absolute/path/.context/",
    "context_shape": "project | aggregate",
    "rationale": "human-readable explanation of why this root was chosen"
  },
  "available_skills": [
    {
      "name": "skill-name",
      "description": "...",
      "path": "/absolute/path/SKILL.md",
      "user-invocable": true
    }
  ],
  "projects": [
    {
      "name": "sub-project-name",
      "root": "/absolute/path",
      "is_resolved_context": true
    }
  ]
}
```

**`instructions`**: path to the canonical instructions file — use `.claude/claude.md` if present, otherwise `.github/copilot-instructions.md`.

**`available_skills`**: populated from the resolved context's skill directory. Return `[]` if no skill directory exists at the resolved root.

**`context_shape`**: read `context_shape` from `<context>/overview.md`.
Report `project` when the key is absent — that is the documented default, not
a guess. Do not infer the shape from which files happen to be present: a
project node that has not written `standards.md` yet would read as
`aggregate` and its consumers would stop expecting the file.

Callers need this because the two shapes hold different things. An agent told
to read `standards.md` at an aggregate node is being pointed at a file that is
absent *by design*, and without the shape it cannot tell that from a genuine
documentation gap it should report.

**`projects`**: list all discovered sub-projects. Set `is_resolved_context: true` on the matched project. For `cross-project` scope, mark all touched projects as `true`.

**All paths must be absolute.**

---

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| `repo_type: project` detected in Step 1 | Return immediately with `root = cwd`, `scope: sub-project`, `available_skills: []` |
| Task spans multiple sub-projects | `scope: cross-project`; root = git root or common ancestor; mark all touched projects |
| No `.context/` in resolved sub-project | Return `available_skills: []`; root and path fields still resolve normally |
| Sub-project names conflict (two projects share a keyword) | Fall through to Priority 3; document ambiguity in `rationale` |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Running inline in the manager's context | Always dispatch as an isolated explore sub-agent |
| Returning relative paths | Every path in the return schema must be absolute |
| Invoking this skill for plain project repos | Check repo type first (Step 1); project repos return immediately |
| Accepting an ambiguous keyword match as confident | Priority 2 only applies to confident matches; ambiguity falls through to Priority 3 |
