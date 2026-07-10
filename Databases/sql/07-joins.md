# 07 — Joins

Combine rows from two or more tables.

[← Keys & Relations](./06-keys-relations.md) · [SQL index](./README.md) · [Next: Normalization →](./08-normalization.md)

---

## Join types

| Join | Keeps |
| --- | --- |
| `INNER JOIN` | Only matching rows in both tables |
| `LEFT JOIN` | All rows from left + matches from right (`NULL` if no match) |
| `RIGHT JOIN` | All rows from right + matches from left |
| `FULL JOIN` | All rows from both (`NULL` where no match) |

Default when you write plain `JOIN` is **INNER JOIN**.

Customers who have at least one order (no match → row dropped). `ON` says how rows link — same `customerid`:

```sql
SELECT *
FROM customers
JOIN orders ON orders.customerid = customers.customerid;
```

Same as above — `INNER JOIN` is explicit:

```sql
SELECT *
FROM customers
INNER JOIN orders ON orders.customerid = customers.customerid;
```

All customers, plus their orders when they exist. Customer with no orders still appears; order columns are `NULL`:

```sql
SELECT *
FROM customers
LEFT JOIN orders ON orders.customerid = customers.customerid;
```

All orders, plus customer info when it exists. Order with no matching customer still appears:

```sql
SELECT *
FROM customers
RIGHT JOIN orders ON orders.customerid = customers.customerid;
```

Every customer and every order. Unmatched sides get `NULL` on the other table’s columns:

```sql
SELECT *
FROM customers
FULL JOIN orders ON orders.customerid = customers.customerid;
```

---

## Self-join

Join a table to itself (e.g. employee → manager). Two aliases (`emp`, `mng`) treat the same table as two roles:

```sql
SELECT
    emp.name AS "emp name",
    mng.name AS "manager name"
FROM employees AS emp
JOIN employees AS mng ON mng.id = emp.reported_to;
```

`emp.reported_to` points at the manager’s `id`. Each result row is one employee paired with their manager.
