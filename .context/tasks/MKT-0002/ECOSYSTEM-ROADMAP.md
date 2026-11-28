# Ecosystem-Inspired Roadmap: Learning from Proven Tools

**Date:** 2026-07-01  
**Approach:** Research-driven adoption of proven patterns from Headroom AI, Graphify, and CyberStrike  
**Goal:** Make ai-playbook more efficient for daily use AND development

---

## Executive Summary

Instead of theorizing about optimization, let's **learn from tools that are already solving these problems in production:**

| Tool | Stars | Key Innovation | What We Can Adopt |
|------|-------|----------------|-------------------|
| **Headroom AI** | ~35 | 60-95% token reduction via smart compression | ContentRouter, CacheAligner, Session learning |
| **Graphify** | 75K+ | Knowledge graph > grep for code discovery | Graph-based context, Lazy-load patterns |
| **CyberStrike** | 1K+ | 7300+ skills with zero context pollution | Sidecar references, Lazy skill loading |

These tools prove that **massive efficiency gains are possible** — not through theory, but through battle-tested patterns.

---

## Part 1: Headroom AI Patterns

### What Headroom Does

**Core Value Prop:** Compresses everything an AI agent reads — tool outputs, logs, RAG chunks, files — before it reaches the LLM. **60-95% token reduction**, same accuracy.

**Key Innovations:**

1. **ContentRouter** - Detects content type (JSON/code/text), selects appropriate compressor
2. **SmartCrusher** - Compresses JSON intelligently (preserves structure)
3. **CodeCompressor** - AST-based code compression
4. **CacheAligner** - Stabilizes prompt prefixes for KV cache hits
5. **CCR (Reversible Compression)** - LLM can retrieve originals via tool if needed
6. **Output Token Reduction** - Trims verbose model responses (preambles, restated code)
7. **Cross-agent Memory** - Shared knowledge store, auto-dedup across sessions
8. **`headroom learn`** - Mines failed sessions, writes corrections to context

### What We Can Adopt for ai-playbook

#### 1. ContentRouter Pattern (Adopt)
**Concept:** Smart routing based on content type.

**Application to ai-playbook:**
- Skills can detect content type and provide optimized reading strategies
- JSON outputs → structural reading patterns
- Code files → AST/symbol-based discovery
- Logs → failure-focused filtering
- Docs → summary-first reading

**Implementation:**
```markdown
## Content-Aware Reading Strategy (in context-loader or implementing-features)

Before reading content, identify its type and use the appropriate strategy:

**JSON/Structured Data:**
- Use jq for targeted queries: `jq '.errors[] | select(.severity=="critical")'`
- Read structure first: `jq 'keys'` before diving into values
- Filter before reading: don't load 10MB JSON, query what you need

**Code Files:**
- Read exports/public API first (top 20 lines usually sufficient)
- Use grep to find specific functions before reading full file
- Use view_range for targeted sections

**Log Files:**
- Filter for errors/warnings: `grep -E "(ERROR|WARN|FATAL)" logfile`
- Use tail for recent entries, not full file
- Request log summaries from tools when possible

**Documentation:**
- Read headers/ToC first to understand structure
- Use grep to find relevant sections
- Load full doc only if entire context needed
```

**Effort:** 2-3 hours  
**Value:** HIGH - Teaches agents to think about content type first

---

#### 2. Cache-Aware Structure (Adapt)
**Concept:** Structure prompts so provider KV caches hit more often.

**Application to ai-playbook:**
- Agent files: static identity/role at top, dynamic state at bottom
- Skills: stable examples/patterns at top, task-specific guidance at bottom
- .context docs: immutable facts first, changelog/recent updates last

**Implementation:**
Update `agents/_shared/conventions.md` and skill templates:

```markdown
# Agent/Skill File Structure for Cache Efficiency

## ⚡ Cache-Friendly Structure

**Static Content (top 70% - likely cached by provider):**
1. Role & identity (never changes)
2. Core capabilities (rarely changes)
3. Standard workflows (stable)
4. Example patterns (stable)

**Dynamic Content (bottom 30% - expect cache miss):**
5. Current task context (changes per session)
6. Session-specific state (changes frequently)
7. Recent learnings (updated periodically)

**Why this matters:** 
Providers cache prompt prefixes. Keeping static content at the top
means cache hits even when dynamic state changes.
```

**Effort:** 3-4 hours (update conventions + document pattern)  
**Value:** MEDIUM - Low effort, potential upside if it helps

---

