"""Build the learning sky from posts/*/meta.json and planets.json.

Outputs (all regenerated, do not edit by hand):
  sky.svg            full sky (one picture)
  sky-0.svg ...      one clickable tile per planet (GitHub cannot click inside an SVG)
  topics/<id>.md     one page per planet listing its posts
  sky-stats.svg      star counter card (stars, stars forming, next star, milestone)
  sky-embed.md       tile block + counter with absolute URLs, for the profile README
  README.md          the SKY and POSTS blocks between the markers
  sky.json           the same sky as data, read by the personal site (zehrabetulcuhadar.github.io)

meta.json v2 (one per post folder, see posts/_template/meta.json):
  status   "draft" or "published". Drafts are invisible everywhere.
  date     YYYY-MM-DD. A published post with a future date appears on that day
           (the daily scheduled run picks it up).
  title, slug, summary   {"tr": "...", "en": "..."}; slug = lowercase a-z, 0-9 and "-".
  topic    one of the ids in planets.json.  series + seriesOrder optional.  tags optional.

Standard library only. Run:  python build_sky.py
"""
import hashlib, json, math, random, re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
OWNER, REPO = "zehrabetulcuhadar", "learning-sky"
planets = json.loads((ROOT / "planets.json").read_text(encoding="utf-8"))
planet_ids = {p["id"] for p in planets}
names = {p["id"]: p["name"] for p in planets}
n = len(planets)

# ---- read posts -----------------------------------------------------------
TODAY = datetime.now(timezone(timedelta(hours=3))).date().isoformat()  # Istanbul
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

def tr_en(m, key, where):
    """v2 fields are {"tr", "en"}; a plain string (old v1 meta) is used for both languages."""
    v = m.get(key)
    if isinstance(v, str):
        v = {"tr": v, "en": v}
    if not isinstance(v, dict) or not v.get("tr") or not v.get("en"):
        raise SystemExit(f'{where}: "{key}" needs both "tr" and "en", e.g. "{key}": {{"tr": "...", "en": "..."}}')
    return {"tr": v["tr"].strip(), "en": v["en"].strip()}

posts, skipped = [], 0
drafts, scheduled = 0, []   # for the counter card: "stars forming" and "next star"
for d in sorted((ROOT / "posts").iterdir()):
    mf = d / "meta.json"
    if not d.is_dir() or d.name.startswith("_") or not mf.exists():
        continue
    m = json.loads(mf.read_text(encoding="utf-8"))
    status = m.get("status", "published")  # v1 meta had no status: treat as published
    if status not in ("draft", "published"):
        raise SystemExit(f'{d.name}: "status" must be "draft" or "published", not "{status}"')
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(m.get("date", ""))):
        if status == "draft":
            skipped += 1
            drafts += 1
            continue
        raise SystemExit(f'{d.name}: "date" must look like 2026-11-20')
    if status == "draft" or m["date"] > TODAY:
        skipped += 1
        if status == "draft":
            drafts += 1
        else:
            scheduled.append(m["date"])
        continue
    if m.get("topic") not in planet_ids:
        raise SystemExit(f"{d.name}: unknown topic '{m.get('topic')}'. Use one of: {sorted(planet_ids)}")
    m["title"] = tr_en(m, "title", d.name)
    m["summary"] = tr_en(m, "summary", d.name)
    m["slug"] = tr_en(m, "slug", d.name)
    for lang, sl in m["slug"].items():
        if not SLUG.match(sl):
            raise SystemExit(f'{d.name}: slug.{lang} "{sl}" may only use a-z, 0-9 and "-" (no Turkish letters, no spaces)')
    m["dir"] = d.name
    posts.append(m)
posts.sort(key=lambda p: p["date"])
for lang in ("tr", "en"):
    seen = {}
    for p in posts:
        sl = p["slug"][lang]
        if sl in seen:
            raise SystemExit(f'slug.{lang} "{sl}" is used by both {seen[sl]} and {p["dir"]}')
        seen[sl] = p["dir"]

# ---- scene ----------------------------------------------------------------
W, H = 900, 420
TW = W / n                      # tile width
SC = min(1.0, 6 / n)            # planets and orbits shrink when there are more than 6 tiles
rnd = random.Random(11)

