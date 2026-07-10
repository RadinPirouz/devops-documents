# 06 — Keys & Relations

Primary keys, foreign keys, delete actions, and relationship types.

[← DML](./05-dml.md) · [SQL index](./README.md) · [Next: Joins →](./07-joins.md)

---

## Primary key + foreign key

```sql
CREATE TABLE users (
    id       SERIAL PRIMARY KEY,
    email    VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(10) UNIQUE NOT NULL,
    pass     VARCHAR(50) NOT NULL
);

CREATE TABLE orders (
    order_id  SERIAL PRIMARY KEY,
    price     VARCHAR(10),
    client_id INTEGER REFERENCES users(id)
);

INSERT INTO users (email, username, pass)
VALUES ('abbas@email.com', 'abbas', '123');

INSERT INTO orders (price, client_id)
VALUES ('1000', 1);
```

`client_id` must match an existing `users.id` (or be `NULL` if the column allows it).

---

## ON DELETE actions

When a parent row is deleted, the foreign key can:

| Action | Behavior |
| --- | --- |
| `NO ACTION` | Reject delete if child rows still reference it (default; check deferred) |
| `RESTRICT` | Reject delete immediately if child rows exist |
| `CASCADE` | Delete child rows too |
| `SET NULL` | Set the FK column to `NULL` on child rows |
| `SET DEFAULT` | Set the FK column to its default value |

```sql
CREATE TABLE orders (
    order_id  SERIAL PRIMARY KEY,
    price     VARCHAR(10),
    client_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
```

Same options exist for `ON UPDATE`.

---

## Relationship types

### Many-to-one (N:1) / One-to-many (1:N)

Many orders belong to one user. FK lives on the “many” side:

```sql
CREATE TABLE orders (
    order_id  SERIAL PRIMARY KEY,
    price     VARCHAR(10),
    client_id INTEGER REFERENCES users(id)  -- many orders → one user
);
```

### One-to-one (1:1)

Same as many-to-one, but the FK is **UNIQUE** so each user has at most one order (or profile, etc.):

```sql
CREATE TABLE profiles (
    profile_id SERIAL PRIMARY KEY,
    bio        TEXT,
    user_id    INTEGER UNIQUE REFERENCES users(id)
);
```

### Many-to-many (M:N)

Use a **junction (link) table**. Example: users ↔ roles:

```sql
CREATE TABLE roles (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE user_roles (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);
```

Each row in `user_roles` links one user to one role. A user can have many roles; a role can belong to many users.