#### 3. Output Verbosity Control (Adopt)
**Concept:** Reduce what the model writes back (ceremonies, restated code, deep thinking on routine steps).

**Application to ai-playbook:**
Add verbosity guidance to agents and skills:

```markdown
## Output Efficiency Guidelines

**For routine operations** (reading files, running passing tests):
- Skip preambles ("Great, let me...", "I'll now...")
- Don't restate the task or previous context
- Provide only the essential observation or next action

**For complex operations** (debugging, architecture decisions):
- Provide reasoning (users want to understand your thinking)
- Show evidence for conclusions
- Explain non-obvious choices

**For error scenarios:**
- Always provide full context and reasoning
- Show stack traces, error messages verbatim
- Explain diagnosis process

**Code changes:**
- Don't echo back unchanged code
- For large files: show only the changed sections with context
- Use edit tool's targeted approach, not full-file rewrites
```

**Effort:** 2 hours  
**Value:** MEDIUM - Improves readability and token efficiency

---

#### 4. Session Learning (Adopt - High Value!)
**Concept:** `headroom learn` mines failed sessions and writes corrections to context.

**Application to ai-playbook:**
This is GOLD for continuous improvement!

**New Skill: `learning-from-failures.md`**

```markdown
# Learning from Failures Skill

## Intent
After a failed or difficult session, extract lessons and update project context
to prevent repeating the same mistakes.

## When to Use
- After debugging a tricky issue
- After discovering project conventions the hard way
- After repeated attempts at the same approach failed
- After user corrected an incorrect assumption

## Process

1. **Identify the Failure Pattern:**
   - What did the agent try that didn't work?
   - What assumption was wrong?
   - What context was missing?

2. **Extract the Lesson:**
   - What should the agent have known upfront?
   - What project-specific fact would have prevented this?
   - What pattern should be avoided?

3. **Choose the Right Location:**
   - Project-wide fact → `.context/overview.md`
   - Architecture pattern → `.context/decisions/NNNN-decision.md` (new ADR)
   - Code convention → `.context/rules/conventions.md`
   - Domain knowledge → `.context/domains/[domain].md`

4. **Write the Learning:**
   Use this format:
   
   ```markdown
   ## [Specific Topic] (Learned: 2026-07-01)
   
   **Context:** [What situation triggered this learning]
   
   **Lesson:** [Clear, actionable guidance]
   
   **Example:**
   [Code or command example showing the right way]
   
   **Anti-pattern:**
   [What NOT to do, if relevant]
   ```

5. **Update Context:**
   Add the learning to the appropriate file, then regenerate INDEX if using one.

## Examples

**Example 1: Database Connection Pattern**
```markdown
## Database Connections (Learned: 2026-07-01)

**Context:** Agents repeatedly tried connecting to `localhost:5432` but our
Postgres instance runs on `localhost:5433` (custom port to avoid conflicts).

**Lesson:** Always check `.env.example` for connection strings before assuming
standard ports.

**Example:**
\`\`\`bash
# Check connection details
grep DATABASE_URL .env.example
# Our instance: postgresql://localhost:5433/mydb
\`\`\`
```

**Example 2: Test Execution Pattern**
```markdown
## Running Tests (Learned: 2026-07-01)

**Context:** `npm test` runs all 2000+ tests (20 minutes). Agents ran full suite
on every small change, wasting time.

**Lesson:** Use targeted test commands for faster feedback.

**Example:**
\`\`\`bash
# Fast: run only affected tests
npm test -- --findRelatedTests src/auth/login.ts

# Fast: run specific test file
npm test src/auth/__tests__/login.test.ts

# Slow: full suite (only for final validation)
npm test
\`\`\`
```

## Agent Instructions

When you encounter a failure pattern:
1. Complete the immediate task first
2. Note the learning for retrospective
3. In task retrospective, invoke this skill to persist the lesson
4. Future agents will benefit from your learning

## Maintenance

