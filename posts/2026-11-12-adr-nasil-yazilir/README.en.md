🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# How do you write an Architecture Decision Record (ADR)?

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** An Architecture Decision Record (ADR) is a short text file describing **one** significant decision. The classic format has five headings: **Title, Status, Context, Decision, Consequences.** It lives next to the code (for example `docs/adr/0001-...md`), is numbered, and is not edited once accepted; if the decision changes, a new ADR is written and the old one is marked "superseded". Its purpose is to let someone six months later (often me) answer "why did we do it this way?"

## 1. What I researched and why

In my first architecture post I wrote that architecture is the set of decisions that are expensive to change. But where do we write those decisions down? Often nowhere. A decision is made in a meeting, the reasoning stays in the heads of the people there, and it disappears when they leave. Then someone new looks at the code, asks "why is this so weird?", and either protects the decision blindly or breaks it without knowing why it was there.

ADRs solve this with a very simple tool: a markdown file. The best way to learn it was to try it on my own project, so I wrote my site's first architecture decision as an ADR.

## 2. Three key takeaways

1. **Five headings are enough.** The format Michael Nygard proposed in 2011 is still the most common:
   - **Title:** a short noun phrase with a number. "0001. Use Astro as the static site generator for the personal site."
   - **Status:** Proposed, Accepted, Rejected, Deprecated or "Superseded by 0007".
   - **Context:** the situation forcing the decision. What is the problem, what are the constraints, and which forces (budget, team skills, time, performance goals) pull against each other? This part should be neutral: it describes the situation, not the solution.
   - **Decision:** one clear sentence in active voice. "We will use Astro." No "maybe" or "we are considering".
   - **Consequences:** **everything** the decision brings, not just the good parts. What becomes easier, what becomes harder, which new risks and tasks appear?

   The most useful part for me is Consequences. Writing down the downsides makes the decision honest, and later lets you say "we knew this and chose it on purpose".

2. **ADRs are immutable; they supersede each other.** Once accepted, an ADR is not edited. If the thinking changes six months later, a new ADR 0007 is written and the old one's status becomes "Superseded by 0007". So the history of decisions accumulates instead of disappearing: you can see what we thought, when, and with what information. It is like Git history, but for decisions instead of lines of code.

   Practical rules:
   - Files live with the code: `docs/adr/0001-short-name.md`. The ADR can be reviewed in the pull request.
   - One ADR = one decision. Not "our frontend, database and deploy decisions" in one file.
   - Keep it short. If it goes past a page or two, there is probably more than one decision in it.
   - Only for architecturally significant decisions. "A variable name" is not an ADR; "which database", "monolith or not", "how authentication works" are.

3. **Writing down the options is how you question your own decision.** In Nygard's format the options are part of the context. Newer templates like MADR (Markdown Any Decision Records) add a separate **"Considered options"** section with pros and cons for each. When writing my own ADR I noticed something: once I had to put Astro next to Angular, Next.js and a blog platform, I saw that part of my decision really came from "I want to learn something new". That is a legitimate reason too, but now it is written down openly.

## 3. What I got wrong or still find unclear

- I thought ADRs were a heavy process for big companies. In fact it is a five-minute task even for a one-person project, and I am the one who benefits most.
- Which decisions "deserve" an ADR is still a judgment call. My rule for now: "if undoing it would take more than a day, write an ADR."
- Are ADRs actually read after they are written? The sources I read say they help most when onboarding someone new and when a decision is being reopened. I will see this over time in my own project.

## 4. Example

[`example/`](example/) contains my site's real first ADR: **"0001. Use Astro for the personal site"**. It has the classic five headings plus the considered options. I also added an empty `template.md` to copy for the next decision.

**AI note:** AI is very good at drafting ADRs because the format is so clear. But I have to give it the context; otherwise it invents a generic one that fits everyone. What works: I write the decision and the constraints as a few bullet points, and ask it to "list the negative consequences completely, too". It finds downsides faster than I do, but I decide which ones really matter for this project. Also, giving ADRs to an AI as context files is the shortest way to explain "why we do things this way in this project".

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- Michael Nygard. "Documenting Architecture Decisions" (2011). https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- ADR GitHub organization, templates and tools. https://adr.github.io/
- MADR, Markdown Any Decision Records. https://adr.github.io/madr/
- Joel Parker Henderson, collection of architecture decision record examples. https://github.com/joelparkerhenderson/architecture-decision-record
- ThoughtWorks Technology Radar, "Lightweight Architecture Decision Records" (Adopt).

---

© 2026 Zehra Betül Çuhadar. The text and figures of this post are licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/): you may share them with credit and a link, for non-commercial purposes and without changes. The code examples are all rights reserved, see [LICENSE-CODE](../../LICENSE-CODE).
