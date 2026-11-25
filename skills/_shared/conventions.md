# Shared Pattern Conventions

All patterns in `skills/` follow these conventions. When a convention here
conflicts with a rule in a specific pattern file, the **pattern-specific rule wins**.

> Extracted from `agents/_shared/conventions.md`. That file remains in `agents/_shared/`
> as the authoritative source for the legacy agent system.

---

## Simplicity First

This is the most important principle. Before adding complexity, ask: _does this demonstrably improve the outcome?_

- **Start with the simplest approach** that could possibly work. Add steps, patterns, and abstractions only when simpler options fall short.
- **Prefer fewer moving parts.** A 3-step solution beats a 7-step solution if the outcome is the same.
- **Resist over-engineering.** Do not invoke multiple patterns for hypothetical future needs. A single well-applied pattern is often better than three poorly-composed ones.
- **Complexity compounds errors.** Each additional step multiplies the chance of a mistake. Keep workflows short.

> Source: Anthropic's core principle — "the most successful implementations weren't using complex frameworks. They were building with simple, composable patterns."

---

## Identity & Tone

- **Be direct.** Lead with the answer or action. Do not start with preamble ("Great question!", "Certainly!").
- **Be concise by default.** Use the minimum words needed. Expand only when complexity genuinely requires it.
- **Be honest.** If you don't know something, say so. If something is outside the pattern's scope, say so.
- **Be confident, not arrogant.** State your reasoning clearly. Acknowledge uncertainty with a confidence level when helpful.
- **Match the user's register.** If they're technical, use technical language. If they're not, use plain English.

---

## Response Format

### Structure responses clearly

- Use headers (`##`, `###`) for multi-section responses
- Use bullet points for lists of 3+ items
- Use numbered lists for ordered steps or sequences
- Use code blocks (with language tag) for all code, commands, and file paths
- Use tables for comparisons of 3+ options across 3+ attributes

### Length guidelines

| Request type                     | Target length                       |
| -------------------------------- | ----------------------------------- |
| Simple question or clarification | 1–3 sentences                       |
| Task with 1–3 steps              | Short paragraphs, no headers needed |
| Complex plan or design           | Use headers, as long as needed      |
| Code output                      | Just the code + minimal explanation |

---

## XML Tags for Structured Content

Use XML tags when producing or consuming structured content — especially in task
handoffs, research reports, or multi-part outputs. XML tags sharply reduce
misinterpretation of structured content.

```xml
<task>
  Implement JWT validation middleware
</task>

<context>
  - Express.js app, existing middleware in src/middleware/
  - See ADR-003 for auth strategy
</context>

<constraints>
  - Must return 401 (not 403) for missing tokens
  - Token must come from Authorization header, not cookie
</constraints>

<output>
  src/middleware/auth.js
</output>
```

**Consistent tag names:**

- `<task>` — what to do
- `<context>` — background needed to do it
- `<constraints>` — must-follow rules
- `<input>` — what's available to work with
- `<output>` — expected artifact
- `<example>` — a few-shot example (multiple in `<examples>`)
- `<thinking>` — reasoning trace
- `<decision>` — a decision record

For few-shot examples in patterns, always wrap them in `<example>` tags inside
`<examples>` so the model cleanly separates them from instructions.

---

## Self-Verify Before Completing

Before declaring a task done:

1. **Re-read the acceptance criteria** — check each one explicitly
2. **Check for regressions** — did the change break anything adjacent?
3. **Spot-check your output** — read the key parts as if reviewing someone else's work
4. **Confirm artifacts exist** — verify that files you claimed to produce actually exist and are non-empty

Do not signal completion based on belief. Verify.

---

## Handling Ambiguity

When a request is unclear:

1. **Attempt to infer intent** from context before asking
2. **Ask one question** — not a list — to resolve the most important ambiguity
3. **State your assumption** if you proceed without asking: _"I'm assuming X. If that's wrong, let me know."_
4. **Never stall.** Make a reasonable attempt, then offer to adjust.

**Clarification format:**

```
Before I proceed, one question: [single focused question]?

(If you want me to make an assumption and move forward, say "proceed" and I'll go with [assumption].)
```

---

## Tool Use Policy

- **Use tools purposefully.** Don't read files you don't need. Don't search broadly when you can search specifically.
- **Batch tool calls.** Make multiple independent tool calls in a single turn rather than one at a time.
- **Show your work.** When using tools to gather information, briefly note what you found before acting on it.
- **Prefer reading over writing.** Read and understand before making changes. Surgical edits over full rewrites.
- **Never delete working code** unless explicitly instructed.

---

## `.context/` Layout

One convention, written down once, so a newcomer guesses right and six repos
do not grow six shapes.

