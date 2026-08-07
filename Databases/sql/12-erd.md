# 12 — ERD (Entity–Relationship Diagram)

Visual map of entities, attributes, and relationships — drawn before (or while) you design tables and keys.

[← DEFAULT & CHECK](./11-check.md) · [SQL index](./README.md) · [Next: Transactions →](./13-transaction.md)

> For how 1:1 / 1:N / M:N become foreign keys in SQL, see [Keys & Relations](./06-keys-relations.md).

---

## Quick picture

An ERD answers: **what things exist**, **what data they hold**, and **how they connect**.

![ER notation styles (Chen, Crow’s Foot, UML, …)](./images/erd-notations.png)

*Same idea — Person born in Location — drawn in several common notations. This guide leans on **Chen** shapes for concepts, and **Crow’s Foot / IE** for practical schemas.*

---

## Entity

An **entity** is a real-world thing you store data about — a table candidate (`users`, `orders`, `products`).

Drawn as a **rectangle**. One row ≈ one instance of that entity.

### Entity types

| Type | Idea | On the diagram |
| --- | --- | --- |
| **Strong entity** | Exists on its own; has its own primary key | Solid rectangle |
| **Weak entity** | Needs a parent to make sense (e.g. `order_items` needs `orders`) | Double rectangle |
| **Associative entity** | Turns a many-to-many into its own entity (junction / link table), often with extra columns | Rectangle (sometimes diamond + rectangle) |

Examples:

- **Strong:** `users` identified by `user_id`
- **Weak:** `order_line` identified by `(order_id, line_no)` — depends on `orders`
- **Associative:** `user_roles` linking `users` ↔ `roles` (may also store `assigned_at`)

---

## Relationship

A **relationship** is how two (or more) entities connect — the verb between nouns (`places`, `belongs to`, `enrolls in`).

Drawn as a **diamond** (Chen) or as a **line** with crow’s-foot ends (IE).

### Relationship types

| Type | Idea | On the diagram |
| --- | --- | --- |
| **Strong (identifying)** | Child’s identity includes the parent’s key (typical for weak entities) | Solid line; often double diamond in Chen |
| **Weak (non-identifying)** | Child has its own key; FK is just a reference, not part of the child’s identity | Dashed line in many tools |

Example: `orders.client_id → users.id` is usually **non-identifying** (order has its own `order_id`).  
`order_items` with PK `(order_id, product_id)` is often **identifying**.

---

## Attribute

An **attribute** is a property of an entity (or relationship) — a column candidate (`email`, `price`, `created_at`).

Drawn as an **oval** connected to its entity (Chen).

| Type | Idea | On the diagram |
| --- | --- | --- |
| **Simple (single-valued)** | One value per instance | Single oval |
| **Composite** | Made of parts (`address` → street, city, zip) | Oval with child ovals |
| **Multivalued** | Several values at once (phones, tags) | **Double oval** |
| **Derived** | Calculated from other data (age from birthdate) | Dashed oval |
| **Key attribute** | Uniquely identifies the entity (primary key) | Oval with **underline** |

> **Underline = primary key.** If an attribute is underlined on the ERD, that attribute (or set) is the entity’s identifier.

**Strong vs weak attributes (informal wording):**

- **Strong / identifying:** part of (or the) primary key — underlined
- **Weak / descriptive:** ordinary data — not underlined

Multivalued attributes usually become a **separate table** in SQL (see 1NF in [Normalization](./08-normalization.md)).

---

## Cardinality (how many)

Cardinality says how many instances of B relate to one instance of A.

| Name | Meaning | Typical SQL |
| --- | --- | --- |
| **One-to-one (1:1)** | Each A links to at most one B, and vice versa | FK on one side, marked `UNIQUE` |
| **One-to-many (1:N)** | One A has many B; each B has one A | FK on the **many** side |
| **Many-to-one (N:1)** | Same as 1:N, viewed from the child | Same as above |
| **Many-to-many (M:N)** | Many A ↔ many B | **Junction table** (associative entity) |

Chen often labels lines with `1` and `N` (or `M`). Crow’s Foot uses the “bird foot” for many and a bar for one.

---

## Chen example (full diagram)

Sample ER model in Chen notation (entities as rectangles, relationships as diamonds, attributes as ovals; underlined attributes are keys):

![Chen notation ERD example](./images/erd-chen-example.png)

---

## Crow’s Foot / IE example (closer to tables)

Same style many tools export: boxes with columns, `PK` / `FK`, and cardinality on the lines:

![ERD schema example with PK/FK](./images/erd-example.png)

---

## From ERD → SQL (cheat sheet)

| On the ERD | In SQL |
| --- | --- |
| Strong entity | `CREATE TABLE` + primary key |
| Weak entity | Table whose PK includes the parent’s key (or a composite PK) |
| Associative entity / M:N | Junction table with two FKs (often composite PK) |
| Attribute | Column |
| Underlined attribute | `PRIMARY KEY` (or part of it) |
| Multivalued attribute | Extra table, FK back to parent |
| 1:N relationship | FK on the N side |
| 1:1 relationship | FK + `UNIQUE` |
| Identifying relationship | Child PK includes parent FK |

```sql
-- 1:N  (many orders → one user)
CREATE TABLE orders (
    order_id  SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES users(id)
);

-- M:N via associative entity
CREATE TABLE user_roles (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);
```

---

## Cheat sheet

| Term | Remember |
| --- | --- |
| Entity | Noun / table |
| Relationship | Verb / link between tables |
| Attribute | Property / column |
| Underline | Primary key |
| Double rectangle | Weak entity |
| Double oval | Multivalued attribute |
| Diamond (Chen) | Relationship |
| Crow’s foot | “Many” side |
| Associative entity | Junction table for M:N |