Run this after:
- `task-retrospective` identifies repeated mistakes
- `systematic-debugging` reveals missing project knowledge
- User says "you should have known..." or "last time you tried..."
```

**Effort:** 3-4 hours (skill creation + integration with task-retrospective)  
**Value:** VERY HIGH - Continuous improvement mechanism

---

## Part 2: Graphify Patterns

### What Graphify Does

**Core Value Prop:** Turn any folder of code/docs/schemas into a **queryable knowledge graph**. Agents query relationships instead of grepping files.

**Key Features:**
- Multi-source graph: code + SQL schemas + docs + PDFs + images + videos
- Query-based discovery: "Show me all auth handlers"
- Interactive HTML visualization
- Export Mermaid callflow diagrams
- Skill-based integration for AI assistants

**Example output:**
```
graphify-out/
├── graph.html        # Interactive visualization
├── GRAPH_REPORT.md   # Key concepts, connections, suggested questions
└── graph.json        # Full queryable graph
```

### What We Can Adopt for ai-playbook

#### 1. Graph-Based Context Discovery (Adapt)
**Concept:** Relationship-based discovery > linear file scanning.

**Application to ai-playbook:**
We don't need full AST graphing (that's language-specific and complex), but we can adopt the **discovery pattern**:

**New Skill: `context-graph.md`**

```markdown
# Context Graph Skill

## Intent
Generate a lightweight relationship map of project context to enable
query-based discovery instead of linear scanning.

## What Gets Graphed

### .context/ Documentation
- Decisions → tags, related decisions, impacted domains
- Rules → applies to (frontend/backend/testing), related rules
- Retrospectives → task, lessons learned, resulted in (decisions/rules)
- Domains → components, dependencies, related domains

### Codebase (Optional - Only if Needed)
- Modules → exports, imports, depends on
- Key classes/functions → used by, calls, implements

## Output Format

`.context/GRAPH.json` (machine-readable) + `.context/GRAPH.md` (human-readable)

**Example GRAPH.md:**
```markdown
# Project Context Graph

## Decisions → Domains

0001-auth-flow → Affects: [auth, mobile, api]
  ├─ Introduces: JWT session tracking
  ├─ Related to: 0003-token-refresh
  └─ Impacts: auth domain, mobile domain

0002-cache-strategy → Affects: [performance, backend]
  ├─ Introduces: Redis prefix matching
  └─ Impacts: all API endpoints

## Domains → Components

auth → [auth-service, login-handler, token-validator]
  ├─ Depends on: database, redis
  └─ Used by: api, mobile

## Recent Learnings → Rules

MKT-0006-retrospective → Created: [rules/git-hooks-standards.md]
  └─ Lesson: Always test hooks in CI before deploying
```

## Query Patterns

Once graph exists, agents can query:
- "What decisions affect the auth domain?"
- "What components depend on Redis?"
- "What retrospectives led to new rules?"
- "Show me the authentication flow from login to token validation"

## Implementation

**Option A: Lightweight Bash Script (Recommended)**
```bash
#!/bin/bash
# scripts/generate-context-graph.sh

# Parse .context/ markdown files for relationships
# Extract: tags, "Related:", "Affects:", "Depends on:" patterns
# Generate JSON + Markdown output
```

**Option B: Manual Maintenance**
- Maintain GRAPH.md by hand during context-maintenance
- Update when adding new decisions/rules/domains
- Keep it simple - focus on major relationships

## When to Use
- During initialize-repo (generate initial graph)
- After context-maintenance (regenerate)
- During context-loader (read graph to find relevant docs)
```

**Effort:** 5-6 hours (script + skill)  
**Value:** MEDIUM-HIGH - Solves discovery problem for mature projects

---

#### 2. Visual Architecture Exports (Adopt - Low Effort)
**Concept:** Export Mermaid diagrams from context for better understanding.

**Application to ai-playbook:**
Add export capability to architecture decisions:

**Enhancement to `designing-systems.md`:**

```markdown
## Architecture Decision Record with Diagrams

When creating an ADR, consider adding a Mermaid diagram for:
- System components and their relationships
- Data flow diagrams
- Sequence diagrams for key interactions
- Decision trees showing options evaluated

**Example:**
```markdown
# ADR 0001: JWT Session Tracking

## Decision
Use JWT tokens for mobile client authentication instead of server-side sessions.

## Architecture

\`\`\`mermaid
sequenceDiagram
    participant Mobile
    participant API
    participant Redis
    
    Mobile->>API: POST /login (credentials)
    API->>Redis: Validate user
    Redis-->>API: User valid
    API->>API: Generate JWT
    API-->>Mobile: JWT token
    Mobile->>API: GET /profile (JWT in header)
    API->>API: Validate JWT
    API-->>Mobile: Profile data
\`\`\`

## Components Affected

\`\`\`mermaid
graph LR
    Auth[Auth Service] --> JWT[JWT Validator]
    Auth --> Redis[(Redis)]
    Mobile[Mobile App] --> Auth
    API[API Gateway] --> JWT
\`\`\`
```

