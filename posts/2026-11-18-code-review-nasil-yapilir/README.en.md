🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# How do you do a code review? What to look at, and in what order?

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** A code review is someone else reading a change before it goes into the main code. Its goal is not just finding bugs: it **keeps the codebase healthy**, **spreads knowledge across the team** and **upholds shared standards**. A good review goes from big to small: first **does the change solve the right problem and is the design sensible**, then **does it work correctly** (edge cases, errors, security), then **tests**, then **readability**, and **style** last. Style (indentation, quotes, ordering) is a job for formatters and linters, not people. Google's review guide has a nice criterion: a change does not have to be perfect; it should be approved if it **improves the overall health of the codebase**.

## 1. What I researched and why

On the English planet I wrote about **how to phrase** review comments. This post is the other half: **what to look at** in a review. In the age of AI this question matters more. As AI writes a growing share of the code, a big part of an engineer's job is reading, questioning and approving. Reviewing has become almost as fundamental a skill as writing code.

## 2. Three key takeaways

1. **Go from big to small: start at the top of the pyramid.** A review that starts with style comments can miss the real problems or wear out the author. My order:
   1. **Purpose:** read the PR description and the linked task. Why does this change exist? Does it solve the right problem? Sometimes the most valuable comment is "do we really need this?"
   2. **Design:** is the change in the right place? Does it fit the existing architecture, or open a new path? Is it needlessly complex (abstractions added "because we might need them")? If there is a big issue here, discuss it before commenting line by line.
   3. **Correctness:** does the code do what it says? Edge cases (empty list, `null`, zero, very large input), error handling (is an error swallowed?), concurrency (what if two requests arrive at once?), security (is user input validated, is there an authorization check, has a secret slipped into the code?), performance (a database query inside a loop, N+1).
   4. **Tests:** is the new behaviour tested? Do the tests actually verify something? If it is a bug fix, is there a test that catches the bug?
   5. **Readability:** are names meaningful? If a comment is needed, is that a sign the code could be clearer? Would someone seeing this code for the first time in six months understand it?
   6. **Style:** there should be almost no human comments here. Prettier, ESLint, `dotnet format` and .NET analyzers should check it automatically in CI. Do not spend a person's attention on something a machine can catch.

2. **Small PRs, fast reviews.** Research and company experience agree: review effectiveness drops quickly as PRs grow. In SmartBear's study at Cisco, defect detection fell noticeably when more than 200-400 lines were reviewed at once; Google's guide also recommends small changes (small CLs). A 50-line PR gets ten comments; a 1500-line PR gets "LGTM".
   - **As the author:** split the change into logical pieces (refactoring first, then the new feature), write a good PR description (what, why, how it was tested, screenshots), and review your own diff once before sending it.
   - **As the reviewer:** be fast. Google's guide recommends responding to a review request within one business day at most. A waiting PR forces the author to switch context and makes merge conflicts grow. Being fast does not mean approving everything immediately; it means giving the first feedback quickly.

3. **A review is a conversation, not gatekeeping.** Signs of a good review culture:
   - **Talk about the code, not the person** (I covered this in detail in my English post).
   - **State the weight:** blocking issue, suggestion or small note? (`nit:`, `suggestion:`, `issue:`)
   - **Write praise too.** Noticing a good solution is part of learning.
   - **The author may be right.** The reviewer's preference is not a rule. If the team has no standard and both ways are reasonable, the author's choice can stay.
   - **Move long debates to a call.** A ten-message comment chain can often be settled in a five-minute conversation; a note with the outcome on the PR is enough.
   - **Review is a learning tool.** A newer person reviewing a senior's code is very valuable too: they learn, and their "I don't understand this" is a signal the code is not clear.

## 3. What I got wrong or still find unclear

- I thought the purpose of review was "finding bugs". A Microsoft study (Bacchelli and Bird, 2013) found that developers expect reviews mainly to find defects, but in practice reviews deliver more knowledge transfer, alternative solutions and code improvements. Finding bugs matters, but it is not the only benefit.
- The feeling "who am I to comment?" when reviewing a senior's code. Every source I read says the opposite: asking a question is one of the most valuable review comments.
- How much AI-powered review tools will replace human review is unclear. What makes sense to me for now: let AI do the first pass (obvious bugs, missing tests), and let a human look at design and context.

## 4. Example

[`example/`](example/) has two things:
- **`pull_request_template.md`**: a PR template I made for my own projects (what, why, how it was tested, a checklist). When placed in the `.github/` folder, GitHub adds it to every new PR automatically.
- **`review-exercise.md`**: a small .NET controller diff with 6 problems planted on purpose, and the answers at the bottom. Review it yourself first, then check the answers.

**AI note:** AI is very good for a first review pass: when I give it the diff and say "review for correctness, security, missing tests and performance; list only real problems, no style comments", it finds useful things. But it has two weaknesses: it does not know the project's context (why a decision was made, the team's rules), and it sometimes invents problems that do not exist or comments on everything. Also, having AI review AI-written code can share the same blind spots. The final approval should come from a human who knows the context.

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- Google Engineering Practices, "The Code Reviewer's Guide". https://google.github.io/eng-practices/review/reviewer/
- Google Engineering Practices, "Small CLs". https://google.github.io/eng-practices/review/developer/small-cls.html
- SmartBear, "Best Practices for Code Review" (the Cisco study). https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/
- Alberto Bacchelli, Christian Bird. "Expectations, Outcomes, and Challenges of Modern Code Review", ICSE 2013.
- GitHub Docs, "Creating a pull request template for your repository". https://docs.github.com/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository

---

© 2026 Zehra Betül Çuhadar. The text and figures of this post are licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/): you may share them with credit and a link, for non-commercial purposes and without changes. The code examples are all rights reserved, see [LICENSE-CODE](../../LICENSE-CODE).
