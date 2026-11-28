---
name: designing-systems
description: >
  Makes a system design or technology decision and documents it as an Architecture
  Decision Record (ADR). Use when: introducing a new technology or service, designing
  a new system component (schema, API contract, service boundary), refactoring at
  non-trivial scale, or resolving competing technical approaches. Do not use when:
  the decision is an implementation detail within an already-decided approach, a
  naming convention choice, or a one-off decision with obvious rationale.
degree_of_freedom: medium
---

# Skill: Designing Systems

## Purpose

Make a clear, documented technical decision — and write an ADR so the decision is
not relitigated in six months. Good architecture decisions are reversible where
possible, boring where practical, and always written down.

Do not invoke this pattern for implementation details within an already-decided
approach. If you know what to build and how, use `implementing-features` directly.

---

## Pre-flight Checks

**Check 1 — Read project context**

Read `.context/overview.md` and scan `.context/decisions/` for relevant prior ADRs.

- If a prior ADR exists for this topic → read it. If you're superseding it, document why.
- If no prior ADR exists → proceed.

**Check 2 — Confirm this is a design decision, not an implementation task**

Ask: "Is there still a genuine choice to make here?"

- If yes (multiple valid approaches, real tradeoffs) → proceed.
- If no (approach is already decided, just needs implementation) → use `implementing-features`.

---

## Execution Steps

### Step 1 — State the Problem and Constraints

Write a clear problem statement:
- What decision needs to be made
- Must-have requirements (non-negotiable)
- Nice-to-have requirements (negotiable)
- Existing constraints from prior ADRs

### Step 2 — Assess Reversibility

Classify this as a **two-way door** or **one-way door** decision.

**Two-way door** (easy to undo later):
- Move quickly. Lightweight documentation is fine.
- Example: choosing a logging format, picking a folder structure

**One-way door** (hard or expensive to undo):
- Slow down. Explore options thoroughly. Write a complete ADR.
- Example: database choice, event vs. request-response architecture, authentication strategy

### Step 3 — Identify and Evaluate Options

Identify ≥2 viable options. For each, evaluate:

| Criterion | Description |
|---|---|
| Correctness | Does it actually solve the problem? |
| Simplicity | How much complexity does it add? |
| Performance | Does it meet load/latency requirements? |
| Maintainability | How hard is it to change or extend? |
| Team familiarity | Does the team know this technology? |
| Reversibility | How hard is it to undo this choice? |

Prefer the **simplest option that meets requirements**. Do not add layers,
abstractions, or services that no current requirement demands.

Before finalizing, check explicitly:
- Attack surface introduced: are there new security risks?
- Scales to 10x current load: does this design hold under realistic growth?
- Failures are observable: will we know when this breaks (logs, metrics, alerts)?

### Step 4 — Decide and Write the ADR

#### A number is claimed when the work lands, not when the ADR is drafted

Write an ADR whenever the thinking is ready — drafting early is encouraged. But **do not take a
number for work that is not done.**

| State of the work | File name | Status | In the index? |
| --- | --- | --- | --- |
| Not started, or in progress | `ADR-NEXT-<slug>.md` | `Proposed (future)` | **No** |
| Done and in force | `ADR-NNN-<slug>.md` | `Accepted` | **Yes** |

On completion, rename it to the next free number and add the index entry **in the same change**.

The index is a list of **decisions in force**, not of drafts. If an ADR is listed, it is live and can
be cited; if it is not listed, it is not yet binding.

**Never pre-assign a number in a backlog story, a plan, or another ADR.** Refer to a future ADR by
its slug ("the customer-media-storage ADR"), never by a number it has not earned. A number reserved
for unfinished work is a number two authors will both believe is theirs, and the collision surfaces
only when the second one tries to commit. Observed failure mode: two backlog stories reserved
numbers; both were taken by work that actually shipped; the placeholders were renumbered; and one of
the new numbers was taken again within days. `ADR-NEXT` cannot collide, because it says plainly that
no number has been claimed.

When you do claim a number, derive it — never guess:

```bash
{ ls .context/decisions/; cat .context/decisions/README.md 2>/dev/null; } \
  | grep -oE 'ADR-[0-9]+' | sort -t- -k2,2n | tail -1
```

Filenames and index rows are read together, because they share **one** numbering space: an entry
listed in the index but not yet written as a file still owns its number.

The sort is numeric on the number field, not lexical. `sort -u | tail -1` picks `ADR-9` out of
`{ADR-9, ADR-100}` and `ADR-99` out of `{ADR-99, ADR-100}`, so the next number it suggests is one
already taken — the exact double-claim this section exists to prevent. `-t- -k2,2n` is POSIX, so it
behaves the same in a consumer repo on any platform.

If you find a `.context/decisions.md`, stop and report it rather than adding to it. Collapsing ADRs
into a single file is drift — `META.md` says `decisions/` is always a folder, and
`scripts/validate.py` fails on that file. Splitting it is not your call either: ADR numbers are
cited from other documents, so guessing where one entry ends and the next begins invents numbers
those documents then point at. `context-maintenance` owns that drift.

#### Writing it

