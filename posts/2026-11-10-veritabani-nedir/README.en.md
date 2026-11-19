🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# What is a database? The relational model, tables and keys

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** A database is software that stores data durably, lets many users read and write it safely at the same time, and guarantees the data keeps following its rules (stays consistent). Relational databases (SQL Server, PostgreSQL, MySQL, SQLite) keep data in **tables**, connect tables with **keys**, and are queried with **SQL**.

## 1. What I researched and why

At work I write .NET code that talks to a database every day, and with EF Core I treat tables like classes. But I did not have a clear answer to "what does a database actually do, and why don't we just write the data to a JSON file?" So the first post on the data planet starts from the very bottom.

My own project has an interesting twist: Learning Sky's "database" is really the `posts/*/meta.json` files and the `sky.json` generated from them. That works great for a small project. Understanding why it would not work for a large system is understanding why databases exist.

## 2. Three key takeaways

1. **A database solves four problems a file cannot.** Writing data to a file is easy. The hard parts are:
   - **Concurrent access:** if two people write the same file at once, one overwrites the other. A database manages this with locks and transactions.
   - **Consistency:** a database enforces rules like "every order must have a customer". A file does not care about any rule.
   - **Crash safety:** if a write is interrupted, a file can be corrupted. A database does all of the work or none of it (atomicity, the A in ACID; more in the transactions post).
   - **Fast lookup:** finding one record in a million-line file means reading it from start to end. A database uses indexes to bring that down to milliseconds.

2. **The relational model: tables, rows, columns and keys.** The model Edgar F. Codd proposed in 1970 is still the most common one. The core idea is to split data into tables without repeating it:
   - **Table:** records of the same kind (for example `posts`).
   - **Row:** one record (one post).
   - **Column:** one property of the record (title, date). Each column has a type.
   - **Primary key:** the column that uniquely identifies a row (`id`). No duplicates, no nulls.
   - **Foreign key:** a column pointing at another table's primary key. `posts.planet_id` → `planets.id`. The database will not let you attach a post to a planet that does not exist. This is called **referential integrity**.

   There are three kinds of relationships: **one-to-one**, **one-to-many** (a planet has many posts) and **many-to-many** (a post has many tags, a tag has many posts). Many-to-many cannot be stored directly, so a **join table** (`post_tags`) sits in between. That is exactly what lies under EF Core's navigation properties.

3. **SQL says what I want, not how to find it.** SQL is a declarative language. When I write `SELECT ... WHERE ... JOIN ...` I describe the result, and the database's **query planner** decides which table to read in which order. That is why the same query can become a hundred times faster after adding an index, without changing a single line of code. It is also why I like LINQ: it describes what I want, too.

## 3. What I got wrong or still find unclear

- I thought "database" and "database management system" (DBMS) were the same. Technically the database is the data itself and SQL Server is the software managing it. In everyday speech both are called "the database".
- Why not keep everything in one big table? To avoid repetition: if I write the planet's name on every post row, renaming it means updating hundreds of rows, and if I miss one the data becomes inconsistent. That is normalization, a topic for another post. Apparently repetition is sometimes added on purpose for performance, and I do not fully get that yet.
- Why do NoSQL databases deliberately relax some of these rules? I will come back to that later on the data planet.

## 4. Example

In [`example/`](example/) I modelled Learning Sky as a small relational database: `planets`, `posts`, `tags` and the join table `post_tags`. The script builds the tables in SQLite, inserts a few rows, runs a JOIN query and then **tries to add a post to a planet that does not exist**. The database refuses because of the foreign key rule. A JSON file would have silently accepted it.

```
planets 1 ── * posts * ── * tags
              (post_tags join table)
```

**AI note:** When I ask AI to design tables I have to state the business rules explicitly ("a post has exactly one planet and can have several tags"). Otherwise it may produce a schema that puts everything in one table or adds relationships nobody needs. In the schema it produces I always check: does every table have a primary key, are foreign keys defined, do `NOT NULL` and `UNIQUE` constraints match the business rules?

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- E. F. Codd. "A Relational Model of Data for Large Shared Data Banks", *Communications of the ACM*, 1970.
- PostgreSQL Documentation, "Constraints" (primary and foreign keys). https://www.postgresql.org/docs/current/ddl-constraints.html
- SQLite Documentation, "SQLite Foreign Key Support". https://www.sqlite.org/foreignkeys.html
- Martin Kleppmann. *Designing Data-Intensive Applications*, O'Reilly, Chapter 2 (data models).
