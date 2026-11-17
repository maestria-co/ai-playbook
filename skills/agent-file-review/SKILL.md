---
name: agent-file-review
description: Evaluate agent definition files (.agent.md, system prompts) against industry best practices and produce a structured report with scores, findings, and actionable rewrites. Use this skill whenever the user asks to review, audit, evaluate, score, or improve an agent file — even if they just say "check this agent" or "is this agent any good". Also triggers for requests like "what's wrong with this agent", "review my prompt", or "grade this system prompt".
---

# Agent File Review

Evaluate a provided agent file against current industry standards and produce a structured report with dimension scores, findings, and concrete rewrite suggestions.

This skill is self-contained — read the agent file, apply the evaluation dimensions, and render the report. Do not delegate to other agents.

## Scope

**Does:** Evaluate `.agent.md` files, system prompts, and agent definition files for quality, efficiency, and adherence to best practices.

**Does not:** Rewrite the agent (suggest rewrites only), evaluate skill files (SKILL.md), or evaluate runtime agent behavior/logs.

---

## Step 1 — Identify Platform

Detect the platform from file format. This determines token thresholds.

| Platform          | Signals                                                    |
| ----------------- | ---------------------------------------------------------- |
| GitHub Copilot    | `.agent.md` extension, `#tool-name` references, markdown   |
| Claude            | System prompt format, XML tags, JSON-schema tool defs      |
| Unknown           | Flag it, evaluate against both standards where they differ |

---

## Step 2 — Measure Token Size

Estimate token count: `character_count ÷ 4`.

Break down by section — the model consuming this agent file pays a cost for every token before the user even speaks, so bloat directly degrades every interaction.

| Platform       | Green          | Yellow            | Red            |
| -------------- | -------------- | ----------------- | -------------- |
| GitHub Copilot | < 800 tokens   | 800–1500 tokens   | > 1500 tokens  |
| Claude         | < 1500 tokens  | 1500–3000 tokens  | > 3000 tokens  |

Flag: repeated instructions saying the same thing differently, filler ("always make sure to", "it is important that"), content that belongs in a skill or context file.

---

## Step 3 — Evaluate Dimensions

Score each dimension independently using the criteria below.

### D1 — Purpose & Scope Clarity

A model follows an agent better when it can summarize the agent's job in one sentence. Vague scope = unpredictable behavior.

Check:
- Can the job be stated in one sentence?
- Are boundaries defined (what it does AND does not do)?
- Is there a clear entry condition (trigger) and exit condition (done)?
- Is it a single-responsibility agent, or a "god agent" doing unrelated things?

Score: **CLEAR** / **VAGUE** / **UNDEFINED**

### D2 — Instruction Clarity & Ambiguity

Ambiguous instructions are the #1 cause of inconsistent agent behavior. "When appropriate" means something different every time — explicit if/then rules don't.

Check:
- Are trigger conditions stated as if/then rules or vague prose?
- Are there undefined phrases like "as needed", "when appropriate", "if necessary"?
- Are negative constraints present where needed ("do NOT do X")?
- Do any instructions conflict with each other?
- Are pronouns clear (no ambiguous "it should", "this must")?

Score: **PRECISE** / **AMBIGUOUS** / **CONTRADICTORY**

### D3 — Prompt vs Skill Separation

When decision logic and output formatting mix together, both get worse. Clean separation means each concern lives in exactly one place.

Check:
- Decision logic, reasoning, "when to do X" → agent prompt only
- Output templates, formatting, API calls → skill definitions only
- No rule appears in more than one place

Score: **CLEAN** / **BOUNDARY EROSION** / **MIXED**

### D4 — Context Window Efficiency

Every token the agent consumes before the user speaks is a token unavailable for the actual conversation. Front-loading context the agent may not need on every task wastes the most constrained resource.

Check:
- What percentage of the context window is consumed before user input?
- Is context loading conditional (on-demand) or unconditional (always)?
- Are there instructions that force tool calls before understanding the request?

| Pre-user budget usage | Assessment  |
| --------------------- | ----------- |
| < 30%                 | Efficient   |
| 30–60%                | Monitor     |
| > 60%                 | Inefficient |

Score: **EFFICIENT** / **MONITOR** / **INEFFICIENT**

### D5 — Performance & Latency

Unnecessary sequential tool calls, missing loop limits, and no fast-path for simple tasks all add latency that compounds across interactions.

Check:
- Are independent tool calls parallelized?
- Is there a hard loop limit to prevent infinite cycles?
- Are there early exit conditions for simple tasks?
- Does the agent over-research when the answer is already available?

Score: **OPTIMIZED** / **IMPROVABLE** / **INEFFICIENT**

### D6 — Agent Best Practice Alignment

These standards come from established patterns in reliable agent design. They exist because agents that follow them are measurably more reliable, predictable, and safe.

| Standard                     | What to check                                                |
| ---------------------------- | ------------------------------------------------------------ |
| Single clear purpose         | Agent does one thing well                                    |
| Minimal footprint            | Requests only necessary permissions and context              |
| Explicit stopping conditions | Agent knows when it is done                                  |
| Human-readable reasoning     | Agent logs or explains its decisions                         |
| Safe defaults                | Errs toward doing less and confirming when uncertain         |
| Narrow tool definitions      | Each tool does one thing                                     |
| No prompt injection risk     | Does not blindly execute instructions from tool outputs      |
| Graceful degradation         | Handles missing context or tool failures without hallucinating |
| Deterministic routing        | Same input produces same routing decision                    |
| Output contracts             | Produces structured, predictable output                      |

Score: **ALIGNED** / **PARTIALLY ALIGNED** / **MISALIGNED**

---

## Step 4 — Render Report

Read the output template from `references/output-template.md` and fill it in with your findings. The template provides the exact structure — follow it.

If the reference file is unavailable, use this structure:
1. Header (agent file, platform, token count, date)
2. Overall health summary (2-3 sentences)
3. Dimension score table
4. Per-dimension findings with: score, finding, fix, rewrite suggestion
5. Priority fix list (ordered by impact)
6. Open questions (decisions needed before fixes apply)

Every finding must include a concrete fix — not just "improve this" but the specific change to make. Include before/after rewrite suggestions for the most impactful issues.

---

## Edge Cases

- **Very short agents (< 100 tokens):** Likely incomplete. Flag but still evaluate what's there.
- **Agent references external files you can't see:** Note the dependency, evaluate only visible content, flag that a complete evaluation requires the referenced files.
- **Mixed format:** If the file combines agent and skill content, flag the separation issue under D3.
