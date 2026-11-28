# Architecture

> **AI Instruction:** Read this to understand how the system is structured before making changes that cross boundaries. This answers *how the system is built* — for *why* specific choices were made, see `decisions/README.md`.

## System Overview

<!-- What are the major parts of this system and how do they relate? -->
<!-- Keep this high-level — a paragraph or simple diagram is enough -->

[e.g., Single-page React app → REST API (Express) → PostgreSQL. Background jobs via Bull queue. No microservices.]

## Layer Structure

<!-- How is the code organized into layers? What are the rules between them? -->

<!-- Example:
```
src/
├── routes/       ← HTTP handlers only — no business logic
├── services/     ← Business logic — no HTTP concerns
├── repositories/ ← Data access only — no business logic
└── models/       ← Types and schema — imported by all layers
```
Rule: dependencies flow inward only. Routes import services. Services import repositories. Never the reverse.
-->

## Key Integration Points

<!-- External systems, APIs, or services this codebase depends on -->

| Integration | Purpose | How configured |
|-------------|---------|----------------|
| | | |

## Infrastructure

<!-- Where does this run and how is it deployed? Keep it brief. -->

- **Hosting:** [e.g., AWS ECS / Vercel / Fly.io / bare metal]
- **Database:** [e.g., PostgreSQL on RDS, connection via `DATABASE_URL` env var]
- **CI/CD:** [e.g., GitHub Actions — see `.github/workflows/`]

<!-- Only add more sections if your system genuinely needs them. Keep this file focused on structure, not decisions. -->