**Export Command:**
```bash
# Generate HTML with all ADR diagrams
scripts/export-architecture-diagrams.sh

# Output: .context/architecture.html (with interactive Mermaid)
```
```

**Effort:** 2-3 hours (update skill + simple export script)  
**Value:** MEDIUM - Better architecture documentation

---

## Part 3: CyberStrike Lazy-Loading Patterns

### What CyberStrike Does

**Core Innovation:** 7300+ specialized skills with **zero context pollution** via lazy loading.

**How they do it:**
1. **Skill Index** - Lightweight metadata (name, tags, one-line description)
2. **Sidecar References** - Detailed skill content in `references/` folder, loaded only when invoked
3. **Domain Intelligence Layer** - Inject domain knowledge just-in-time
4. **Lazy Discovery** - Agent searches index, loads details only for relevant skills

**Example structure:**
```
skills/
├── index.json                    # Lightweight: 7300 skills, ~500KB
└── skills/
    ├── web-app-testing/
    │   ├── SKILL.md              # Concise (when to use, what it does)
    │   └── references/           # Detailed content (examples, edge cases)
    │       ├── owasp-wstg.md
    │       ├── common-vulns.md
    │       └── test-procedures.md
```

### What We Can Adopt for ai-playbook

#### 1. Sidecar References Pattern (Adopt - High Value!)
**Concept:** Keep SKILL.md concise, move detailed content to `references/` folder.

**Current Problem:**
Some skills are getting long (700+ lines) with examples, edge cases, troubleshooting guides. This pollutes agent context when they read skills.

**Solution:**
Split skills into:
- `SKILL.md` - Core guidance (when to use, workflow, decision tree) — 100-200 lines
- `references/` - Detailed content loaded on-demand

**Example refactor for `implementing-features`:**

**BEFORE (700 lines):**
```
skills/implementing-features/
└── SKILL.md  # Contains everything: patterns, examples, edge cases, troubleshooting
```

**AFTER (lean):**
```
skills/implementing-features/
├── SKILL.md                    # 150 lines - core workflow only
└── references/
    ├── code-patterns.md        # Common implementation patterns
    ├── testing-integration.md  # How to integrate with writing-tests
    ├── edge-cases.md           # Handling unusual scenarios
    └── troubleshooting.md      # Common issues and solutions
```

**SKILL.md becomes:**
```markdown
# Implementing Features Skill

## Intent
Implements a feature, bug fix, or refactor from a clear specification.

## When to Use
- Task has clear acceptance criteria
- Spec is unambiguous
- No architecture decisions needed

## Core Workflow

1. **Understand the Spec:**
   - Read acceptance criteria
   - Identify affected files
   - Check related decisions in .context/

2. **Plan the Implementation:**
   - Which files need changes?
   - What tests are needed?
   - Any dependencies on other tasks?

3. **Implement:**
   - Make targeted changes (see references/code-patterns.md for examples)
   - Follow project conventions (.context/rules/)
   - Write tests alongside code (references/testing-integration.md)

4. **Verify:**
   - Run tests
   - Check acceptance criteria
   - See `verification-checklist` skill

## When You Need More Detail

- **Code patterns:** `references/code-patterns.md`
- **Testing approach:** `references/testing-integration.md`
- **Edge cases:** `references/edge-cases.md`
- **Common issues:** `references/troubleshooting.md`

**Agent note:** Read references/ files only when you encounter the specific scenario.
Don't pre-load all references "just in case."
```

**Migration Plan:**
1. Start with longest skills: `implementing-features`, `writing-tests`, `systematic-debugging`
2. Refactor 3-5 skills as proof-of-concept
3. Measure: do agents still work correctly with leaner skills?
4. If successful, apply pattern to remaining skills

**Effort:** 8-10 hours (refactor 5 skills)  
**Value:** HIGH - Reduces context pollution, keeps skills maintainable

---

#### 2. Lazy Skill Loading Guidance (Adopt)
**Concept:** Teach agents to load skill details only when needed.

**New guidance in `using-skills.md`:**

```markdown
## Efficient Skill Usage

**Discovery Phase:**
1. Read GUIDE.md to identify which skill matches your task
2. Read SKILL.md for that skill (concise, ~150 lines)
3. Start working

**Deep Dive (Only if Needed):**
4. If you encounter an edge case → read `references/edge-cases.md`
5. If implementation pattern unclear → read `references/code-patterns.md`
6. If something fails → read `references/troubleshooting.md`

