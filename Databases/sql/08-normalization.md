# 08 — Normalization

Reduce duplication and keep data consistent by organizing tables into normal forms.

[← Joins](./07-joins.md) · [SQL index](./README.md) · [Next: Key Types →](./09-keys.md)

> **WIP** — expand with more real schemas as you practice.

---

## Why normalize?

- Avoid storing the same fact in many places
- Make updates safer (change once, not in every row)
- Keep relationships clear with keys

---

## First Normal Form (1NF)

Rules:

1. Each column holds a **single** value (no lists/arrays in a cell for classic 1NF).
2. Each row is unique (usually via a primary key).
3. No repeating groups of columns (`phone1`, `phone2`, `phone3` → separate rows or a phones table).

**Bad (not 1NF):**

| order_id | products |
| --- | --- |
| 1 | apple, banana, milk |

**Good (1NF):**

| order_id | product |
| --- | --- |
| 1 | apple |
| 1 | banana |
| 1 | milk |

---

## Second Normal Form (2NF)

Rules:

1. Must already be in **1NF**.
2. Every non-key column depends on the **whole** primary key (no partial dependency).

Matters when the PK is **composite**.

**Bad (not 2NF)** — `product_name` depends only on `product_id`, not on `(order_id, product_id)`:

| order_id | product_id | product_name | qty |
| --- | --- | --- | --- |
| 1 | 10 | Mouse | 2 |
| 1 | 20 | Keyboard | 1 |

**Good (2NF)** — split:

```sql
CREATE TABLE products (
    product_id   SERIAL PRIMARY KEY,
    product_name VARCHAR(50) NOT NULL
);

CREATE TABLE order_items (
    order_id   INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    qty        INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
```

---

## Third Normal Form (3NF)

Rules:

1. Must already be in **2NF**.
2. Non-key columns must depend **only on the key**, not on other non-key columns (no transitive dependency).

**Bad (not 3NF)** — `city` determines `zip`; `zip` is not the key:

| customer_id | name | zip | city |
| --- | --- | --- | --- |
| 1 | Abbas | 11369 | Tehran |

**Good (3NF):**

```sql
CREATE TABLE zip_codes (
    zip  VARCHAR(10) PRIMARY KEY,
    city VARCHAR(50) NOT NULL
);

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name        VARCHAR(50) NOT NULL,
    zip         VARCHAR(10) REFERENCES zip_codes(zip)
);
```

---

## Quick checklist

| Form | Ask yourself |
| --- | --- |
| 1NF | One value per cell? Unique rows? |
| 2NF | Non-key fields depend on the full PK? |
| 3NF | Non-key fields depend only on the key (not on each other)? |

In practice, aiming for **3NF** is enough for most application schemas.
