# 09 — Mapping

Field types, explicit mappings, multi-fields, and dynamic templates.

[← Relevance](./08-Relevance.md) · [ELK index](./README.md) · [Next: Runtime fields →](./10-Runtime-Fields.md)

---

## What is a mapping?

The mapping is the **schema** of an index: each field’s type and how it is indexed/analyzed.

```http
GET /books/_mapping
```

---

## Common field types

| Type | Use |
| --- | --- |
| `text` | Full-text search (analyzed) |
| `keyword` | Exact match, sort, aggs |
| `long` / `integer` | Whole numbers |
| `double` / `float` | Decimals |
| `date` | Timestamps |
| `boolean` | true / false |
| `object` | Inner JSON objects |
| `nested` | Arrays of objects queried independently |
| `ip` | IPv4 / IPv6 |
| `geo_point` | lat/lon |

---

## Explicit mapping

Define before indexing (or on create):

```http
PUT /users
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword", "ignore_above": 256 }
        }
      },
      "age": { "type": "integer" },
      "created_at": { "type": "date" },
      "tags": { "type": "keyword" }
    }
  }
}
```

`name` is searchable as full-text; `name.keyword` is exact / aggregatable.

---

## Dynamic mapping

If you index a new field without defining it, Elasticsearch **guesses** the type. Convenient for demos; risky in production (a `"20"` string vs `20` number can map differently).

Control with:

```json
"mappings": {
  "dynamic": "strict"
}
```

`true` (default) | `runtime` | `false` | `strict`.

---

## Update mapping

You can **add** new fields:

```http
PUT /users/_mapping
{
  "properties": {
    "l_name": { "type": "text" }
  }
}
```

You generally **cannot** change a field’s type in place — reindex into a new index (with aliases — [13-Alias](./13-Alias.md)).

---

## Multi-fields

One source value, multiple index representations:

```json
"title": {
  "type": "text",
  "fields": {
    "raw": { "type": "keyword" },
    "en": {
      "type": "text",
      "analyzer": "english"
    }
  }
}
```

Query `title` / `title.en`; aggregate on `title.raw`.

---

## `nested` vs `object`

```json
"authors": [
  { "first": "A", "last": "One" },
  { "first": "B", "last": "Two" }
]
```

With `object`, Lucene flattens fields — a query for `first:A` AND `last:Two` can falsely match across array elements. Use `"type": "nested"` when each array element must stay independent.

---

## Summary

* Map `text` for search, `keyword` for exact / sort / aggs
* Prefer explicit mappings in production (`dynamic: strict`)
* Adding fields is OK; changing types needs reindex
* Multi-fields give text + keyword (or multiple analyzers) together
