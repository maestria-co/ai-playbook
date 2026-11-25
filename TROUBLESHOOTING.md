# Troubleshooting Guide

Common problems using the agentless pattern system and how to fix them.

---

## Pattern Outputs

### "The pattern gave me a vague plan with no specifics"

**Cause:** Not enough context in your prompt.

**Fix:** Always fill in the `<context>` block completely:
- Specific file paths (not "the auth folder" — `src/auth/login.js`)
- Acceptance criteria as a checklist
- Stack details (language, framework, test runner)
- Constraints that limit the solution

**Anti-pattern:**
```
<task>Add caching.</task>
```

**Better:**
```
<task>Add Redis caching to GET /users/:id.</task>
<context>
Stack: Node.js/Express, ioredis
Endpoint: src/routes/users.js line 45 (getUserById)
ADR: .context/decisions/ADR-007-caching-strategy.md
Spec:
- [ ] Cache key: user:{id}
- [ ] TTL: 60 seconds
- [ ] Invalidate on PATCH /users/:id
</context>
```

---

### "The pattern gave me too much — a massive implementation when I needed a small change"

**Cause:** The task was scoped too broadly.

**Fix:** Break the task down first with `planning-tasks`, then run `implementing-features` per task (one at a time), not for the whole plan at once.

---

### "implementing-features changed things I didn't ask it to change"

**Cause:** The implementation scope was open-ended.

**Fix:** Add a constraints block:

```
<constraints>
- Only touch src/routes/users.js and src/models/User.js
- Do not modify the test files
- Do not change the existing User model schema
</constraints>
```

---

### "researching-options gave me 5 options with no recommendation"

**Cause:** The task was framed as "tell me about options" instead of "recommend one."

**Fix:** Reframe the task to explicitly ask for a recommendation:

```
<task>Which JWT library should we use? Make a recommendation and explain why.</task>
```

The `researching-options` pattern is designed to recommend, not list. If it's listing, the prompt framing is too neutral.

---

### "designing-systems wrote an ADR but didn't explain the implementation"

**Cause:** ADR scope is decision + rationale. Implementation details are separate.

**Fix:** After the ADR is written, pass it to `implementing-features` or `planning-tasks`:

```
Use the planning-tasks skill.

<task>Plan the implementation per ADR-007.</task>
<context>
ADR: .context/decisions/ADR-007-caching-strategy.md
</context>
```

---

### "writing-tests is blocked because the code isn't testable"

**Cause:** The implementation has dependencies that can't be injected (module-level singletons, global state, etc.).

**Fix:** This is a real blocker. The test result should say `❌ Blocked` with a specific reason. Don't force tests — fix the implementation first:

```
Use the implementing-features skill.

<task>Refactor Redis client to use dependency injection so it can be mocked in tests.</task>
<context>
Current: src/cache/redis.js exports a module-level singleton
Needed: accept Redis client as constructor/function argument
Files: src/cache/redis.js, any files that import it
</context>
```

Then re-run `writing-tests`.

---

## Pattern Selection

### "I don't know which pattern to use"

Start here:

```
Does the task produce code?
  └─ Yes → implementing-features (or planning-tasks first if 4+ steps)
  └─ No → Does it produce a decision?
            └─ Yes → designing-systems (or researching-options first if options unclear)
            └─ No → Does it produce a list of steps?
                      └─ Yes → planning-tasks
                      └─ No → Is it a question about technology?
                                └─ Yes → researching-options
```

If you're still unsure, use `planning-tasks` — it will tell you what patterns to use next.

---

### "I used coordinating-work but it just told me to use other patterns"

**That's correct behavior.** `coordinating-work` produces a sequenced list of pattern invocations — it doesn't run them. You then run each pattern in sequence.

If this feels like extra steps for a simple task, you probably don't need `coordinating-work`. Use patterns directly in sequence.

**Only use `coordinating-work` when:**
- You have 3+ patterns and you're not sure of the sequence
- There are complex dependencies between pattern outputs
- You want an explicit check on stopping conditions before each step

---

## Quality Issues

### "The output quality is inconsistent across runs"

**Cause:** Patterns with `degree_of_freedom: high` (like `researching-options`) have more variance.

**Fix:** Add more constraints to the prompt, or pin the approach in the `<context>` block:

```
<context>
Approach: evaluate only passport.js and a custom implementation — no other libraries
Format: recommendation first, then tradeoffs table, then confidence level
</context>
```

---

### "The pattern output is good but doesn't match our codebase conventions"

**Cause:** The pattern doesn't know your project's conventions unless you tell it.

**Fix:** Include a conventions reference in `<context>`:

```
<context>
Follow patterns in: .context/standards/code-style.md
Follow error handling from: .context/standards/error-handling.md
Use existing pattern from: src/routes/auth.js (for route structure)
</context>
```

Alternatively, update your `.context/overview.md` with a "Conventions" section so it's always available.

---

## Context and State

### "I resumed a task after a context reset and the pattern doesn't know what was done"

**Fix:** Follow the context recovery steps:

```bash
git log --oneline -10         # what changed recently
cat .context/overview.md
cat .context/tasks/[ID]/brief.md
cat .context/tasks/[ID]/plan.md   # what's the current task list
```

Then resume with:

```
Use the implementing-features skill.

<task>[NEXT INCOMPLETE TASK from plan.md]</task>
<context>
Context recovery: tasks 1-3 are complete (see git log). Starting task 4.
Plan: .context/tasks/[ID]/plan.md
</context>
```

---

### "The pattern is writing to the wrong files"

**Fix:** The patterns specify output locations in their pre-flight checks. If output is going somewhere unexpected, explicitly specify in the prompt:

```
<constraints>
Write output to: .context/tasks/feature-x/research.md
Do not create any new directories.
</constraints>
```

---

## When Patterns Aren't Enough

Patterns don't help with:
- **Product decisions** — what to build, feature prioritization, business rules. Route to your product owner.
- **Infrastructure provisioning** — Terraform, cloud setup, DNS. Use specialized tools.
- **Performance profiling** — patterns can write optimized code but can't profile runtime behavior. Use profiling tools directly.
- **Dependency conflicts** — package resolution issues. Run package manager commands directly.

For anything that feels like it needs a "super-agent" with many tools — break it down. A well-scoped `implementing-features` invocation with a clear brief almost always outperforms a broad, open-ended request.
