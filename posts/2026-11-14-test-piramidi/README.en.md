🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# Why write tests? What is the test pyramid?

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** Automated tests are code that checks, **within seconds after every change**, that other code behaves as expected. Their real value is not finding a bug once, but letting you **change code without fear**. The **test pyramid**, proposed by Mike Cohn and popularized by Martin Fowler, is a balance: many fast, cheap **unit tests** at the base, fewer **integration tests** in the middle, and very few slow, brittle **end-to-end (e2e) tests** at the top. The logic is simple: the higher a test sits, the more realistic it is, but also the slower, more expensive and harder to maintain.

## 1. What I researched and why

On the quality planet, after tools (terminal, Git), testing is what I was most curious about. To be honest, I often treated tests as something to do "if there is time left". But once AI started writing code, my view changed: if I am not the one writing the code, how do I know it works? By clicking through it by hand every time? Tests look like the safety net for code written by AI.

## 2. Three key takeaways

1. **The real benefit of tests is the courage to change things.** In a codebase without tests every change is a gamble: "if I fix this, will I break something else?" That fear makes people avoid changes, and the code rots. Tests give:
   - **Regression safety:** noticing immediately that something that worked yesterday broke today.
   - **Refactoring confidence:** proving behaviour stays the same while the structure changes.
   - **Living documentation:** a well-named test (`Should_reject_order_when_quantity_is_negative`) tells you what the code should do, and it does not go stale, because when it does, it turns red.
   - **Design feedback:** code that is hard to test is usually code with too many dependencies doing too much. If writing the test is hard, the design is telling you something.

2. **The pyramid balances the cost of each layer.**

   ```
          /\        e2e (few): real browser, real API, real database
         /  \
        /----\      integration (some): several parts together, e.g. API + database
       /      \
      /--------\    unit (many): one function or class, dependencies faked
   ```

   - **Unit test:** tests a single unit (a function, a class) in isolation. Takes milliseconds; thousands run in seconds. When one fails, you know where the problem is. xUnit/NUnit in .NET, Jasmine/Karma or Vitest/Jest in Angular.
   - **Integration test:** tests that several parts work together: that the API can really write to the database, that a service correctly parses a real HTTP response. Slower, needs setup. In .NET it is common to spin up the whole API in memory with `WebApplicationFactory`; for the database, Testcontainers can run a real SQL Server in Docker.
   - **E2E test:** behaves like a user: opens a browser, clicks a button, checks the result. The most realistic, but the slowest and most brittle (it can break when a button moves or the network is slow). Playwright, Cypress. Only for the most critical flows: login, payment, sign-up.

   An inverted pyramid, where most tests are e2e, is known as the "ice cream cone" anti-pattern: the suite takes hours, often fails for no real reason, and the team stops trusting the tests.

3. **A good unit test: AAA, one behaviour, fast and independent.** The skeleton is **Arrange-Act-Assert**: set up, run, verify. A good unit test:
   - Tests **one behaviour** (there should be one "reason it can fail" per test).
   - Is **fast and independent**: it does not depend on a database, the network, the clock or random numbers; those are replaced with fakes or mocks.
   - Tests **behaviour, not implementation**: the visible result, not the internals of private methods. That way refactoring does not break the tests.
   - Covers **edge cases**: empty list, zero, negative numbers, `null`, very large input.

   Code coverage is a useful signal, not a goal: 100% coverage does not guarantee the tests check the right things. A test that asserts nothing also "covers" lines.

## 3. What I got wrong or still find unclear

- I thought the pyramid's ratios were a strict rule (say 70/20/10). It is a direction, not a law. Kent C. Dodds' "Testing Trophy" puts integration tests at the centre for frontends; Spotify's "honeycomb" is integration-heavy for microservices too. The pyramid is debated, but "few slow tests, many fast ones" is common to every model.
- The line between unit and integration is contested. Is a "unit" one class or one unit of behaviour? There are two schools (London and Classic/Detroit), and how much you mock depends on it. I will open that up in the "mock, stub, fake" post.
- I have not really tried TDD (writing the test first) yet.

## 4. Example

[`example/`](example/) has a small example using Node.js' built-in test runner (`node --test`, no packages): a cart discount function with unit tests in AAA style, and a small integration test that runs the function together with a fake repository. One test deliberately catches an edge case (a negative quantity).

**AI note:** AI is very fast at writing tests but has two traps. First, it tests what the existing code **does**, not what it **should do**; if the code has a bug, it can write a test that accepts the bug as "correct". Second, it can produce tests that mock everything and really test nothing. So I first describe the behaviour myself ("a negative quantity must be rejected, 10% off above 1000 TL") and have it write the tests from that. Then, while the test passes, I deliberately break the code and check that the test turns red. A test that never turns red is not a test.

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- Martin Fowler. "Test Pyramid" (2012). https://martinfowler.com/bliki/TestPyramid.html
- Ham Vocke. "The Practical Test Pyramid", martinfowler.com (2018). https://martinfowler.com/articles/practical-test-pyramid.html
- Mike Cohn. *Succeeding with Agile*, Addison-Wesley, 2009 (origin of the pyramid).
- Kent C. Dodds. "The Testing Trophy and Testing Classifications". https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
- Microsoft Learn, "Integration tests in ASP.NET Core". https://learn.microsoft.com/aspnet/core/test/integration-tests
- Vladimir Khorikov. *Unit Testing: Principles, Practices, and Patterns*, Manning, 2020.

---

© 2026 Zehra Betül Çuhadar. The text and figures of this post are licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/): you may share them with credit and a link, for non-commercial purposes and without changes. The code examples are all rights reserved, see [LICENSE-CODE](../../LICENSE-CODE).
