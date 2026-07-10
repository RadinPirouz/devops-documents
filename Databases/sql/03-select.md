# 03 — SELECT

Read rows with filters, sorting, pattern matching, and limits.

[← Tables](./02-tables.md) · [SQL index](./README.md) · [Next: Aggregates →](./04-aggregates.md)

---

## Basic select

Return every column and every row from `customers`:

```sql
SELECT * FROM customers;
```

Return only the `country` column (one value per row):

```sql
SELECT country FROM customers;
```

---

## DISTINCT

Same country can appear many times. `DISTINCT` keeps each value once:

```sql
SELECT DISTINCT country FROM customers;
```

Distinct on a pair: keep unique `(country, city)` combinations (Tehran/Iran and Berlin/Germany both stay):

```sql
SELECT DISTINCT country, city FROM customers;
```

---

## WHERE

Keep only rows that match a condition. This returns customers in Iran:

```sql
SELECT * FROM customers WHERE country = 'Iran';
```

`OR` — keep the row if **either** condition is true (Iran **or** Tehran):

```sql
SELECT * FROM customers WHERE country = 'Iran' OR city = 'Tehran';
```

`NOT` flips a condition. This keeps rows that are **not** Iran **or** **not** Tehran (almost everything except “Iran + Tehran”):

```sql
SELECT * FROM customers WHERE NOT country = 'Iran' OR NOT city = 'Tehran';
```

Combine `AND` / `OR` carefully. Parentheses control order: not Iran, **and** city is Berlin or Paris:

```sql
SELECT * FROM customers
WHERE NOT country = 'Iran'
  AND (city = 'Berlin' OR city = 'Paris');
```

`IN` is a short form of many `OR`s on the same column — country is Iran, Germany, or USA:

```sql
SELECT * FROM customers WHERE country IN ('Iran', 'Germany', 'USA');
```

---

## ORDER BY

Sort result rows by `country` (default is ascending A→Z):

```sql
SELECT * FROM customers ORDER BY country;
```

`ASC` = ascending, `DESC` = descending (Z→A):

```sql
SELECT * FROM customers ORDER BY country ASC;
SELECT * FROM customers ORDER BY country DESC;
```

---

## LIKE

Match text patterns. `%` = any number of characters, `_` = exactly one character. Names starting with `R`:

```sql
SELECT * FROM customers WHERE customer_name LIKE 'R%';
```

| Pattern | Meaning |
| --- | --- |
| `R%` | starts with `R` |
| `%R` | ends with `R` |
| `%R%` | contains `R` |
| `R_` | `R` + exactly one character |

---

## Aliases & expressions

Compute a value per row and name the result column with `AS` (here: income = sell_count × price):

```sql
SELECT sell_count * price AS income FROM customers;
```

---

## LIMIT

Same expression as above, but return at most 10 rows:

```sql
SELECT sell_count * price AS income FROM customers LIMIT 10;
```
