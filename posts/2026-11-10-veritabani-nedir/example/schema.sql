PRAGMA foreign_keys = ON;  -- SQLite needs this, SQL Server and PostgreSQL enforce foreign keys by default

CREATE TABLE planets (
  id   TEXT PRIMARY KEY,           -- 'basics', 'data', ...
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE posts (
  id        INTEGER PRIMARY KEY,
  planet_id TEXT NOT NULL REFERENCES planets(id),  -- foreign key: one planet, many posts
  title     TEXT NOT NULL,
  date      TEXT NOT NULL
);

CREATE TABLE tags (
  id   INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

-- many-to-many: a post has many tags, a tag has many posts
CREATE TABLE post_tags (
  post_id INTEGER NOT NULL REFERENCES posts(id),
  tag_id  INTEGER NOT NULL REFERENCES tags(id),
  PRIMARY KEY (post_id, tag_id)
);

INSERT INTO planets VALUES ('architecture', 'Architecture'), ('data', 'Data');
INSERT INTO posts VALUES
  (1, 'architecture', 'What is software architecture?', '2026-11-10'),
  (2, 'data',         'What is a database?',            '2026-11-10');
INSERT INTO tags VALUES (1, 'trade-off'), (2, 'sql'), (3, 'basics');
INSERT INTO post_tags VALUES (1, 1), (1, 3), (2, 2), (2, 3);

.headers on
.mode column
SELECT p.date, pl.name AS planet, p.title, GROUP_CONCAT(t.name, ', ') AS tags
FROM posts p
JOIN planets pl  ON pl.id = p.planet_id
JOIN post_tags pt ON pt.post_id = p.id
JOIN tags t      ON t.id = pt.tag_id
GROUP BY p.id
ORDER BY p.date;

-- This planet does not exist, so the database refuses the row:
INSERT INTO posts VALUES (3, 'astrology', 'Oops', '2026-11-11');
