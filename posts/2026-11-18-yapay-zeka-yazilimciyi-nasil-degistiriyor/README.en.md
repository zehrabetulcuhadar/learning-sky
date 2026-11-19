🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# How is AI changing a software developer's job?

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** AI is rapidly lowering the cost of **writing** code; but the cost of **choosing** the right code, **verifying** it and **fitting it into the whole system** is not falling, and may be rising. So the developer's job is shifting from producing code line by line toward: clearly **specifying** the problem (specs and context), **reviewing and testing** generated code, making architecture and technical **decisions**, and taking **responsibility** for the results. Research shows a mixed picture: AI use has become nearly universal, but trust in its accuracy is low and productivity gains are not always as large as they feel.

## 1. What I researched and why

This question is the whole starting point of Learning Sky. I decided to relearn computing from scratch because I was asking **what I need to know** in a world where AI writes most of the code. In this extra post on the AI planet I wanted to compare my intuition with data: what is really changing, and what is not?

## 2. Three key takeaways

1. **Use is universal, trust is not.** In Stack Overflow's 2025 Developer Survey, about 84% of respondents said they use or plan to use AI tools. But in the same survey, more developers **distrusted** AI accuracy (about 46%) than **trusted** it (about 33%). The most common complaint was solutions that are "almost right, but not quite". That matches my experience: AI-written code often looks like it works, but hides small mistakes in edge cases, project rules or current APIs. "Almost right" code is more dangerous than obviously wrong code, because it is harder to notice.

2. **Felt speed and measured speed can differ.** In a randomized controlled study published by the research organization METR in 2025, experienced developers working in large open-source projects they knew well completed tasks about 19% **slower** on average when using AI tools. The interesting part: even after finishing, the same developers believed AI had made them about 20% **faster**. It is one study measuring a specific situation (complex codebases they knew very well); other studies found speed-ups on simpler or newer tasks. But the lesson is clear: I should judge productivity by measuring, not by feel. Google's DORA reports carry a similar warning: in the 2024 report, increased AI adoption came with a small drop in delivery stability; the reports conclude that AI does not replace good engineering practices (small changes, strong tests, fast feedback) but **amplifies** whatever is already there.

3. **Skills that gain value: specifying, judging, deciding.** The picture I put together from my reading and my own observations:

   | Losing value | Gaining value |
   |---|---|
   | Knowing syntax by heart | Clearly specifying the problem (specs, acceptance criteria) |
   | Typing boilerplate fast | Giving the right context (rules, examples, architecture decisions) |
   | Remembering an API's parameters | Reading and judging code: is it correct, secure, needlessly complex? |
   | Writing a function from scratch alone | Writing tests and verifying |
   | | Architecture and trade-off decisions |
   | | Fundamentals: networking, databases, memory, concurrency (to spot what is wrong) |
   | | Communication: with the team, the business side, and the AI |

   There is a paradox here: AI makes fundamentals **more** necessary, not less. To notice that a query has an N+1 problem, that a `catch` swallows an error, or that a CORS policy is too broad, you need to know the topic. AI can write the "what"; answering "is this right?" is still my job. That is why all the fundamentals posts on Learning Sky exist.

   And there is responsibility: whoever wrote the code, I am the one approving it and shipping it to production. "The AI wrote it" is not a valid explanation in a bug report.

## 3. What I got wrong or still find unclear

- At first I was looking for a yes or no answer to "will AI replace developers?" The more I read, the more I think the question is wrong: the job does not seem to be disappearing, but its content is changing. Nobody knows for sure how fast this will happen, especially what it means for juniors.
- I see a dilemma for beginners: the way to build fundamentals used to be doing the small tasks yourself, the very tasks AI now does. How will fundamentals be learned while AI does them? My answer for now is Learning Sky: deliberately learn from the ground up, and use AI as a teacher and sparring partner.
- This field changes very fast. The numbers in this post are 2025 data; they may be out of date within months.

## 4. Example

[`example/`](example/) contains my own AI workflow (`workflow.md`): the short spec template I write before having AI build a feature, the rules I follow while working, and my checklist before accepting code. This post's "working example" is a process, not code, because what is changing is not the code, it is the process.

**AI note:** While preparing this post I asked an AI "how is AI changing developers' jobs?" and it painted an optimistic, generic picture, with numbers but no sources. I checked every figure in this post against its primary source (the survey report, the research paper). When the topic is AI itself, that check matters even more.

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- Stack Overflow, "2025 Developer Survey", AI section. https://survey.stackoverflow.co/2025/
- METR. "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity" (July 2025). https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- Google Cloud, DORA "Accelerate State of DevOps Report 2024". https://dora.dev/research/2024/dora-report/
- Google Cloud, DORA "State of AI-assisted Software Development" (2025). https://dora.dev/
- Addy Osmani. *Beyond Vibe Coding*, O'Reilly, 2025.
