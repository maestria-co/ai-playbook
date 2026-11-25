# Retrospective Log

This directory contains the rolling learning log — a record of what agents and humans learned while doing the work. It is the primary mechanism by which this agent system improves over time.

---

## How It Works

1. **Agents append entries** after completing significant tasks (see `template.md`)
2. **Humans review** entries periodically (weekly recommended)
3. **Valuable learnings are promoted** to permanent locations:
   - Patterns and rules → agent definition files in `agents/`
   - Technical decisions → `decisions/ADR-NNN-*.md`
   - Project facts → `.context/overview.md`
4. **Promoted entries are marked** so we don't re-review them

---

## File Naming

One file per week (or per sprint):
```
YYYY-MM-DD.md    ← Start date of the period
```

Example: `2025-03-10.md` covers the week of March 10–17, 2025.

---

## Log Index

| Period | Key Learnings | Promoted? |
|---|---|---|
| *(none yet)* | — | — |

---

## What Makes a Good Retrospective Entry?

**Useful:**
- "Coder agent produced over-engineered code when the spec wasn't specific enough about scope. Fix: Planner should include explicit scope boundaries in handoffs."
- "Researcher outputs were too long and not actionable. Fix: Added a 'Recommendation' section at the top of all research reports."
- "Discovered that `src/utils/date.js` contains shared date formatting logic — agents were duplicating this."

**Not useful:**
- "Task went well."
- "No issues."
- "Used the Coder agent."

---

## Promotion Criteria

An entry should be promoted when:
- The same pattern appears in 2+ retro entries
- A rule change would prevent a whole class of mistakes
- A fact discovered should be in `overview.md`
- A decision was made that should be an ADR

An entry does NOT need to be promoted if it was a one-off issue unlikely to recur.
