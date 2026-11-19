import random, sqlite3, time

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, planet TEXT, date TEXT, title TEXT)")
planets = ["basics", "backend", "frontend", "data", "quality", "architecture", "ai", "english", "news"]
random.seed(42)
rows = [
    (i, random.choice(planets), f"{random.randint(2020, 2030)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}", f"Post {i}")
    for i in range(1, 300_001)
]
db.executemany("INSERT INTO posts VALUES (?, ?, ?, ?)", rows)

def run(label, sql, repeat=20):
    plan = " / ".join(r[-1] for r in db.execute("EXPLAIN QUERY PLAN " + sql))
    start = time.perf_counter()
    for _ in range(repeat):
        db.execute(sql).fetchall()
    ms = (time.perf_counter() - start) / repeat * 1000
    print(f"{label:<34} {ms:8.3f} ms   plan: {plan}")
    return ms

query = "SELECT title FROM posts WHERE date = '2026-11-21'"
before = run("1. no index", query)

db.execute("CREATE INDEX ix_posts_date ON posts(date)")
after = run("2. with index on date", query)
run("3. index, but column in a function", "SELECT title FROM posts WHERE substr(date, 1, 7) = '2026-11'")
run("4. index, rewritten as a range", "SELECT title FROM posts WHERE date >= '2026-11-01' AND date < '2026-12-01'")

print(f"\nThe indexed lookup was about {before / after:,.0f}x faster on this machine.")
