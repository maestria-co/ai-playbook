# OAuth 2.0 and OpenID Connect Checklist

Rules grouped by the role a component plays. Each item names its source so a finding can cite it.

**Source key**

- `RFC 9700` — OAuth 2.0 Security Best Current Practice
- `ASVS` — OWASP Application Security Verification Standard 5.0. The level (L1, L2, L3) follows the ID.
- `OIDC Core` — OpenID Connect Core 1.0
- `RFC 8252` — OAuth 2.0 for Native Apps
- `RFC 8725` — JSON Web Token Best Current Practices
- `Browser BCP` — OAuth 2.0 for Browser-Based Applications (IETF `draft-ietf-oauth-browser-based-apps`)

**Target level:** treat L1 and L2 items as required. Report L3 items as Minor unless the repository's own documents ask for L3.

---

## 1. Authorization server / OpenID Provider

With Ory, Hydra plays this role. Most items are checked in Hydra's config and in each client's registration. The config keys are in `ory-kratos-hydra-checklist.md` §1.

The "Consent and logout" items are the exception. The custom login and consent app implements them, so check them in that app's code.

### Redirects

- [ ] Redirect URIs are pre-registered per client and compared by exact string match. No wildcards. (RFC 9700 §2.1, ASVS 10.4.1 L1)
- [ ] No `http` redirect URIs, except loopback for native apps. (RFC 9700 §2.6)
- [ ] No open redirector on the authorization server or on any client. (RFC 9700 §2.1)
- [ ] Authorization responses never travel over an unencrypted connection. (RFC 9700 §2.6)
- [ ] The authorization endpoint does not allow CORS. (RFC 9700 §2.6)

### Grants and flows

- [ ] Each client is allowed only the grant types it needs. (ASVS 10.4.4 L1)
- [ ] The implicit grant is off: no `token` response type. (RFC 9700 §2.1.2, ASVS 10.4.4 L1, ASVS 10.6.1 L2)
- [ ] The resource owner password grant is off. (RFC 9700 §2.4, ASVS 10.4.4 L1)
- [ ] Each client is assigned only the scopes it needs. (ASVS 10.4.11 L2, RFC 9700 §2.3)
- [ ] Dynamic client registration is off, or it validates client metadata and requires consent. (ASVS 10.4.7 L2)

### Authorization codes and PKCE

- [ ] PKCE is supported and required for the code grant. (RFC 9700 §2.1.1, ASVS 10.4.6 L2)
- [ ] Only the `S256` challenge method is accepted. `plain` is rejected. (RFC 9700 §2.1.1, ASVS 10.4.6 L2)
- [ ] The token endpoint rejects a missing or wrong `code_verifier` when a challenge was sent, and rejects a verifier when no challenge was sent (downgrade defense). (RFC 9700 §2.1.1)
- [ ] Metadata publishes `code_challenge_methods_supported`. (RFC 9700 §2.1.1)
- [ ] An authorization code works once. Reuse is rejected and the tokens issued from it are revoked. (ASVS 10.4.2 L1)
- [ ] Authorization codes live 10 minutes or less. (ASVS 10.4.3 L1)

### Tokens

- [ ] Refresh tokens for public clients rotate on use or are sender-constrained. Reuse of a rotated token revokes the whole chain. (RFC 9700 §2.2.2, ASVS 10.4.5 L1)
- [ ] Refresh tokens have an absolute expiry, even with sliding expiry. (ASVS 10.4.8 L2)
- [ ] Access tokens carry the least privilege needed and are restricted to an audience. (RFC 9700 §2.3)
- [ ] Users can revoke refresh tokens and consents. (ASVS 10.4.9 L2, ASVS 10.7.3 L2)
- [ ] Clients cannot choose their own `client_id` or other values that could be mistaken for a real user's subject. (RFC 9700 §2.6)

### Client authentication

- [ ] Confidential clients authenticate on every back-channel request: token, revocation, introspection. (ASVS 10.4.10 L2, RFC 9700 §2.5)
- [ ] Public clients (browser and mobile apps) hold no client secret. (RFC 8252 §8.5)
- [ ] Asymmetric client authentication (`private_key_jwt` or mutual TLS) is preferred over shared secrets. (RFC 9700 §2.5, ASVS 10.4.16 L3)

### Consent and logout

- [ ] Consent is requested for each authorization request, and always when the client's identity cannot be assured. (ASVS 10.7.1 L2)
- [ ] The consent screen names the application, the permissions, and how long the grant lasts. (ASVS 10.7.2 L2)
- [ ] Consent is skipped only for first-party clients the same organization owns.
- [ ] Logout requests need user confirmation or a valid `id_token_hint`, so a third party cannot force a logout. (ASVS 10.6.2 L2)
- [ ] `post_logout_redirect_uri` values are pre-registered per client and matched exactly. (OpenID Connect RP-Initiated Logout 1.0 §2)

### Discovery

- [ ] Authorization Server Metadata is published. (RFC 9700 §2.6)
- [ ] The `issuer` value in metadata is the exact HTTPS URL that appears in the `iss` claim of every token. (OIDC Discovery 1.0 §4.3)

### Level 3, report as Minor

- [ ] Pushed authorization requests (PAR) for the code grant. (ASVS 10.4.13 L3)
- [ ] Sender-constrained access tokens with mutual TLS or DPoP. (RFC 9700 §2.2.1, ASVS 10.4.14 L3)
- [ ] Only the `response_mode` values each client needs. (ASVS 10.4.12 L3)

---

## 2. OAuth client / relying party

A backend-for-frontend, a web app, or a mobile app that starts the login and receives tokens.

