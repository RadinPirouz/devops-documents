# 04 — Aggregates

Summarize rows with aggregate functions and `GROUP BY`.

[← SELECT](./03-select.md) · [SQL index](./README.md) · [Next: DML →](./05-dml.md)

---

## Aggregate functions

Collapse many rows into one number. Lowest, average, highest, and total of `price` across all orders:

```sql
SELECT MIN(price) FROM orders;
SELECT AVG(price) FROM orders;
SELECT MAX(price) FROM orders;
SELECT SUM(price) FROM orders;
```

How many non-`NULL` country values exist (one count for the whole table):

```sql
SELECT COUNT(country) FROM customers;
```

How many **different** countries (duplicates ignored):

```sql
SELECT COUNT(DISTINCT country) FROM customers;
```

`COUNT(*)` counts all rows, including `NULL`s. `COUNT(column)` skips `NULL`s.

---

## GROUP BY

Split rows into groups (one group per country), then count how many users are in each group. `ORDER BY` sorts the groups:

```sql
SELECT country, COUNT(*)
FROM users
GROUP BY country
ORDER BY country ASC;
```

`HAVING` filters **groups** after they are built. Only countries with more than 5 users, largest groups first:

```sql
SELECT country, COUNT(*) AS total
FROM users
GROUP BY country
HAVING COUNT(*) > 5
ORDER BY total DESC;
```

> `WHERE` filters rows **before** grouping. `HAVING` filters groups **after** grouping.
