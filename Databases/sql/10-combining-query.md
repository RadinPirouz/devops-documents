# 10 — Combining Queries

Stack result sets from two (or more) `SELECT`s with set operators.

[← Key Types](./09-keys.md) · [SQL index](./README.md) · [Next: DEFAULT & CHECK →](./11-check.md)

---

## Overview

| Operator | Keeps |
| --- | --- |
| `UNION` | Rows from both queries, **duplicates removed** |
| `UNION ALL` | Rows from both queries, **duplicates kept** |
| `INTERSECT` | Only rows that appear in **both** results |
| `EXCEPT` | Rows from the **first** query that are **not** in the second |

Rules that apply to all of them:

- Each `SELECT` must return the **same number of columns**.
- Matching columns should have **compatible types** (e.g. both text, both numbers).
- Column names in the result come from the **first** query.
- By default, `UNION` / `INTERSECT` / `EXCEPT` remove duplicates (same as writing `… DISTINCT`). `UNION ALL` keeps them.

---

## UNION

Cities from `foods` and cities from `customers`, each city listed once even if it appears in both tables (or twice in one table):

```sql
SELECT city FROM foods
UNION
SELECT city FROM customers;
```

`UNION DISTINCT` is the same idea made explicit (PostgreSQL):

```sql
SELECT city FROM foods
UNION DISTINCT
SELECT city FROM customers;
```

---

## UNION ALL

Same as `UNION`, but keep every row — including duplicates. Faster when you don’t need uniqueness:

```sql
SELECT city FROM foods
UNION ALL
SELECT city FROM customers;
```

If `"Tehran"` is in both tables, it shows up twice (or more).

---

## INTERSECT

Only cities that appear in **both** `foods` and `customers`:

```sql
SELECT city FROM foods
INTERSECT
SELECT city FROM customers;
```

---

## EXCEPT

Cities in `foods` that are **not** in `customers` (first query minus second):

```sql
SELECT city FROM foods
EXCEPT
SELECT city FROM customers;
```

Order matters: `A EXCEPT B` ≠ `B EXCEPT A`.

---

## Cheat sheet

| Want… | Use |
| --- | --- |
| Both results, no duplicates | `UNION` |
| Both results, keep duplicates | `UNION ALL` |
| Only shared rows | `INTERSECT` |
| First minus second | `EXCEPT` |
