# Example: Learning Sky as a relational database

`schema.sql` creates four tables (`planets`, `posts`, `tags`, `post_tags`), inserts sample rows, runs a JOIN and then tries to insert a post with a planet that does not exist.

Run it with the SQLite command line tool:

```bash
sqlite3 :memory: < schema.sql
```

No SQLite installed? Python ships with it: `python run.py`.

The last statement fails with `FOREIGN KEY constraint failed`. That error is the point of the example.
