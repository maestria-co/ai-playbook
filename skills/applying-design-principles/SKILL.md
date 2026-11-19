---
name: applying-design-principles
description: Use when reviewing a change, writing or refactoring code, or making a design decision that should rest on a named principle — SOLID, DRY, the Rule of Three, a code smell, a design pattern, Domain-Driven Design, Clean Architecture, lean, SRE, or a law like Brooks's, Postel's, Conway's, or Hyrum's. Also use when asked "does this follow SOLID?", "is this a code smell?", or "what should I read about this?".
user-invocable: true
---

# Applying Design Principles

## Overview

Back each design decision and review finding with one named principle and a link to its source, so a reader can check it. SOLID is required in new code.

## Order of Precedence

1. The project's own written rules.
2. Security and privacy. At a trust boundary, validate input strictly, whatever Postel's Law says ([RFC 9413](https://www.rfc-editor.org/rfc/rfc9413)).
3. SOLID.
4. The rest of `references/principles-and-laws.md`, when it fits the problem.

## SOLID (required)

| Principle | The rule | Smell that shows it is broken |
| --- | --- | --- |
| [Single Responsibility](https://github.com/dwmkerr/hacker-laws#the-single-responsibility-principle) | One reason to change. | [Divergent Change](https://refactoring.guru/smells/divergent-change), [Large Class](https://refactoring.guru/smells/large-class) |
| [Open/Closed](https://github.com/dwmkerr/hacker-laws#the-openclosed-principle) | Add behavior by adding code, not by editing working code. | [Switch Statements](https://refactoring.guru/smells/switch-statements) on a type, [Shotgun Surgery](https://refactoring.guru/smells/shotgun-surgery) |
| [Liskov Substitution](https://github.com/dwmkerr/hacker-laws#the-liskov-substitution-principle) | A subtype works anywhere its base type works. | [Refused Bequest](https://refactoring.guru/smells/refused-bequest), overrides that throw "not supported" |
| [Interface Segregation](https://github.com/dwmkerr/hacker-laws#the-interface-segregation-principle) | Callers depend only on methods they use. | Implementers stubbing out methods |
| [Dependency Inversion](https://github.com/dwmkerr/hacker-laws#the-dependency-inversion-principle) | Business rules depend on abstractions, not on I/O. | Business logic that creates its own database or HTTP client |

An interface earns its place when it has two implementations today, or when it wraps I/O (database, network, clock, files) that a test replaces ([Seemann](https://blog.ploeh.dk/2010/12/02/Interfacesarenotabstractions/)). A class that *is* the adapter to a vendor may import that vendor.

## Duplication

Extract shared code on the third copy, not the second ([Rule of Three](https://en.wikipedia.org/wiki/Rule_of_three_%28computer_programming%29)). Two look-alike functions that encode different business rules are two pieces of knowledge, so DRY does not ask you to merge them.

## How to Cite a Principle

Each finding or decision names the one principle that best explains it:

```
**<Principle>** (<link>): <what breaks it>, `<file>:<line>`.
```

Example:

```
**Interface Segregation** (https://github.com/dwmkerr/hacker-laws#the-interface-segregation-principle):
`NotificationSender` forces SMS callers to implement `sendEmail`, `src/notify/sender.ts:12`.
```

## Review Shape

A review lists its findings in this order:

1. Bugs and build breaks
2. Security
3. SOLID breaks in new code (moderate)
4. Other principles, only where the diff itself shows the problem (minor)

## References

- `references/principles-and-laws.md`: the full catalog with a source for each entry, including Domain-Driven Design, Clean Architecture, dependency injection, lean, SRE, and the laws for debugging and planning.
- `references/sources-and-reading.md`: trusted authors (Robert C. Martin, Martin Fowler, refactoring.guru and the Gang of Four, Mark Seemann, Eric Evans, Gene Kim, Google SRE, and others), what each learned the hard way, and a reading list.
