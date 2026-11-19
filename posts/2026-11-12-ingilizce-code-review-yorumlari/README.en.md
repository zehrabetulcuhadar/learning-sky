🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# How do you write code review comments in English? Polite and clear patterns

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** A good code review comment in English does three things: it **talks about the code, not the person** ("this function does" instead of "you did"), it **says how important it is** (blocking, a suggestion or a small note) and it **explains why**. A question ("What do you think about...?", "Could we...?") reads softer than an order, but it must not become vague. Labelled comments (`suggestion:`, `issue:`, `nit:`) make it easy to do all three in one line.

## 1. What I researched and why

Code review is where English is most sensitive. A commit message is written for the machine and the future; a review comment is written to a person, about their work. Directness that feels natural in Turkish can read as harsh in written English, or the opposite: too much politeness leaves people wondering "is this a suggestion or a requirement?"

Reviewing also matters more in the age of AI: if AI writes most of the code, the human's job increasingly becomes reading and commenting. That is why the second extra post on the English planet is about this.

## 2. Three key takeaways

1. **Talk about the code, not the person.** The same feedback reads completely differently when the subject changes:
   - ❌ *"You forgot to handle null here."* → blaming
   - ✅ *"This will throw if `user` is null. Should we add a guard?"* → the code's behaviour + a suggestion
   - ❌ *"Why did you do it this way?"* → puts people on the defensive
   - ✅ *"Can you help me understand why we chose a loop here instead of LINQ?"* → curiosity
   - ❌ *"This is wrong."*
   - ✅ *"I think this returns the previous value, not the updated one. Am I missing something?"*

   Using "we" ("Could we...?", "Should we...?") makes the code feel shared. "I think" and "I'm not sure, but" show the comment is an opinion, not a verdict.

2. **State the weight.** When politeness turns into vagueness, the author either treats every comment as mandatory or ignores them all. The fix is to say explicitly how important a comment is. **Conventional Comments** does this with labels:
   - `praise:` appreciate something good. *"praise: Nice use of `switchMap` here, it cancels the old request."*
   - `nitpick:` or `nit:` trivial, optional. *"nit: Typo in the variable name (`recieve`)."*
   - `suggestion:` a proposed improvement. *"suggestion: We could extract this into a pipe so the template stays simple."*
   - `issue:` a real problem. *"issue: This query runs inside the loop, so it will hit the database once per item."*
   - `question:` something you are unsure about. *"question: Is this endpoint called by anything else?"*
   - `thought:` an idea, not a blocker.
   - Decorations: `(blocking)`, `(non-blocking)`. *"suggestion (non-blocking): ..."*

   Google's review guide says the same: mark non-mandatory comments with "Nit:" or "Optional:".

3. **Give the reason and a way forward.** "Change this" is not enough; it needs a "why" and, if possible, a "how". My template: **observation → impact → suggestion.**
   - *"This subscription is never unsubscribed (observation), so it will leak when the component is destroyed (impact). We could use `takeUntilDestroyed()` here (suggestion)."*

   Patterns I use:
   - *"Have you considered ...?"*, *"What do you think about ...?"*, *"Would it make sense to ...?"*
   - *"It might be worth ..."*, *"One option could be ..."*
   - *"I'd suggest ..."*, *"I'd prefer ... because ..."*
   - *"This looks good to me"* (LGTM), *"Approving with a couple of nits."*
   - Accepting: *"Good catch, fixed in abc123."*, *"Done."*, *"Thanks, updated."*
   - Disagreeing: *"I see your point, but I'd keep it because ... What do you think?"*

## 3. What I got wrong or still find unclear

- I thought adding "please" made everything polite. "Please fix this." is still an order. A question and a reason do more than "please".
- Softening too much is also a problem: *"Maybe, if you have time, it could possibly be nice to..."* hides what I want. If there is a real bug, being clear is not being rude.
- It varies by culture. Some teams prefer directness, others indirectness. In a new team, reading old review comments first to get the tone seems like a good idea.

## 4. Example

[`example/`](example/) has review comments on a small Angular component: each one first in its "bad" form, then the labelled and reasoned "good" form. There is also the phrase bank I keep at hand (`phrase-bank.md`).

**AI note:** AI is very good at turning a comment I think in Turkish into English and softening its tone. I ask: "Make this comment polite but clear and add a Conventional Comments label." What I watch for: sometimes it over-softens and erases the actual problem, or changes a technical detail. Before sending, I check: "does it still say the same thing technically?"

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- Conventional Comments. https://conventionalcomments.org/
- Google Engineering Practices, "How to write code review comments". https://google.github.io/eng-practices/review/reviewer/comments.html
- Michael Lynch. "How to Do Code Reviews Like a Human". https://mtlynch.io/human-code-reviews-1/
- Erin Meyer. *The Culture Map*, on direct and indirect feedback.
