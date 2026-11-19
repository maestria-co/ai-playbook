# Authentication, Authorization, and Personal Data Checklist

Checks that apply to any service, whatever its OAuth role. IDs refer to OWASP Application Security Verification Standard (ASVS) 5.0. The level (L1, L2, L3) follows the ID.

**Target level:** treat L1 and L2 items as required. Report L3 items as Minor unless the repository's own documents ask for L3.

---

## 1. Authentication

### Passwords

- [ ] Minimum length is 8, and 15 or more is encouraged. Passwords of 64 characters or more are accepted. (6.2.1 L1, 6.2.9 L2)
- [ ] No composition rules, and no forced periodic change. (6.2.5 L1, 6.2.10 L2)
- [ ] New passwords are checked against common and breached password lists. (6.2.4 L1, 6.2.12 L2)
- [ ] Passwords are verified exactly as typed. No truncation, no case change. (6.2.8 L1)
- [ ] Paste and password managers work. (6.2.7 L1)
- [ ] Changing a password needs the current password. (6.2.3 L1)

### Every login path

- [ ] Every way to authenticate is written down, and the same strength is enforced on each. No undocumented path exists. (6.1.3 L2, 6.3.4 L2)
- [ ] Rate limiting or another brute-force defense covers every credential check, without letting an attacker lock real users out. (6.1.1 L1, 6.3.1 L1)
- [ ] No default accounts. (6.3.2 L1)
- [ ] Multi-factor authentication is required, or its absence is a written decision. (6.3.3 L2)
- [ ] Responses do not reveal whether an account exists, through message, status code, or timing. This includes registration and recovery. (6.3.8 L3)
- [ ] Users are told when their credentials, email, or phone change. (6.3.7 L3)

### One-time codes and out-of-band factors

- [ ] A code works once. (6.5.1 L2)
- [ ] Codes come from a cryptographic random source and have at least 20 bits of entropy (6 digits). (6.5.3 L2, 6.5.4 L2)
- [ ] Codes expire in 10 minutes or less. (6.5.5 L2)
- [ ] A code is bound to the login attempt that requested it and cannot be used on another. (6.6.2 L2)
- [ ] Code entry is rate limited. (6.6.3 L2)
- [ ] SMS or phone codes go only to numbers already verified, and a stronger option is offered. (6.6.1 L2)
- [ ] Email as an authentication factor is a known weakness at the highest level. Record it as an accepted risk if the product relies on it. (6.3.6 L3)

### Recovery

- [ ] Recovery cannot bypass multi-factor authentication. (6.4.3 L2)
- [ ] Recovery and activation codes are random, short-lived, and single-use. (6.4.1 L1)
- [ ] No security questions or password hints. (6.4.2 L1)

---

## 2. Sessions

- [ ] Session tokens are verified on a trusted backend. (7.2.1 L1)
- [ ] Session tokens are random with at least 128 bits of entropy. No static API keys used as sessions. (7.2.2 L1, 7.2.3 L1)
- [ ] A new session token is issued at login, and the old one ends. (7.2.4 L1)
- [ ] Inactivity timeout and absolute lifetime exist and are written down. (7.1.1 L2, 7.3.1 L2, 7.3.2 L2)
- [ ] Logout ends the session on the server. A terminated session cannot be used again. (7.4.1 L1)
- [ ] Disabling or deleting an account ends all its sessions. (7.4.2 L1)
- [ ] Changing a password, email, phone, or factor requires a fresh login. (7.5.1 L2)
- [ ] Users can end their other sessions after changing a factor. (7.4.3 L2)
- [ ] Logout is easy to find on every signed-in page. (7.4.4 L2)
- [ ] In a single sign-on setup, the systems that hold sessions, their lifetimes, and how they end together are written down. (7.1.3 L2, 7.6.1 L2)

### Cookies

