# 05 — DML (INSERT / UPDATE / DELETE)

Write and change data.

[← Aggregates](./04-aggregates.md) · [SQL index](./README.md) · [Next: Keys & Relations →](./06-keys-relations.md)

---

## INSERT

Add one new row. List the columns, then matching values in the same order:

```sql
INSERT INTO customers (customerid, company, country)
VALUES ('abbas', 'BMW', 'GE');
```

PostgreSQL: insert and immediately return the new row (handy after serial IDs or defaults):

```sql
INSERT INTO customers (customerid, company, country)
VALUES ('abbas', 'BMW', 'GE')
RETURNING *;
```

Same idea, but only return the columns you care about:

```sql
INSERT INTO customers (customerid, company, country)
VALUES ('abbas', 'BMW', 'GE')
RETURNING customerid, company, country;
```

Table with `SERIAL` primary key: omit `id` — the database fills it automatically:

```sql
INSERT INTO users (email, username, pass)
VALUES ('abbas@gmail.com', 'abbas', 'abbas123');
```

---

## UPDATE

Change existing rows. Always use `WHERE` unless you mean to update **every** row. Here: set company to BENZ for that customer, then return the updated fields:

```sql
UPDATE customers
SET company = 'BENZ'
WHERE customerid = 'abbas'
RETURNING customerid, company, country;
```

---

## DELETE

Remove matching rows. Without `WHERE`, this would delete the whole table’s data:

```sql
DELETE FROM customers WHERE customerid = 'abbas';
```

---

## Copy rows into another table

Create a **new** table and fill it from a query (`SELECT INTO` — PostgreSQL). Copies BMW/BENZ customers into `ge_customers`:

```sql
SELECT * INTO ge_customers
FROM customers
WHERE company IN ('BMW', 'BENZ');
```

`ge_customers` already exists — copy matching rows into it with `INSERT … SELECT`:

```sql
INSERT INTO ge_customers
SELECT * FROM customers
WHERE company IN ('BMW', 'BENZ');
```
