# 13 — Index aliases

Point a stable name at one or more indices — zero-downtime reindex and multi-index reads.

[← Settings](./12-Settings.md) · [ELK index](./README.md) · [Next: Index template →](./14-Index-Template.md)

---

## Create an alias

```http
POST /_aliases
{
  "actions": [
    { "add": { "index": "books", "alias": "books_current" } }
  ]
}
```

Or on create:

```http
PUT /books_v1
{
  "aliases": {
    "books_current": {}
  }
}
```

Clients always use `books_current`. You can swap the underlying index later.

---

## Atomic switch (reindex pattern)

```http
POST /_aliases
{
  "actions": [
    { "remove": { "index": "books_v1", "alias": "books_current" } },
    { "add": { "index": "books_v2", "alias": "books_current" } }
  ]
}
```

Both actions in one request = no window where the alias is missing.

---

## Write vs read aliases

```http
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "logs-2024-09",
        "alias": "logs-write",
        "is_write_index": true
      }
    },
    {
      "add": {
        "index": "logs-2024-08",
        "alias": "logs-read"
      }
    },
    {
      "add": {
        "index": "logs-2024-09",
        "alias": "logs-read"
      }
    }
  ]
}
```

* **Write alias** → exactly one `is_write_index: true` when multiple indices share the alias
* **Read alias** → can span many indices

---

## Filtered alias

```http
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "users",
        "alias": "adults",
        "filter": {
          "range": { "age": { "gte": 18 } }
        }
      }
    }
  ]
}
```

Searches on `adults` always apply that filter.

---

## Inspect

```http
GET /_alias/books_current
```

```http
GET /books/_alias
```

---

## Summary

* Alias = stable API name over changing concrete indices
* Swap with one `_aliases` request after reindex
* Use write index + multi-index read aliases for time-based data