def scene():
    o = []
    a = o.append
    a('<defs>')
    a('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070b1f"/><stop offset=".55" stop-color="#14103a"/><stop offset="1" stop-color="#241552"/></linearGradient>')
    a('<radialGradient id="gold" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fcd34d"/></radialGradient>')
    a('<linearGradient id="tail" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>')
    for p in planets:
        c = p["color"]
        a(f'<radialGradient id="h-{p["id"]}" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{c}" stop-opacity=".35"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>')
    a('</defs>')
    a('<style>')
    a('.tw{transform-box:fill-box;transform-origin:center;animation:tw 4s ease-in-out infinite}')
    a('.st{transform-box:fill-box;transform-origin:center;animation:st 3.4s ease-in-out infinite}')
    a('.new{transform-box:fill-box;transform-origin:center;animation:nw 2.2s ease-in-out infinite}')
    a('.ring{transform-box:fill-box;transform-origin:center;animation:rg 2.2s ease-out infinite}')
    a('.pl{animation:fl 7s ease-in-out infinite}')
    a('.ss{animation:shoot 10s linear infinite;opacity:0}')
    a(f'.lbl{{font:500 {13 if n <= 6 else 11}px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#c7d2fe;text-anchor:middle}}')
    a('.ttl{font:700 20px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:#f5f3ff}')
    a('.sub{font:500 13px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:#a5b4fc}')
    a('@keyframes tw{0%,100%{opacity:.25}50%{opacity:.9}}')
    a('@keyframes st{0%,100%{opacity:.55;transform:scale(.8) rotate(0)}50%{opacity:1;transform:scale(1.1) rotate(45deg)}}')
    a('@keyframes nw{0%,100%{opacity:.8;transform:scale(1) rotate(0)}50%{opacity:1;transform:scale(1.35) rotate(45deg)}}')
    a('@keyframes rg{0%{opacity:.7;transform:scale(.6)}100%{opacity:0;transform:scale(2.2)}}')
    a('@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}')
    a('@keyframes shoot{0%{transform:translateX(0);opacity:0}1%{opacity:1}8%{transform:translateX(440px);opacity:0}100%{transform:translateX(440px);opacity:0}}')
    a('@media (prefers-reduced-motion:reduce){.tw,.st,.new,.ring,.pl,.ss{animation:none}.ring,.ss{opacity:0}}')
    a('</style>')
    a(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    for _ in range(70):
        x, y, r = rnd.uniform(6, W-6), rnd.uniform(10, H-10), rnd.choice([.8, 1, 1.2, 1.6])
        a(f'<circle class="tw" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#e0e7ff" style="animation-delay:{rnd.uniform(0,4):.2f}s;animation-duration:{rnd.uniform(3,6):.1f}s"/>')

    pos = {}
    for i, p in enumerate(planets):
        pos[p["id"]] = ((i + .5) * TW, 215 + 45 * math.sin(i * 1.3), round((24 + (i * 7) % 10) * SC, 1))

    def planet_svg(style, x, y, r, c, pid):
        P = []
        P.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{min(r*2.1, TW/2-2):.1f}" fill="url(#h-{pid})"/>')
        clip = f'cl-{pid}'
        P.append(f'<clipPath id="{clip}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/></clipPath>')
        if style == "ring":
            P.append(f'<g transform="rotate(-20 {x:.1f} {y:.1f})"><ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r*1.85:.1f}" ry="{r*.5:.1f}" fill="none" stroke="{c}" stroke-opacity=".55" stroke-width="3"/></g>')
        if style == "wire":
            P.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#0b1026" fill-opacity=".85" stroke="{c}" stroke-width="2"/>')
            P.append(f'<g clip-path="url(#{clip})" fill="none" stroke="{c}" stroke-opacity=".7" stroke-width="1.2">'
                     f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r*.45:.1f}" ry="{r}"/><ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r*.85:.1f}" ry="{r}"/>'
                     f'<line x1="{x-r:.1f}" y1="{y:.1f}" x2="{x+r:.1f}" y2="{y:.1f}"/>'
                     f'<ellipse cx="{x:.1f}" cy="{y-r*.5:.1f}" rx="{r*.87:.1f}" ry="{r*.18:.1f}"/><ellipse cx="{x:.1f}" cy="{y+r*.5:.1f}" rx="{r*.87:.1f}" ry="{r*.18:.1f}"/></g>')
        else:
            P.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>')
            P.append(f'<g clip-path="url(#{clip})">')
            if style == "bands":
                for dy in (-.5, -.05, .4):
                    P.append(f'<rect x="{x-r:.1f}" y="{y+r*dy:.1f}" width="{2*r:.1f}" height="{r*.2:.1f}" fill="#fff" fill-opacity=".28"/>')
            if style == "craters":
                for cx, cy, cr in ((-.35, -.3, .22), (.3, .15, .28), (-.1, .5, .16)):
                    P.append(f'<circle cx="{x+r*cx:.1f}" cy="{y+r*cy:.1f}" r="{r*cr:.1f}" fill="#000" fill-opacity=".22"/>')
            P.append(f'<circle cx="{x+r*.55:.1f}" cy="{y+r*.35:.1f}" r="{r:.1f}" fill="#05071a" fill-opacity=".42"/>')
            P.append('</g>')
            P.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1"/>')
        if style == "ring":
            P.append(f'<g transform="rotate(-20 {x:.1f} {y:.1f})"><path d="M {x-r*1.85:.1f} {y:.1f} A {r*1.85:.1f} {r*.5:.1f} 0 0 0 {x+r*1.85:.1f} {y:.1f}" fill="none" stroke="{c}" stroke-opacity=".85" stroke-width="3"/></g>')
        if style == "moon":
            P.append(f'<g><circle cx="{x+r*1.7:.1f}" cy="{y:.1f}" r="{r*.22:.1f}" fill="#e0e7ff"/>'
                     f'<animateTransform attributeName="transform" type="rotate" from="0 {x:.1f} {y:.1f}" to="360 {x:.1f} {y:.1f}" dur="14s" repeatCount="indefinite"/></g>')
        return "".join(P)

    byplanet = {p["id"]: [] for p in planets}
    for s in posts:
        byplanet[s["topic"]].append(s)
    spos = {}
    for pid, lst in byplanet.items():
        x, y, r = pos[pid]
        slots = (60, 20, -25, 110, 150, 190, -150)   # degrees; the bottom is kept free for the label
        for k, s in enumerate(lst):
            ang = math.radians(slots[k % len(slots)])
            rx, ry = r + 34 * SC + (k // len(slots)) * 14 * SC, r + 22 * SC + (k // len(slots)) * 10 * SC
            spos[s["dir"]] = (x + rx * math.cos(ang), y - ry * math.sin(ang) - 6)

    for p in planets:
        x, y, r = pos[p["id"]]
        a(f'<g class="pl" style="animation-delay:{(x%7)*.3:.1f}s">')
        a(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r+34*SC:.1f}" ry="{r+22*SC:.1f}" fill="none" stroke="{p["color"]}" stroke-opacity=".22" stroke-dasharray="2 6"/>')
        a(planet_svg(p.get("style", "plain"), x, y, r, p["color"], p["id"]))
        a(f'<text class="lbl" x="{x:.1f}" y="{y + r + 46 * SC + 8:.1f}">{escape(p.get("label", p["name"]))}</text>')
        a('</g>')

    series = {}
    for s in posts:
        if s.get("series"):
            series.setdefault(s["series"], []).append(s)
    for lst in series.values():
        lst.sort(key=lambda s: (s.get("seriesOrder", 0), s["date"]))
        if len(lst) > 1:
            pts = " ".join(f'{spos[s["dir"]][0]:.1f},{spos[s["dir"]][1]:.1f}' for s in lst)
            a(f'<polyline points="{pts}" fill="none" stroke="#fde68a" stroke-opacity=".45" stroke-width="1" stroke-dasharray="2 4"/>')

    def spark(x, y, r, cls, delay):
        return (f'<g transform="translate({x:.1f} {y:.1f})"><path class="{cls}" style="animation-delay:{delay:.2f}s" '
                f'd="M0 {-r} Q0 0 {r} 0 Q0 0 0 {r} Q0 0 {-r} 0 Q0 0 0 {-r}Z" fill="url(#gold)"/></g>')
    for i, s in enumerate(posts):
        x, y = spos[s["dir"]]
        if i == len(posts) - 1:
            a(f'<g transform="translate({x:.1f} {y:.1f})"><circle class="ring" r="9" fill="none" stroke="#fde68a" stroke-width="1.2"/></g>')
            a(spark(x, y, 11, "new", 0))
        else:
            a(spark(x, y, 7, "st", i * .45))

    for sx, sy, sd in ((40, 90, 1.5), (120, 250, 5.5), (260, 40, 8.2)):
        a(f'<g transform="translate({sx} {sy}) rotate(26)"><g class="ss" style="animation-delay:{sd}s"><line x1="-90" y1="0" x2="0" y2="0" stroke="url(#tail)" stroke-width="2" stroke-linecap="round"/><circle r="2.2" fill="#fff"/></g></g>')
    return o

body = scene()
desc = f'{len(posts)} stars across {n} topic planets. Each post adds a star.'

# full sky (one picture, with title)
sub = (f'{len(posts)} star{"s" if len(posts) != 1 else ""} · {n} planets · every post adds a new star' if posts
       else 'The first star is on its way ✦')
full = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Learning sky">',
        f'<title>Learning sky</title><desc>{desc}</desc>',
        '<clipPath id="all"><rect width="900" height="420" rx="18"/></clipPath><g clip-path="url(#all)">'] + body + [
        '<text class="ttl" x="28" y="40">Zehra’s Learning Sky ✦</text>', f'<text class="sub" x="28" y="62">{sub}</text>', '</g></svg>']
(ROOT / "sky.svg").write_text("\n".join(full), encoding="utf-8")

# tiles
R = 18
for old in ROOT.glob("sky-[0-9]*.svg"):
    old.unlink()
for i, p in enumerate(planets):
    x0, x1 = i * TW, (i + 1) * TW
    if n == 1:
        d = f'M {x0+R} 0 H {x1-R} Q {x1} 0 {x1} {R} V {H-R} Q {x1} {H} {x1-R} {H} H {x0+R} Q {x0} {H} {x0} {H-R} V {R} Q {x0} 0 {x0+R} 0 Z'
    elif i == 0:
        d = f'M {x0+R} 0 H {x1} V {H} H {x0+R} Q {x0} {H} {x0} {H-R} V {R} Q {x0} 0 {x0+R} 0 Z'
    elif i == n - 1:
        d = f'M {x0} 0 H {x1-R} Q {x1} 0 {x1} {R} V {H-R} Q {x1} {H} {x1-R} {H} H {x0} Z'
    else:
        d = f'M {x0} 0 H {x1} V {H} H {x0} Z'
    t = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} 0 {TW:.2f} {H}" width="{TW:.0f}" height="{H}" role="img" aria-label="{escape(p.get("label", p["name"]))}">',
         f'<title>{escape(p["name"])}</title>', f'<clipPath id="tile"><path d="{d}"/></clipPath><g clip-path="url(#tile)">'] + body + ['</g></svg>']
    (ROOT / f"sky-{i}.svg").write_text("\n".join(t), encoding="utf-8")

