# Task Plan: MKT-0004 — Output Verbosity Control

**Task ID:** MKT-0004  
**Type:** Documentation Enhancement  
**Priority:** P1  
**Effort:** 2h  
**Branch:** feature/MKT-0004-output-verbosity  

---

## Goal

Add output efficiency guidelines to agent definitions so agents use concise output for routine operations and verbose output only for complex work or errors, helping users focus on essential information.

---

## Acceptance Criteria

1. ✅ Given the `agents/manager.agent.md`, when I read the new "Output Efficiency Guidelines" section, then it distinguishes three scenarios: Routine Operations, Complex Operations, and Error Scenarios, with guidance for each.

2. ✅ Given a routine operation (reading files, running passing tests), when an agent responds, then it avoids preambles ("Great, let me..."), doesn't restate context, and provides only essential observation or next action.

3. ✅ Given a complex operation (debugging, architecture decisions), when an agent responds, then it provides reasoning and evidence for conclusions.

4. ✅ Given an error scenario, when an agent responds, then it always provides full context, stack traces, and step-by-step diagnosis regardless of other guidelines.

5. ✅ Given the `agents/coder.agent.md`, when I read the new "Code Output Efficiency" section, then it shows patterns for routine vs. complex code changes.

6. ✅ Given the `agents/tester.agent.md`, when I read the new "Test Output" section, then it shows concise summaries for passing tests and full output for failures.

---

## Steps

1. **[DONE]** Analyze current agent output patterns to identify verbosity patterns and insertion points for efficiency guidelines.
   - Reviewed manager, coder, and tester agents
   - Identified insertion points before Anti-Rationalization/Constraints sections

2. **[DONE]** Design output efficiency guidelines: define 3 scenarios (Routine, Complex, Error) with specific guidance for each.
   - 3 scenarios defined with When/Do/Don't patterns
   - Consistent formatting across all agents

3. **[DONE]** Add "Output Efficiency Guidelines" section to `agents/manager.agent.md` distinguishing the 3 scenarios.
   - Added section before Anti-Rationalization (+52 lines)
   - 3 subsections with guidance and examples

4. **[DONE]** Add "Code Output Efficiency" section to `agents/coder.agent.md` showing patterns for routine vs complex code changes.
   - Added section before Constraints (+60 lines)
   - 2 subsections: Routine and Complex code changes

5. **[DONE]** Add "Test Output" section to `agents/tester.agent.md` showing concise summaries for passing tests, full output for failures.
   - Added section before Constraints (+59 lines)
   - 2 subsections: Passing and Failing tests

6. **[DONE]** Test guidelines clarity: verify all 6 acceptance criteria are met.
   - All 6 ACs verified ✅

7. **[DONE]** Final verification: run checklist, commit, and prepare for completion.
   - Committed: ca594d9
   - Ready for retrospective

---

## Context

**From Trello Card:**
- **Story:** As an agent user, I want agents to use concise output for routine operations and verbose output only for complex work or errors, so that I can focus on essential information and avoid unnecessary preambles for standard tasks.

**Affected Components:**
- `agents/manager.agent.md` — Add Output Efficiency Guidelines section
- `agents/coder.agent.md` — Add Code Output Efficiency section
- `agents/tester.agent.md` — Add Test Output section

**Complexity:** S (Small)  
**Effort:** 2h

---

## Decisions

None yet.

---

## Progress Log

- **2026-07-10 08:38** — Implementation complete. All 6 ACs verified. Committed ca594d9. Next: retrospective.
- **2026-07-10 08:31** — Task created, branch feature/MKT-0004-output-verbosity created