### Starting the flow

- [ ] The client uses the authorization code flow with PKCE. Public clients must. Confidential clients should. (RFC 9700 §2.1.1)
- [ ] `code_verifier`, `state`, and `nonce` are created with a cryptographic random source, are fresh for every request, and are bound to the user's browser session. (RFC 9700 §2.1.1, ASVS 10.1.2 L2)
- [ ] The client requests only the scopes it needs. (ASVS 10.2.3 L3)
- [ ] Endpoints come from the provider's metadata, and the client rejects metadata whose `issuer` does not exactly match the configured issuer. (RFC 9700 §2.6, ASVS 10.5.3 L2)

### Receiving the response

- [ ] The callback accepts a code only for a flow the same browser session started. (ASVS 10.1.2 L2, RFC 9700 §2.1.1)
- [ ] The flow is protected against cross-site request forgery by PKCE or by checking `state`. (RFC 9700 §2.1, ASVS 10.2.1 L2)
- [ ] A client that talks to more than one authorization server checks the `iss` response parameter. (RFC 9700 §2.1, ASVS 10.2.2 L2)
- [ ] `error` and `error_description` from the callback are treated as untrusted input and never rendered as HTML.

### Validating the ID token (OIDC Core §3.1.3.7)

- [ ] The signature is verified with a key from the provider's JWKS. (ASVS 6.8.2 L2, ASVS 9.1.1 L1)
- [ ] The algorithm is on an allowlist. `none` is rejected. (ASVS 9.1.2 L1, RFC 8725 §3.1)
- [ ] `iss` exactly matches the configured issuer.
- [ ] `aud` contains this client's `client_id`. (ASVS 10.5.4 L2)
- [ ] `exp` is in the future, and `iat` is recent. (ASVS 9.2.1 L1)
- [ ] `nonce` matches the value sent in the request. (ASVS 10.5.1 L2)
- [ ] `auth_time`, `acr`, and `amr` are checked when the app needs a certain strength or recency of login. (ASVS 6.8.4 L2)
- [ ] The user is identified by `iss` plus `sub`. Never by email or phone, which can be reassigned. (ASVS 10.5.2 L2, OIDC Core §5.7)
- [ ] An ID token is never sent to an API as an access token. (ASVS 9.2.2 L2)
- [ ] The `sub` returned by UserInfo matches the `sub` in the ID token. (OIDC Core §5.3.2)

### Keeping tokens

- [ ] Tokens go only to the components that need them. A browser app keeps them on the server in a backend-for-frontend. (ASVS 10.1.1 L2, Browser BCP)
- [ ] No token is stored in `localStorage`, `sessionStorage`, or IndexedDB. (ASVS 14.3.3 L2, Browser BCP)
- [ ] Token cookies are `HttpOnly`, `Secure`, and `SameSite=Lax` or `Strict`, and use the `__Host-` prefix where the path allows it.
- [ ] Backend-for-frontend endpoints that use those cookies have cross-site request forgery protection.
- [ ] The backend-for-frontend pins `client_id` and `redirect_uri` on the server. It does not pass through values the browser supplied.
- [ ] Tokens never appear in URLs, logs, or error messages. (ASVS 14.2.1 L1)
- [ ] Logout revokes the refresh token and clears the cookies. (ASVS 7.4.1 L1)

### Mobile apps (RFC 8252)

- [ ] Login opens the system browser (`ASWebAuthenticationSession`, Custom Tabs). No embedded web view. (RFC 8252 §8.12)
- [ ] The redirect is a claimed `https` link or a private-use scheme the app owns. (RFC 8252 §7)
- [ ] No client secret ships in the app. (RFC 8252 §8.5)
- [ ] Tokens are stored in the platform keystore (Keychain, Keystore).

### Back-channel logout, when used

- [ ] The logout token's type, `events` claim, and absence of `nonce` are checked, and it is short-lived. (ASVS 10.5.5 L2)

---

## 3. Resource server

Any API that accepts an access token.

- [ ] Every request's token is validated on the server: signature for a JWT, introspection for an opaque token. (ASVS 9.1.1 L1, ASVS 7.2.1 L1)
- [ ] The JWT algorithm is pinned to an allowlist. `none` is rejected, and a symmetric algorithm is never accepted where an asymmetric key is expected. (ASVS 9.1.2 L1, RFC 8725 §3.1)
- [ ] Signing keys come only from the configured issuer's JWKS URL. `jku`, `x5u`, and `jwk` headers in the token are ignored. (ASVS 9.1.3 L1)
- [ ] `iss` matches the configured issuer exactly.
- [ ] `aud` names this API. Tokens issued for another service are refused. (RFC 9700 §2.3, ASVS 10.3.1 L2, ASVS 9.2.3 L2)
- [ ] `exp` and `nbf` are enforced. (ASVS 9.2.1 L1)
- [ ] The token type is checked, so an ID token or a refresh token is not accepted as an access token. (ASVS 9.2.2 L2, RFC 8725 §3.11)
- [ ] Authorization decisions use `sub`, `scope`, and other claims from the token. Never values the caller put in the request body or headers. (ASVS 10.3.2 L2)
- [ ] The user is identified by `iss` plus `sub`. (ASVS 10.3.3 L2)
- [ ] Endpoints that need a strong or recent login check `acr`, `amr`, or `auth_time`. (ASVS 10.3.4 L2)
- [ ] The introspection endpoint is reachable only by the services that need it.
- [ ] Machine-to-machine tokens (client credentials) are told apart from user tokens, and each is limited to its own endpoints.
- [ ] TLS is used end to end between client and API. (RFC 9700 §2.6)
