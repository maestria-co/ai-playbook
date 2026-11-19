# Sources and Reading

The people below built real systems, watched some of them fail, and wrote down what they learned. Use their lessons instead of repeating their mistakes.

**(free online)** marks a source you can read in full at no cost.

## Trusted authors

| Who | What they learned the hard way | Use them for |
| --- | --- | --- |
| **Robert C. Martin ("Uncle Bob")** | Decades of consulting on codebases that became too hard to change. | SOLID, *Clean Code*, and the Dependency Rule ([The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html), [his blog](https://blog.cleancoder.com/)) **(free online)** |
| **Martin Fowler** | Refactoring legacy enterprise systems at ThoughtWorks. | Refactoring, code smells, enterprise patterns, architecture ([martinfowler.com](https://martinfowler.com), [refactoring catalog](https://refactoring.com/catalog/)) **(free online)** |
| **Kent Beck** | Created Extreme Programming and Test-Driven Development on real projects. | Simple design ([Beck Design Rules](https://martinfowler.com/bliki/BeckDesignRules.html)), small safe changes ([Tidy First?](https://tidyfirst.substack.com/)) **(free online)** |
| **Eric Evans** | Saw projects fail when the code's language drifted away from the business's. | Domain-Driven Design: naming, boundaries, models ([domainlanguage.com](https://www.domainlanguage.com/ddd/), [DDD Reference](https://www.domainlanguage.com/ddd/reference/)) **(DDD Reference free online)** |
| **The Gang of Four** (Gamma, Helm, Johnson, Vlissides) | Catalogued the designs that kept recurring in working object-oriented systems. | Design patterns ([Design Patterns](https://en.wikipedia.org/wiki/Design_Patterns), taught at [refactoring.guru](https://refactoring.guru/design-patterns)) **(refactoring.guru free online)** |
| **Mark Seemann** | Years of dependency injection and testability work in .NET and F#. | Dependency injection, functional architecture, SOLID in practice ([blog.ploeh.dk](https://blog.ploeh.dk/)) **(free online)** |
| **Andrew Hunt and David Thomas** | Working programmers; two of the authors of the Agile Manifesto. | Day-to-day craft ([The Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)) |
| **Fred Brooks** | Managed IBM's OS/360, a famously late project, and wrote down why. | Schedules, team size, conceptual integrity (*The Mythical Man-Month*) |
| **Michael Nygard** | Production outages at scale. He also proposed Architecture Decision Records. | Stability patterns such as Circuit Breaker, Bulkhead, and Timeouts ([Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/)); ADRs ([Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)) **(ADR post free online)** |
| **Michael Feathers** | Rescuing untested legacy code without rewriting it. | Getting legacy code under test safely ([Working Effectively with Legacy Code](https://www.informit.com/store/working-effectively-with-legacy-code-9780131177055)) |
| **Gene Kim** | Studied IT organizations that could and could not ship safely. | Flow, feedback, and continuous improvement ([The Phoenix Project](https://itrevolution.com/product/the-phoenix-project/), [The Three Ways](https://itrevolution.com/articles/the-three-ways-principles-underpinning-devops/), [The DevOps Handbook](https://itrevolution.com/product/the-devops-handbook-second-edition/)) |
| **Nicole Forsgren, Jez Humble, Gene Kim** | Years of survey research into what high-performing delivery teams do. | Measuring delivery ([Accelerate](https://itrevolution.com/product/accelerate/), [DORA](https://dora.dev/)) **(DORA free online)** |
| **Google SRE** (Beyer, Jones, Petoff, Murphy, editors) | Running Google's production systems. | SLOs, error budgets, toil, blameless postmortems ([SRE books](https://sre.google/books/)) **(free online)** |
| **Titus Winters, Tom Manshreck, Hyrum Wright** | Keeping Google's codebase healthy over decades. Hyrum's Law comes from here. | Code that must live a long time ([Software Engineering at Google](https://abseil.io/resources/swe-book)) **(free online)** |
| **Martin Kleppmann** | Built data infrastructure at LinkedIn. | Databases, replication, consistency trade-offs ([Designing Data-Intensive Applications](https://dataintensive.net/)) |
| **Gregor Hohpe** | Enterprise integration work and chief architect roles. | Messaging and integration patterns ([Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/)), the architect's role ([Architect Elevator](https://architectelevator.com/)) **(pattern catalog free online)** |
| **Werner Vogels** | Amazon's CTO: "everything fails all the time." | Designing for failure on AWS ([All Things Distributed](https://www.allthingsdistributed.com/), [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)) **(free online)** |
| **Matthew Skelton and Manuel Pais** | Helped organizations untangle teams and systems. | Shaping teams on purpose, with Conway's Law in mind ([Team Topologies](https://teamtopologies.com/)) |
| **Sam Newman** | Helped teams split monoliths, and warns against splitting too early. | Read before splitting any service ([Building Microservices](https://samnewman.io/books/building_microservices_2nd_edition/)); start with a monolith ([Fowler, Monolith First](https://martinfowler.com/bliki/MonolithFirst.html)) |
| **Taiichi Ohno and Toyota** | Built the Toyota Production System, the root of lean. | Kaizen, stop-the-line, removing waste ([Toyota Production System](https://global.toyota/en/company/vision-and-philosophy/production-system/), [The Toyota Way](https://en.wikipedia.org/wiki/The_Toyota_Way)) |
| **Eliyahu Goldratt** | Theory of Constraints, told as a novel in *The Goal*, the book *The Phoenix Project* follows. | Finding the bottleneck ([The Goal](https://en.wikipedia.org/wiki/The_Goal_%28novel%29)) |

## Other people's failures

- [Dan Luu's post-mortems list](https://github.com/danluu/post-mortems) collects public incident write-ups from many companies **(free online)**. Read one before designing something similar. Why: their outage is a free lesson.
- [Hacker Laws](https://github.com/dwmkerr/hacker-laws) and [Laws of UX](https://lawsofux.com) explain most entries in `principles-and-laws.md` **(free online)**.

## Reading list

### Start here, in this order

1. *The Pragmatic Programmer* (Hunt and Thomas): the broadest practical tour of these ideas. ([Amazon](https://www.amazon.com/s?k=The+Pragmatic+Programmer+20th+Anniversary+Edition))
2. *A Philosophy of Software Design* (John Ousterhout): short and sharp on complexity and module design. ([Amazon](https://www.amazon.com/s?k=A+Philosophy+of+Software+Design+Ousterhout))
3. *The Phoenix Project* (Gene Kim, Kevin Behr, George Spafford): a novel that teaches flow, Kaizen, and lean thinking in IT. ([IT Revolution](https://itrevolution.com/product/the-phoenix-project/))
4. *The Mythical Man-Month* (Fred Brooks): the source of Brooks's Law and a classic on why software projects run late. ([Amazon](https://www.amazon.com/s?k=The+Mythical+Man-Month+Brooks))
5. *Clean Code* (Robert C. Martin): code-level habits. ([Amazon](https://www.amazon.com/s?k=Clean+Code+Robert+Martin))
6. *Clean Architecture* (Robert C. Martin): the deep dive on SOLID and its relatives. ([Amazon](https://www.amazon.com/s?k=Clean+Architecture+Robert+Martin))
7. *Domain-Driven Design* (Eric Evans): modeling the business in code. ([Amazon](https://www.amazon.com/s?k=Domain-Driven+Design+Eric+Evans)) Start with the free [DDD Reference](https://www.domainlanguage.com/ddd/reference/).
8. *Site Reliability Engineering* (Google): running production systems. ([free online](https://sre.google/sre-book/table-of-contents/)) Then [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/) for how to apply it.

### When the problem in front of you calls for it

| Problem | Book |
| --- | --- |
| Changing code without breaking it | *Refactoring* (Fowler) ([catalog](https://refactoring.com/catalog/)), *Tidy First?* (Beck) |
| Changing untested legacy code | *Working Effectively with Legacy Code* (Feathers) |
| Picking a design pattern | *Design Patterns* (Gang of Four), or [refactoring.guru](https://refactoring.guru/design-patterns) **(free online)** |
| Testable, well-shaped code | *Code That Fits in Your Head* (Seemann) ([book page](https://blog.ploeh.dk/code-that-fits-in-your-head/)) |
| Surviving production | *Release It!* (Nygard) |
| Storing and moving data | *Designing Data-Intensive Applications* (Kleppmann) |
| Integrating systems with messages | *Enterprise Integration Patterns* (Hohpe and Woolf) ([patterns](https://www.enterpriseintegrationpatterns.com/)) |
| Code that must last for years | *Software Engineering at Google* ([free online](https://abseil.io/resources/swe-book)) |
| Shipping faster and safer | *The DevOps Handbook* (Kim and others), *Accelerate* (Forsgren, Humble, Kim) |
| Team structure | *Team Topologies* (Skelton and Pais) |
| Splitting a service | *Building Microservices* (Newman). Read *Monolith First* before you start. |
| Lean and continuous improvement | *The Goal* (Goldratt), *The Toyota Way* (Liker), *Lean Software Development* (Mary and Tom Poppendieck) ([overview](https://en.wikipedia.org/wiki/Lean_software_development)) |