# topic pages
(ROOT / "topics").mkdir(exist_ok=True)
for old in (ROOT / "topics").glob("*.md"):
    if old.stem not in planet_ids:
        old.unlink()  # planet removed from planets.json
for p in planets:
    mine = sorted([s for s in posts if s["topic"] == p["id"]], key=lambda s: s["date"], reverse=True)
    L = [f'# {p.get("label", p["name"])}', '', f'**{p["name"]}** planet: every post about this topic is a star here. [← Back to the sky](../README.md)', '']
    if mine:
        L += ['| Date | Title | Read |', '| :-- | :-- | :-- |']
        for s in mine:
            dd = f'../posts/{s["dir"]}'
            L.append(f'| {s["date"]} | {s["title"]["en"]} | [🇬🇧 EN]({dd}/README.en.md) · [🇹🇷 TR]({dd}/README.tr.md) |')
    else:
        L.append('No stars here yet ✦ The first post on this topic is coming soon.')
    (ROOT / "topics" / f'{p["id"]}.md').write_text("\n".join(L) + "\n", encoding="utf-8")

# star counter card (sky-stats.svg): how many stars, how many are forming, when the next one rises
def nice_date(iso):
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%d %b %Y").lstrip("0")

def stats_svg():
    SW, SH, GOAL = 900, 170, 2           # GOAL: the first milestone is 2 stars on every planet
    cnt = {p["id"]: 0 for p in planets}
    for s in posts:
        cnt[s["topic"]] += 1
    total = len(posts)
    reached = sum(min(c, GOAL) for c in cnt.values())
    goal_total = GOAL * n
    lit = sum(1 for c in cnt.values() if c > 0)
    nxt = nice_date(min(scheduled)) if scheduled else "soon ✦"
    last = nice_date(posts[-1]["date"]) if posts else "not yet"
    sans = "-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
    mono = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SW} {SH}" width="{SW}" height="{SH}" role="img" aria-label="Learning sky: {total} stars">',
         f'<title>Learning sky counter</title><desc>{total} published posts, {drafts} drafts, {len(scheduled)} scheduled, across {n} planets.</desc>',
         '<defs><linearGradient id="sbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070b1f"/><stop offset=".55" stop-color="#14103a"/><stop offset="1" stop-color="#241552"/></linearGradient>',
         '<radialGradient id="sgold" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fcd34d"/></radialGradient>',
         '<linearGradient id="sbar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fcd34d"/><stop offset="1" stop-color="#f28ac0"/></linearGradient></defs>',
         '<style>',
         f'.big{{font:800 56px {sans};fill:#fde68a}} .k{{font:600 11px {mono};fill:#a5b4fc;letter-spacing:.12em}}',
         f'.v{{font:600 15px {sans};fill:#f5f3ff}} .m{{font:500 12px {sans};fill:#c7d2fe}} .pl{{font:500 10px {mono};fill:#c7d2fe;text-anchor:middle}}',
         f'.pc{{font:700 12px {sans};fill:#fff;text-anchor:middle}}',
         '.tw{transform-box:fill-box;transform-origin:center;animation:tw 3.4s ease-in-out infinite}',
         '.dim{opacity:.45}',
         '@keyframes tw{0%,100%{opacity:.6;transform:scale(.85) rotate(0)}50%{opacity:1;transform:scale(1.12) rotate(45deg)}}',
         '@media (prefers-reduced-motion:reduce){.tw{animation:none}}',
         '</style>',
         f'<rect width="{SW}" height="{SH}" rx="18" fill="url(#sbg)"/>']
    r2 = random.Random(5)
    for _ in range(26):
        o.append(f'<circle cx="{r2.uniform(8, SW-8):.1f}" cy="{r2.uniform(8, SH-8):.1f}" r="{r2.choice([.7, 1, 1.3])}" fill="#e0e7ff" opacity="{r2.uniform(.2, .6):.2f}"/>')
    # left: the big number
    o.append('<g transform="translate(46 62)"><path class="tw" d="M0 -16 Q0 0 16 0 Q0 0 0 16 Q0 0 -16 0 Q0 0 0 -16Z" fill="url(#sgold)"/></g>')
    o.append(f'<text class="big" x="72" y="84">{total}</text>')
    o.append(f'<text class="k" x="30" y="114">{"STAR" if total == 1 else "STARS"} IN THE SKY</text>')
    o.append(f'<text class="m" x="30" y="138">✧ {drafts} forming · {len(scheduled)} on the way</text>')
    # middle: one dot per planet, its stars stacked above it
    x0, x1 = 280, 620
    step = (x1 - x0) / max(n - 1, 1)
    for i, p in enumerate(planets):
        x, c = x0 + i * step, cnt[p["id"]]
        dim = "" if c else ' class="dim"'
        o.append(f'<g{dim}><circle cx="{x:.1f}" cy="104" r="11" fill="{p["color"]}"/>'
                 f'<clipPath id="sc{i}"><circle cx="{x:.1f}" cy="104" r="11"/></clipPath>'
                 f'<circle cx="{x+5:.1f}" cy="108" r="11" fill="#05071a" fill-opacity=".35" clip-path="url(#sc{i})"/></g>')
        o.append(f'<text class="pc" x="{x:.1f}" y="108">{c}</text>')
        for k in range(min(c, 4)):
            y = 80 - k * 12
            o.append(f'<path d="M{x:.1f} {y-5} Q{x:.1f} {y} {x+5:.1f} {y} Q{x:.1f} {y} {x:.1f} {y+5} Q{x:.1f} {y} {x-5:.1f} {y} Q{x:.1f} {y} {x:.1f} {y-5}Z" fill="url(#sgold)"/>')
        if c > 4:
            o.append(f'<text class="pl" x="{x:.1f}" y="34">+{c-4}</text>')
        o.append(f'<text class="pl" x="{x:.1f}" y="134">{escape(p.get("short", p["id"][:6]))}</text>')
    o.append(f'<text class="k" x="{x0-10}" y="34">{lit}/{n} PLANETS LIT</text>')
    # right: next star, last star, first milestone
    rx = 660
    o.append(f'<text class="k" x="{rx}" y="36">NEXT STAR</text><text class="v" x="{rx}" y="56">{escape(nxt)}</text>')
    o.append(f'<text class="k" x="{rx+124}" y="36">LAST STAR</text><text class="v" x="{rx+124}" y="56">{escape(last)}</text>')
    o.append(f'<text class="k" x="{rx}" y="96">MILESTONE · {GOAL} ON EVERY PLANET</text>')
    bw = 210
    o.append(f'<rect x="{rx}" y="106" width="{bw}" height="10" rx="5" fill="#ffffff" fill-opacity=".12"/>')
    if reached:
        o.append(f'<rect x="{rx}" y="106" width="{max(10, bw * reached / goal_total):.1f}" height="10" rx="5" fill="url(#sbar)"/>')
    o.append(f'<text class="m" x="{rx}" y="138">{reached} / {goal_total} stars</text>')
    o.append('</svg>')
    return "\n".join(o)

