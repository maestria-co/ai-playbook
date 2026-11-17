# Agent Evaluation Report — Output Template

Use this template when rendering evaluation results. Fill in every bracket placeholder.

---

# Agent Evaluation Report

**Agent file:** [filename]
**Platform:** [GitHub Copilot | Claude | Unknown]
**Estimated token count:** [N tokens (~N characters)]
**Evaluation date:** [date]

---

## Overall Health

**[EXCELLENT | GOOD | NEEDS WORK | RESTRUCTURE REQUIRED]**

[Two to three sentences summarizing the agent's overall state. What is working well. What is the single most important thing to fix.]

---

## Dimension Scores

| Dimension                  | Score   | Status                  |
| -------------------------- | ------- | ----------------------- |
| Purpose & Scope Clarity    | [score] | [PASS / WARNING / FAIL] |
| Instruction Clarity        | [score] | [PASS / WARNING / FAIL] |
| Prompt vs Skill Separation | [score] | [PASS / WARNING / FAIL] |
| Context Window Efficiency  | [score] | [PASS / WARNING / FAIL] |
| Performance & Latency      | [score] | [PASS / WARNING / FAIL] |
| Anthropic Best Practices   | [score] | [PASS / WARNING / FAIL] |

---

## Dimension Findings

### D1 — Purpose & Scope Clarity

**Score:** [CLEAR | VAGUE | UNDEFINED]

**Finding:** [What was found]

**Fix:** [Specific change]

**Rewrite suggestion:**

```
[Proposed one-sentence job description]
[Proposed scope boundary — does / does not]
```

---

### D2 — Instruction Clarity & Ambiguity

**Score:** [PRECISE | AMBIGUOUS | CONTRADICTORY]

**Finding:** [List each ambiguous instruction with exact text]

**Ambiguous instructions found:**

- "[exact text]" — [why ambiguous] — [what it should say]

**Rewrite suggestion:**

```
BEFORE: [ambiguous instruction]
AFTER:  [precise rewrite]
```

---

### D3 — Prompt vs Skill Separation

**Score:** [CLEAN | BOUNDARY EROSION | MIXED]

**Finding:** [List each violation]

| Content       | Currently in           | Should be in           |
| ------------- | ---------------------- | ---------------------- |
| [description] | [agent prompt / skill] | [agent prompt / skill] |

**Fix:** [What to move and where]

---

### D4 — Context Window Efficiency

**Score:** [EFFICIENT | MONITOR | INEFFICIENT]

**Finding:** [Token budget usage, unconditional vs conditional loading]

**Unconditional context loads found:**

- [description] — ~[N] tokens — [could this be conditional?]

**Fix:** [What to make conditional or move to external files]

---

### D5 — Performance & Latency

**Score:** [OPTIMIZED | IMPROVABLE | INEFFICIENT]

**Finding:** [Tool call patterns, loop limits, fast paths]

**Issues found:**

- [issue] — [impact] — [fix]

---

### D6 — Anthropic Best Practice Alignment

**Score:** [ALIGNED | PARTIALLY ALIGNED | MISALIGNED]

| Standard                     | Status      | Finding |
| ---------------------------- | ----------- | ------- |
| Single clear purpose         | [PASS/FAIL] | [note]  |
| Minimal footprint            | [PASS/FAIL] | [note]  |
| Explicit stopping conditions | [PASS/FAIL] | [note]  |
| Human-readable reasoning     | [PASS/FAIL] | [note]  |
| Safe defaults                | [PASS/FAIL] | [note]  |
| Narrow tool definitions      | [PASS/FAIL] | [note]  |
| No prompt injection risk     | [PASS/FAIL] | [note]  |
| Graceful degradation         | [PASS/FAIL] | [note]  |
| Deterministic routing        | [PASS/FAIL] | [note]  |
| Output contracts             | [PASS/FAIL] | [note]  |

**Fix:** [Which standards need addressing and how]

---

## Token Size Analysis

**Total estimated tokens:** [N]

**Top contributors:**

- [section name] — ~[N] tokens — [assessment]
- [repeat for each major section]

**Flags:** [Repeated instructions, filler language, content that should be externalized]

---

## Priority Fix List

Ordered by impact — fix these first:

1. **[Fix title]** — [One sentence on what to do and why it matters most]
2. **[Fix title]** — [One sentence]
3. **[Fix title]** — [One sentence]

---

## Open Questions

Decisions needed before fixes can be applied:

1. [Question] — [Why it matters and what the answer changes]
