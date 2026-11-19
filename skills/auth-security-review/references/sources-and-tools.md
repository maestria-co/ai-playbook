# Sources and Tools

Where every checklist item comes from, the off-the-shelf tools that sit beside this skill, and what other teams learned building AI security reviewers.

---

## 1. Standards the checklists cite

| Short name | Document | Link |
| --- | --- | --- |
| RFC 9700 | OAuth 2.0 Security Best Current Practice | https://www.rfc-editor.org/rfc/rfc9700.html |
| ASVS | OWASP Application Security Verification Standard 5.0 | https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en |
| OIDC Core | OpenID Connect Core 1.0 | https://openid.net/specs/openid-connect-core-1_0.html |
| OIDC Discovery | OpenID Connect Discovery 1.0 | https://openid.net/specs/openid-connect-discovery-1_0.html |
| RP-Initiated Logout | OpenID Connect RP-Initiated Logout 1.0 | https://openid.net/specs/openid-connect-rpinitiated-1_0.html |
| RFC 8252 | OAuth 2.0 for Native Apps | https://www.rfc-editor.org/rfc/rfc8252.html |
| RFC 8725 | JSON Web Token Best Current Practices | https://www.rfc-editor.org/rfc/rfc8725.html |
| Browser BCP | OAuth 2.0 for Browser-Based Applications | https://datatracker.ietf.org/doc/draft-ietf-oauth-browser-based-apps/ |

**ASVS chapters used:** V6 Authentication, V7 Session Management, V8 Authorization, V9 Self-contained Tokens, V10 OAuth and OIDC, V14 Data Protection, V16 Security Logging and Error Handling.

**ASVS levels:** L1 is the minimum for any application. L2 is what most applications should aim for. L3 is for the highest-risk systems. The checklists require L1 and L2, because an auth service holds personal data and credentials.

## 2. Ory documentation

| Topic | Link |
| --- | --- |
| Docs index written for AI tools | https://www.ory.com/docs/llms.txt |
| Hydra production guide | https://www.ory.com/docs/hydra/self-hosted/production |
| Hydra security architecture | https://www.ory.com/docs/hydra/security-architecture |
| Hydra secrets and key rotation | https://www.ory.com/docs/hydra/self-hosted/secrets-key-rotation |
| Hydra config schema | https://github.com/ory/hydra/blob/master/spec/config.json |
| Custom login and consent flow | https://www.ory.com/docs/oauth2-oidc/custom-login-consent/flow |
| Kratos production guide | https://www.ory.com/docs/kratos/guides/production |
| Kratos security concepts | https://www.ory.com/docs/kratos/concepts/security |
| Kratos secret rotation | https://www.ory.com/docs/kratos/guides/secret-key-rotation |
| Kratos cookie settings | https://www.ory.com/docs/kratos/guides/configuring-cookies |
| Kratos config schema | https://github.com/ory/kratos/blob/master/embedx/config.schema.json |

The docs index also points to an Ory Docs MCP server for looking up a single page.

When a checklist item and the Ory docs for the pinned version disagree, the Ory docs win. Report the mismatch so the checklist gets fixed.

## 3. Off-the-shelf tools

Use these before writing anything custom. None of them is replaced by this skill.

### OpenID Foundation conformance suite

- **What it does:** runs the official protocol tests against a running OpenID Provider.
- **Why it matters:** it is the only real answer to "are we following OpenID Connect?". A code review cannot give that answer.
- **Cost:** free to use. Only formal certification has a fee.
- **How it runs:** locally in Docker, or in CI with the suite's `scripts/run-test-plan.py`.
- **Watch for:** skipping the consent screen makes the certification tests fail, so test with a client that shows consent.
- **Links:** https://openid.net/certification/about-conformance-suite/ and https://gitlab.com/openid/conformance-suite/

### Claude Code `/security-review`

- **What it does:** reviews pending changes for general vulnerability classes: injection, broken authentication and authorization, data exposure, weak cryptography, insecure configuration, cross-site scripting.
- **Cost:** ships with Claude Code. No extra install.
- **How to extend:** copy `security-review.md` into the repository's `.claude/commands/` folder and add project rules or false-positive filters.
- **GitHub Action:** `anthropics/claude-code-security-review` runs the same review on pull requests. Its README says it is not hardened against prompt injection and should review trusted pull requests only.
- **Link:** https://github.com/anthropics/claude-code-security-review

### Trail of Bits skills

- **What it is:** a free skill set from a security firm, licensed CC-BY-SA-4.0.
- **Useful here:** `spec-to-code-compliance` (code against a specification), `insecure-defaults` (settings that fail open), `differential-review` (security review of a diff), `sharp-edges` (configs that are easy to misuse), `audit-context-building` (understand the code before hunting bugs).
- **Install:** `/plugin marketplace add trailofbits/skills`
- **Link:** https://github.com/trailofbits/skills

### Community "security engineer" skills

Several exist on public skill registries. They are generic and unverified. Read one fully before installing it, because an unreviewed skill is a supply-chain risk in its own right. No published skill covering Ory was found, which is why this skill exists.

## 4. What other teams learned

These shaped the process in `SKILL.md`.

| Lesson | Where it shows up |
| --- | --- |
| A generic AI review misses authorization flaws because it does not know the product's roles | Step 2: load the role model first |
| One-pass scans report patterns, not exploitable flaws | Step 5: every finding needs an attack sentence and a traced path |
| Re-reporting the same false positive trains people to ignore the tool | Step 2: check the tracked list. Step 6: "Already tracked" |
| Deterministic tools should run first, with the AI used for judgment | "Do not use it to replace these" table |
| Agent output is a hypothesis, not a verdict | Overview, and the confidence column in the report |
| Model behavior changes between versions | Cite a requirement for every finding, so a person can check it without the model |

**Sources for these lessons:**

- https://dev.to/alanwest/why-one-shot-llm-security-audits-keep-missing-real-bugs-p41
- https://www.kunalganglani.com/blog/ai-code-review-tools-2026-compared
- https://dev.to/hopkins_jesse_cdb68cfa22c/the-5-mistakes-i-made-building-an-ai-code-review-agent-so-you-dont-have-to-770

These are practitioner write-ups without published data. Treat their numbers as anecdotes.

## 5. Keeping this skill current

- When Ory or a standard publishes a new version, re-read the linked page and update the checklist item and its citation together.
- When a real review finds a flaw no checklist item covers, add the item with its source.
- Facts about one repository (its roles, its accepted risks, its open security tickets) belong in that repository's `.context/`, not here.
