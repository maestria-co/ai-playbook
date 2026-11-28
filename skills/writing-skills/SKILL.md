---
name: writing-skills
description: Use when creating a new skill, editing an existing skill, or helping a user author a skill for this system. Covers structure, discoverability, quality, and discipline hardening.
user-invocable: true
---

# Writing Skills

## Overview

**Skill authorship mirrors test-driven development for process artifacts.** Spot failure modes (agent missteps absent guidance), craft skills targeting those precise failures, then confirm agent conformance.

**Foundation:** Without observing agent failure absent the skill, required skill content remains unknown.

## When to Create a Skill

**Create when:**
- Technique proved counterintuitive — initial attempts failed
- Cross-project consultation anticipated
- Pattern exhibits broad applicability (transcends single project)
- Collective benefit from codified workflow

**Defer creation for:**
- Isolated solutions to singular problems
- Standard methodologies thoroughly documented externally
- Project-confined conventions (archive in `.context/standards/`)
- Mechanically-enforceable constraints via linting/validation — automate those, preserve skills for judgment-requiring scenarios

## Skill Types

| Type | Characterization | Instances |
|----------|------------------|-----------|
| **Technique** | Structured methodology with explicit steps | `systematic-debugging`, `initialize-repo` |
| **Discipline** | Constraints preventing documented failure modes | `testing-discipline`, `verification-checklist` |
| **Process** | Workflow embedding decision junctures | `task-retrospective`, `design-first` |
| **Format** | Schema templates with organizational guidance | `jira-story`, `asana-story` |

## Directory Structure

```
skills/
  skill-name/
    SKILL.md              # Core reference (required)
    references/           # Extracted supporting content, named for what it holds
      code-patterns.md
```

**Inline preservation:** Principles, concepts, code snippets under 50 lines, examples.
**File extraction:** Heavyweight reference (100+ lines), reusable scripts/templates.

Extracted files go in `references/`. Name each for its content — there is no
fixed file set:

| Skill | `references/` |
| --- | --- |
| `implementing-features` | `code-patterns.md` |
| `writing-tests` | `code-patterns.md`, `edge-cases.md`, `troubleshooting.md` |
| `agent-file-review` | `output-template.md` |
| `applying-design-principles` | `principles-and-laws.md`, `sources-and-reading.md` |

## SKILL.md Structure

### Frontmatter (YAML)

```yaml
---
name: skill-name-with-hyphens
description: Use when [exact triggering circumstances and indicators]
---
```

- **`name`**: Letters, numerals, hyphens exclusively. Verb-initial gerunds excel (`writing-skills`, `executing-plans`).
- **`description`**: Third-person voice. Opens with "Use when..." Captures EXCLUSIVELY triggering circumstances — NEVER skill accomplishments or workflow.

**Rationale for excluding workflow from descriptions:** Descriptions articulating "dispatches subagent per task with code review between tasks" risk agents executing that synopsis rather than reading complete skill. Workflow-encapsulating descriptions generate shortcuts circumventing genuine process. Articulate the PROBLEM or TRIGGER, never the SOLUTION.

```yaml
# ❌ BAD: Workflow encapsulation — agent might execute this bypassing skill reading
description: Use for TDD - write test first, watch it fail, write minimal code, refactor

# ✅ GOOD: Triggering circumstances exclusively — agent must read skill for workflow
description: Use when writing tests, reviewing test quality, or deciding what to mock
```

### Content Structure

```markdown
# Skill Name

## Overview
Foundational principle in 1-2 sentences. What is this and why does it matter?

## When to Use
Bulleted enumeration of indicators and scenarios.
When NOT to use.

## The Process (or Core Pattern)
Actual technique, steps, or constraints.
Before/after juxtapositions for techniques.

## Common Mistakes
What fails and remediation approach.

## Rationalization Prevention (for discipline skills)
Matrix of agent excuses and counterarguments.
```

Not every skill demands every section. Calibrate to complexity — elementary technique skills might occupy 40 lines; discipline skills might occupy 150.

**Step and Phase heading conventions** — When skills articulate numbered workflows, prefix every step or phase heading with skill identifier:

```markdown
## skill-name: Step 1: Accomplish Something  ← appropriate
## skill-name: Phase 2: Confirm              ← appropriate
## Step 1: Accomplish Something              ← inappropriate — agent cannot identify owning skill
```

When skills incorporate nested workflows (stages encapsulating steps), embed both stage and step identifiers in every heading:

