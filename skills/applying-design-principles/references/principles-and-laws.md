# Principles and Laws Catalog

One line per entry, with a link to a source that defines it. SOLID, the Rule of Three, and how to cite a principle are in `SKILL.md`.

## Code and design principles

- **DRY (Don't Repeat Yourself)**: every piece of knowledge should live in one place. It is about knowledge, not look-alike code. Use the Rule of Three before extracting. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#the-dry-principle))
- **KISS (Keep It Simple, Stupid)**: the simplest solution that works usually wins. Prefer fewer tools, files, and moving parts. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#the-kiss-principle))
- **YAGNI (You Aren't Gonna Need It)**: don't build features for problems you don't have yet. ([Fowler](https://martinfowler.com/bliki/Yagni.html))
- **Principle of Least Astonishment**: a system should behave the way a newcomer expects. If a reasonable person would be surprised by where something lives, what it is called, or what it does, change the design, not the explanation. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#the-principle-of-least-astonishment), [Raymond, The Art of Unix Programming](http://catb.org/esr/writings/taoup/html/ch01s06.html))
- **Law of Demeter**: an object should only talk to its immediate friends (avoid `a.b.c.d.doThing()`). Smell: [Message Chains](https://refactoring.guru/smells/message-chains). Fix: [Hide Delegate](https://refactoring.guru/hide-delegate). ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#the-law-of-demeter))
- **Separation of Concerns**: each module handles one distinct responsibility. ([Dijkstra, EWD447](https://www.cs.utexas.edu/~EWD/transcriptions/EWD04xx/EWD447.html))
- **Composition over Inheritance**: build behavior by combining small pieces instead of deep class trees. Fix: [Replace Inheritance with Delegation](https://refactoring.guru/replace-inheritance-with-delegation). ([Wikipedia](https://en.wikipedia.org/wiki/Composition_over_inheritance))
- **Tell, Don't Ask**: tell objects what to do instead of pulling their data out and deciding for them. Smell: [Feature Envy](https://refactoring.guru/smells/feature-envy). ([Fowler](https://martinfowler.com/bliki/TellDontAsk.html))
- **Command-Query Separation**: a method should either change state or return data, not both. ([Fowler](https://martinfowler.com/bliki/CommandQuerySeparation.html))
- **Fail Fast**: surface errors right away instead of limping along with bad state. ([Jim Shore, IEEE Software, on martinfowler.com](https://martinfowler.com/ieeeSoftware/failFast.pdf))
- **Principle of Least Privilege**: give each component only the access it needs. ([Wikipedia](https://en.wikipedia.org/wiki/Principle_of_least_privilege))
- **Rule of Three**: wait until you've written something three times before you abstract it. Smell when ignored: [Speculative Generality](https://refactoring.guru/smells/speculative-generality). ([Wikipedia](https://en.wikipedia.org/wiki/Rule_of_three_%28computer_programming%29))
- **Boy Scout Rule**: leave the code a little cleaner than you found it. Keep the cleanup inside files the change already touches, so the diff stays reviewable. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#the-scout-rule), [Fowler on opportunistic refactoring](https://martinfowler.com/bliki/OpportunisticRefactoring.html))
- **Chesterton's Fence**: don't remove something until you understand why it's there. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#chestertons-fence))
- **Design patterns (Gang of Four)**: use a pattern only when the problem it solves is already in the code, and use the pattern's standard name so readers recognize it. ([refactoring.guru catalog](https://refactoring.guru/design-patterns/catalog))
- **Tesler's Law (Conservation of Complexity)**: every system has complexity that can't be removed, only moved, so decide who carries it (the user or the developer). ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#the-law-of-conservation-of-complexity-teslers-law))

## Laws about systems and abstractions

- **Hyrum's Law**: with enough users, every observable behavior of your API will be depended on by somebody, documented or not. It pairs with Postel's Law. ([hyrumslaw.com](https://www.hyrumslaw.com/))
- **Postel's Law (Robustness Principle)**: be conservative in what you send and liberal in what you accept. At a security boundary, validate strictly instead: security comes first. ([RFC 1122 §1.2.2](https://www.rfc-editor.org/rfc/rfc1122#section-1.2.2); its costs: [RFC 9413](https://www.rfc-editor.org/rfc/rfc9413))
- **Law of Leaky Abstractions (Joel Spolsky)**: every non-trivial abstraction leaks eventually. ([Joel on Software](https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/))
- **Gall's Law**: complex systems that work grew out of simple systems that worked. Complex systems designed from scratch tend to fail. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#galls-law))
- **Conway's Law**: systems end up mirroring the communication structure of the org that builds them. ([Fowler](https://martinfowler.com/bliki/ConwaysLaw.html))
- **Zawinski's Law**: every program grows until it can read email (it's about scope creep). ([Jargon File](http://www.catb.org/jargon/html/Z/Zawinskis-Law.html))
- **Greenspun's Tenth Rule**: any sufficiently complicated program contains a half-baked version of Lisp. ([Wikipedia](https://en.wikipedia.org/wiki/Greenspun%27s_tenth_rule))
- **Fallacies of Distributed Computing**: eight false assumptions, like "the network is reliable" and "latency is zero." ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#the-fallacies-of-distributed-computing))
- **CAP Theorem**: a distributed data store can guarantee only two of Consistency, Availability and Partition tolerance. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#cap-theorem-brewers-theorem))
- **Amdahl's Law**: speeding up part of a system is capped by the part you can't parallelize. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#amdahls-law))

## Laws about teams and schedules

- **Brooks's Law**: adding people to a late software project makes it later. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#brooks-law); source: *The Mythical Man-Month*, in `sources-and-reading.md`)

## Architecture (Robert C. Martin, Eric Evans)

- **The Dependency Rule**: source code dependencies point inward, toward business rules. Business rules never import frameworks, databases, or the UI. ([The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html))
- **Ubiquitous Language**: code, tickets, and conversation use the same words the business uses. If the business says "order", the class is not `Purchase`. This is Least Astonishment applied to the domain. ([Fowler](https://martinfowler.com/bliki/UbiquitousLanguage.html))
- **Bounded Context**: one model per area of the business, with a clear edge, instead of one model that tries to fit everything. ([Fowler](https://martinfowler.com/bliki/BoundedContext.html))
- **Aggregate**: a cluster of objects that changes together and is saved together, reached through one root. ([Fowler](https://martinfowler.com/bliki/DDD_Aggregate.html))
- **Monolith First**: start with one deployable unit, and split it only when a boundary has proven itself. ([Fowler](https://martinfowler.com/bliki/MonolithFirst.html))

## Dependency injection (Mark Seemann)

- **Interfaces are not abstractions**: an interface with one implementation adds a file without decoupling anything. Add one at an I/O boundary a test must replace, or when a second implementation exists. ([Seemann](https://blog.ploeh.dk/2010/12/02/Interfacesarenotabstractions/))
- **Impureim sandwich**: read input, run pure logic, write output. A pure core gets Dependency Inversion without a framework. ([Seemann](https://blog.ploeh.dk/2020/03/02/impureim-sandwich/), [Functional architecture is Ports and Adapters](https://blog.ploeh.dk/2016/03/18/functional-architecture-is-ports-and-adapters/), [Dependency rejection](https://blog.ploeh.dk/2017/02/02/dependency-rejection/))
- **Composition Root**: build the object graph in one place at the app's entry point and pass dependencies in. ([Seemann](https://blog.ploeh.dk/2011/07/28/CompositionRoot/))
- **Service Locator is an anti-pattern**: it hides what a class needs. ([Seemann](https://blog.ploeh.dk/2010/02/03/ServiceLocatorisanAnti-Pattern/))

## Lean and continuous improvement (Toyota, *The Goal*, *The Phoenix Project*)

- **Kaizen**: improve continuously in small steps, made by the people who do the work. ([Wikipedia](https://en.wikipedia.org/wiki/Kaizen))
- **The Three Ways**: (1) make work flow fast from left to right, (2) shorten and amplify feedback from right to left, (3) build a culture of continual learning and experimentation. ([IT Revolution](https://itrevolution.com/articles/the-three-ways-principles-underpinning-devops/))
- **Theory of Constraints**: a system moves only as fast as its bottleneck. Improving anything else is waste. ([Wikipedia](https://en.wikipedia.org/wiki/Theory_of_constraints))
- **Muda (waste)**: remove work that adds no value, such as waiting, handoffs, partly done work, and unused features. ([Wikipedia](https://en.wikipedia.org/wiki/Muda_%28Japanese_term%29))
- **Stop the line (Jidoka, Andon)**: when a defect appears, stop and fix the cause before going on. A red build blocks merging. This is Fail Fast for a process. ([Autonomation](https://en.wikipedia.org/wiki/Autonomation), [Andon](https://en.wikipedia.org/wiki/Andon_%28manufacturing%29))
- **Poka-yoke (mistake-proofing)**: design the process so the mistake can't happen, such as a git hook that rejects a bad commit message. ([Wikipedia](https://en.wikipedia.org/wiki/Poka-yoke))
- **Five Whys**: ask "why?" until you reach a cause you can fix in the process, not a person to blame. ([Wikipedia](https://en.wikipedia.org/wiki/Five_whys))

## Reliability (Google SRE, Michael Nygard)

- **Service Level Objectives**: set a measurable reliability target from the user's point of view, and alert on it rather than on every metric. ([SRE book](https://sre.google/sre-book/service-level-objectives/))
- **Error budgets**: 100% reliability is the wrong target. The gap between the target and 100% is a budget to spend on shipping changes. ([Embracing Risk](https://sre.google/sre-book/embracing-risk/), [Error Budget Policy](https://sre.google/workbook/error-budget-policy/))
- **Eliminate toil**: manual, repetitive work that a machine could do should be automated. ([SRE book](https://sre.google/sre-book/eliminating-toil/))
- **Blameless postmortems**: after an incident, write down what happened and fix the system, not the person. ([SRE book](https://sre.google/sre-book/postmortem-culture/))
- **Stability patterns**: every call that crosses a network gets a timeout, and repeated failures trip a circuit breaker so one failing dependency can't take down the rest (bulkheads). ([Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/))

## Laws about debugging and quality

- **Kernighan's Law**: debugging is twice as hard as writing the code, so code written as cleverly as you can manage is code you can't debug. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#kernighans-law))
- **Linus's Law**: given enough eyeballs, all bugs are shallow. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#linuss-law))
- **Knuth's rule**: premature optimization is the root of all evil. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#premature-optimization-effect))
- **Eagleson's Law**: code you haven't looked at in six months might as well have been written by someone else. (Widely quoted; no primary source found.)
- **Cunningham's Law**: the best way to get the right answer online is to post the wrong one. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#cunninghams-law))
- **Occam's Razor**: when two explanations fit the facts, prefer the one with fewer assumptions. When you're debugging, check the simple cause (a typo, a config value, a stale cache) before you suspect the compiler or the framework. In design, pick the solution with the fewest moving parts. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#occams-razor))
- **Hanlon's Razor**: never attribute to malice what can be explained by a mistake. This is useful in code reviews and incident postmortems. ([Hacker Laws](https://github.com/dwmkerr/hacker-laws#hanlons-razor))

## UX laws (the user-facing cousins of Least Astonishment)

- **Jakob's Law**: users expect your product to work like the others they already use. ([Laws of UX](https://lawsofux.com/jakobs-law/))
- **Hick's Law**: decision time grows with the number of choices. ([Laws of UX](https://lawsofux.com/hicks-law/))
- **Fitts's Law**: bigger, closer targets are faster to click. ([Laws of UX](https://lawsofux.com/fittss-law/))

## Where to go deeper

The authors behind these ideas, what they learned the hard way, and the reading list are in `sources-and-reading.md`.
