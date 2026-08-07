# 13 — Transactions

A **transaction** is a group of SQL statements treated as **one unit of work**: either everything succeeds, or nothing is kept.

[← ERD](./12-erd.md) · [SQL index](./README.md) · [Next: Indexes →](./14-index.md)

---

## Why use them?

Without a transaction, a crash or error mid-way can leave the database half-updated (money left one account but never arrived in the other).

Classic example — transfer $100 from Alice to Bob:

1. Debit Alice  
2. Credit Bob  

Both must happen, or neither should.

---

## Use in MySQL / MariaDB

```sql
START TRANSACTION;
SELECT * FROM users;
UPDATE users SET name = 'radin' WHERE id = 1;
COMMIT;
```

`START TRANSACTION` begins the unit. Changes stay private until `COMMIT`. If something goes wrong, undo with `ROLLBACK` instead:

```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Alice
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- Bob
-- oops: Bob's row missing → undo both
ROLLBACK;
```

---

## PostgreSQL note

Same idea; `BEGIN` is the usual start (also accepts `START TRANSACTION`):

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

---

## ACID properties

| Letter | Name | Meaning |
| --- | --- | --- |
| **A** | Atomicity | All statements succeed, or the whole transaction is undone — no partial apply |
| **C** | Consistency | Before and after the transaction, rules hold (constraints, keys, valid balances, …) |
| **I** | Isolation | Concurrent transactions don’t see each other’s uncommitted mess; each looks like it ran alone |
| **D** | Durability | After `COMMIT`, data survives crashes / restarts (written safely to durable storage) |

### Atomicity

Either the full transfer lands, or `ROLLBACK` restores the previous balances. Never “Alice lost money and Bob got nothing.”

### Consistency

If a `CHECK` says `balance >= 0`, a transaction that would leave a negative balance is rejected. The database moves from one valid state to another.

### Isolation

Two transfers at the same time shouldn’t overwrite or double-spend each other. Engines use locks / MVCC; isolation *levels* (`READ COMMITTED`, `REPEATABLE READ`, …) trade strictness vs speed.

### Durability

Once the server confirms `COMMIT`, a power cut should not lose that committed work.

---

## Transaction states

Typical lifecycle of a transaction:

```text
                ┌─────────┐
                │  Active │  ← executing statements
                └────┬────┘
         success     │     error / crash
                     ▼
          ┌──────────────────┐
          │ Partially        │  ← last statement done;
          │ Committed        │    waiting to make durable
          └────────┬─────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
   ┌──────────┐        ┌─────────┐
   │ Committed│        │ Failed  │
   └──────────┘        └────┬────┘
                            │ undo
                            ▼
                       ┌─────────┐
                       │ Aborted │  ← ROLLBACK done / undone
                       └─────────┘
```

| State | Meaning |
| --- | --- |
| **Active** | Transaction has started; statements are running |
| **Partially committed** | Last statement finished; commit work (flush to disk) not finished yet |
| **Failed** | Something went wrong (constraint, crash, explicit abort) — must undo |
| **Committed** | Changes are permanent and durable |
| **Aborted** | Changes were rolled back; database looks as before the transaction |

In practice you mostly write: start → work → `COMMIT` or `ROLLBACK`.

---

## SAVEPOINT (partial undo)

Undo only part of a transaction without aborting the whole thing:

```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
SAVEPOINT after_debit;
UPDATE accounts SET balance = balance + 100 WHERE id = 999;  -- bad id
ROLLBACK TO SAVEPOINT after_debit;  -- keep the debit? or fix, then continue
-- fix and retry credit, or ROLLBACK the whole transaction
COMMIT;
```

---

## Cheat sheet

| Want… | Use |
| --- | --- |
| Start a unit of work | `START TRANSACTION;` or `BEGIN;` |
| Keep all changes | `COMMIT;` |
| Undo all changes in the transaction | `ROLLBACK;` |
| Undo back to a named point | `SAVEPOINT name;` then `ROLLBACK TO SAVEPOINT name;` |
| Guarantee all-or-nothing + safe commit | Rely on **ACID** (engine + correct `COMMIT`/`ROLLBACK`) |
