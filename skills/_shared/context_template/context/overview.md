---
context_shape: project
---

# Project Overview

> **AI Instruction:** Read this before starting any task. Update when you discover undocumented facts about the project that aren't obvious from the code. Keep it high-level — detail belongs in subdirectory files.

---

## Project

**Name:** [PROJECT_NAME]

**Description:** [One sentence: what this system does and for whom.]

---

## Purpose & Goals

**Problem solved:** [What pain does this solve? What breaks without it?]

**Primary users:** [Who uses this? Developers? End users? Internal ops team?]

**Success looks like:** [What's the measurable outcome when this works well?]

---

## Tech Stack

| Layer | Choice | Notes |
|---|---|---|
| Language | [e.g., TypeScript 5.x] | [Any version constraints?] |
| Framework | [e.g., Next.js 14] | [App router? Pages router?] |
| Database | [e.g., PostgreSQL 15 + Prisma] | [Connection pooling?] |
| Auth | [e.g., NextAuth.js] | [Providers used?] |
| Hosting | [e.g., Vercel + Supabase] | [Region?] |
| CI/CD | [e.g., GitHub Actions] | [Workflow file location?] |
| Testing | [e.g., Vitest + Testing Library] | [Coverage reporter?] |
| Key libraries | [e.g., Zod, React Query, Tailwind] | [Any pinned versions?] |

---

## Architecture Overview

[2-4 sentences describing the system shape. E.g.: "This is a Next.js monorepo with a single server-side app. Feature logic lives in `src/features/`, shared utilities in `src/lib/`. The database is accessed exclusively through repository classes in `src/repositories/`. External services are wrapped in adapters under `src/adapters/`."]

---

## Key Directories

| Path | What lives there |
|---|---|
| `src/features/` | [Feature modules, each self-contained] |
| `src/lib/` | [Shared utilities, helpers] |
| `src/repositories/` | [Database access layer] |
| `src/adapters/` | [External service integrations] |
| `src/components/` | [Shared UI components] |
| `tests/` | [Integration tests] |
| `.context/` | [Project memory — patterns, decisions, domain knowledge] |

---

## Team Conventions

**Branch naming:** [e.g., `feat/TICKET-123-description`, `fix/TICKET-456-description`]

**PR process:** [e.g., 1 approval required, CI must pass, linked ticket required]

**Code conventions:** See `standards/` for detail. Short version: [e.g., "feature-based folder structure, no class components, Zod for all validation"]

---

## Current State

**Phase:** [e.g., MVP / Beta / Production / Maintenance]

**Actively being built:** [What's in flight right now?]

**Recently completed:** [What just shipped?]

---

## Known Constraints

- **Performance:** [e.g., API responses must be under 300ms p95]
- **Compliance:** [e.g., GDPR — no PII in logs, data residency in EU]
- **Third-party limits:** [e.g., Stripe API rate limit: 100 req/s]
- **Infrastructure:** [e.g., Vercel hobby plan — no background jobs over 10s]

---

## Links

| Resource | URL |
|---|---|
| Repository | [GitHub URL] |
| Docs / Wiki | [URL] |
| Issue tracker | [URL] |
| Staging | [URL] |
| Production | [URL] |
| CI/CD | [URL] |