stats = stats_svg()
(ROOT / "sky-stats.svg").write_text(stats, encoding="utf-8")
# Version stamp for the profile README image URLs. GitHub caches images (camo); a new ?v= on every
# real change makes the profile show the new sky at once. It only changes when the pictures change.
VER = hashlib.sha1(("\n".join(body) + stats).encode("utf-8")).hexdigest()[:8]

# tile blocks (relative for this repo, absolute for the profile README)
def tiles_block(base_img, base_link, q=""):
    w = f"{math.floor(1000 / n) / 10:.1f}%"
    imgs = "".join(f'<a href="{base_link}topics/{p["id"]}.md"><img src="{base_img}sky-{i}.svg{q}" width="{w}" alt="{escape(p.get("label", p["name"]))}"></a>' for i, p in enumerate(planets))
    return f'<div align="center">\n\n<p>{imgs}</p>\n\n</div>'
def counter_block(base_img, link, q=""):
    return f'<div align="center">\n\n<a href="{link}"><img src="{base_img}sky-stats.svg{q}" width="100%" alt="{len(posts)} stars in the learning sky"></a>\n\n</div>'
RAW = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/main/"
rel = tiles_block("", "")
absb = tiles_block(RAW, f"https://github.com/{OWNER}/{REPO}/blob/main/", f"?v={VER}")
(ROOT / "sky-embed.md").write_text(absb + "\n\n" + counter_block(RAW, f"https://github.com/{OWNER}/{REPO}#-posts", f"?v={VER}") + "\n", encoding="utf-8")

