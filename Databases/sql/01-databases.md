# 01 — Databases

Create, drop, and rename databases.

[← SQL index](./README.md) · [Next: Tables →](./02-tables.md)

---

## Create

Create an empty database named `test`:

```sql
CREATE DATABASE test;
```

Same, but set character encoding (PostgreSQL):

```sql
CREATE DATABASE test WITH ENCODING = 'UTF8';
```

---

## Drop

Delete the database (fails if something is still connected, depending on the engine):

```sql
DROP DATABASE test;
```

Safe drop — no error if `test` is already gone:

```sql
DROP DATABASE IF EXISTS test;
```

Force drop (PostgreSQL — terminates open connections, then drops):

```sql
DROP DATABASE IF EXISTS test WITH (FORCE);
```

---

## Rename

Rename `test` to `abbas`:

```sql
ALTER DATABASE test RENAME TO abbas;
```
