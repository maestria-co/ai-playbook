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

## How to Apply

### When designing

- **Start simple and grow it** ([Gall's Law](https://github.com/dwmkerr/hacker-laws#galls-law), [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html)). Why: complex systems built from scratch rarely work. Name the principle behind each structural choice in the ADR.
- **Name things in the business's words, and draw boundaries where the business does** ([Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html), [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html), from Eric Evans's Domain-Driven Design). Why: a name the business doesn't use astonishes everyone who reads it.
- **Point dependencies inward, toward business rules** ([The Dependency Rule](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)). Why: business rules that don't import the database or framework can be tested and kept when those change.
- **Check the team shape** ([Conway's Law](https://martinfowler.com/bliki/ConwaysLaw.html)). Why: a design that cuts across how the team talks will drift back to match it.
- **Treat every observable behavior of a public API as the contract** ([Hyrum's Law](https://www.hyrumslaw.com/)). Why: someone will depend on it, so changing it is a breaking change.
- **For anything that crosses a network, say which [fallacies](https://github.com/dwmkerr/hacker-laws#the-fallacies-of-distributed-computing) you are designing against, and which side of [CAP](https://github.com/dwmkerr/hacker-laws#cap-theorem-brewers-theorem) you choose.** Why: an assumption nobody wrote down is one nobody tests.

### When writing code

- **Find out why code is there before deleting it** ([Chesterton's Fence](https://github.com/dwmkerr/hacker-laws#chestertons-fence)). Check `git log -L` or `git blame` first.
- **Measure before optimizing** ([premature optimization](https://github.com/dwmkerr/hacker-laws#premature-optimization-effect), [Amdahl's Law](https://github.com/dwmkerr/hacker-laws#amdahls-law)). Why: a speed-up to code that isn't the bottleneck costs clarity and buys nothing.
- **Leave the files you touch a little cleaner** ([Scout Rule](https://github.com/dwmkerr/hacker-laws#the-scout-rule)). Keep the cleanup inside files the change already touches. Why: unrelated cleanups make the diff hard to review.
- **Use a Gang of Four pattern only when the problem it solves is already in the code** ([refactoring.guru catalog](https://refactoring.guru/design-patterns/catalog)). Use the pattern's standard name in class names or comments. Why: a reader who knows the pattern understands the code at once, and the standard name makes it searchable.

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

Name each smell from the [refactoring.guru smells catalog](https://refactoring.guru/refactoring/smells) and the refactoring that fixes it ([refactoring.guru techniques](https://refactoring.guru/refactoring/techniques), [Fowler's catalog](https://refactoring.com/catalog/)). Word comments by [Hanlon's Razor](https://github.com/dwmkerr/hacker-laws#hanlons-razor): assume a mistake, not malice.

## Reading a Linked Source

When you need more from a linked source than this skill says, run:

```bash
python3 <this skill's base directory>/scripts/fetch_link.py <url>
```

It prints the page as markdown from this skill's `cache/` folder, and fetches the page only when there is no copy or the copy is more than 60 days old. A link with `#section` prints only that section. Use it instead of a web fetch tool for every link in this skill.

## References

- `references/principles-and-laws.md`: the full catalog with a source for each entry, including Domain-Driven Design, Clean Architecture, dependency injection, lean, SRE, and the laws for debugging and planning.
- `references/sources-and-reading.md`: trusted authors (Robert C. Martin, Martin Fowler, refactoring.guru and the Gang of Four, Mark Seemann, Eric Evans, Gene Kim, Google SRE, and others), what each learned the hard way, and a reading list.
