# Ory Kratos and Ory Hydra Checklist

Config and code checks for a self-hosted Ory stack: Hydra as the OpenID Provider, Kratos as the identity provider, and a custom login and consent app between them.

Key names and defaults below were read from the Ory config schemas (`ory/hydra` `spec/config.json`, `ory/kratos` `embedx/config.schema.json`). Defaults change between releases, so confirm against the schema for the version the repository pins.

Every key can also be set as an environment variable: upper case, dots replaced by underscores (`secrets.system` becomes `SECRETS_SYSTEM`). Check Docker Compose and deployment files as well as the YAML.

---

## 1. Hydra (OpenID Provider)

### Exposure

- [ ] The admin API (default port 4445) is not published to the host or the internet. **It has no authentication of its own.** Anyone who reaches it can create clients and accept logins. (Ory Hydra production guide)
- [ ] Only the public port (default 4444) receives outside traffic, behind a gateway or load balancer that terminates TLS. (Ory Hydra production guide)
- [ ] `/oauth2/introspect` is restricted at the gateway to the services that need it. (Ory Hydra production guide)
- [ ] The gateway passes the public `Host` header and strips its routing prefix, so challenge URLs are computed correctly. (Ory Hydra production guide)

### Unsafe switches

- [ ] `dev` is `false`, and `hydra serve` has no `--dev` flag. Dev mode turns off HTTPS checks. A dev flag belongs only in a file that cannot reach production.
- [ ] `oauth2.expose_internal_errors` is `false` (the default). `true` leaks debug detail to clients.
- [ ] `log.leak_sensitive_values` is `false` (the default). `true` logs cookies and URL parameters.
- [ ] `oidc.dynamic_client_registration.enabled` is `false` (the default) unless open registration is a product requirement.

### Secrets and keys

- [ ] `secrets.system` is set, random, and at least 16 characters. If it is not set, Hydra generates one, and stored data becomes unreadable on restart. (Ory Hydra production guide)
- [ ] `secrets.cookie` is set. It falls back to `secrets.system` otherwise.
- [ ] Secrets come from a secret manager or environment, never from a committed file. Generate with `openssl rand -base64 32`.
- [ ] Secret rotation keeps the old value later in the list so existing data still decrypts. (Ory Hydra secrets and key rotation guide)
- [ ] `oauth2.session.encrypt_at_rest` is `true` (the default).
- [ ] The database connection string uses TLS (`sslmode=require` or `verify-full` for PostgreSQL) outside local development.

### Protocol settings

- [ ] `urls.self.issuer` is the exact public HTTPS URL. It becomes the `iss` claim.
- [ ] `oauth2.pkce.enforced` is `true`, or at minimum `oauth2.pkce.enforced_for_public_clients` is `true`. Neither has a default in the schema, so an unset key means PKCE is optional.
- [ ] `strategies.scope` is `exact`. The default `wildcard` lets a grant of `foo.*` match broader scopes.
- [ ] `strategies.access_token` is a deliberate choice. `opaque` (the default) needs introspection. `jwt` cannot be revoked before it expires, so keep its lifetime short.
- [ ] `ttl.access_token` (default `1h`), `ttl.id_token` (default `1h`), and `ttl.refresh_token` (default `720h`) are set on purpose. `ttl.refresh_token: -1` means never expire and is a finding.
- [ ] `ttl.auth_code` is `10m` (the default) or shorter.
- [ ] `oauth2.grant.refresh_token.rotation_grace_period` is `0s` and `rotation_grace_reuse_count` is `0` (the defaults). A grace period lets a stolen refresh token be replayed.
- [ ] `serve.cookies.same_site_mode` is `Lax` or `Strict`. The default is `None`.
- [ ] `clients.http.disallow_private_ip_ranges` is `true`. The default `false` lets client-supplied URLs (such as `jwks_uri`) reach internal services.
- [ ] `oidc.subject_identifiers.supported_types` includes `pairwise`, with a salt, when third-party clients exist. It stops them matching users across apps.
- [ ] `urls.login`, `urls.consent`, and `urls.logout` point at the login and consent app over HTTPS. `urls.post_logout_redirect` is set.
- [ ] CORS on the public endpoints (`serve.public.cors`) is off, or lists exact origins. No `*`.

### Each OAuth client

Check the registration or seeding script for every client.

- [ ] `redirect_uris` are exact HTTPS URLs. No wildcards, and no `http` outside loopback.
- [ ] `grant_types` lists only what the client uses. No `implicit`. No `password`.
- [ ] `response_types` is `["code"]`.
- [ ] `token_endpoint_auth_method` is `none` for public clients only. Confidential clients use `client_secret_basic`, `client_secret_post`, or `private_key_jwt`.
- [ ] `scope` and `audience` list only what the client needs.
- [ ] `skip_consent` is `true` only for first-party clients the same organization owns.
- [ ] `post_logout_redirect_uris` are exact and pre-registered.
- [ ] `allowed_cors_origins`, when set, lists exact origins.
- [ ] Client secrets are generated, not typed in, and never committed.

