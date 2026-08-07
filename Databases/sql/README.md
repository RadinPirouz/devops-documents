# SQL Basics

Practical SQL reference — databases, tables, queries, relations, joins, and normalization.

> **Status:** work in progress. Examples lean toward **PostgreSQL** (`SERIAL`, `RETURNING`, `DROP … WITH (FORCE)`). Most syntax also works on MySQL/MariaDB with small differences.

[← Back to Databases](../README.md)

## Suggested order

| # | Guide | Topics |
| --- | --- | --- |
| 01 | [Databases](./01-databases.md) | `CREATE` / `DROP` / `ALTER DATABASE` |
| 02 | [Tables](./02-tables.md) | `CREATE` / `ALTER TABLE`, columns, constraints |
| 03 | [SELECT](./03-select.md) | `SELECT`, `DISTINCT`, `WHERE`, `ORDER BY`, `LIKE`, `LIMIT`, aliases |
| 04 | [Aggregates](./04-aggregates.md) | `COUNT`, `MIN`, `MAX`, `AVG`, `SUM`, `GROUP BY` |
| 05 | [DML](./05-dml.md) | `INSERT`, `UPDATE`, `DELETE`, copy rows |
| 06 | [Keys & Relations](./06-keys-relations.md) | Primary/foreign keys, `ON DELETE`, 1:1 / 1:N / M:N |
| 07 | [Joins](./07-joins.md) | `INNER`, `LEFT`, `RIGHT`, `FULL`, self-join |
| 08 | [Normalization](./08-normalization.md) | 1NF, 2NF, 3NF |
| 09 | [Key Types](./09-keys.md) | Super / candidate / primary / alternate / composite / natural / surrogate / foreign |
| 10 | [Combining Queries](./10-combining-query.md) | `UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT` |
| 11 | [DEFAULT & CHECK](./11-check.md) | `DEFAULT`, column / table `CHECK`, named constraints |
| 12 | [ERD](./12-erd.md) | Entities, relationships, attributes, cardinality, Chen / Crow’s Foot |
| 13 | [Transactions](./13-transaction.md) | `START TRANSACTION` / `BEGIN`, `COMMIT`, `ROLLBACK`, ACID, states, `SAVEPOINT` |
| 14 | [Indexes](./14-index.md) | `CREATE` / `DROP INDEX`, unique & composite indexes, when to use, `EXPLAIN` |

## Notes

- Prefer table name `users` over `user` (`user` is reserved in many engines).
- Use single quotes for string literals: `'Iran'`, not `"Iran"`.