```markdown
## skill-name: Stage 1: Preparation
### skill-name: Stage 1: Step 1: Accomplish X ← appropriate — complete path maintained
### skill-name: Stage 1: Step 2: Accomplish Y ← appropriate
## skill-name: Stage 2: Implementation
### skill-name: Stage 2: Step 1: Accomplish Z ← appropriate

### Stage 1: Step 1: Accomplish X             ← inappropriate — skill identifier absent
### skill-name: Step 1: Accomplish X          ← inappropriate — stage ambiguous
```

Complete path (`skill-name: Stage N: Step N`) guarantees agents encountering isolated headings can always ascertain which skill, which stage, and which step — without backward scrolling for context.

## Discovery Enhancement

Prospective agents locate your skill via description matching. Enhance for discovery:

**1. Description field richness** — Embed indicators, error signatures, and triggering contexts.

**2. Keyword density** — Deploy words agents pursue: error messages, indicators ("flaky", "timeout", "race condition"), tool identifiers, synonyms.

**3. Naming clarity** — Verb-initial, active construction:
- ✅ `commit-discipline` not `git-commit-guidelines`
- ✅ `design-first` not `pre-implementation-review`
- ✅ `context-maintenance` not `context-directory-updates`

**4. Registration protocol** — Post-creation, append to routing matrix in `skills/GUIDE.md` and skill catalog in `README.md`. For multi-skill sequence contributors, append to common workflow matrix in `skills/using-skills/SKILL.md`.

## Token Economics

Skills activate on-demand into context. Every word imposes token expense.

**Targets:**
- Frequently-activated skills: target < 200 words
- Standard skills: target < 500 words
- Sophisticated discipline skills: permissible excess, but validate every line

**Optimization techniques:**
- Cross-reference companion skills rather than content duplication
- Single exemplary example dominates multiple mediocre ones
- Compress examples — exhibit the pattern, not the narrative
- Purge redundancy — bypass explaining the self-evident

## Discipline Skill Authorship

Discipline skills (constraints preventing failure modes) require supplementary hardening because agents rationalize away constraints under duress.

### 1. Loophole Elimination

Articulate the constraint and prohibit particular workarounds:

```markdown
# ❌ Bad
Write code before test? Delete it.

# ✅ Fortified
Write code before test? Delete it. Restart.
**Zero exceptions:**
- Don't preserve it as "reference"
- Don't "modify" it while executing tests
- Delete means delete
```

### 2. Rationalization Matrix Construction

Capture agent justifications and refute each:

```markdown
| Red Flag | Action |
|----------|--------|
| "Too elementary to test" | Elementary code fails. Testing requires 30 seconds. |
| "I already tested it works" | Show the proof. |
| "I'll test next" | Next-tests prove nothing regarding intent. |
```

### 3. Red Flag Establishment

Self-audit catalog for detecting imminent constraint violations:

```markdown
## Red Flags — HALT
- "This differs because..."
- "I'll return to this next"
- "It concerns the spirit, not the letter"
All these indicate: execute the workflow.
```

## Code Specimens in Skills

**Single exemplary specimen dominates multiple mediocre ones.** Choose the most germane language for the technique. Bypass implementing in 5 languages.

**Quality specimens exhibit:**
- Completeness and executability
- Commentary explaining WHY (not what)
- Realistic scenario basis
- Adaptation readiness

**Bypass:**
- Template skeletons
- Artificial specimens misaligning with authentic usage
- Multi-language dispersion

## Quality Validation Catalog

Before declaring skill complete:

- [ ] Name employs exclusively letters, numerals, hyphens
- [ ] Description opens with "Use when..." and embeds specific triggers
- [ ] Description EXCLUDES workflow encapsulation
- [ ] Overview articulates foundational principle in 1-2 sentences
- [ ] Content targets specific failure modes (not hypothetical ones)
- [ ] Discipline skills embed rationalization prevention
- [ ] Examples exhibit concreteness, not abstraction
- [ ] Token-efficient — every line validates its inclusion
- [ ] Appended to `skills/GUIDE.md` routing matrix
- [ ] Appended to `README.md` skill catalog
- [ ] Appended to `using-skills` common workflow matrix when skill contributes to multi-skill sequences

## Antipatterns

| Antipattern | Avoidance Rationale |
|-------------|---------------------|
| **Narrative exposition** ("In session X, we discovered...") | Excessive specificity, non-reusable. Articulate the technique. |
| **Multi-language specimens** | Mediocre quality, maintenance burden. Single exemplary specimen. |
| **Abstract labels** (step1, helper2) | Labels should convey semantic content. |
| **Duplicating companion skill content** | Cross-reference instead. Preserve tokens. |
| **"Obviously clear" without testing** | Clear to you ≠ clear to agents. Test. |
