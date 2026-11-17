---
name: agent-system-audit
description: Use when evaluating or auditing an agent system design, reviewing agent definitions for role overlap or responsibility leakage, or when orchestrator routing clarity, skill responsibility, or sub-agent job clarity is in question.
user-invocable: true
---

# Agent System Audit

## Overview

**Crisp boundaries distinguish scalable architectures from deteriorating ones.** Every problem belongs to exactly one resolver; every skill executes exactly one operation; routing intelligence resides solely in the orchestrator.

## Application Scenarios

- Architecting a fresh agent framework
- Auditing deployed agent specifications for overlap or drift
- Investigating anomalous agent conduct potentially rooted in structural flaws
- Pre-publication validation of agent frameworks

---

Assess the presented agent architecture against these 5 principles:

PRINCIPLE 1 — PROMPT vs SKILL DEMARCATION
- Decision-making, reasoning mechanisms, and conditional triggers → reside in agent prompts
- Output schemas, API invocations, transformation templates → reside in skill specifications
- Flag reasoning embedded in skills that should migrate to prompts
- Flag templates embedded in prompts that should migrate to skills

PRINCIPLE 2 — INFORMATION SINGULARITY
- Every constraint or rule must occupy exactly ONE location
- Flag duplicated rules appearing across multiple definitions
- Flag behaviors potentially governed by competing directives

PRINCIPLE 3 — SUB-AGENT ROLE PRECISION
- Every sub-agent must possess ONE unambiguous responsibility articulable as an answerable question
- Its product must flow to the orchestrator prior to skill invocation
- Flag sub-agents with overlapping jurisdictions
- Flag sub-agents bypassing orchestrator to communicate directly with skills
- Flag sub-agents with vague or multiply-interpretable mandates

PRINCIPLE 4 — SKILL OPERATIONAL SCOPE
- Skills must execute ONE action (format/invoke/return)
- Skills must exclude reasoning, conditionals, or decision trees
- Skills must specify clear, structured response contracts
- Flag skills containing decision logic rather than mere execution
- Flag skills whose behavior varies by calling context

PRINCIPLE 5 — ORCHESTRATOR AUTHORITY
- Orchestrators must monopolize all routing determinations
- Orchestrators must exclusively invoke terminal skills
- Orchestrators must aggregate all sub-agent responses before skill invocation
- Flag routing intelligence distributed outside orchestrators
- Flag pathways permitting sub-agents to trigger terminal skills

---

Per principle, structure responses as:

PRINCIPLE [N] — [PASS / WARNING / FAIL]
Finding: [observed pattern]
Problem: [architectural risk introduced]
Fix: [concrete remediation]

---

Post-evaluation, synthesize:

OVERALL HEALTH: [CLEAN / NEEDS WORK / RESTRUCTURE REQUIRED]

PRIORITY FIXES: (urgency-ordered)
1. [highest-priority remediation]
2. [subsequent remediation]
3. [etc.]

OPEN QUESTIONS: (required clarifications before implementing fixes)
1. [clarification needed]
2. [etc.]

---

## Anti-Rationalization Audit

When adding or editing Anti-Rationalization rows in any agent:

1. Read every item in the agent's **Process** section.
2. Check for direct contradictions — a Process step that would require the behavior the Anti-Rationalization row forbids.
3. Remove or reword any conflicting Process step before committing.

A contradiction between Process and Anti-Rationalization is worse than a gap — the agent will exhibit inconsistent behavior on every invocation.
