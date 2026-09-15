# 06 — Compound queries

Combine leaf queries with `bool`, plus `constant_score` and boosting.

[← Query](./05-Query.md) · [ELK index](./README.md) · [Next: Aggregation →](./07-Aggregation.md)

---

## `bool` — the workhorse

```http
GET /books/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "synopsis": "java" } }
      ],
      "filter": [
        { "range": { "amazon_rating": { "gte": 4.0 } } }
      ],
      "should": [
        { "match": { "title": "effective" } }
      ],
      "must_not": [
        { "term": { "edition": 1 } }
      ],
      "minimum_should_match": 0
    }
  }
}
```

| Clause | Effect |
| --- | --- |
| `must` | Must match; **contributes to score** |
| `filter` | Must match; **no score**, often cached |
| `should` | Nice-to-have; boosts score (required if alone) |
| `must_not` | Must not match; no score |

Put exact checks (`term`, `range`, `exists`) in **`filter`**. Keep full-text in **`must`** / **`should`**.

---

## `minimum_should_match`

When `must` / `filter` are present, `should` is optional unless you set:

```json
"minimum_should_match": 1
```

Useful for “at least one of these tags/phrases”.

---

## Nested bool

You can nest `bool` inside `must` / `should` for OR-of-ANDs style logic:

```http
GET /books/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "bool": {
            "must": [
              { "match": { "title": "java" } },
              { "range": { "amazon_rating": { "gte": 4.5 } } }
            ]
          }
        },
        { "match_phrase": { "synopsis": "design patterns" } }
      ],
      "minimum_should_match": 1
    }
  }
}
```

---

## `constant_score`

Wrap a filter so every hit gets the same score (or a fixed `boost`):

```http
GET /books/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "term": { "edition": 11 }
      },
      "boost": 1.0
    }
  }
}
```

---

## Name queries (debug)

```json
{ "match": { "title": { "query": "java", "_name": "title_java" } } }
```

Matched named queries appear under `matched_queries` on each hit.

---

## Summary

* Prefer `bool` + `filter` for structured constraints
* Use `must` / `should` for scored full-text
* Nest `bool` for complex boolean logic
