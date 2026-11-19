🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# How do you write a good commit message in English?

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** A good commit subject is about 50 characters at most, written in the **imperative mood** ("Add", "Fix", "Remove"; not "Added" or "Adding"), starts with a capital letter and has no period at the end. If needed, a body after one blank line explains **what and why**; the code already shows how. A practical test: the subject should correctly complete the sentence "If applied, this commit will ...".

## 1. What I researched and why

I now commit almost every day for Learning Sky and my personal site, and I write the messages in English. One day I looked at my own history: "update", "fix", "changes", "final version". Six months from now none of these will tell me anything.

Commit messages are also where I write English most often. They are short, follow patterns and repeat every day. So they are a perfect starting point for both a Git habit and English practice.

## 2. Three key takeaways

1. **The subject is imperative because Git itself talks that way.** Git uses the imperative in the messages it generates: `Merge branch 'main'`, `Revert "..."`. That is also the common community rule. The check sentence: *"If applied, this commit will __"*.
   - ✅ `Add dark mode toggle to the header` → "...will add dark mode toggle" ✔
   - ❌ `Added dark mode toggle` → "...will added" ✘
   - ❌ `Adding dark mode` / `dark mode stuff` / `fix`

   Subject rules (from Chris Beams' widely quoted "seven rules"): separate subject from body with a blank line, limit the subject to about 50 characters, capitalize it, do not end it with a period, use the imperative mood, wrap the body at 72 characters, and use the body to explain what and why rather than how.

2. **The body is a note to the future.** `git diff` shows *what* changed. What it does not show is *why*. Six months later, whoever lands on a line through `git blame` (usually me) will ask "why is it like this?" The body answers that:

   ```
   Generate sky.json in CI instead of by hand

   Editing sky.json manually caused it to drift from the posts.
   The workflow now runs build_sky.py on every push, so meta.json
   is the single source of truth.
   ```

   Useful English patterns: *"Previously, ..."*, *"This caused ..."*, *"Now ..."*, *"so that ..."*, *"Without this, ..."*. And linking: *"Closes #12"*, *"Refs #34"*.

3. **Conventional Commits is an option, not a requirement.** Many projects prefix the subject with a type: `feat: add search box`, `fix: handle empty post list`, `docs: update README`, `refactor:`, `test:`, `chore:`. This makes automatic release notes and version numbers easier. One difference I noticed: with Conventional Commits it is common to start lowercase after the prefix. Whatever rule I pick, what matters is staying **consistent** within a repo.

## 3. What I got wrong or still find unclear

- I thought the imperative sounded rude (like shouting "Add!"). It is not an order, it is a description: it says what the commit will do.
- English mistakes I often make: `Fixed bug` (past tense), `Fix a bug` (which bug?), `Update files` (which files, and why?). Concrete verbs instead of vague ones: `Rename`, `Extract`, `Replace`, `Prevent`, `Handle`, `Drop`.
- Does every small commit need a body? I think not. For a one-line change a good subject is enough. A body is needed when the "why" is not obvious. I am still finding that line by trying.

## 4. Example

[`example/`](example/) contains a small commit message checker. It takes a message and checks the subject length, the capital letter, a trailing period, a past-tense or "-ing" first verb, and a blank line after the subject. It can also be used as a Git `commit-msg` hook.

Verbs I use often:

| Verb | When |
|---|---|
| Add | You add something new |
| Fix | You fix a bug |
| Remove / Drop | You delete something |
| Rename | Only a name changes |
| Refactor / Extract | Same behaviour, different structure |
| Update / Bump | You upgrade a dependency or version |
| Improve | Performance or readability gets better (but say what) |
| Revert | You undo an earlier commit |

**AI note:** AI tools are good at writing a commit message from `git diff`, but they usually just list *what* changed ("Update index.astro and add styles"). They do not know *why*, because the why is in my head. Once I give them one sentence like "I made this change to solve this problem", the message becomes genuinely useful. I still run the subject through the "If applied, this commit will..." test.

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- Chris Beams. "How to Write a Git Commit Message". https://cbea.ms/git-commit/
- Conventional Commits 1.0.0. https://www.conventionalcommits.org/
- Pro Git, "Contributing to a Project: Commit Guidelines". https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project
- Tim Pope. "A Note About Git Commit Messages" (2008).

---

© 2026 Zehra Betül Çuhadar. The text and figures of this post are licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/): you may share them with credit and a link, for non-commercial purposes and without changes. The code examples are all rights reserved, see [LICENSE-CODE](../../LICENSE-CODE).
