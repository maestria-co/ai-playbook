---
name: applying-design-principles
description: Use when designing, writing, refactoring, or reviewing code or architecture and a choice needs a named principle behind it — SOLID, DRY, YAGNI, the Rule of Three, a code smell, a Gang of Four design pattern, Domain-Driven Design, Clean Architecture, lean and Kaizen, Google SRE reliability practices, or a software law such as Brooks's, Postel's, Conway's, or Hyrum's. Also use when asked "does this follow SOLID?", "is this a code smell?", "which pattern fits here?", "what would Uncle Bob, Fowler, Evans, or Seemann say about this?", or "what should I read about this?".
user-invocable: true
---

# Applying Design Principles

## Overview

Back every design choice and review finding with a named principle and a link to the source that defines it. "This breaks the Interface Segregation Principle" can be checked. "This feels wrong" cannot.

SOLID is required for all new code. The other principles and laws are tools: use the one that fits the problem in front of you.

## When to Use

- Designing a module, service, or API
- Writing or refactoring code
- Reviewing a change
- Debugging, to decide which cause to check first
- Planning people or schedules (Brooks's Law, Conway's Law)
- Designing for production, or writing up an incident (Google SRE, *Release It!*)
- Running a retrospective (Kaizen, Five Whys)

**Do not use it to** justify a pattern or layer the code does not need yet. A principle is a reason to simplify, not a licence to add.

## Order of Precedence

1. **The project's own written rules** win every conflict. Why: they record decisions this skill cannot know about.
2. **Security and privacy** come before convenience. Least privilege and strict input validation are not traded for simplicity.
3. **SOLID** is required. Breaking it in new code is a review finding.
4. **Everything in `references/principles-and-laws.md`** applies when it fits the problem. When two conflict, prefer the simpler design (KISS) and the one a newcomer would expect (Least Astonishment).

## SOLID (required)