# README blocks
rows = ["| Date | Topic | Title | Read |", "| :-- | :-- | :-- | :-- |"]
for s in sorted(posts, key=lambda p: p["date"], reverse=True):
    d = f'posts/{s["dir"]}'
    rows.append(f'| {s["date"]} | {names[s["topic"]]} | {s["title"]["en"]} | [🇬🇧 EN]({d}/README.en.md) · [🇹🇷 TR]({d}/README.tr.md) |')
if not posts:
    rows.append("| – | – | The first post is coming soon ✦ | – |")
text = (ROOT / "README.md").read_text(encoding="utf-8")
def fill(t, name, content):
    pat = rf"(<!-- {name}:START -->).*?(<!-- {name}:END -->)"
    if not re.search(pat, t, flags=re.S):
        raise SystemExit(f"README.md is missing the <!-- {name}:START --> / <!-- {name}:END --> markers")
    return re.sub(pat, lambda m: f"{m.group(1)}\n{content}\n{m.group(2)}", t, flags=re.S)
text = fill(text, "SKY", rel + "\n\n" + counter_block("", "#-posts"))
text = fill(text, "POSTS", "\n".join(rows))
(ROOT / "README.md").write_text(text, encoding="utf-8")
# sky.json: the same sky as data, for the personal site
counts = {p["id"]: 0 for p in planets}
for s in posts:
    counts[s["topic"]] += 1
sky = {
    "version": 2,
    "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "planets": [{"id": p["id"], "name": p["name"], "color": p["color"], "style": p.get("style", "plain"), "count": counts[p["id"]]} for p in planets],
    "posts": [
        {
            "id": s["dir"], "date": s["date"], "topic": s["topic"],
            "series": s.get("series") or None, "seriesOrder": s.get("seriesOrder"),
            "title": s["title"], "slug": s["slug"], "summary": s["summary"], "tags": s.get("tags", []),
        }
        for s in posts
    ],
}
(ROOT / "sky.json").write_text(json.dumps(sky, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"ok: {len(posts)} published post(s), {skipped} draft/scheduled skipped, {n} planets, {n} tiles")
