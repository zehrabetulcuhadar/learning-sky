🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# How do you keep up with the software industry? My weekly reading routine

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** Keeping up with software is not about reading everything; it is about reading **a few trusted sources** at **a fixed time** with **a filter**. My setup has three layers: a 10-minute summary every day (a daily briefing), a 30-45 minute deep read once a week (official blogs and release notes of the tools I use, one or two curated newsletters), and a monthly "what I learned" note (the news posts on Learning Sky). The filter is a single question: **"Will this change my work or my learning plan in the next 6 months?"** If not, I read the headline and move on.

## 1. What I researched and why

One of Learning Sky's planets is dedicated to news; every four weeks I write a monthly summary. While preparing the first ones I noticed the real problem is not finding news, it is **not drowning in it**. Every day there is a new AI model, a new framework version, a new "X is dead" article. Trying to follow all of it is exhausting and keeps derailing my learning plan. In this post I built myself a routine.

## 2. Three key takeaways

1. **Layer sources by trust.** Not every source is worth the same:
   - **Primary sources (most trustworthy):** official blogs and release notes of the tools I use. For me: the .NET Blog, the Angular Blog, TypeScript release notes, the GitHub Changelog, official announcements from the AI tools I use. This is where I read what a feature really does.
   - **Curated secondary sources:** newsletters and publications filtered by an editor (InfoQ, the ThoughtWorks Technology Radar, weekly JavaScript or .NET newsletters). The Radar is especially valuable: it classifies technologies as "Adopt, Trial, Assess, Hold" and comes out twice a year, so there is little noise.
   - **Community (noisiest):** Hacker News, Reddit, X, LinkedIn. Good for early signals, not for accuracy. I do not count something I heard there as "learned" until I check the primary source.
   - **Postmortems:** technical reports companies publish after big outages. Some of the most educational texts in the industry, because they show how real systems fail with real mistakes.

2. **Fixed time, fixed box: a routine beats a feed.** Reading news randomly during the day keeps breaking my attention. The setup I am trying:
   - **Daily (10 min):** the morning briefing. Headlines and two- or three-sentence summaries only. The goal is a rough answer to "what is going on?"
   - **Weekly (30-45 min, Friday afternoon):** primary sources in the RSS reader. What changed this week in the tools I use? Is something worth reading in depth? If so, it goes on my reading list.
   - **Monthly:** the news post. Writing the month's 3-5 most important developments in my own words tests whether I really understood them.
   - **Notifications off.** News does not come to me; I go to the news at the time I chose.

   RSS helps a lot here: no algorithm, only the sources I picked, in chronological order. With an RSS reader (or a small script) I collect the primary sources in one place.

3. **The hype filter: "how much does this affect me?"** I ask every piece of news the same questions:
   - **Does it affect something I use?** (.NET, Angular, TypeScript, the AI tools I use) → Read in detail.
   - **Is it related to a topic in my learning plan?** → Take a note, come back when that lesson arrives.
   - **Is it just new and exciting?** → Read the headline, move on. If it really matters, people will still be talking about it in six months.
   - **Does it say "X is dead" or "this changes everything"?** → Be skeptical, look for the primary source.

   And what I remind myself against FOMO (fear of missing out): fundamentals (networking, databases, architecture) change slowly, tools change fast. Learning the fundamentals also makes tool news easier to understand.

## 3. What I got wrong or still find unclear

- I thought the more sources I followed, the better informed I would be. The opposite happened: the more sources, the less I understood what I read. Now when I add a source I try to remove one.
- The AI field moves so fast that even a weekly routine feels insufficient. But "knowing everything" is not my goal. My goal is to notice what matters for my work in time.
- I am still missing good Turkish sources. I am looking for Turkish technical newsletters and communities worth following.

## 4. Example

[`example/`](example/) has a small Python RSS reader written with the standard library. It fetches the last 7 days of posts from the sources in `feeds.txt` and lists them by date. It reads both RSS and Atom, and skips a source it cannot reach. I run it during my weekly reading slot: no algorithm, only the sources I chose.

**AI note:** Asking an AI "what happened in software this week?" is risky: the model has a knowledge cutoff and, without web search, may present old information as current. Even with tools that search the web I open and check the source links. The best use, I think: give it a long release note or postmortem and ask it to "summarize the parts that affect an Angular/.NET developer". In other words, it does not find the news, I do; it only summarizes.

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- ThoughtWorks Technology Radar. https://www.thoughtworks.com/radar
- InfoQ. https://www.infoq.com/
- .NET Blog. https://devblogs.microsoft.com/dotnet/
- Angular Blog. https://blog.angular.dev/
- GitHub Changelog. https://github.blog/changelog/
- Cal Newport. *Deep Work*, 2016 (on attention and fixed time blocks).

---

© 2026 Zehra Betül Çuhadar. The text and figures of this post are licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/): you may share them with credit and a link, for non-commercial purposes and without changes. The code examples are all rights reserved, see [LICENSE-CODE](../../LICENSE-CODE).