**Don't:**
- ❌ Read all reference files upfront "just in case"
- ❌ Read multiple full skills when you only need one
- ❌ Re-read skills you've already used in this session

**Do:**
- ✅ Read skills on-demand as you need them
- ✅ Load reference files only when you hit that specific scenario
- ✅ Trust your memory - if you've read a skill this session, you know it
```

**Effort:** 1 hour (add guidance)  
**Value:** MEDIUM - Teaches better habits

---

## Integrated Roadmap: Ecosystem-Inspired Improvements

### Phase 1: Quick Wins (Week 1) — 15-20 hours

**Adopted from Headroom:**
- [ ] Content-Aware Reading Strategies (context-loader, implementing-features) — 2-3h
- [ ] Output Verbosity Control guidance (agents, skills) — 2h
- [ ] Cache-Aware Structure documentation (conventions.md) — 3-4h

**Adopted from CyberStrike:**
- [ ] Lazy Skill Loading guidance (using-skills) — 1h
- [ ] Sidecar References POC (refactor 2-3 skills) — 5-6h

**Original (from previous evaluation):**
- [ ] Lean Task Tracking templates (task-plan) — 2h

**Deliverables:**
- Updated skills with content-aware reading
- Refactored 2-3 skills with sidecar references
- Documentation on cache-friendly structure
- Lazy-loading guidance

---

### Phase 2: Discovery & Learning (Week 2) — 12-15 hours

**Adopted from Headroom:**
- [ ] Session Learning skill (learning-from-failures) — 3-4h
- [ ] Integration with task-retrospective — 2h

**Adopted from Graphify:**
- [ ] Context Graph skill + bash script — 5-6h
- [ ] Integration with context-loader — 2h

**Deliverables:**
- `learning-from-failures` skill operational
- `.context/GRAPH.md` generation working
- Context-loader uses graph for discovery

---

### Phase 3: Sidecar Migration (Week 3) — 8-10 hours

**Adopted from CyberStrike:**
- [ ] Refactor remaining long skills (5+ more) — 6-8h
- [ ] Update GUIDE.md to explain sidecar pattern — 1h
- [ ] Test: do agents still work correctly? — 1h

**Deliverables:**
- 8-10 skills refactored with references/
- Pattern documented
- Validation complete

---

### Phase 4: Validation & Measurement (Week 4) — 5-8 hours

- [ ] Use improved ai-playbook on 10 real tasks
- [ ] Measure: token usage (if possible), task completion time, user satisfaction
- [ ] Gather feedback: do improvements feel natural or forced?
- [ ] Document findings

**Deliverables:**
- Validation report
- Decision: keep/adjust/rollback changes
- Lessons learned document

---

## Why This Approach is Better

### Compared to Original Roadmap:

| Aspect | Original Roadmap | Ecosystem-Inspired |
|--------|------------------|-------------------|
| **Validation** | Theoretical | Proven in production (75K+ stars for Graphify) |
| **Scope** | 3-4 months | 3-4 weeks |
| **Risk** | High (unproven ideas) | Low (copying proven patterns) |
| **Maintenance** | High (custom tools) | Low (mostly guidance + simple scripts) |
| **Portability** | Medium (Python deps) | High (mostly markdown + bash) |

### What We're Learning From:

1. **Headroom (35 stars, active development):** 
   - ContentRouter teaches us to think about content type first
   - Session learning shows how to continuously improve
   - Output control reduces verbosity

2. **Graphify (75K stars, YC-backed):**
   - Graph-based discovery > linear scanning
   - Multi-source context (not just code)
   - Export visualizations for better understanding

3. **CyberStrike (1K stars, 7300+ skills):**
   - Sidecar pattern keeps skills concise
   - Lazy loading prevents context pollution
   - Domain intelligence layer (just-in-time knowledge injection)

---

## Next Steps

1. **Review this roadmap** - Does this feel more grounded?

2. **Prioritize phases** - Which phase has highest value for your daily work?

3. **Pick a starting point** - Which patterns should we implement first?

4. **Validate incrementally** - After each phase, measure impact before continuing

**Questions for you:**

1. **Which tool's patterns resonate most** with your daily pain points?
   - Headroom (token efficiency, session learning)
   - Graphify (context discovery)
   - CyberStrike (skill organization)

2. **What would make the biggest difference** in your daily use right now?

3. **Should we start with Phase 1** (quick wins) or jump to a specific pattern that solves a current pain point?

I'm ready to implement whichever direction you choose!
