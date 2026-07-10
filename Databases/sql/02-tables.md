# 02 — Tables

Create and alter tables, columns, and basic constraints.

[← Databases](./01-databases.md) · [SQL index](./README.md) · [Next: SELECT →](./03-select.md)

---

## Create table

Define columns and constraints. `UNIQUE` / `NOT NULL` reject bad inserts; `age` is optional (`NULL` allowed):

```sql
CREATE TABLE users (
    email    VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(10) UNIQUE NOT NULL,
    pass     VARCHAR(50) NOT NULL,
    age      SMALLINT
);
```

Add `id` as primary key. `SERIAL` = auto-increment integer in PostgreSQL (you omit it on insert):

```sql
CREATE TABLE users (
    id       SERIAL PRIMARY KEY,
    email    VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(10) UNIQUE NOT NULL,
    pass     VARCHAR(50) NOT NULL
);
```

> Use `users`, not `user` — `user` is a reserved keyword in many databases.

---

## Alter table

Remove the `age` column (and its data):

```sql
ALTER TABLE users DROP COLUMN age;
```

Add `age` back; new rows must supply a value (`NOT NULL`):

```sql
ALTER TABLE users ADD COLUMN age SMALLINT NOT NULL;
```

Rename a column (PostgreSQL):

```sql
ALTER TABLE users RENAME COLUMN pass TO password;
```

Rename the whole table:

```sql
ALTER TABLE users RENAME TO accounts;
```
