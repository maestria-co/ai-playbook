---
name: code-quality-rules
description: Use when conducting a code review and evaluating whether a change meets project quality standards.
user-invocable: false
---

# Code Quality Rules

## Overview

Specifies assessment standards, issue severity rankings, and a systematic multi-pass inspection methodology. These guidelines govern evaluation of any codebase modification.

## Assessment Standards

**Code Hygiene**: Purge all commented-out code blocks. Strip debug print statements. Never silently swallow exceptions—handle errors explicitly at every failure point. Never commit secrets—use environment variables. Choose descriptive identifiers consistently. Replace magic numbers with named constants. Apply the Don't Repeat Yourself principle rigorously.

**Security Posture**: Never expose sensitive data through logging or error messages. Validate and sanitize all untrusted input at system boundaries. Prevent SQL injection through parameterized queries exclusively. Apply output encoding to block XSS attacks. Ban eval() and related dynamic execution. Verify auth/authz implementation thoroughly—confirm authorization logic executes at the service tier, never solely in presentation layers. Keep credentials out of repositories. New API endpoints and data paths must enforce access restrictions. Changes touching authentication or authorization warrant heightened scrutiny—verify modifications don't accidentally broaden permissions.

**Performance Characteristics**: Eliminate N+1 query antipatterns. Release resources explicitly—close database connections, file handles, network streams. Move computationally expensive operations away from hot execution paths.

**Test Coverage**: New features require corresponding test cases. Assertions must verify genuine behavior, not merely mock presence. Include edge cases and failure scenarios in test suites. Avoid polluting production code with test-only methods. When altering decision logic, verify presence of the standardized **Coverage Evidence Block** from `testing-discipline`. Consider this coaching guidance: flag missing evidence as developmental feedback, not automatic rejection.

**Verification Evidence**: Confirm build and test execution actually occurred—demand output artifacts or reproducible steps, never accept assumptions.

**Maintainability Factors**: Limit method length to reasonable bounds. Manage cyclomatic complexity actively. Preserve clear responsibility boundaries between components. Prevent circular dependency graphs.

## Structural Fixes Over Instance Fixes

When a bug class is "this recurs whenever someone forgets," fix the structure, not
the instances. Prefer the fix that makes the mistake impossible over the one that
makes it merely discouraged. Four examples from one session:

- Six test classes wrote `public new async Task InitializeAsync()` where they meant
  `override`. `new` hides the method without joining the interface map, so the test
  framework silently called the base version and all six classes' seeding never ran —
  no compiler warning, 41 of 56 suite failures. The fix was not correcting six
  keywords: the base entry point was made non-virtual and delegates to a new
  `protected virtual SeedAsync()`, so the mistake became impossible to repeat.
- Removing a blanket `InvalidOperationException → 409` mapping broke five tests,
  because five genuine conflicts had silently depended on it. The fix was a
  `ConflictException` base type matched once by the middleware, so the next conflict
  is correct by construction instead of by convention.
- A reflection test now fails the build if any request body has a non-nullable enum,
  lacks a validator, or lacks a null-check rule — enforcing the pattern structurally
  instead of relying on review catching it.
- A shared `NotDeleted` SQL predicate replaced copy-pasted filters, with the
  deliberate exceptions documented at each opt-out site.

**Corollary — record exceptions explicitly:** when you add a guard, name the
deliberate exceptions (an explicit allow-list, a comment at each opt-out site) so a
future tidy-up can't silently remove them. Add a test that fails if an allow-list
entry goes stale.

**Corollary — find what taught the bug:** a README in the repo where the `new`/
`override` mistake occurred explicitly recommended the `new` keyword — that's how the
mistake reached six files. When you fix a recurring mistake, find and fix whatever
taught it, not just the code that learned it.

## Severity Classifications

**Critical Priority**: Security vulnerabilities, data corruption risks, runtime crashes, breaking modifications to public contracts, faulty business logic implementation.

**Moderate Priority**: Performance degradation, absent error handling, missing test coverage for critical paths, departure from established architectural patterns.

**Minor Priority**: Style inconsistencies beyond linter scope, documentation enhancement opportunities, discretionary refactoring suggestions.

## Focused Review Methodology

Execute comprehensive reviews through multiple targeted inspection passes rather than attempting omniscient single-pass review. Each pass concentrates on a specific quality dimension to prevent oversight.

### Pass 1: Logic & Correctness
- Does implementation fulfill stated requirements?
- Are boundary errors, null scenarios, or timing hazards present?
- Do error paths receive handling equal to success paths?
- Does execution flow align with intended semantics?

### Pass 2: Security & Trust Perimeter
- Does input validation occur before consumption?
- Does authorization enforcement happen at service boundaries (not UI only)?
- Are credentials, tokens, and PII handled securely (never logged, never exposed)?
- Do newly introduced endpoints and data access channels enforce access policies?
- Are database queries parameterized? Is output properly encoded?

### Pass 3: System Integration & Ripple Effects
- How do these modifications interact with surrounding code?
- Could unintended consequences affect dependent components?
- Do shared utility changes propagate correctly to consumers?
- Can database schema changes support backward compatibility?
- Can API modifications preserve existing contracts?

### Pass 4: Clarity & Long-term Sustainability
- Could an unfamiliar developer comprehend this without external documentation?
- Are identifiers meaningful and consistent with project conventions?
- Is complexity warranted, or could simpler approaches achieve identical outcomes?
- Are unexplained literal values, cryptic abbreviations, or deceptive names present?

### Pass 5: Substantiation & Scope Adherence
- Did the author execute build processes and provide tangible evidence?
- Do tests exist for new functionality with assertions verifying actual behavior?
- Are specification requirements comprehensively addressed?
- Does scope creep introduce changes beyond stated objectives?

### Appropriate Pass Selection

**Complete multi-pass inspection**: New feature development, cross-module modifications, security-critical code, public interface changes.

**Condensed inspection (Passes 1, 4, 5 exclusively)**: Isolated bug fixes, documentation updates, configuration adjustments, test augmentations.

Review output should employ the standard Findings taxonomy (Critical / Moderate / Minor), annotating which pass surfaced each finding—this contextualizes the issue category for the author.
