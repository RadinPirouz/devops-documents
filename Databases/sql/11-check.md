# 11 — DEFAULT & CHECK

Set fallback values and reject rows that break your rules.

[← Combining Queries](./10-combining-query.md) · [SQL index](./README.md)

---

## DEFAULT

If an `INSERT` omits a column, the database fills in the default. Here `price` becomes `1000` when not supplied:

```sql
CREATE TABLE products (
    product_num INTEGER,
    name        TEXT,
    price       NUMERIC DEFAULT 1000
);
```

---

## CHECK (column)

`CHECK` rejects inserts/updates that fail the condition. Price must be greater than zero:

```sql
CREATE TABLE products (
    product_num INTEGER,
    name        TEXT,
    price       NUMERIC DEFAULT 1000 CHECK (price > 0)
);
```

---

## Named constraints

Name a constraint so error messages and `ALTER TABLE … DROP CONSTRAINT` are clearer:

```sql
CREATE TABLE products (
    product_num INTEGER,
    name        TEXT,
    price       NUMERIC DEFAULT 1000 CONSTRAINT positive_price CHECK (price > 0)
);
```

---

## Several checks

Column checks run per column. A **table-level** `CHECK` can compare columns (discount cannot exceed price):

```sql
CREATE TABLE products (
    product_num INTEGER,
    name        TEXT,
    price       NUMERIC DEFAULT 1000 CONSTRAINT positive_price CHECK (price > 0),
    discount    NUMERIC DEFAULT 0    CONSTRAINT non_negative_discount CHECK (discount >= 0),
    CHECK (discount <= price)
);
```

---

## Cheat sheet

| Want… | Use |
| --- | --- |
| Value when column omitted | `DEFAULT …` |
| Rule on one column | `CHECK (…)` after the column |
| Named rule (easier to drop/debug) | `CONSTRAINT name CHECK (…)` |
| Rule across columns | Table-level `CHECK (…)` |
