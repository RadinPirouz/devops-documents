# 09 — Key Types

What each kind of key means, how they relate, and how they show up in SQL.

[← Normalization](./08-normalization.md) · [SQL index](./README.md)

> For foreign-key actions (`ON DELETE`) and relationship shapes (1:1 / 1:N / M:N), see [Keys & Relations](./06-keys-relations.md).

---

## Quick map

| Term | Idea |
| --- | --- |
| **Super key** | Any set of columns that uniquely identifies a row (may include extras) |
| **Candidate key** | A **minimal** super key (no column can be removed and still stay unique) |
| **Primary key** | The candidate key you **choose** as the main row identifier |
| **Alternate key** | Any candidate key that is **not** the primary key |
| **Composite key** | A key made of **two or more** columns |
| **Natural key** | A key from real-world data (email, national ID, ISBN, …) |
| **Surrogate key** | A key invented by the system (`SERIAL` / UUID) with no business meaning |
| **Foreign key** | A column (or set) that **references** a key in another table |

Hierarchy in one line:

**super key ⊇ candidate key → pick one as primary key; the rest are alternate keys.**

---

## Super key

Any column set that uniquely identifies each row. It can be wider than necessary.

Example table: `users (id, email, username, national_id)`

| Super key examples | Why unique? |
| --- | --- |
| `(id)` | one id per user |
| `(email)` | emails are unique |
| `(id, email)` | still unique — but `email` is extra |
| `(id, email, username)` | still unique — lots of extras |

`(id, email)` is a super key, but **not** minimal.

---

## Candidate key

A super key with **no unnecessary columns**. Remove any column and uniqueness breaks.

From the same table, typical candidate keys:

- `(id)`
- `(email)`
- `(username)`
- `(national_id)` (if unique and always present)

`(id, email)` is **not** a candidate key — you can drop `email` and still identify the row.

---

## Primary key

The candidate key you designate as the official identifier. Rules in practice:

- Unique
- `NOT NULL`
- One primary key per table (may be one column or several)

```sql
CREATE TABLE users (
    id       SERIAL PRIMARY KEY,          -- chosen primary key
    email    VARCHAR(50) UNIQUE NOT NULL, -- also a candidate key
    username VARCHAR(10) UNIQUE NOT NULL  -- also a candidate key
);
```

You pick **one** primary key; other unique columns stay as alternate keys (often via `UNIQUE`).

---

## Alternate key

A candidate key that was **not** chosen as the primary key.

In the example above:

| Role | Columns |
| --- | --- |
| Primary key | `id` |
| Alternate keys | `email`, `username` |

```sql
-- email is an alternate key: unique, but not the PK
CREATE TABLE users (
    id    SERIAL PRIMARY KEY,
    email VARCHAR(50) UNIQUE NOT NULL
);
```

---

## Composite key

A key that uses **more than one column**. Common for junction tables and order lines.

```sql
CREATE TABLE order_items (
    order_id   INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    qty        INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id)  -- composite primary key
);
```

Neither `order_id` nor `product_id` alone is unique here; the **pair** is.

Same idea as a composite **foreign** key when both columns together reference another table’s composite PK.

---

## Natural key

Taken from real-world / business data — something users already know.

Examples: email, ISBN, vehicle plate, country code (`IR`, `DE`).

```sql
CREATE TABLE countries (
    code CHAR(2) PRIMARY KEY,   -- natural key: ISO country code
    name VARCHAR(50) NOT NULL
);
```

**Pros:** meaningful, no extra id column.  
**Cons:** can change (email rename), may be long, privacy-sensitive, or not always available.

---

## Surrogate key

Invented by the database/app — usually a number or UUID with **no business meaning**.

```sql
CREATE TABLE users (
    id    SERIAL PRIMARY KEY,   -- surrogate key
    email VARCHAR(50) UNIQUE NOT NULL
);
```

**Pros:** stable, short, never changes when business data changes.  
**Cons:** opaque; you still need `UNIQUE` on natural fields you care about (like `email`).

Most app schemas use a **surrogate** PK (`id`) plus **unique natural** columns as alternate keys.

---

## Foreign key

A column (or set of columns) whose values must match a key in another table (usually that table’s primary key). Links parent → child rows.

```sql
CREATE TABLE users (
    id    SERIAL PRIMARY KEY,
    email VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE orders (
    order_id  SERIAL PRIMARY KEY,
    price     INTEGER NOT NULL,
    client_id INTEGER REFERENCES users(id)  -- foreign key → users.id
);
```

- `client_id = 5` is allowed only if `users` has `id = 5` (or `client_id` is `NULL` if the column allows it).
- The referenced side is often the primary key; it can also be any candidate/unique key.

See [Keys & Relations](./06-keys-relations.md) for `ON DELETE` / `ON UPDATE` and 1:1, 1:N, M:N patterns.

---

## How they fit together (example)

```sql
CREATE TABLE users (
    id           SERIAL PRIMARY KEY,           -- surrogate + primary
    email        VARCHAR(50) UNIQUE NOT NULL,  -- natural + alternate
    username     VARCHAR(10) UNIQUE NOT NULL,  -- natural + alternate
    national_id  VARCHAR(20) UNIQUE            -- natural + alternate (nullable)
);

CREATE TABLE orders (
    order_id  SERIAL PRIMARY KEY,              -- surrogate + primary
    client_id INTEGER NOT NULL
        REFERENCES users(id),                  -- foreign key
    total     INTEGER NOT NULL
);
```

| Column(s) | Types that apply |
| --- | --- |
| `users.id` | surrogate, candidate, **primary**, super |
| `users.email` | natural, candidate, **alternate**, super |
| `(users.id, users.email)` | super (not candidate — not minimal) |
| `orders.client_id` | **foreign** (references `users.id`) |
| `(order_id, product_id)` on a line-items table | **composite** primary (often) |

---

## Cheat sheet

| Question | Answer |
| --- | --- |
| What uniquely IDs a row (maybe with extras)? | Super key |
| What’s a minimal unique set? | Candidate key |
| Which candidate did we pick? | Primary key |
| Other candidates we didn’t pick? | Alternate key |
| Key from real data? | Natural key |
| Fake system-generated id? | Surrogate key |
| Key spanning several columns? | Composite key |
| Points at another table’s key? | Foreign key |
