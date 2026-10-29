# Maestria True North

These apply to **every** suggestion, plan, design, and line of code an AI assistant produces for Maestria. They are not tie-breakers — they are requirements. Any option that violates one is not a valid recommendation unless the user explicitly accepts the violation.

True North has two parts: **Core Values** (what we care about) and **Principles** (how we think).

---

## Core Values

Values are part of our internal system that guides our behavior. They are subjective, personal, and arguable — which is why each one says what it means in practice.

| Value | Meaning |
| --- | --- |
| **Free and Frugal** | We operate at the free tier at all costs. We only spend when it is our last option. |
| **Off The Shelf** | We only build product solutions. We use off the shelf products for our non-product needs. |
| **Cruise Control** | We believe in automated solutions to get the job done. People are there to ensure the automation is monitored and corrected. |
| **Bury The Treasure** | We believe in protecting people's information. |
| **K.I.S.S.** | Keep It Simple, Stupid. Think less is more. |

### How to apply them

Before making any suggestion, check it against all five:

- **Free and Frugal** — Does it run on a free tier or always-free offering? If anything costs money (even cents, a trial that expires, or a usage limit we could exceed), say what it costs, why no free option works, and how to cap the spend (budgets, alerts, hard limits).
- **Off The Shelf** — Is this our product, or a supporting need (hosting, CI/CD, auth, email, monitoring, analytics, forms)? For supporting needs, use an existing managed product or service; do not propose building it. Custom code is for the product itself.
- **Cruise Control** — Is it automated end to end (e.g., deploy on push via GitHub Actions, infrastructure as code, scheduled jobs)? Manual steps are allowed only as a one-time setup or as a human checkpoint that monitors/corrects the automation — call them out explicitly.
- **Bury The Treasure** — Does it protect people's information? Default to least privilege, no long-lived secrets (prefer OIDC/short-lived credentials), secrets in a secret manager never in code, encryption in transit and at rest, private-by-default storage, and collecting only the personal data we actually need.
- **K.I.S.S.** — Is this the simplest thing that works? Prefer fewer tools, services, files, steps, and moving parts. Don't add a layer, abstraction, or option nobody asked for. When two options both satisfy the other values, pick the one with less to build, run, and explain.

---

## Principles

Principles are objective, factual, and impersonal. They are like law. They are listed in order of thinking: apply them top to bottom.

1. **Least Astonishment** — A system should behave the way a newcomer expects. Structure, layout, and names must make the right place obvious and the wrong place unlikely. If a reasonable person would be surprised by where something lives, what it is called, or what it does, change the design — not the explanation.

### How to apply them

- Before settling on a name, folder layout, or architecture, ask: would someone new to this guess where to find it and what it does?
- Prefer one obvious convention over several clever ones, and write the convention down where the next person will look.

---

## When a core value or principle would be violated

If the only workable option — or the option the user asked for — violates a core value or a principle, **stop and tell the user before proceeding**. Use this format:

> ⚠️ **Core value conflict: <Value>** — <what violates it and why>. <Alternatives considered and why they don't work>. <What it would cost / risk, and how to limit it>.

For a principle, write **Principle conflict: <Principle>** in place of the first part.

Never silently trade one away, and never bury the conflict at the end of a long answer.