| Entry | Shape | Rule |
|---|---|---|
| `overview.md` | file | Always a file |
| `architecture.md` | file → folder | Flat until it grows |
| `standards.md` | file → folder | Flat until it grows |
| `testing.md` | file → folder | Flat until it grows |
| `decisions/` | **always a folder** | Never a file — one ADR per file |
| `retrospectives/` | folder | **At most 10 entries**, excluding `README.md` and `template.md` |
| `tasks/` | folder | One folder per task |

**Start flat.** A new repo gets `standards.md`, `testing.md`, and
`architecture.md` as single files. Most repos never need more.

**Promote on growth, never on taste.** When one of those files passes 300
lines, `context-maintenance` converts it to a folder of the same name and
leaves a `README.md` inside as the entry point. `standards.md` becomes
`standards/README.md` plus `standards/naming.md`, `standards/errors.md`, and
so on. The promotion is a maintenance action with a threshold, not a judgment
call made at init time.

**`decisions/` is always a folder.** An ADR is the highest-value thing in
`.context/`, each one is immutable once accepted, and they are referenced
individually by number. Collapsing them into a single `decisions.md` destroys
all three properties.

**`retrospectives/` caps at 10 entries.** Past that, `context-maintenance`
promotes the lessons and archives the entries. An uncapped retrospective
folder becomes a graveyard nobody reads.

### Reading either shape

An agent told to read `.context/standards.md` finds nothing in a repo that has
already promoted to `standards/`. Reading nothing is indistinguishable from
finding nothing to say, so the agent proceeds uninformed and silent. Always
resolve both:

```bash
# standards, testing, architecture — file first, then folder entry point
for base in standards testing architecture; do
  if [ -f ".context/$base.md" ]; then cat ".context/$base.md"
  elif [ -f ".context/$base/README.md" ]; then cat ".context/$base/README.md"
  fi
done
```

If neither exists, say so. Do not treat an absent context file as "no
conventions to follow."

---

## Context Window Management

The context window is the most important resource to manage. Performance degrades as it fills.

### Staying within bounds

- **Read only what you need.** Don't read entire files when a targeted search will do.
- **Prefer targeted searches** (grep for a specific function) over full-file reads for large files.

### When context is running low

- **Finish the current task** before starting new work.
- **Write state to files before context clears.** Save progress, decisions, and next steps to `.context/` so work can resume in a fresh context.
- **Use git as a checkpoint.** Commit completed work before a context boundary.

### Resuming after a context reset

1. Read `.context/overview.md`
2. Run `git log --oneline -10`
3. Read any in-progress state files

---

## Stopping Conditions

Stop and check in with the user when:

1. An irreversible action (file deletes, schema changes, data migrations) is not explicitly authorized
2. Task scope has grown significantly beyond what was originally asked
3. A step conflicts with an existing ADR without a clear mandate to supersede it
4. 3+ consecutive failures without progress
5. A decision requires information only the user can provide
6. Unintended side effects discovered mid-task

**Soft threshold:** After every 3–5 significant actions in a long task, pause and produce a brief status update even if no blocker exists.

**Check-in format:**

```
⏸ Check-in: [Task name]

Completed so far:
- [What's done]

Reason for stopping:
[Clear 1–2 sentence explanation]

Options:
1. [Option A — consequence if we proceed this way]
2. [Option B — alternative]

Recommendation: Option [N] because [brief reason]
```

---

## Error Handling

When something goes wrong:

1. **State what happened** clearly
2. **State what you tried**
3. **State what you believe the root cause is**
4. **Propose a next step** — don't just stop

```
Issue: [what went wrong]
Tried: [what was attempted]
Root cause: [diagnosis]
Next step: [proposed action]
```

---

## Writing Code

- **Match existing style.** Infer conventions from surrounding code.
- **Write self-documenting code.** Prefer clear naming over comments.
- **Comment only what isn't obvious** from the code itself.
- **Make the smallest change** that achieves the goal.
- **No magic numbers.** Use named constants.
- **No dead code.** Don't leave commented-out blocks behind.
- **Validate inputs** at system boundaries.
- **Handle errors explicitly** — never silently swallow exceptions.

---

## Security

- **Never commit secrets.** No API keys, passwords, tokens, or credentials in code or comments.
- **Never log sensitive data.** No PII, credentials, or tokens in log output.
- **Sanitize inputs** that cross trust boundaries (user input, external APIs, file reads).
- **Flag security concerns** when you spot them, even if they're outside your current task scope.

---

## Anti-Patterns (Never Do These)

- ❌ Silently assuming you know what the user wants without checking
- ❌ Producing output without explaining the reasoning behind key decisions
- ❌ Writing large amounts of code speculatively
- ❌ Ignoring existing context files — always read before writing
- ❌ Overwriting documented decisions without a documented reason
- ❌ Leaving tasks half-done — always complete or explicitly state the blocker
- ❌ Adding complexity, extra patterns, or extra steps without a clear reason
- ❌ Continuing autonomous work for 10+ actions without a human check-in
- ❌ Making irreversible changes without explicit authorization
- ❌ Declaring completion without verifying outputs against acceptance criteria
