# mje0007: Encode Six Session Lessons into Skill Kit

## Branch

`docs/mje0007-encode-session-lessons`

## Objective

Six lessons came out of a maestria-api integration-suite session (56 failing/76 passing
→ 209 passing/0 failing, PRs #19–#27). Each cost real time or caused a real mistake.
Encode each as a tight, evidence-backed rule into the existing skill kit so the next
agent doesn't repeat them. Extend existing skills — don't create new ones. One PR,
one commit per lesson.

## Acceptance Criteria

- [x] Gap for each lesson verified against current file content (not assumed)
- [x] Lesson 1 (stacked PRs) added to `skills/commit-discipline/SKILL.md`
- [x] Lesson 2 (tool success ≠ evidence) added to `skills/common-constraints/SKILL.md` Constraint 1
- [x] Lesson 3 (passing tests can be wrong) added to `skills/testing-discipline/SKILL.md`
- [x] Lesson 4 (structural fix over instance fix) added to `skills/code-quality-rules/SKILL.md`
- [x] Lesson 5 (read before recommending) added to `skills/common-constraints/SKILL.md` Constraint 3
- [x] Lesson 6 (ad-hoc completion ritual) added to `skills/common-constraints/SKILL.md` as new Constraint 8
- [x] Each change committed individually with a conventional-commit message citing the concrete failure
- [x] One PR opened against `main` with a body listing changed skills and anything deliberately omitted — PR #26

## Decisions

- **Decision:** Lesson 6 goes into `common-constraints` (new Constraint 8), not `using-skills`.
  **Rationale:** `common-constraints` is "always active during any agent work" — that's
  exactly the property needed (trigger on "a rule changed", not "a task-plan phase ended").
  `using-skills` is a discovery/navigation skill, not a completion-discipline skill, and
  `task-plan-phase-completion` already covers the task-plan-flow case (lines ~34, ~61) —
  the gap is specifically the ad-hoc-work path.
- **Decision:** Route the actual file edits to @coder (Coder agent), not write them as
  manager, since these are skill-kit deliverable files (the product itself), not
  `.context/tasks/` orchestration artifacts.
- **Decision:** One Coder dispatch covering all 6 edits + 6 commits, since the manager
  supplies the exact text for each (verified against `writing-skills` structure/tone
  conventions) — this isn't open-ended authorship, it's precise insertion.

## Key Files

- `skills/commit-discipline/SKILL.md` — add "Stacked PRs" section (Lesson 1)
- `skills/common-constraints/SKILL.md` — extend Constraint 1, Constraint 3, add Constraint 8 (Lessons 2, 5, 6)
- `skills/testing-discipline/SKILL.md` — add "Passing For the Wrong Reason" section (Lesson 3)
- `skills/code-quality-rules/SKILL.md` — add "Structural Fixes Over Instance Fixes" section (Lesson 4)

## Task Breakdown

1. [x] Verify each gap against current file content
2. [x] Create task folder, branch, plan.md
3. [x] Delegate the 6 edits + 6 commits to @coder with exact text and commit messages
4. [x] Verify commits (content present, diff review against `main`)
5. [x] Push branch, open PR with body per deliverable spec — PR #26
6. [x] Update plan.md, report to user

## Progress Log

- **2026-11-10 (final):** @coder produced all 6 commits on `docs/mje0007-encode-session-lessons`
  (`2017b8f`, `2efe94d`, `85fafc1`, `fd4b981`, `c510905`, `0bb5237`). Verified
  `git diff main` directly — each insertion lands exactly where specified across the
  4 touched files (`commit-discipline`, `common-constraints` x3, `testing-discipline`,
  `code-quality-rules`), no unrelated changes, tree clean. Pushed and opened
  https://github.com/maestria-co/ai-playbook/pull/26. Task complete.
- **2026-11-10:** Verified all six gaps by grepping/reading the five target files —
  confirmed none already cover the described content. Created branch
  `docs/mje0007-encode-session-lessons` and this plan. Next: dispatch @coder with
  exact section text and per-lesson commit messages.

## Blockers

(none)
