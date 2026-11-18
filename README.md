<div align="center">

# ✦ Learning Sky

**A learning log. Every post becomes a star.**

</div>

<!-- SKY:START -->
<div align="center">

<p><a href="topics/basics.md"><img src="sky-0.svg" width="11.1%" alt="~/basics"></a><a href="topics/backend.md"><img src="sky-1.svg" width="11.1%" alt="~/backend"></a><a href="topics/frontend.md"><img src="sky-2.svg" width="11.1%" alt="~/frontend"></a><a href="topics/data.md"><img src="sky-3.svg" width="11.1%" alt="~/data"></a><a href="topics/quality.md"><img src="sky-4.svg" width="11.1%" alt="~/quality"></a><a href="topics/architecture.md"><img src="sky-5.svg" width="11.1%" alt="~/architecture"></a><a href="topics/ai.md"><img src="sky-6.svg" width="11.1%" alt="~/ai"></a><a href="topics/english.md"><img src="sky-7.svg" width="11.1%" alt="~/english"></a><a href="topics/news.md"><img src="sky-8.svg" width="11.1%" alt="~/news"></a></p>

</div>

<div align="center">

✦ The first star is on its way · 9 planets. Click a planet to see its posts.

</div>
<!-- SKY:END -->

I am relearning computing from the ground up. For each topic I write down what I learned, what I got wrong and what is still unclear.
Every post is published in **English** and **Türkçe**, with a small runnable example.
Posts are drafted with AI assistance and reviewed by me.

## 📚 Posts

<!-- POSTS:START -->
| Date | Topic | Title | Read |
| :-- | :-- | :-- | :-- |
| – | – | The first post is coming soon ✦ | – |
<!-- POSTS:END -->

## ✍️ Adding a new post (new star)

1. Copy `posts/_template` to a new folder named `YYYY-MM-DD-short-topic-name`.
2. Edit `meta.json`:
   - `status`: keep `"draft"` while writing. Drafts are invisible everywhere, so you can push unfinished work.
   - `date`, `topic` (one of the ids in `planets.json`), optional `series` + `seriesOrder`, `tags`.
   - `title`, `slug`, `summary` in both languages: `{"tr": "...", "en": "..."}`. A slug uses only `a-z`, `0-9` and `-`.
3. Write `README.en.md` and `README.tr.md`, and put the small runnable code in `example/`.
4. To publish, set `"status": "published"` and commit. A GitHub Action rebuilds the sky, the table above and `sky.json`,
   then tells the personal site to rebuild. A published post with a future `date` appears on that day.

Generated files, never edit by hand: `sky*.svg`, `topics/*.md`, `sky-embed.md`, `sky.json`.

## 🪐 Planets (topics)

Planets are defined in `planets.json`. Add a new object there to add a new topic.

## 🧱 Post structure

1. What I researched this week and why
2. Three key takeaways
3. What I got wrong or still find unclear
4. Sources
