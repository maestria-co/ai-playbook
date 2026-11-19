---
name: task-retrospective
description: >
  Structured reflection after completing tasks to capture lessons learned. Use this
  skill after finishing any medium or complex task, after encountering surprising
  behavior, after a task that took much longer than expected, or after debugging a
  tricky issue. If you learned something during a task that would help next time,
  use this skill — the knowledge captured here feeds into `context-maintenance` for
  promotion to permanent docs.
---

# Skill: Task Retrospective

## Purpose

Capture what was learned during a task so the knowledge isn't lost when context clears.
A good retrospective takes 5 minutes and prevents hours of repeated mistakes.

Run it as Kaizen: blameless, ask "why?" until you reach a process cause (Five Whys), and end with one small change you can ship. Why: blame hides the real cause, and small changes actually get made. See `applying-design-principles` (Lean and continuous improvement).

---

## When to Run

| Situation                          | Run retrospective?                       |
| ---------------------------------- | ---------------------------------------- |
| Completed a multi-step feature     | Yes                                      |
| Fixed a non-trivial bug            | Yes                                      |
| Task took 2x+ longer than expected | Yes — especially important               |
| Simple one-line change             | No                                       |
| Research task                      | No — the research output is the artifact |
| Encountered a surprising behavior  | Yes — even if the task was simple        |

---

## Retrospective Structure

Write the retrospective in `.context/retrospectives/` using this format:

```markdown
## [Date] — [Task ID or short title]

### What Went Well

- [Specific thing that worked, with enough detail to be useful]

### What Could Be Improved

- [Problem]: [Root cause] → [What to do differently]

### Lessons Learned

- [Concrete, actionable insight]

### Promotion Items

- [ ] [Insight] → promote to [target file]
```

---

## Section Guidance

### What Went Well

Don't skip this. Reinforcing what works is as important as fixing what doesn't.

**Be specific:**

```
BAD:  "Implementation went smoothly"
GOOD: "Using the repository pattern from .context/architecture.md meant
       the database swap only required changes in one file"
```

### What Could Be Improved

Always include the **root cause**, not just the symptom. Use the format:
`[Problem]: [Root cause] → [What to do differently]`

```
BAD:  "Tests were slow"
GOOD: "Integration tests took 45s: each test spun up a fresh database
       → Use a shared test database with transaction rollback"
```

### Lessons Learned

These are insights that apply beyond this specific task. Think: "What would I tell
another developer starting a similar task?"

```
BAD:  "The API was tricky"
GOOD: "The payment gateway returns HTTP 200 with an error body for declined cards.
       Always check the response body status field, not just the HTTP status."
```

### Promotion Items

Each lesson that should become permanent documentation gets a promotion checkbox.
The `context-maintenance` skill handles the actual promotion.

```markdown
### Promotion Items

- [ ] Payment gateway error handling → promote to .context/standards.md
- [ ] Repository pattern for data access → promote to .context/architecture.md
- [x] Already promoted: naming convention for API routes
```

---

## Root Cause Analysis

When something went wrong, dig deeper than the surface:

### 5 Whys (simplified)

1. **What happened?** Tests failed after deployment
2. **Why?** Environment variable was missing in production
3. **Why?** It was added locally but not to the CI config
4. **Why?** No checklist for new environment variables
5. **Action:** Add "update CI config" to the deployment checklist in `.context/workflows/ci-cd.md`

### Common Root Causes

| Symptom                      | Likely root cause                                   |
| ---------------------------- | --------------------------------------------------- |
| Spent time on wrong approach | Didn't research alternatives first                  |
| Broke existing functionality | Didn't read surrounding code                        |
| Missed edge case             | Didn't review acceptance criteria thoroughly        |
| Integration failure          | Assumptions about external API not validated        |
| Task took too long           | Scope was unclear or expanded during implementation |

---

## Examples

### Good Retrospective

```markdown
## 2024-01-15 — TASK-42: Add email notification for failed payments

### What Went Well

- Using the existing notification service made the email integration straightforward
- Writing the test first caught a race condition before it hit production

### What Could Be Improved

- Email template took 3x longer than expected: HTML email rendering is fragile
  across clients → Use a template library (mjml) instead of raw HTML next time
- Didn't check rate limits on the email service → almost hit the sending cap
  during testing

### Lessons Learned

- The email service rate-limits to 100/hour in dev. Use a mock for most tests
  and one real integration test.
- HTML email must be tested in Outlook, Gmail, and Apple Mail — they render
  differently. Document this in testing standards.

### Promotion Items

- [ ] Email service rate limits → promote to domains/glossary.md
- [ ] Email testing requirements → promote to .context/testing.md
```

### Bad Retrospective

```markdown
## 2024-01-15 — TASK-42

### What Went Well

- Done

### What Could Be Improved

- Took too long

### Lessons Learned

- Email is hard
```

---

## Constraints

- Write the retrospective immediately after completing the task — not later
- Be specific — vague entries are useless
- Include at least one promotion item if lessons were learned
- Don't turn it into a blame log — focus on process, not people
- Keep each retrospective under 30 lines — brevity forces clarity
- The retrospective goes in `.context/retrospectives/`, not the task folder

## Delegation Boundaries

| What you're doing | Use |
|---|---|
| Updating `.context/retrospectives/` (this skill's output) | Write directly |
| Promoting lessons to permanent `.context/` docs | Invoke `context-maintenance` |
| Initializing or reorganizing a `.context/` directory | Delegate to `@context-specialist` |
