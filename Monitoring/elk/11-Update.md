# 11 — Update

Partial updates, scripts, upsert, and update-by-query.

[← Runtime fields](./10-Runtime-Fields.md) · [ELK index](./README.md) · [Next: Settings →](./12-Settings.md)

---

## Partial document update

Merge fields into an existing doc (fetch → merge → reindex under the hood):

```http
POST /users/_update/1
{
  "doc": {
    "age": 21
  }
}
```

---

## Upsert

Update if present; insert if missing:

```http
POST /users/_update/99
{
  "doc": {
    "name": "sara",
    "age": 30
  },
  "doc_as_upsert": true
}
```

Or separate upsert body:

```http
POST /users/_update/99
{
  "script": {
    "source": "ctx._source.age += 1",
    "lang": "painless"
  },
  "upsert": {
    "name": "sara",
    "age": 1
  }
}
```

---

## Scripted update

```http
POST /users/_update/1
{
  "script": {
    "source": "ctx._source.age += params.inc",
    "lang": "painless",
    "params": { "inc": 1 }
  }
}
```

Remove a field: `ctx._source.remove('temp')`.  
Replace whole source carefully; prefer `doc` for simple merges.

---

## Detect noop

```http
POST /users/_update/1
{
  "doc": { "age": 21 },
  "detect_noop": true
}
```

If the doc is unchanged, version may not bump (`result: noop`).

---

## Update by query

Update every document matching a query:

```http
POST /books/_update_by_query
{
  "query": {
    "range": { "amazon_rating": { "lt": 4.0 } }
  },
  "script": {
    "source": "ctx._source.tags.add('needs-review')",
    "lang": "painless"
  }
}
```

Add `"conflicts": "proceed"` to keep going on version conflicts. Check task API for large jobs.

---

## Delete by query

```http
POST /users/_delete_by_query
{
  "query": {
    "match": { "name": "obsolete" }
  }
}
```

---

## Reindex

Copy (and optionally transform) into another index:

```http
POST /_reindex
{
  "source": { "index": "books" },
  "dest": { "index": "books_v2" }
}
```

Combine with a new mapping on `books_v2`, then flip an alias ([13-Alias](./13-Alias.md)).

---

## Summary

| API | Purpose |
| --- | --- |
| `_update` | One doc: `doc` merge or script |
| `doc_as_upsert` / `upsert` | Create if missing |
| `_update_by_query` | Script many docs |
| `_delete_by_query` | Delete many docs |
| `_reindex` | Copy / migrate index |
