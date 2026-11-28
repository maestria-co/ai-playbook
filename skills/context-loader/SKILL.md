---
name: context-loader
description: >
  Teaches agents how to efficiently discover and read `.context/` files. Use this
  skill at the start of every task — any time you begin work on a feature, bug fix,
  refactoring, test writing, or architecture decision. Also use when resuming work
  after a context reset, switching between tasks, or whenever you're unsure which
  context files are relevant. If you're about to start coding without checking project
  context first, stop and use this skill.
---

# Skill: Context Loader

## Purpose

Efficiently load the right `.context/` files for the current task without reading
everything. Context windows are finite — loading irrelevant files wastes capacity
that should go to actual work.

This skill defines the loading order and selection strategy for different task types.

---

## Context Discovery Order

Always read in this order. Stop as soon as you have enough context for the task.

### Level 1 — Always Read (every task)

1. `CLAUDE.md` or `.github/copilot-instructions.md` — big picture, key commands
2. `.context/overview.md` — tech stack, architecture, current state

`overview.md` also tells you **what kind of node this is**, via its
`context_shape` key — `project` when absent. Read it before Level 2, because
it decides which of the files below exist at all:

| Shape | Level 2 and 3 files that exist |
|---|---|
| `project` | all of them |
| `aggregate` | `architecture.md`, `decisions/`, `domains/`, `workflows/` only |

An `aggregate` node — a monorepo root, a grouping directory, a workspace root
— holds no `standards.md`, `testing.md`, `retrospectives/` or `tasks/` by
design. Do not report those as gaps there, and do not go looking for a
project's conventions at a node that has no code. When you need them, they
are in the project node you are actually working in.

### Level 2 — Read Based on Task Type

| Task type              | Read these `.context/` files                                           |
| ---------------------- | ---------------------------------------------------------------------- |
| Feature implementation | `domains/` (relevant entity), `architecture.md`, `standards.md`        |
| Bug fix                | `domains/` (affected area), `testing.md`, `standards.md`               |
| Refactoring            | `architecture.md`, `standards.md`, `standards.md`                      |
| Test writing           | `testing.md`, `testing.md`, `standards.md`                             |
| Architecture decision  | `architecture.md`, `decisions/README.md`, all relevant `domains/` files |
| New domain work        | `domains/entities.md`, `domains/glossary.md`, `architecture.md`        |
| CI/CD changes          | `workflows/ci-cd.md`, `workflows/branching.md`                         |
| UI/styling work        | `styling.md` (if frontend project), `standards.md`                     |

### Level 3 — Read When Resuming

Project shape only — an aggregate node has neither of the first two.

1. `.context/retrospectives/` — last few entries for recent lessons
2. `.context/tasks/[TASK-ID]/plan.md` — if resuming a specific task
3. `git log --oneline -10` — recent commit history

---

## Reading Strategies

### Scan, Don't Read Everything

For large `.context/` directories:

1. List files first: `ls .context/domains/`
2. Read file headers (first 20 lines) to determine relevance
3. Read fully only the files that match your task

### Search Specifically

If you know what you're looking for:

- grep for entity names, pattern names, or error codes across `.context/`
- Don't read entire files hoping to stumble on relevant content

### Cache What You Found

After loading context, note the key facts in your working memory:

- Tech stack and version constraints
- Naming conventions for the area you're working in
- Relevant business rules or domain constraints
- Applicable ADRs

---

## Content-Aware Reading Strategies

Match your reading strategy to the file type. Loading entire files is often inefficient — use targeted queries instead.

### JSON and Structured Data

❌ **Inefficient:**
```bash
view package.json  # Loads entire file (1000+ lines)
```

✅ **Efficient:**
```bash
jq '.dependencies' package.json           # Query specific field
jq '.scripts | keys' package.json        # List available scripts
jq '.version, .name' package.json        # Extract multiple fields
```

**When to use:** Configuration files (package.json, tsconfig.json), API responses, data exports

---

### Code Files

❌ **Inefficient:**
```bash
view src/services/UserService.ts  # Loads entire file hoping to find relevant functions
```

✅ **Efficient:**
```bash
# Step 1: Find exports/functions first
grep -n "export\|function\|class" src/services/UserService.ts

# Step 2: Load only relevant sections
view src/services/UserService.ts --view_range [45, 75]  # Load only the function you need
```

**When to use:** Understanding existing code, finding implementation patterns, locating specific functions

---

### Log Files

❌ **Inefficient:**
```bash
view logs/app.log  # Loads entire log (10,000+ lines)
```

✅ **Efficient:**
```bash
# Step 1: Filter for problems first
grep -i "error\|warn\|fatal" logs/app.log | tail -20

# Step 2: If you need context around an error
grep -B 5 -A 5 "specific error message" logs/app.log
```

**When to use:** Debugging, error investigation, production incident analysis

---

### Documentation

❌ **Inefficient:**
```bash
view README.md  # Entire file when you only need setup instructions
```

✅ **Efficient:**
```bash
# Search for specific section
grep -A 10 "## Installation" README.md
grep -A 5 "## Quick Start" README.md

# Or load specific line range if you know the structure
view README.md --view_range [1, 30]  # Just the overview
```

**When to use:** Finding setup instructions, API documentation, specific sections of long docs

---

### Test Output

❌ **Inefficient:**
```bash
bash "npm test" --initial_wait 120  # Wait for all output, read everything
```

✅ **Efficient:**
```bash
# Step 1: Run tests, capture output
bash "npm test 2>&1 | tee /tmp/test-output.txt" --initial_wait 60

# Step 2: Filter for failures
grep -i "fail\|error" /tmp/test-output.txt

# Step 3: Only if failures exist, read relevant sections
grep -B 10 "FAILED" /tmp/test-output.txt
```

**When to use:** Test execution, CI/CD debugging, coverage analysis

---

### Decision Flow: Which Strategy to Use?

```
Is the file JSON/YAML/structured data?
  → Use jq/yq to query specific fields

Is the file source code?
  → grep for exports/functions first, then view_range

Is the file a log?
  → Filter for errors/warnings first with grep

Is the file documentation?
  → Search for section headers, load ranges

Is the file test output?
  → Capture to temp file, filter for failures
```

---

## When to Create New Context

During or after a task, create new `.context/` files when:

| Situation                              | Action                                                      |
| -------------------------------------- | ----------------------------------------------------------- |
| Working in an undocumented domain area | Create `domains/[area-name].md`                             |
| Discovering a non-obvious pattern      | Add to `architecture.md`                                    |
| Finding inconsistent error handling    | Document the correct pattern in `standards.md`              |
| Making an architecture decision        | Create `decisions/ADR-NNN-title.md` via `designing-systems` |
| Learning a lesson worth preserving     | Add entry to `retrospectives/`                              |

---

## Constraints

- Do not read all `.context/` files at the start of every task — be selective
- Do not spend more than 2 minutes on context loading — if you can't find what you need, proceed and note the gap
- Do not modify `.context/` files during loading — that's `context-maintenance`
- Prefer targeted searches over full-file reads for large context directories
