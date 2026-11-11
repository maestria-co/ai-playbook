---
name: testing-discipline
description: >
  Test quality standards and TDD practices. Use this skill whenever writing tests,
  reviewing test quality, deciding what to mock, choosing test strategy, or evaluating
  test coverage. Also use when you notice tests that are brittle, slow, or always
  passing regardless of implementation. Complements `writing-tests` (which handles
  test execution) with the principles that make tests actually useful.
---

# Skill: Testing Discipline

## Purpose

Tests that exist but don't catch bugs are worse than no tests — they create false
confidence. This skill focuses on test quality over test quantity: TDD workflow,
test structure, mocking strategy, anti-patterns, and when coverage numbers lie.
Use alongside `writing-tests` for the full testing workflow.

---

## TDD Process

Write the test before the implementation. This sounds simple but is frequently skipped.

### The Cycle

1. **Red** — Write a failing test that describes the desired behavior
2. **Green** — Write the minimum code to make the test pass
3. **Refactor** — Improve the code without changing behavior (tests stay green)
4. **Repeat** — Next behavior, next test

### When TDD Applies

| Situation                              | Use TDD?                                                   |
| -------------------------------------- | ---------------------------------------------------------- |
| New function with clear inputs/outputs | Yes                                                        |
| Bug fix                                | Yes — write the failing test that reproduces the bug first |
| Complex algorithm                      | Yes — build it test by test                                |
| UI/visual changes                      | Usually no — visual regression tools are better            |
| Exploratory prototyping                | No — but write tests before promoting to production        |
| Configuration changes                  | No — integration test after the change                     |

---

## Test Structure: Arrange-Act-Assert

Every test follows this pattern:

```
// Arrange — set up preconditions
const user = createTestUser({ role: 'admin' });
const service = new AuthService(mockRepo);

// Act — perform the action under test
const result = service.canAccess(user, '/admin/settings');

// Assert — verify the outcome
expect(result).toBe(true);
```

### Rules

- **One act per test** — if you have two "Act" sections, split into two tests
- **Clear test names** — describe the scenario and expected outcome:
  `"admin user can access admin settings"` not `"test auth"`
- **No logic in tests** — no `if`, `for`, `switch` in test code. Tests are linear.
- **Independent tests** — no test depends on another test's state or execution order

---

## Mocking Strategy

### When to Mock

| Dependency                                | Mock?                                 |
| ----------------------------------------- | ------------------------------------- |
| External API (HTTP, database, filesystem) | Yes — always                          |
| Time (Date.now, timestamps)               | Yes — for deterministic tests         |
| Random values                             | Yes — seed or inject                  |
| Internal utility functions                | No — test through them                |
| Same-module functions                     | No — test the public surface          |
| Configuration/environment                 | Depends — mock if flaky, real if fast |

### Mocking Principles

- **Mock at boundaries**, not internals. If you're mocking a private method, your
  test is too coupled to implementation.
- **Prefer fakes over mocks** when the dependency is simple. A fake in-memory database
  is clearer than 15 mock setup lines.
- **Verify interactions sparingly.** Assert on outputs first. Only verify mock calls
  when the side effect _is_ the behavior (e.g., "did it send the email?").

### Anti-Pattern: Over-Mocking

```
// BAD — mocking everything makes the test meaningless
const mockA = mock(ServiceA);
const mockB = mock(ServiceB);
const mockC = mock(ServiceC);
const result = handler(mockA, mockB, mockC);
// What are you even testing?

// GOOD — mock only the external boundary
const mockDB = createFakeDatabase();
const service = new UserService(mockDB);
const result = service.getActiveUsers();
expect(result).toHaveLength(3);
```

---

## Test Categories

### Unit Tests

- Test a single function or class
- No I/O, no network, no filesystem
- Run in < 100ms each
- **Target:** All non-trivial business logic

### Integration Tests

- Test two or more components working together
- May use a test database or test server
- Run in < 5 seconds each
- **Target:** API endpoints, database queries, service interactions

