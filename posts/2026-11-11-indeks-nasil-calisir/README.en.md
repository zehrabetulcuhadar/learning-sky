🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# How does a database index work? When does it hurt?

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** An index is a **sorted copy** of one or more columns of a table, with a pointer to where each row lives. In most relational databases that copy is stored as a **B-tree**. Without an index the database reads the whole table to find what it needs (a *full table scan*); with one it gets to the right place in a few steps, even among millions of rows. The cost: every `INSERT`, `UPDATE` and `DELETE` must update the index too, and the index takes up disk space. So "the more indexes the better" is not true.

## 1. What I researched and why

I have heard "the query is slow, let's add an index" many times. But I did not know what is inside an index, why it speeds things up, or why it is sometimes not used at all. Also, when I work with EF Core I rarely see the SQL it generates. To understand why a query is slow, I need to understand how indexes think.

## 2. Three key takeaways

1. **An index is like the index at the back of a book.** I am looking for the word "deadlock" in a 600-page book. Two options: read the whole book (full scan), or check the alphabetical index at the back, see "p. 412" and jump straight there (index). Because the book's index is sorted, I do not read that from the start either; I jump to "d".

   The database does this "jump" with a **B-tree**. A B-tree is a balanced, shallow tree where each node holds many sorted keys. One node fits in one disk page (often 8 KB) and can hold hundreds of keys. So the tree stays very shallow: roughly 3 to 4 levels even for a table with millions of rows. A lookup means reading 3-4 pages from root to leaf. A full scan means reading thousands. That is the difference: O(log n) instead of O(n).

   The leaves are also sorted and linked to each other, so a B-tree helps not only with equality but also with **ranges** (`WHERE date BETWEEN ...`), **sorting** (`ORDER BY`) and **prefixes** (`LIKE 'abc%'`).

2. **Having an index does not guarantee it will be used.** This was the most surprising part. Typical cases where an index does not help:
   - **Wrapping the column in a function:** `WHERE YEAR(created_at) = 2026` or `WHERE LOWER(email) = ...`. The index is sorted by `created_at`, not by `YEAR(created_at)`. Fix: `WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'`.
   - **Leading wildcard:** `LIKE '%sky'`. You cannot find "everything ending in sky" in a sorted list.
   - **Column order in a composite index:** an index on `(planet_id, date)` works for `WHERE planet_id = ...` and for both together, but usually not for `WHERE date = ...` alone. If a phone book is sorted by surname, you cannot search by first name. This is the **leftmost prefix rule**.
   - **Low selectivity:** `WHERE is_active = 1` when 95% of rows are active. The planner may find scanning the table cheaper than jumping through the index row by row.
   - **Implicit type conversion:** for example sending an `nvarchar` parameter for a `varchar` column (a classic SQL Server trap) can prevent the index from being used.

3. **Every index slows writes, so an index is a trade-off.** When I insert a row, the database must update **every** index on that table. Inserting into a table with five indexes means updating six structures. Indexes also take disk and memory. Read-heavy tables (a product catalog) benefit from more indexes; on write-heavy tables (logs, event records) every index needs a reason. The trade-off idea from my architecture post showed up here too.

   A few more terms:
   - **Clustered index:** the table itself is stored in this order, so there can be only one. In SQL Server the primary key is clustered by default.
   - **Nonclustered index:** a separate structure whose leaves point to the row.
   - **Covering index:** all the columns the query needs are in the index, so the table is not touched at all.

## 3. What I got wrong or still find unclear

- I thought defining a foreign key automatically creates an index. In SQL Server and PostgreSQL it **does not** (MySQL's InnoDB engine does). EF Core, on the other hand, usually adds an index on foreign key columns in its migrations. So the answer depends on the tool and needs checking.
- The planner decides whether to use an index based on statistics. When statistics get stale it can pick a bad plan. I will dig into this when I learn to read query plans.
- There are other index types too: hash, GIN, full-text. For now I stayed with B-trees.

## 4. Example

In [`example/`](example/) I use Python and SQLite to build a 300,000-row table and run the same query with and without an index. The script shows two things:

1. The `EXPLAIN QUERY PLAN` output: `SCAN posts` (full scan) without the index, `SEARCH posts USING INDEX ...` with it.
2. The timing difference, and that a query wrapping the column in a function, like `WHERE substr(date, 1, 4) = '2026'`, still scans even when the index exists.

On my machine the indexed query was hundreds of times faster. The numbers vary by machine, but the SCAN vs SEARCH difference in the plan is the same everywhere.

**AI note:** When I say "this query is slow, suggest an index", AI often suggests an index on every column in the WHERE clause. Instead I give it the query, the approximate row count, the read/write ratio and, if possible, the query plan. Then I check its suggestion with two questions: which writes will this index slow down? Does the query wrap the column in a function? The final word is always the real query plan.

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- Markus Winand. *Use The Index, Luke!* (a guide to SQL indexing). https://use-the-index-luke.com/
- PostgreSQL Documentation, "Indexes". https://www.postgresql.org/docs/current/indexes.html
- Microsoft Learn, "SQL Server index architecture and design guide". https://learn.microsoft.com/sql/relational-databases/sql-server-index-design-guide
- SQLite Documentation, "EXPLAIN QUERY PLAN". https://www.sqlite.org/eqp.html
- Microsoft Learn, EF Core "Indexes". https://learn.microsoft.com/ef/core/modeling/indexes
