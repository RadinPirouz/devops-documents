# 14 — Indexes

An **index** is a lookup structure on one or more columns. It speeds up `WHERE`, joins, and `ORDER BY` — like a book index instead of scanning every page.

[← Transactions](./13-transaction.md) · [SQL index](./README.md)

---

## Why use them?

Without an index, finding `email = 'radin@gmail.com'` means a **full table scan** (check every row).

With an index on `email`, the engine jumps near the matching rows.

Trade-off: indexes use disk/memory, and every `INSERT` / `UPDATE` / `DELETE` must also update the index.

---

## Create an index

Speed up lookups on `email`:

```sql
CREATE INDEX idx_users_email ON users (email);
```

Then queries like this can use the index:

```sql
SELECT * FROM users WHERE email = 'radin@gmail.com';
```

Name indexes clearly (`idx_table_column`) so they are easy to drop later.

---

## Unique index

Same as a normal index, but values must be unique (like a `UNIQUE` constraint):

```sql
CREATE UNIQUE INDEX idx_users_email ON users (email);
```

> `PRIMARY KEY` and `UNIQUE` constraints already create unique indexes behind the scenes. You usually don’t need a second index on the same column.

---

## Composite index

One index on **several columns**. Order matters: the index helps filters that match a **left prefix**.

```sql
CREATE INDEX idx_orders_user_created
ON orders (user_id, created_at);
```

| Query shape | Likely uses this index? |
| --- | --- |
| `WHERE user_id = 5` | Yes (leftmost column) |
| `WHERE user_id = 5 AND created_at > '2024-01-01'` | Yes |
| `WHERE created_at > '2024-01-01'` alone | Usually **no** — skipped the first column |

Put the most selective / most-filtered column first when you can.

---

## Drop an index

```sql
DROP INDEX idx_users_email;           -- PostgreSQL
DROP INDEX idx_users_email ON users;  -- MySQL
```

---

## When to add an index

Good candidates:

- Columns in `WHERE`, `JOIN … ON`, or `ORDER BY` on large tables
- Foreign keys you join on often (`orders.user_id`)
- Columns you search by equality or range (`id`, `email`, `created_at`)

Often skip / rethink:

- Tiny tables (scan is cheap)
- Columns that change constantly and are rarely filtered
- Low-cardinality columns alone (`is_active` true/false) — little selectivity
- Indexing every column “just in case” (hurts writes, wastes space)

---

## Check if the planner uses it (PostgreSQL)

```sql
EXPLAIN SELECT * FROM users WHERE email = 'radin@gmail.com';
```

Look for `Index Scan` / `Index Only Scan` vs `Seq Scan` (full table scan).

MySQL:

```sql
EXPLAIN SELECT * FROM users WHERE email = 'radin@gmail.com';
```

Same idea — see whether `key` shows your index name.

---

## Cheat sheet

| Want… | Use |
| --- | --- |
| Faster lookups on a column | `CREATE INDEX name ON table (col);` |
| Unique values + fast lookup | `CREATE UNIQUE INDEX …` or `UNIQUE` / `PRIMARY KEY` |
| Filter on several columns together | Composite: `ON table (a, b)` — left prefix matters |
| Remove an index | `DROP INDEX name;` (MySQL: `DROP INDEX name ON table;`) |
| See if it helps | `EXPLAIN` the query |
| Remember | Faster reads, slower writes + extra storage |
