# 10 — Runtime fields

Compute fields at query time without reindexing.

[← Mapping](./09-Mapping.md) · [ELK index](./README.md) · [Next: Update →](./11-Update.md)

---

## Why runtime fields?

Mapped fields are indexed at write time (fast reads, schema changes need reindex). **Runtime fields** are evaluated when you search — flexible, slightly more CPU per query.

Use them to:

* Derive a value from `_source` without reindex
* Experiment before promoting a field into the mapping
* Shadow / override a mapped field temporarily

---

## Define in the mapping

```http
PUT /users/_mapping
{
  "runtime": {
    "name_upper": {
      "type": "keyword",
      "script": {
        "source": "emit(doc['name.keyword'].value.toUpperCase())"
      }
    }
  }
}
```

Then query / return it:

```http
GET /users/_search
{
  "fields": ["name_upper"],
  "query": {
    "term": { "name_upper": "RADIN" }
  }
}
```

---

## Define in the query only

Ephemeral — exists for that request:

```http
GET /books/_search
{
  "runtime_mappings": {
    "rating_bucket": {
      "type": "keyword",
      "script": {
        "source": """
          if (doc['amazon_rating'].size() == 0) return;
          double r = doc['amazon_rating'].value;
          if (r >= 4.5) emit('excellent');
          else if (r >= 4.0) emit('good');
          else emit('other');
        """
      }
    }
  },
  "fields": ["rating_bucket"],
  "query": {
    "term": { "rating_bucket": "excellent" }
  }
}
```

---

## Runtime vs indexed

| | Indexed (mapping) | Runtime |
| --- | --- | --- |
| Cost | Pay at index time | Pay at query time |
| Schema change | Reindex to change type/analysis | Script change only |
| Aggregations / sort | Very fast | Supported but heavier |
| Best for | Stable, hot fields | Exploration, rare fields |

---

## Tips

* Prefer `doc['field']` when the field is indexed; use `params._source` only if needed
* Scripts must `emit(...)` values matching the runtime type
* Promote useful runtime fields to real mapped fields later for speed

---

## Summary

* Runtime fields = query-time computed properties
* Set in mapping (`runtime`) or per request (`runtime_mappings`)
* Great for prototyping; index hot paths for production scale
