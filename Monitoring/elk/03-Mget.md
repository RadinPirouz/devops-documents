# 03 — Multi-get (`_mget`)

Fetch many documents in one round trip.

[← Index](./02-Index.md) · [ELK index](./README.md) · [Next: Search →](./04-Search.md)

---

## Why `_mget`?

`GET /index/_doc/id` is one document per request. `_mget` batches several ids (optionally across indices) into a single response — less latency and fewer HTTP calls.

---

## By docs array

```http
GET /users/_mget
{
  "docs": [
    { "_id": "2" },
    { "_id": "3" }
  ]
}
```

Each item can also set `"_index"` if you omit the index in the path, or override it per doc.

---

## Short form: `ids`

When every id is in the same index from the URL:

```http
GET /users/_mget
{
  "ids": ["2", "3"]
}
```

---

## Limit returned fields

Use `_source` to include only some fields:

```http
GET /users/_mget
{
  "docs": [
    {
      "_id": "2",
      "_source": ["name"]
    }
  ]
}
```

`"_source": false` skips the body entirely (metadata only). You can also use `"_source": { "includes": [...], "excludes": [...] }`.

---

## Response shape

You get `"docs": [ ... ]` in the same order as the request. Each entry has `"found": true|false`. Missing ids do not fail the whole request — check `found` per item.

---

## Summary

* `_mget` = batch get by id
* Prefer `ids` for one index; use `docs` for per-doc options or multi-index
* Filter payload with `_source`
