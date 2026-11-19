# Example: the same query with and without an index

```bash
python index_demo.py
```

Needs only Python 3 (SQLite is built in). It builds a 300,000-row `posts` table in memory, then prints the query plan and the time for:

1. a lookup without an index (`SCAN`),
2. the same lookup with an index (`SEARCH ... USING INDEX`),
3. a query that wraps the indexed column in a function (back to `SCAN`).
