# Task Retrospective: MKT-0004 Output Verbosity Control

**Date:** 2026-07-10  
**Task ID:** MKT-0004  
**Type:** Documentation Enhancement  
**Duration:** Single session (~20 minutes)  
**Branch:** feature/MKT-0004-output-verbosity  

---

## What We Built

Added output efficiency guidelines to three agent definitions to distinguish routine (concise) from complex/error (verbose) output:

1. **agents/manager.agent.md** (+52 lines)
   - New "Output Efficiency Guidelines" section before Anti-Rationalization
   - 3 subsections: Routine Operations, Complex Operations, Error Scenarios
   - Each with When/Do/Don't guidance and realistic examples

2. **agents/coder.agent.md** (+60 lines)
   - New "Code Output Efficiency" section before Constraints
   - 2 subsections: Routine Code Changes, Complex Code Changes
   - Each with When/Do/Don't guidance and code output examples

3. **agents/tester.agent.md** (+59 lines)
   - New "Test Output" section before Constraints
   - 2 subsections: Passing Tests, Failing Tests
   - Passing: concise summary; Failing: full output with traces

**Artifacts:**
- 3 agent files updated (+171 lines)
- 2 commits on feature branch
- 1 retrospective document

---

## What Worked Well

### ✅ Consistent When/Do/Don't Pattern
Used the same structure across all three agents: When (trigger), Do (required behaviors), Don't (antipatterns), followed by example. Creates muscle memory — agents see the pattern once and recognize it everywhere.

**Evidence:** All 3 agents use identical section structure. Manager has 3 When/Do/Don't blocks, coder has 2, tester has 2.

### ✅ Coherent Cross-Agent Examples
All examples use the same JWT/auth domain (checking token expiration, validating signatures). Reading across agents feels like a unified scenario, not disconnected fragments.

**Evidence:** Manager example shows delegation to auth module, coder example shows JWT validation code, tester example shows auth test failures — all reference the same domain.

### ✅ Error Scenario Exception Clause
Error Scenarios guidance includes explicit "regardless of other guidelines" note. Makes it clear that error handling overrides all conciseness rules.

**Evidence:** manager.agent.md line says "Always provide full context, stack traces, and step-by-step diagnosis regardless of other guidelines."

### ✅ Strategic Positioning
Inserted new sections before Anti-Rationalization (manager) or Constraints (coder/tester) — after all workflow content, before behavioral guardrails. Agents see guidelines as final filter before output, not mid-workflow interruption.

**Evidence:** Sections positioned at lines where agents have already decided *what* to output and are now deciding *how* to format it.

---

## What Could Be Improved

### 🔄 No Guidance on Mixed Scenarios
What happens when a routine operation uncovers an error? The guidelines treat scenarios as mutually exclusive, but real workflows often transition mid-task.

**Impact:** Low — agents will likely default to error scenario (verbose) when in doubt, which is the safer choice.

**Mitigation:** Add transition guidance if feedback shows confusion (e.g., "If a routine operation reveals an error, switch to Error Scenario output immediately").

### 🔄 No Metrics for "Routine" vs "Complex"
Guidelines use subjective terms like "routine" and "complex" without quantitative boundaries. What makes a code change "complex"? Number of files? Lines changed? Dependencies touched?

**Impact:** Medium — agents must use judgment, which may be inconsistent across agents or contexts.

**Mitigation:** Consider adding heuristics in future iteration (e.g., "Routine: 1 file, <20 lines. Complex: 3+ files or architectural changes").

### 🔄 Tester Section Overlaps with Existing Output Format
tester.agent.md already has an "Output Format" section (bug report template). The new "Test Output" section is adjacent but distinct — both address output formatting but for different purposes (general reporting vs test-specific verbosity).

**Impact:** Low — sections complement rather than conflict, but proximity might cause confusion.

**Mitigation:** Add cross-reference note linking the two sections (e.g., "See Output Format for bug report structure").

---

## Lessons for Next Time

### 🎓 Consistent Patterns Across Related Content
When adding guidance to multiple files, use identical structure (headings, subsections, example format). Reduces cognitive load and signals to agents that this is a unified policy, not file-specific quirks.

**Action:** Document "cross-file consistency" as a documentation standard when updating multiple agents simultaneously.

### 🎓 Coherent Examples Beat Independent Ones
Using JWT/auth domain across all three agents makes examples feel like parts of a real workflow. More effective than three unrelated synthetic examples.

**Action:** When documenting multi-agent workflows, choose one domain and reuse it across all examples. Prefer realistic domains from the project itself.