### End-to-End Tests

- Test the full user flow
- Use a running application instance
- Run in < 30 seconds each
- **Target:** Critical user paths only (login, checkout, etc.)

---

## Coverage Targets

Coverage is a signal, not a goal. 100% coverage with bad tests is worse than 70%
coverage with good tests.

### Guidelines

| Code type               | Minimum coverage               |
| ----------------------- | ------------------------------ |
| Business logic          | 80%+                           |
| Utility functions       | 90%+                           |
| API handlers            | 70%+ (integration tests)       |
| Configuration/glue code | 50%+                           |
| Generated code          | 0% (don't test generated code) |

### What Coverage Doesn't Tell You

- Whether edge cases are tested
- Whether assertions are meaningful
- Whether the tests would catch real bugs
- Whether the tests are maintainable

---

## Anti-Patterns

### 1. Testing Implementation, Not Behavior

```
// BAD — tests the internal method call chain
expect(service.internalHelper).toHaveBeenCalledWith(42);

// GOOD — tests the observable behavior
expect(service.calculate(42)).toBe(84);
```

### 2. Snapshot Abuse

```
// BAD — snapshot of a complex object (breaks on any change)
expect(result).toMatchSnapshot();

// GOOD — assert on specific properties that matter
expect(result.status).toBe('active');
expect(result.items).toHaveLength(3);
```

### 3. Test Names That Don't Describe Behavior

```
// BAD
it('test 1', ...)
it('should work', ...)
it('handles the case', ...)

// GOOD
it('returns 404 when user does not exist', ...)
it('retries failed payment up to 3 times', ...)
it('sends welcome email after successful registration', ...)
```

### 4. Setup Pollution

```
// BAD — shared mutable state across tests
let sharedUser;
beforeEach(() => { sharedUser = createUser(); });

// GOOD — each test creates what it needs
it('deactivates user', () => {
  const user = createUser({ active: true });
  deactivate(user);
  expect(user.active).toBe(false);
});
```

---

## Passing For the Wrong Reason

A test that passes can still be a false claim — "tests are green" means nothing if a
test never exercised what its name says it does. Three real instances from one
session:

- A test asserted `403 Forbidden` while sending NO auth token at all. It passed, but
  never exercised the authorization policy it was named after — it exercises
  authentication being missing, not authorization being denied.
- `Create_WithZeroAmount_Returns422` sent an invalid enum value alongside the zero
  amount. The request body failed to **bind** and returned 400 before the validator
  ran — the test had never once exercised the zero-amount rule it claimed to cover.
- Six test classes had dead setup code (see `code-quality-rules` on structural fixes).
  Enabling the setup made one class go from 7 failures to 8 — a test had been
  "passing" only because the broken setup never ran.

**Rules:**

- After fixing a harness, fixture, or infrastructure bug, re-examine the tests that
  were PASSING before the fix. Some were green only because the broken thing never
  executed.
- Expect the pass count to DROP before it rises once a harness bug is fixed. Treat
  that as progress and report it as such — don't read a falling count as a regression.
- Before trusting a test, ask what would have to be true for it to pass for the wrong
  reason. A test whose name describes a behavior it cannot reach is worse than no test.
- **Flaky vs. regression:** before calling a failure either one, check the test's
  history and re-run it in isolation. Example: a wall-clock test failed at 8.9s against
  a 2s budget, then ran at 245ms on re-run and 330ms on a clean trunk — machine
  contention, not a regression. Guessing either way would have been wrong.
- Prefer a structural assertion over a wall-clock one where possible. "This work
  happens off the request path" survives machine noise; "this responds in under 2s"
  doesn't.

---

## Constraints

- Never skip failing tests to make the build pass — fix the test or the code
- Never write tests that pass regardless of implementation (tautological tests)
- Test names must describe the scenario and expected outcome
- Flaky tests must be fixed immediately or quarantined with a tracking issue
- Tests are production code — apply the same quality standards
