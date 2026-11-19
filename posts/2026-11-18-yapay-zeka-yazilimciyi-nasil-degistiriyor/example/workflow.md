# My AI workflow

## 1. Before: a five-minute spec

```markdown
## Goal
One sentence: what should exist when this is done?

## Context
- Where in the codebase (files, modules)
- Existing patterns to follow (link one example)
- Constraints (no new packages, must work offline, .NET 10, Angular signals...)

## Acceptance criteria
- [ ] Given ..., when ..., then ...
- [ ] Edge cases: empty, null, very large, unauthorized user
- [ ] Errors: what the user sees when it fails

## Out of scope
What it should NOT do or touch.
```

## 2. During: rules

1. **Plan first, code second.** Ask for a plan and read it before any code is written.
2. **Small steps.** One change at a time, each one buildable and testable.
3. **Tests early.** Ask for tests from the acceptance criteria, ideally before the implementation.
4. **Never paste secrets or personal data.** Mask first (see my post on what not to share with AI).
5. **Ask for assumptions.** "List the assumptions you made." A wrong assumption breaks everything after it.
6. **Devil's advocate.** After a decision: "What is the weakest point of this, and when will it hurt?"

## 3. After: before I accept the code

- [ ] I can explain every line. If not, I ask until I can, or I rewrite it.
- [ ] It builds, tests pass, and I broke the code once on purpose to see a test fail.
- [ ] Packages and APIs it uses really exist and are current (no invented methods).
- [ ] Errors are handled, not swallowed; user input is validated on the server.
- [ ] It follows the project's existing patterns instead of inventing a new style.
- [ ] It is not more complex than the problem needs.
- [ ] The commit message explains why, in my words.
