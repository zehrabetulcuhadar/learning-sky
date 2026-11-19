# 0001. Use Astro for the personal site

- **Status:** Accepted
- **Date:** 2026-11-18
- **Decider:** Zehra

## Context

I want a personal site that shows my learning posts as an interactive, animated sky (Three.js) and works as a small CV.

Forces:
- **Cost:** it must be free to host. GitHub Pages is free for public repos but only serves static files.
- **Content:** posts already live in a separate repo (`learning-sky`) and are exported as `sky.json`. The site only reads them.
- **Performance:** the 3D scene is heavy, so everything else should ship as little JavaScript as possible. Many visitors will be on phones.
- **Skills:** I use Angular at work. Using it here would be familiar but would ship a full SPA runtime for a mostly static page.
- **Learning:** I want this project to teach me something new.

## Considered options

1. **Angular SPA**: familiar; but a full client-side app for static content, larger first load, SEO needs extra setup (SSR/prerender).
2. **Next.js (React)**: powerful and popular; but I do not know React yet, and many of its strengths (server features) are lost on GitHub Pages.
3. **Hosted blog platform**: zero setup; but no control over the 3D sky, the main idea of the site.
4. **Astro**: content-first static site generator, ships zero JavaScript by default and loads scripts only where needed; can import Three.js directly; outputs plain static files for GitHub Pages.

## Decision

We will build the personal site with **Astro**, deploy the static output to **GitHub Pages** with a GitHub Actions workflow, and read posts from `learning-sky`'s `sky.json` at build time.

## Consequences

Positive:
- Free hosting, no server to maintain, small attack surface.
- Fast first load: only the galaxy script ships as JavaScript.
- Posts stay independent of the site; the site can be rebuilt or replaced without touching them.

Negative:
- No server-side logic: comments, forms or search need an external service or must run in the browser.
- New posts appear only after a rebuild, so the two repos need a trigger (`repository_dispatch`) and a nightly scheduled build for future-dated posts.
- Astro is new to me: slower at first, and fewer people at work could help.
- If the site later needs user accounts or dynamic data, this decision must be revisited (a new ADR would supersede this one).
