"""Build the learning sky from posts/*/meta.json and planets.json.

Outputs (all regenerated, do not edit by hand):
  sky.svg            full sky (one picture)
  sky-0.svg ...      one clickable tile per planet (GitHub cannot click inside an SVG)
  topics/<id>.md     one page per planet listing its posts
  sky-embed.md       tile block with absolute URLs, for the profile README
  README.md          the SKY and POSTS blocks between the markers

Standard library only. Run:  python build_sky.py
"""
import json, math, random, re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
OWNER, REPO = "zehrabetulcuhadar", "learning-sky"
planets = json.loads((ROOT / "planets.json").read_text(encoding="utf-8"))
planet_ids = {p["id"] for p in planets}
names = {p["id"]: p["name"] for p in planets}
n = len(planets)

# ---- read posts -----------------------------------------------------------
posts = []
for d in sorted((ROOT / "posts").iterdir()):
    mf = d / "meta.json"
    if not d.is_dir() or d.name.startswith("_") or not mf.exists():
        continue
    m = json.loads(mf.read_text(encoding="utf-8"))
    if m.get("topic") not in planet_ids:
        raise SystemExit(f"{d.name}: unknown topic '{m.get('topic')}'. Use one of: {sorted(planet_ids)}")
    m["dir"] = d.name
    posts.append(m)
posts.sort(key=lambda p: p["date"])

# ---- scene ----------------------------------------------------------------
W, H = 900, 420
TW = W / n                      # tile width
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
    a('.lbl{font:500 13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#c7d2fe;text-anchor:middle}')
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
        pos[p["id"]] = ((i + .5) * TW, 215 + 45 * math.sin(i * 1.3), 24 + (i * 7) % 10)

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
            rx, ry = r + 34 + (k // len(slots)) * 14, r + 22 + (k // len(slots)) * 10
            spos[s["dir"]] = (x + rx * math.cos(ang), y - ry * math.sin(ang) - 6)

    for p in planets:
        x, y, r = pos[p["id"]]
        a(f'<g class="pl" style="animation-delay:{(x%7)*.3:.1f}s">')
        a(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r+34}" ry="{r+22}" fill="none" stroke="{p["color"]}" stroke-opacity=".22" stroke-dasharray="2 6"/>')
        a(planet_svg(p.get("style", "plain"), x, y, r, p["color"], p["id"]))
        a(f'<text class="lbl" x="{x:.1f}" y="{y + r + 46:.1f}">{escape(p.get("label", p["name"]))}</text>')
        a('</g>')

    series = {}
    for s in posts:
        if s.get("series"):
            series.setdefault(s["series"], []).append(s)
    for lst in series.values():
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
desc = f'{len(posts)} stars across {n} topic planets. Each weekly post adds a star.'

# full sky (one picture, with title)
sub = f'{len(posts)} stars · {n} planets · every weekly post adds a new star' if posts else 'The first star is on its way ✦'
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
for p in planets:
    mine = sorted([s for s in posts if s["topic"] == p["id"]], key=lambda s: s["date"], reverse=True)
    L = [f'# {p.get("label", p["name"])}', '', f'**{p["name"]}** planet: every post about this topic is a star here. [← Back to the sky](../README.md)', '']
    if mine:
        L += ['| Date | Title | Read |', '| :-- | :-- | :-- |']
        for s in mine:
            dd = f'../posts/{s["dir"]}'
            L.append(f'| {s["date"]} | {s["title"]} | [🇬🇧 EN]({dd}/README.en.md) · [🇹🇷 TR]({dd}/README.tr.md) |')
    else:
        L.append('No stars here yet ✦ The first post on this topic is coming soon.')
    (ROOT / "topics" / f'{p["id"]}.md').write_text("\n".join(L) + "\n", encoding="utf-8")

# tile blocks (relative for this repo, absolute for the profile README)
def tiles_block(base_img, base_link):
    w = f"{math.floor(1000 / n) / 10:.1f}%"
    imgs = "".join(f'<a href="{base_link}topics/{p["id"]}.md"><img src="{base_img}sky-{i}.svg" width="{w}" alt="{escape(p.get("label", p["name"]))}"></a>' for i, p in enumerate(planets))
    return f'<div align="center">\n\n<p>{imgs}</p>\n\n</div>'
caption = (f'✦ **{len(posts)} star{"s" if len(posts)!=1 else ""}** · {n} planets. Click a planet to see its posts.' if posts
           else f'✦ The first star is on its way · {n} planets. Click a planet to see its posts.')
rel = tiles_block("", "")
absb = tiles_block(f"https://raw.githubusercontent.com/{OWNER}/{REPO}/main/", f"https://github.com/{OWNER}/{REPO}/blob/main/")
(ROOT / "sky-embed.md").write_text(absb + "\n", encoding="utf-8")

# README blocks
rows = ["| Date | Topic | Title | Read |", "| :-- | :-- | :-- | :-- |"]
for s in sorted(posts, key=lambda p: p["date"], reverse=True):
    d = f'posts/{s["dir"]}'
    rows.append(f'| {s["date"]} | {names[s["topic"]]} | {s["title"]} | [🇬🇧 EN]({d}/README.en.md) · [🇹🇷 TR]({d}/README.tr.md) |')
if not posts:
    rows.append("| – | – | The first post is coming soon ✦ | – |")
text = (ROOT / "README.md").read_text(encoding="utf-8")
def fill(t, name, content):
    pat = rf"(<!-- {name}:START -->).*?(<!-- {name}:END -->)"
    if not re.search(pat, t, flags=re.S):
        raise SystemExit(f"README.md is missing the <!-- {name}:START --> / <!-- {name}:END --> markers")
    return re.sub(pat, lambda m: f"{m.group(1)}\n{content}\n{m.group(2)}", t, flags=re.S)
text = fill(text, "SKY", rel + "\n\n<div align=\"center\">\n\n" + caption + "\n\n</div>")
text = fill(text, "POSTS", "\n".join(rows))
(ROOT / "README.md").write_text(text, encoding="utf-8")
print(f"ok: {len(posts)} post(s), {n} planets, {n} tiles")