Write the ADR to `.context/decisions/ADR-NEXT-<slug>.md`, or `ADR-NNN-<slug>.md` if the work it
decides is already done.

ADR format:
```markdown
# ADR-NNN: [Title]

**Date:** YYYY-MM-DD  
**Status:** Accepted  
**Supersedes:** ADR-NNN (if applicable)

## Context
[The problem and why a decision is needed]

## Decision
[What was decided — one clear sentence]

## Options Considered

### Option A: [Name]
Pros: ...
Cons: ...

### Option B: [Name]
Pros: ...
Cons: ...

## Rationale
[Why this option was chosen over the alternatives]

## Consequences
- [What changes as a result]
- [What tradeoffs are accepted]
- [What monitoring/validation is needed]
```

**Index it only if the work is done.** For a completed decision, add it to the index at
`.context/decisions/README.md` in the same change that lands the work. For an `ADR-NEXT` draft,
leave the index untouched: adding it would advertise a decision as in force before it is.

### Step 5 — Produce Implementation Guidance

Produce the artifacts the implementer needs to build from:
- API contracts (request/response shape, status codes)
- Database schemas (tables, columns, indexes, constraints)
- ASCII architecture diagrams for complex interactions
- Explicit patterns to follow
- Explicit things NOT to do

---

## Output Format

```
Decision: [What was decided — one sentence]
ADR: .context/decisions/ADR-NNN-title.md

Outputs:
- [Artifact 1 — e.g., schema, API contract, ASCII diagram]

Tradeoffs accepted:
- [What was given up and why it's acceptable]

Implementation notes:
- [Key patterns to follow]
- [Explicit things NOT to do]

Suggested next: implementing-features (if implementation follows directly)
```

---

## Examples

<examples>

<example>
<scenario>Choosing a caching strategy for a read-heavy API</scenario>
<input>
<task>Decide whether to use Redis or in-memory caching for the user profile endpoint
that's being hit 500 times/second.</task>
<context>
- Node.js API, single instance today, planned to scale to 3 instances next quarter
- User profiles change infrequently (< 5 updates/day per user)
- Cache TTL of 60 seconds is acceptable per product
- Team has no prior Redis experience
- See .context/decisions/ — no prior caching ADR
</context>
</input>
<output>
Decision: Use Redis for user profile caching to support multi-instance deployment.
ADR: .context/decisions/ADR-007-caching-strategy.md

Tradeoffs accepted:
- Added infrastructure dependency (Redis) vs. in-memory simplicity
- Team must learn Redis basics; offset by ioredis library's clear docs

Implementation notes:
- Use ioredis with a 60-second TTL on key pattern `user:profile:{userId}`
- Always write-through on profile updates (invalidate cache on write)
- Do NOT use Redis for session storage — that's handled by express-session (ADR-003)

Suggested next: implementing-features — implement the ioredis integration
</output>
</example>

<example>
<scenario>Designing an API contract for a new resource</scenario>
<input>
<task>Design the REST API contract for the OAuth provider resource.</task>
<context>
- Existing REST API follows RESTful conventions (see .context/decisions/ADR-001)
- OAuthProvider model: id, userId, provider (google/github), providerId, accessToken, refreshToken, expiresAt
- Must support: connect provider, disconnect provider, list connected providers
</context>
</input>
<output>
Decision: Three-endpoint REST design for OAuth providers under /users/:userId/oauth.
ADR: .context/decisions/ADR-008-oauth-api-contract.md

API Contract:
  GET    /users/:userId/oauth           → 200 [{provider, connected, expiresAt}]
  POST   /users/:userId/oauth/:provider → 201 {provider, connected} | 409 already connected
  DELETE /users/:userId/oauth/:provider → 204 | 404 not connected

Tradeoffs accepted:
- Nested route under /users/:userId adds verbosity vs. top-level /oauth-providers
- Chosen for discoverability and alignment with existing resource nesting (ADR-001)

Implementation notes:
- Never return accessToken or refreshToken in responses — internal use only
- Validate :provider against enum ['google', 'github'] — return 400 for unknown values
</output>
</example>

<example>
<scenario>Two-way door decision that doesn't need a full ADR</scenario>
<input>
<task>Decide where to put the OAuth helper utilities — lib/ or utils/?</task>
</input>
<output>
This is a two-way door decision with no meaningful tradeoff between the options.

Decision: Place OAuth helpers in src/lib/oauth/ (consistent with existing auth helpers in src/lib/auth/).

No ADR needed — this is a naming/organization choice within an already-decided
folder structure. Document in a code comment if the placement is non-obvious.

Suggested next: implementing-features
</output>
</example>

</examples>

---

## Constraints

- Do not write production code — pseudocode, schemas, and interface sketches are acceptable
- Do not contradict existing ADRs silently — if superseding, write a new ADR that references and explains why
- Do not add layers, abstractions, or services that no current requirement demands (YAGNI)
- Name the principle behind each structural choice in the ADR, with its link (`applying-design-principles`)
- Always write an ADR for one-way door decisions — undocumented decisions get relitigated
- Do not make the decision without evaluating ≥2 options
- Scope: reads `.context/decisions/`, writes `.context/decisions/ADR-NNN-*.md`
