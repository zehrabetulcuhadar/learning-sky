"""List the last N days of posts from the feeds in feeds.txt (RSS 2.0 and Atom)."""
import pathlib
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

ATOM = "{http://www.w3.org/2005/Atom}"
days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
since = datetime.now(timezone.utc) - timedelta(days=days)


def parse_date(text):
    if not text:
        return None
    try:
        d = parsedate_to_datetime(text)  # RSS: "Tue, 15 Dec 2026 10:00:00 GMT"
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(text.replace("Z", "+00:00"))  # Atom: ISO 8601
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def read_feed(url):
    req = urllib.request.Request(url, headers={"User-Agent": "weekly-feed-reader/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        root = ET.fromstring(r.read())
    source = root.findtext("channel/title") or root.findtext(f"{ATOM}title") or url
    for item in root.iter("item"):  # RSS
        yield source, item.findtext("title"), item.findtext("link"), parse_date(item.findtext("pubDate"))
    for entry in root.iter(f"{ATOM}entry"):  # Atom
        link = entry.find(f"{ATOM}link")
        date = entry.findtext(f"{ATOM}updated") or entry.findtext(f"{ATOM}published")
        yield source, entry.findtext(f"{ATOM}title"), link.get("href") if link is not None else "", parse_date(date)


feeds = [l.strip() for l in (pathlib.Path(__file__).parent / "feeds.txt").read_text().splitlines()
         if l.strip() and not l.startswith("#")]
posts = []
for url in feeds:
    try:
        posts += [p for p in read_feed(url) if p[3] and p[3] >= since]
    except Exception as e:  # one broken feed should not stop the rest
        print(f"! skipped {url}: {e}", file=sys.stderr)

for source, title, link, date in sorted(posts, key=lambda p: p[3], reverse=True):
    print(f"{date:%Y-%m-%d}  [{source[:24]}]  {(title or '').strip()}\n            {link}")
print(f"\n{len(posts)} posts from {len(feeds)} feeds in the last {days} days.")
