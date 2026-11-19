# Runs schema.sql with Python's built-in sqlite3 (dot commands are skipped).
import pathlib, sqlite3

sql = pathlib.Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
statements = [s for s in sql.split(";") if s.strip()]
db = sqlite3.connect(":memory:")
for s in statements:
    s = "\n".join(l for l in s.splitlines() if not l.startswith("."))
    try:
        rows = db.execute(s).fetchall()
        for r in rows:
            print(" | ".join(map(str, r)))
    except sqlite3.IntegrityError as e:
        print("Refused by the database:", e)