| Principle | The rule | Smell that shows it is broken |
| --- | --- | --- |
| [Single Responsibility](https://github.com/dwmkerr/hacker-laws#the-single-responsibility-principle) | A module has one reason to change. | [Divergent Change](https://refactoring.guru/smells/divergent-change), [Large Class](https://refactoring.guru/smells/large-class) |
| [Open/Closed](https://github.com/dwmkerr/hacker-laws#the-openclosed-principle) | Add behavior by adding code, not by editing code that already works. | [Switch Statements](https://refactoring.guru/smells/switch-statements) on a type, [Shotgun Surgery](https://refactoring.guru/smells/shotgun-surgery) |
| [Liskov Substitution](https://github.com/dwmkerr/hacker-laws#the-liskov-substitution-principle) | A subtype works anywhere its base type works. | [Refused Bequest](https://refactoring.guru/smells/refused-bequest), overrides that throw "not supported" |
| [Interface Segregation](https://github.com/dwmkerr/hacker-laws#the-interface-segregation-principle) | Callers depend only on the methods they use. | Fat interfaces whose implementers stub out half the methods |
| [Dependency Inversion](https://github.com/dwmkerr/hacker-laws#the-dependency-inversion-principle) | Business rules depend on abstractions, not on databases, HTTP clients, or clocks. | Business logic that creates its own database or HTTP client |

Robert C. Martin explains why SOLID still matters in [Solid Relevance](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html).

### SOLID without over-engineering

SOLID never asks for a layer nobody uses. If following it seems to need one, re-read the principle before adding anything. Mark Seemann's rules keep SOLID and KISS on the same side:

- **One implementation is not an abstraction yet.** Add an interface only at a boundary to I/O (database, network, clock, file system) that tests must replace. Why: an interface with one implementation adds a file and a jump without decoupling anything ([Interfaces are not abstractions](https://blog.ploeh.dk/2010/12/02/Interfacesarenotabstractions/)).
- **Keep side effects at the edges.** Read input, run pure logic, write output. Why: a pure core gets you Dependency Inversion without a framework ([Impureim sandwich](https://blog.ploeh.dk/2020/03/02/impureim-sandwich/), [Functional architecture is Ports and Adapters](https://blog.ploeh.dk/2016/03/18/functional-architecture-is-ports-and-adapters/), [Dependency rejection](https://blog.ploeh.dk/2017/02/02/dependency-rejection/)).
- **Wire dependencies in one place.** Build the object graph at the app's entry point and pass dependencies in. Why: a newcomer finds every wiring decision in one file ([Composition Root](https://blog.ploeh.dk/2011/07/28/CompositionRoot/)). Never pass a service locator around, because it hides what a class needs ([Service Locator is an Anti-Pattern](https://blog.ploeh.dk/2010/02/03/ServiceLocatorisanAnti-Pattern/)).

## How to Apply

### When designing

- **Start simple and grow it** ([Gall's Law](https://github.com/dwmkerr/hacker-laws#galls-law), [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html)). Why: complex systems built from scratch rarely work. Name the principle behind each structural choice in the ADR.
- **Name things in the business's words, and draw boundaries where the business does** ([Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html), [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html), from Eric Evans's Domain-Driven Design). Why: a name the business doesn't use astonishes everyone who reads it.
- **Point dependencies inward, toward business rules** ([The Dependency Rule](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)). Why: business rules that don't import the database or framework can be tested and kept when those change.
- **Check the team shape** ([Conway's Law](https://martinfowler.com/bliki/ConwaysLaw.html)). Why: a design that cuts across how the team talks will drift back to match it.
- **Treat every observable behavior of a public API as the contract** ([Hyrum's Law](https://www.hyrumslaw.com/)). Why: someone will depend on it, so changing it is a breaking change.
- **Be strict at security boundaries, whatever Postel's Law says** ([Robustness Principle](https://github.com/dwmkerr/hacker-laws#the-robustness-principle-postels-law)). Why: security comes before convenience. Accepting malformed input at a trust boundary is how injection and parser bugs get in. [RFC 9413](https://www.rfc-editor.org/rfc/rfc9413) explains how tolerance for bad input damages protocols over time.
- **For anything that crosses a network, say which [fallacies](https://github.com/dwmkerr/hacker-laws#the-fallacies-of-distributed-computing) you are designing against, and which side of [CAP](https://github.com/dwmkerr/hacker-laws#cap-theorem-brewers-theorem) you choose.** Why: an assumption nobody wrote down is one nobody tests.

### When writing code

- **Wait for the third copy before abstracting** ([Rule of Three](https://en.wikipedia.org/wiki/Rule_of_three_%28computer_programming%29)). DRY is about one source of truth for *knowledge*, not about lines that look alike. Why: two look-alike blocks that change for different reasons are two pieces of knowledge, and merging them couples them.
- **Find out why code is there before deleting it** ([Chesterton's Fence](https://github.com/dwmkerr/hacker-laws#chestertons-fence)). Check `git log -L` or `git blame` first.
- **Measure before optimizing** ([premature optimization](https://github.com/dwmkerr/hacker-laws#premature-optimization-effect), [Amdahl's Law](https://github.com/dwmkerr/hacker-laws#amdahls-law)). Why: a speed-up to code that isn't the bottleneck costs clarity and buys nothing.
- **Leave the files you touch a little cleaner** ([Scout Rule](https://github.com/dwmkerr/hacker-laws#the-scout-rule)). Keep the cleanup inside files the change already touches. Why: unrelated cleanups make the diff hard to review.
- **Use a Gang of Four pattern only when the problem it solves is already in the code** ([refactoring.guru catalog](https://refactoring.guru/design-patterns/catalog)). Use the pattern's standard name in class names or comments. Why: a reader who knows the pattern understands the code at once, and the standard name makes it searchable.

### When reviewing

- Name the smell from the [refactoring.guru smells catalog](https://refactoring.guru/refactoring/smells), and the refactoring that fixes it from [refactoring.guru techniques](https://refactoring.guru/refactoring/techniques) or [Fowler's catalog](https://refactoring.com/catalog/).
- Rate a SOLID violation in new code as a moderate finding (it departs from a required practice). Rate a missed optional principle as minor.
- Word review comments and postmortems by [Hanlon's Razor](https://github.com/dwmkerr/hacker-laws#hanlons-razor): assume a mistake, not malice.

### When running in production

- **Set an SLO from the user's point of view and alert on it** ([SRE book](https://sre.google/sre-book/service-level-objectives/)). Why: alerts on every metric train people to ignore alerts.
- **Give every network call a timeout, and wrap flaky dependencies in a circuit breaker** ([Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/)). Why: one slow dependency without a timeout can take down every caller.
- **Automate toil** ([SRE book](https://sre.google/sre-book/eliminating-toil/)). Why: manual repeated steps are where mistakes happen, and they take time from real work.

### When debugging

- **Check the simple cause first** ([Occam's Razor](https://github.com/dwmkerr/hacker-laws#occams-razor)): a typo, a config value, a stale cache.
- **If the code is too clever to debug, simplify it, then fix it** ([Kernighan's Law](https://github.com/dwmkerr/hacker-laws#kernighans-law)).

### When planning

- **Adding people to a late project makes it later** ([Brooks's Law](https://github.com/dwmkerr/hacker-laws#brooks-law)). Cut scope or move the date instead. Why: new people need time to ramp up and add more channels for communication.
- **Find the bottleneck before speeding anything up** ([Theory of Constraints](https://en.wikipedia.org/wiki/Theory_of_constraints), as taught in *The Phoenix Project*). Why: work done faster upstream of a bottleneck just piles up in front of it.

### When improving after a task or incident

- **Run every retrospective and postmortem as Kaizen: blameless, Five Whys, one small change** ([Kaizen](https://en.wikipedia.org/wiki/Kaizen), [Blameless postmortems](https://sre.google/sre-book/postmortem-culture/)). Why: blame hides causes, and a small change that ships beats a big plan that doesn't.
- **Prefer mistake-proofing to reminders** ([Poka-yoke](https://en.wikipedia.org/wiki/Poka-yoke)). A check that blocks the mistake, such as a git hook that rejects a malformed commit message, beats a rule people must remember. Why: people forget; automated checks don't.
- **Before building something risky, read how others failed at it** ([Dan Luu's post-mortems](https://github.com/danluu/post-mortems)). Why: their outage is a free lesson.

## How to Cite a Principle

Use this format in a review finding, ADR, or PR description:

```
**<Principle>** (<link>): <what breaks it>, `<file>:<line>`.
```

Example:

```
**Interface Segregation** (https://github.com/dwmkerr/hacker-laws#the-interface-segregation-principle):
`NotificationSender` forces SMS callers to implement `sendEmail`, `src/notify/sender.ts:12`.
```

## Trusted Sources

Trust these first, and cite them by name:

- **Robert C. Martin ("Uncle Bob")**: SOLID, *Clean Code*, Clean Architecture ([blog](https://blog.cleancoder.com/))
- **Martin Fowler**: refactoring, code smells, architecture ([martinfowler.com](https://martinfowler.com))
- **refactoring.guru and the Gang of Four**: design patterns, smells, refactoring techniques ([refactoring.guru](https://refactoring.guru))
- **Mark Seemann**: dependency injection and functional architecture ([blog.ploeh.dk](https://blog.ploeh.dk/))
- **Eric Evans**: Domain-Driven Design ([DDD Reference](https://www.domainlanguage.com/ddd/reference/))
- **Hunt and Thomas**: *The Pragmatic Programmer*
- **Gene Kim**: *The Phoenix Project*, The Three Ways, lean and Kaizen
- **Google SRE**: reliability, SLOs, toil, postmortems ([free books](https://sre.google/books/))

`references/sources-and-reading.md` lists more authors (Kent Beck, Fred Brooks, Michael Nygard, Michael Feathers, Martin Kleppmann, Gregor Hohpe, Werner Vogels, and others), what each learned the hard way, and the reading list. Free online sources are marked there.

The full catalog of principles and laws is in `references/principles-and-laws.md`.
