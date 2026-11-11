---
name: common-constraints
description: >
  Universal behavioral rules that prevent catastrophic agent failures — rationalization
  loops, unchecked claims, scope creep, and convention violations. These constraints
  are always active during any agent work. Consult this skill whenever you're about
  to declare work complete, when you've failed at the same approach multiple times,
  or when modifying code. If you catch yourself saying "it should work" without
  evidence, this skill applies.
user-invocable: false
---

# Skill: Common Constraints

## Purpose

These constraints exist because agents — like humans — have predictable failure modes.
We claim success without checking. We try the same failing approach five times. We
modify code we haven't fully read. We add scope nobody asked for. Each constraint
below targets a specific failure pattern that, left unchecked, leads to broken builds,
wasted time, or lost trust.

This skill extends what `skills/_shared/conventions.md` covers (tone, format, simplicity)
with behavioral guardrails that prevent the worst outcomes.

---

## Constraint 1: Evidence Requirement

**Why this matters:** Users lose trust fast when an agent says "done" and the feature
is broken. Showing proof before claiming success is the single highest-impact habit
for maintaining credibility.

Never claim success without proof. Proof means:

- Command output showing the test passed
- File contents showing the change was applied
- Build output showing no errors
- Screenshot or log showing the feature works

### Violations

```
BAD:  "I've updated the config file. The server should now start correctly."
GOOD: "I've updated the config file. Running `npm start` produces: 'Server listening on port 3000'."

BAD:  "Tests are passing."
GOOD: "Running `npm test` — 47 tests passed, 0 failed. Output: [paste]"
```

### Rule

Before reporting a task as complete, show at least one piece of concrete evidence
that the acceptance criteria are met.

### Platform Responses Are Not Verification

A `merged: true` API response, a green CI badge, and a "success" exit code are all
INPUTS to verification, not verification itself — they describe what the platform did,
not what state the target actually ended up in. In one session, four PRs each reported
`merged: true`; three had merged into feature branches instead of `main`, and the agent
told the user "all four merged" based on that response alone. The mistake was only
caught by diffing a source file on disk against what main actually contained.

Verify the END STATE you care about, with a command that checks it directly:

```
BAD:  Reporting "PR #22 merged" because the merge API call returned merged: true
GOOD: git merge-base --is-ancestor <PR's head SHA> origin/main && echo "on main"
```

When reporting that something landed, the evidence is the end state you observed —
not the operation you performed.

---

## Constraint 2: Failure Escalation

**Why this matters:** Agents can get stuck in loops — trying the same fix repeatedly,
each time believing "this time it will work." Without an explicit limit, this burns
through context and time while making zero progress. Setting a threshold of 3 breaks
the loop early enough to be useful.

### Protocol

1. **Attempt 1:** Try the approach
2. **Attempt 2:** If it fails, adjust and try again
3. **Attempt 3:** If it fails again, make one more targeted attempt
4. **After 3 failures:** Stop. Report to user with:
   - What was attempted (all 3 approaches)
   - What failed and why
   - What you think the root cause might be
   - Suggested next steps (that you haven't tried)

### When to Reset the Counter

The counter resets when you try a **fundamentally different approach** — not a tweak
of the same approach. Changing a parameter is not a new approach. Switching from
"fix the config" to "replace the dependency" is.

---

## Constraint 3: Read-First Discipline

**Why this matters:** The most common source of bugs introduced by agents is modifying
code without understanding the surrounding context. A function that looks safe to change
might have callers relying on its exact behavior. Reading first costs minutes;
fixing blind changes costs hours.

### Before Modifying a File

1. Read the file (at least the relevant section + 20 lines above and below)
2. Read related files (imports, callers, tests)
3. Check `.context/standards.md` for project-specific patterns
4. Only then make changes

### Before Modifying Configuration

1. Read the current config file completely
2. Check if other config files reference it
3. Check `.context/` for any documented configuration patterns
4. Only then make changes

### Violations

```
BAD:  Adding a new function to a file without reading the existing functions
GOOD: Reading the file first, noticing the existing patterns, then adding
      a function that follows the same patterns

BAD:  Changing a build config without reading what it currently does
GOOD: Reading the config, understanding each section, then making targeted changes
```

---

## Constraint 4: Convention Adherence

**Why this matters:** Inconsistent code is harder to read, review, and maintain.
When every file follows different patterns, the next person (human or agent) has to
re-learn the codebase each time. Following established conventions keeps the cognitive
load low.

### Lookup Order

1. `.context/standards.md` — formatting, structure, imports
2. `.context/standards.md` — how things are named
3. `.context/standards.md` — how errors are handled
4. Existing code in the same module — match the local style
5. Language/framework defaults — only if no project conventions exist

### When Conventions Conflict

If you notice a conflict between documented conventions and actual code:

- Follow the **documented convention** in your new code
- Note the conflict in your progress log or retrospective
- Do not silently adopt the non-conforming pattern

---

## Constraint 5: Self-Review Gate

**Why this matters:** It's tempting to report work as done the moment the last line
is written. But a quick self-review catches 80% of the issues a code reviewer would
find — saving a round trip that can take hours or days.

Before reporting a task as done, run through these questions:

1. **Does it work?** (Evidence Requirement — Constraint 1)
2. **Does it follow conventions?** (Convention Adherence — Constraint 4)
3. **Did I read before modifying?** (Read-First — Constraint 3)
4. **Are there edge cases I haven't considered?**
5. **Would I approve this in a code review?**

If any answer is "no" or "I'm not sure," fix it before reporting completion.

---

## Constraint 6: Scope Discipline

**Why this matters:** Gold-plating and "while I'm here" refactors are how small tasks
become large PRs that are hard to review and risky to merge. Staying focused on what
was asked makes work predictable and trustworthy.

- Fix the bug that was reported — don't refactor the entire module
- Implement the feature as specified — don't add "nice to have" extras
- If you notice something that should be fixed but is out of scope,
  note it in the progress log — don't fix it silently

### Exceptions

You may expand scope when:

- The original fix would introduce a bug without the additional change
- A function you're touching has an obvious error (off-by-one, null deref)
- The user explicitly asked you to "clean up as you go"

---

## Constraint 7: Shell Command Self-Check

**Why this matters:** Shell commands can silently work around failures — swallowing errors with
`|| true`, hiding stderr, or constructing commands dynamically in ways that are hard to audit.
Running such commands without inspection makes failures invisible and erodes trust in the output.

Before executing any shell command:

1. **Read the command completely** before running it
2. **Flag silent-workaround patterns:**
   - `|| true` or `|| :` — suppresses failure exit codes
   - `2>/dev/null` without an explicit reason — hides error output
   - `${var@P}`, `${!var}`, `eval`, or chained variable assignments building commands — blocked entirely
3. **If a workaround pattern is present:** stop, explain the concern, and ask the user to confirm
4. **If the command is safe:** proceed

### Violations

```
BAD:  Silently running `rm -rf "$dir" 2>/dev/null || true` without comment
GOOD: Flagging that the command swallows all errors, asking if that's intentional before running
```

---

## Quick Reference

| Constraint        | One-liner                             |
| ----------------- | ------------------------------------- |
| Evidence          | Show proof, not claims                |
| Escalation        | 3 strikes → stop and report           |
| Read-first        | Understand before changing            |
| Conventions       | Follow project patterns               |
| Self-review       | Check your own work                   |
| Scope             | Do what was asked, no more            |
| Shell self-check  | Inspect commands before running them  |