- [ ] Session and token cookies are `HttpOnly` and `Secure`.
- [ ] `SameSite` is `Lax` or `Strict`.
- [ ] The cookie domain is as narrow as possible. The `__Host-` prefix is used where the path allows it.
- [ ] Every state-changing request has cross-site request forgery protection, and the check runs before the handler.
- [ ] No setting that turns off secure cookies is on by default, including in example environment files.

---

## 3. Authorization

- [ ] The rules for who may call each function and read each record are written down. (8.1.1 L1)
- [ ] Every endpoint checks that the caller has explicit permission for the function. (8.2.1 L1)
- [ ] Every read and write of a record checks that the caller may access that specific record. An ID in the URL or body is never enough. (8.2.2 L1)
- [ ] Field-level rules stop a caller reading or writing fields they should not, such as a role or owner field on an update. (8.2.3 L2)
- [ ] Authorization runs on the server. Hidden buttons and client-side checks do not count. (8.3.1 L1)
- [ ] The decision uses the identity from the validated session or token. Never a user ID, role, or tenant from the request.
- [ ] In a multi-tenant system, a caller cannot touch another tenant's data. (8.4.1 L2)
- [ ] A service acting for a user uses the user's permissions, not its own broader ones. (8.3.3 L3)
- [ ] Admin interfaces have more than network location protecting them. (8.4.2 L3)
- [ ] Service-to-service calls authenticate the calling service, and each service may call only the endpoints it needs.
- [ ] New endpoints deny by default. A route with no authorization check is a finding unless it is public on purpose and says so.

**How to check:** for each changed endpoint, ask "what stops user A calling this with user B's ID?" and find the line that stops it.

---

## 4. Personal data

- [ ] Only the personal data the product needs is collected. Each new field has a stated purpose.
- [ ] Sensitive data is identified and classified, including data that is only encoded, such as JWT payloads. Report a gap here only when the change adds a new kind of personal data that no document covers. (14.1.1 L2)
- [ ] ID token and access token claims hold the minimum. A JWT is readable by anyone who holds it.
- [ ] Sensitive data travels in the body or headers. Never in a URL or query string. (14.2.1 L1)
- [ ] API responses return only the fields the caller needs. (14.2.6 L3)
- [ ] Sensitive data is not sent to third parties such as analytics or trackers. (14.2.3 L2)
- [ ] Responses with sensitive data carry `Cache-Control: no-store`. (14.3.2 L2)
- [ ] The browser stores no sensitive data in `localStorage`, `sessionStorage`, or IndexedDB. (14.3.3 L2)
- [ ] Client storage is cleared at logout. (14.3.1 L1)
- [ ] Data is encrypted in transit and at rest. Database connections use TLS outside local development.
- [ ] Storage is private by default.
- [ ] Data that is no longer needed is deleted on a schedule, and a deleted account's data is removed. (14.2.7 L3)

---

## 5. Logging and errors

- [ ] Logs never contain passwords, tokens, one-time codes, session IDs, secrets, or full personal data. Mask or hash them. (16.2.5 L2)
- [ ] Every login attempt, pass or fail, is logged with the method used. (16.3.1 L2)
- [ ] Failed authorization checks are logged. (16.3.2 L2)
- [ ] Each log entry has time, actor, and action. (16.2.1 L2)
- [ ] User-controlled values are encoded before logging, so they cannot forge log lines. (16.4.1 L2)
- [ ] Errors shown to users are generic. No stack traces, queries, keys, or tokens. (16.5.1 L2)
- [ ] A failed check stops the request. Nothing fails open. (16.5.3 L2)
- [ ] A missing or empty secret stops the service at startup. It does not fall back to a default.

---

## 6. Secrets

- [ ] No secret, key, or token is committed. This includes example files and test fixtures holding real values.
- [ ] Secrets live in a secret manager. Short-lived credentials (OIDC federation) are used where the platform offers them.
- [ ] Every secret is generated by a cryptographic random source.
- [ ] Each role and service account has the least privilege it needs.
