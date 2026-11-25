---
name: researching-options
description: >
  Investigates a technical question and produces an opinionated recommendation with
  evidence. Use when: an unknown blocks planning or implementation, a library or
  approach needs evaluation before adoption, multiple valid options exist and a
  comparison is needed, or security and performance implications need assessment.
  Do not use when: the answer is obvious, it's an implementation detail within an
  already-decided approach, or it's a business/product decision.
degree_of_freedom: high
---

# Skill: Researching Options

## Purpose

Fill a knowledge gap so a decision can be made or implementation can proceed.
Research ends with an explicit recommendation — not a list of options for the reader
to evaluate. Transferring the evaluation burden without adding analysis is a failure mode.

Timebox every investigation. Exhaustive research is itself a failure mode. Set a
"good enough" bar at the start and stop when you reach it.

---

## Pre-flight Checks

**Check 1 — Scope the question**

Restate the research question precisely before investigating.

- If the question is vague (e.g., "research auth") → narrow it: "Which Node.js JWT library
  should we use given our Express stack and TypeScript requirement?"
- If the question is actually a business/product decision → stop. State: "This is a
  product decision, not a technical one. Route to the appropriate stakeholder."

**Check 2 — Check for prior research**

Read `.context/tasks/*/research/` to see if this question (or a close variant) was already researched.

- If recent research exists (< 30 days) → read it. Determine if circumstances have changed
  enough to warrant re-investigation. If not, return the existing recommendation.
- If no prior research exists → proceed.

---

## Execution Steps

### Step 1 — Define the "Good Enough" Bar

State explicitly:
- What decision this research will enable
- The minimum evidence needed to make that decision confidently
- What is out of scope for this investigation

This prevents scope creep. Stop when you reach the bar.

### Step 2 — Identify Viable Options

List ≥2 options that could plausibly solve the problem. For each, identify:
- What it is and what it does
- Rough fit for the project's constraints

Eliminate options that clearly don't fit before spending time on them.

### Step 3 — Gather Evidence

For each viable option, evaluate against relevant criteria. Common criteria:

| Criterion | What to check |
|---|---|
| Maintenance | Recent commits, open issues, last release date |
| Adoption | Download stats, GitHub stars, ecosystem usage |
| Security | Known CVEs, security audit history, dependency count |
| License | Compatible with project's license requirements |
| Fit | TypeScript support, framework compatibility, bundle size |
| Docs quality | Are examples clear? Is the API documented? |

Adjust criteria to the question. Not all criteria apply to every investigation.

### Step 4 — Analyze Honestly

For each option, state:
- Its primary strength for this use case
- Its genuine downside (not just "it's less popular")
- Your confidence level if uncertain

Do not cherry-pick evidence. If the "worse" option has a genuine advantage, say so.

### Step 5 — Recommend Explicitly

State the recommendation clearly:

```
Recommendation: [Option]

Reason: [2–3 sentences. Why this option, given the project's specific constraints.]

Main tradeoff accepted: [What we're giving up by choosing this over the alternatives.]

Confidence: [High / Medium / Low — with one sentence on why if not High]
```

Never write "here are the options, you decide." That transfers cognitive load without
adding value. Make the call.

### Step 6 — Save the Report

Write the full report to `.context/tasks/[task-id]/research/[topic-slug].md`. If there is no
task id, generate one (`local-YYYY-MM-DD-<slug>`) — a report belongs to the
work that prompted it, so it is pruned when that task folder is.

Report structure:
```markdown
# Research: [Topic]
Date: YYYY-MM-DD | Status: Complete

## Recommendation
> **[Option]** — [one sentence why]

[2–3 sentences on the primary tradeoff accepted]

## Options Evaluated
| Criterion | [Option A] | [Option B] | [Option C] |
|---|---|---|---|

## Key Findings
- [finding with evidence]

## Sources
- [source with date accessed]
```

---

## Output Format

```
Research complete: [Topic]

Recommendation: [Option] — [one sentence]
Main tradeoff: [what we're accepting]
Confidence: [High/Medium/Low]
Full report: .context/tasks/[task-id]/research/[slug].md
Follow-up unknowns: [none | question to investigate]
```

---

## Examples

<examples>

<example>
<scenario>Choosing a JWT library for a Node.js/TypeScript API</scenario>
<input>
<task>Research the best JWT library for our Express + TypeScript API.</task>
<context>
- Express 4.x, TypeScript 5, Node 20
- Need: sign, verify, refresh token support
- Security is a primary concern — this is an auth service
- Current auth uses sessions (express-session); migrating to stateless JWT
- See .context/decisions/ADR-003-auth-strategy.md
</context>
</input>
<output>
Research complete: JWT Library Selection for Node.js/TypeScript

Recommendation: jsonwebtoken (jose as fallback for PKCS8/JWKS needs)
Main tradeoff: jsonwebtoken uses synchronous crypto by default; for high-throughput 
services, jose's async WebCrypto API is faster.
Confidence: High

Full report: .context/tasks/MAE-0042/research/jwt-library-selection.md

Key finding: jsonwebtoken has 50M+ weekly downloads, maintained by Auth0, full 
TypeScript types via @types/jsonwebtoken. CVE history clean since 2022 patch.
jose is the modern alternative with native WebCrypto but steeper API.
For an Express auth service under moderate load, jsonwebtoken is the safer, 
better-documented choice.
</output>
</example>

<example>
<scenario>Evaluating approaches for database migrations in a live service</scenario>
<input>
<task>Research zero-downtime column rename strategies for PostgreSQL with a live 
service that cannot have more than 30 seconds of read downtime.</task>
<context>
- PostgreSQL 15, ~50k rows in the affected table
- Service is read-heavy (95% reads, 5% writes)
- Column: user_name → username across 12 files
- Constraint: no more than 30 seconds read downtime
</context>
</input>
<output>
Research complete: Zero-downtime column rename in PostgreSQL

Recommendation: Expand-contract migration (3-phase: add new column → dual-write → 
drop old column across 3 deployments)
Main tradeoff: Requires 3 separate deployments instead of 1. Adds ~1 sprint of 
migration overhead.
Confidence: High

The single-migration rename approach locks the table for ~2-5 seconds at 50k rows, 
which violates the 30-second constraint but is borderline. Expand-contract is the 
only approach that guarantees zero read downtime. Trigger-based sync is an 
alternative but adds DB-level complexity that's harder to reason about.

Full report: .context/tasks/local-2026-11-25-column-rename/research/postgres-zero-downtime-column-rename.md
</output>
</example>

<example>
<scenario>Research question that turns out to be a product decision</scenario>
<input>
<task>Research whether we should support social login or only email/password auth.</task>
</input>
<output>
This is a product decision, not a technical one. The technical implementation of 
either approach is well-understood. The choice depends on:
- Target user demographic and their auth preferences
- Team's willingness to maintain OAuth integrations
- Regulatory requirements (GDPR, CCPA) for social auth data

Route this question to the product owner or stakeholder before proceeding. Once 
the product decision is made, the implementing-features or designing-systems 
pattern can handle the technical side.
</output>
</example>

</examples>

---

## Constraints

- Do not write production code — usage snippets illustrating an API are acceptable
- Do not make final architecture decisions — make recommendations; decisions are recorded in ADRs via `designing-systems`
- Do not do unbounded research — scope the question first, timebox the investigation, produce output
- Always save the report to `.context/tasks/[task-id]/research/` — do not deliver findings only in chat
- Do not fabricate citations — if uncertain about a source, say "unverified" explicitly
- If the question is a business/product decision, say so and stop