### 🎓 Explicit Exception Clauses Prevent Misapplication
"Regardless of other guidelines" note in Error Scenarios prevents agents from applying conciseness rules where they don't belong. Explicit overrides beat implicit priorities.

**Action:** When guidelines have priority levels, state exceptions explicitly rather than expecting agents to infer precedence.

---

## Decisions Made

### D1: Use When/Do/Don't Pattern Instead of Imperative Rules
**Decision:** Structure each scenario as When (trigger condition), Do (required behaviors), Don't (antipatterns) instead of a flat list of imperatives ("Always do X", "Never do Y").

**Rationale:** When/Do/Don't pattern provides context (when does this apply?), positive guidance (what to do), and negative guidance (what to avoid). More complete than imperative-only rules.

**Alternative Rejected:** Flat list of imperatives. Rejected because it lacks context — agents wouldn't know when to apply each rule.

**Outcome:** All 3 agents use consistent structure. Examples clearly demonstrate both Do and Don't patterns.

---

### D2: Position Before Anti-Rationalization/Constraints
**Decision:** Insert new sections before Anti-Rationalization (manager) or Constraints (coder/tester), not mid-workflow.

**Rationale:** Agents encounter these guidelines after deciding *what* to output, at the formatting stage. Mid-workflow insertion would interrupt decision-making flow.

**Alternative Rejected:** Insert after first workflow step. Rejected because agents wouldn't have output to format yet — guidance would be premature.

**Outcome:** Guidelines positioned where agents are ready to use them immediately.

---

### D3: Keep Error Scenarios Verbose by Default
**Decision:** Error Scenarios always use verbose output "regardless of other guidelines." No exceptions for routine-looking errors.

**Rationale:** Missing context in error output wastes more time than verbose error output costs. Better to over-inform than under-inform when debugging.

**Alternative Rejected:** Apply conciseness to "obvious" errors. Rejected because "obvious" is subjective — what's obvious to the agent may not be obvious to the user.

**Outcome:** Error Scenarios explicitly override all other verbosity rules.

---

## Metrics

- **Files Modified:** 3
- **Lines Added:** +171 (52 to manager, 60 to coder, 59 to tester)
- **Lines Deleted:** 0
- **Commits:** 2 (setup + implementation)
- **Acceptance Criteria:** 6/6 met
- **Failures:** 0
- **Iterations:** 1 (implementation completed on first pass)

---

## Knowledge to Promote

### Pattern: When/Do/Don't Guidance Structure
**Context:** Adding behavioral guidelines to agent definitions.

**Solution:** Structure each scenario as:
- **When:** Trigger condition (when does this guidance apply?)
- **Do:** Positive behaviors (what should the agent do?)
- **Don't:** Antipatterns (what should the agent avoid?)
- **Example:** Realistic demonstration of Do and Don't patterns

**When to Use:** Agent behavioral guidelines, decision rules, output formatting rules.

**Evidence:** MKT-0004 used this pattern across 3 agents for 7 total scenarios (3 in manager, 2 in coder, 2 in tester). Consistent and actionable.

**Promotion Target:** `.context/standards.md` under "Agent Design Patterns" or create `agent-guidance-patterns` skill.

---

### Pattern: Coherent Cross-Agent Examples
**Context:** Documenting multi-agent workflows or policies that span multiple agents.

**Solution:** Choose one realistic domain and reuse it across all examples. Make examples feel like parts of a real workflow, not disconnected fragments.

**When to Use:** Multi-agent documentation, cross-cutting policies, workflow examples.

**Evidence:** JWT/auth domain used across manager (delegating auth check), coder (validating JWT), tester (auth test failures). Reads as unified scenario.

**Promotion Target:** `.context/standards.md` under "Documentation Standards."

---

### Pattern: Explicit Exception Clauses
**Context:** Guidelines with priority levels or scenarios where one rule overrides others.

**Solution:** State exceptions explicitly with "regardless of other guidelines" or "overrides all other rules" language. Don't expect agents to infer precedence.

**When to Use:** Safety-critical guidelines, error handling, security policies, any rule that must never be compromised.

**Evidence:** Error Scenarios section explicitly states "regardless of other guidelines" to prevent agents from applying conciseness rules during error handling.

**Promotion Target:** `.context/standards.md` under "Agent Design Patterns."

---

## Tags

- #documentation
- #agent-behavior
- #output-efficiency
- #verbosity-control
- #cross-agent-patterns

---

## Follow-Up Tasks

None identified. Guidelines are complete and ready for agent use.