### What Hydra already does

Do not report these as missing. Check only that config has not switched them off. (Ory Hydra security architecture)

- Redirect URIs must be pre-registered, and are validated
- Authorization codes are bound to `client_id` and `redirect_uri`
- Refresh tokens rotate, and tokens derived from an abused token are revoked
- Only token signatures are stored, so a database leak does not yield usable tokens
- JSON Web Keys are encrypted at rest with AES-GCM
- Requests without a `state` or `nonce` that looks random are rejected
- Opaque tokens carry the prefixes `ory_at_`, `ory_rt_`, and `ory_ac_`, which secret scanners can detect

---

## 2. Kratos (identity provider)

### Exposure

- [ ] The admin API (default port 4434) is not published to the host or the internet. **It has no authentication of its own.** (Ory Kratos production guide)
- [ ] `kratos serve` has no `--dev` flag, and `dev` is `false`. (Ory Kratos production guide)
- [ ] `oauth2_provider.url` (Hydra's admin URL) is reachable only on the internal network.
- [ ] CORS on the public API (`serve.public.cors`) is off (the default), or lists exact origins.
- [ ] `clients.http.disallow_private_ip_ranges` is `true` when webhooks or other outgoing URLs can be configured. The default is `false`. (Ory Kratos production guide)

### Secrets and stored data

- [ ] `secrets.default`, `secrets.cookie`, and `secrets.cipher` are all set to random values. `secrets.cipher` must be 32 characters. (Ory Kratos production guide)
- [ ] `ciphers.algorithm` is `xchacha20-poly1305` or `aes`. The default `noop` stores sensitive values, such as social sign-in tokens, without encryption.
- [ ] `hashers.algorithm` is `argon2`, or `bcrypt` with `hashers.bcrypt.cost` of 12 (the default) or more.
- [ ] A production database is used. Not SQLite. (Ory Kratos production guide)
- [ ] `log.leak_sensitive_values` is `false`. `true` puts emails and other sensitive values in logs.
- [ ] The mail server connection (`courier.smtp.connection_uri`) uses TLS and its password is not committed.

### Sessions and cookies

- [ ] `session.lifespan` (default `24h`) is set on purpose and written down. (ASVS 7.1.1 L2)
- [ ] `cookies.same_site` is `Lax` (the default) or `Strict`. `None` is a finding.
- [ ] `cookies.secure` is not forced to `false` outside local development.
- [ ] `cookies.domain` and `session.cookie.domain` are as narrow as the product allows. A parent domain shares the session cookie with every subdomain.
- [ ] `selfservice.flows.settings.privileged_session_max_age` (default `1h`) is short, so changing a password or email needs a recent login. (ASVS 7.5.1 L2)
- [ ] `selfservice.flows.settings.required_aal` is `highest_available` (the default), and `session.whoami.required_aal` matches the product's multi-factor rule.

### Flows

- [ ] `selfservice.allowed_return_urls` lists exact URLs. A broad entry is an open redirect. (RFC 9700 §2.1)
- [ ] `selfservice.methods.code.config.lifespan` is `10m` or less. The default is `1h`. (ASVS 6.5.5 L2)
- [ ] Recovery and verification flow lifespans (default `1h`) are short.
- [ ] `security.account_enumeration.mitigate` is `true`, or the product accepts the risk in writing. The default `false` lets an attacker learn which accounts exist. (ASVS 6.3.8 L3)
- [ ] `selfservice.methods.password.config.haveibeenpwned_enabled` is `true` (the default), and `min_password_length` is 8 or more. (ASVS 6.2.1 L1, ASVS 6.2.12 L2)
- [ ] `selfservice.methods.password.config.ignore_network_errors` is a deliberate choice. The default `true` skips the breached-password check when the lookup fails.
- [ ] Recovery cannot bypass a second factor. (ASVS 6.4.3 L2)
- [ ] Webhooks (`web_hook` actions) call HTTPS URLs and authenticate. A webhook that must block the flow is not set to be ignored on failure.

### Rate limiting

- [ ] Login, registration, recovery, verification, and code-entry endpoints are rate limited at the gateway. **Open-source Kratos does not throttle failed logins.** Built-in brute-force protection exists only on Ory Network and the Ory Enterprise License. (Ory Kratos security concepts, ASVS 6.3.1 L1, ASVS 6.6.3 L2)
- [ ] The reverse proxy sets the client IP headers (`True-Client-IP`, `Cf-Connecting-IP`, `X-Real-IP`, `X-Forwarded-For`) from the real connection and strips values the client sent. Otherwise IP-based limits can be spoofed. (Ory Kratos security concepts)

### Identity schema

- [ ] The schema collects only the traits the product uses.
- [ ] Each login identifier (email, phone) must be verified before it is trusted.

---

## 3. Login and consent app

The custom app that Hydra redirects to. Hydra's certification does not cover this code.

**Source for every item in this section without its own citation:** Ory custom login and consent flow guide. Cite it as `ory-kratos-hydra-checklist.md §3 (Ory custom login and consent flow guide)`.

**What Hydra enforces when the app calls accept is not listed here.** Whether Hydra caps `grant_scope` or `grant_access_token_audience` to what was requested depends on the Hydra version. Do not assume it does. Give the finding the confidence "Depends on Hydra" and name the check: read the pinned version's source, or send one accept call with an extra scope on a running local stack.

### Login

- [ ] The handler fetches the request from Hydra with the `login_challenge`. It trusts nothing else in the query string.
- [ ] `acceptOAuth2LoginRequest` is called only after the user is authenticated in this request, or when Hydra returned `skip: true`.
- [ ] `subject` is the stable identity ID. Never an email, phone, or username, which can change or be reassigned. (ASVS 10.5.2 L2)
- [ ] `subject` comes from the server-side session. Never from a form field or query parameter.
- [ ] `remember_for` is a finite number of seconds. `0` means the login session never expires.
- [ ] Users who may not use OAuth are rejected with `rejectOAuth2LoginRequest`.

### Consent

- [ ] The handler fetches the request from Hydra with the `consent_challenge`, and fetches it again in the POST handler before accepting.
- [ ] `grant_scope` holds only scopes that were requested and that the user approved. **How to check:** the submitted scopes are intersected with `requested_scope` from the re-fetched request. A value taken straight from the form body fails this item. (RFC 9700 §2.3, ASVS 10.4.11 L2)
- [ ] `grant_access_token_audience` holds only audiences from the re-fetched request. (RFC 9700 §2.3)
- [ ] Any business rule that must hold before tokens are issued (for example, the account is fully set up) is enforced here, before accept.
- [ ] `remember_for` is finite and written down. (ASVS 10.7.2 L2)
- [ ] The consent screen is skipped only when Hydra returned `skip: true` or the client has `skip_consent: true`. (ASVS 10.7.1 L2)
- [ ] The list of trusted client IDs, when one exists, is short and controlled.

### Token claims set at consent

Claims added through `session.id_token` and `session.access_token` become what every API trusts.

- [ ] Every claim an API authorizes on (user ID, tenant ID, role) is looked up on the server from the `subject` in the request fetched from Hydra. Never from the form, a cookie, or the browser session. (ASVS 10.3.2 L2)
- [ ] ID token traits come from the identity whose ID equals the consent `subject`. A browser session that belongs to a different identity is rejected.
- [ ] Every path that accepts consent (the skip path and the form path) sets the same claims.
- [ ] Consent is rejected when a required claim cannot be resolved. A token missing a required claim is never issued.
- [ ] Each ID token claim is included only when its scope was granted. (OIDC Core §5.4)
- [ ] Access token claims hold opaque internal IDs only. No email, phone, name, or other personal data. With the `jwt` strategy anyone holding the token can read its claims. With `opaque`, anyone who can introspect it can. (ASVS 14.1.1 L2)

### Both

- [ ] Every reject or redirect branch returns straight after responding. A missing `return` lets execution continue into the accept path.
- [ ] The browser is sent only to the `redirect_to` value Hydra returned, and its host is checked against the expected issuer host.
- [ ] Every form carries a cross-site request forgery token, and the middleware runs before the handler. (Ory custom login and consent flow guide)
- [ ] Login, consent, and registration pages cannot be framed: `Content-Security-Policy: frame-ancestors 'none'` or `X-Frame-Options: DENY`.
- [ ] Error pages do not reveal whether an account exists. (ASVS 6.3.8 L3)
- [ ] Challenge values, verifiers, and one-time codes are not logged.
- [ ] The conformance test helper (`oidcConformityMaybeFakeSession` and `CONFORMITY_FAKE_CLAIMS` in Ory's reference app) cannot run in production.
- [ ] Cookie and CSRF secrets are required at startup. The app exits when one is missing or empty. It does not fall back to a default.

### Logout

- [ ] Logout goes through Hydra's RP-initiated logout endpoint, so every client session ends.
- [ ] The logout handler accepts the logout request only after fetching it from Hydra with the `logout_challenge`.
