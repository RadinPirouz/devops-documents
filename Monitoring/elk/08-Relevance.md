# 08 — Relevance

How `_score` is built, and how to boost, sort, and explain matches.

[← Aggregation](./07-Aggregation.md) · [ELK index](./README.md) · [Next: Mapping →](./09-Mapping.md)

---

## What is relevance?

Full-text queries assign each hit a **`_score`**. Higher usually means a better match for the query. Filters and `constant_score` do not use TF-IDF/BM25 the same way — they contribute 0 (or a fixed boost).

Modern Elasticsearch uses **BM25** by default.

---

## See why a doc matched

```http
GET /books/_search
{
  "explain": true,
  "query": {
    "match": { "synopsis": "java reference" }
  }
}
```

Or for one id:

```http
GET /books/_explain/1
{
  "query": {
    "match": { "synopsis": "java reference" }
  }
}
```

---

## Boosting fields

In `multi_match` or query string style field lists:

```http
GET /books/_search
{
  "query": {
    "multi_match": {
      "query": "java",
      "fields": ["title^3", "synopsis"]
    }
  }
}
```

`title^3` triples that field’s contribution.

Per-clause boost:

```json
{ "match": { "title": { "query": "java", "boost": 2 } } }
```

---

## `function_score`

Modify scores with field values or decay functions:

```http
GET /books/_search
{
  "query": {
    "function_score": {
      "query": { "match": { "synopsis": "java" } },
      "field_value_factor": {
        "field": "amazon_rating",
        "factor": 1.2,
        "modifier": "sqrt",
        "missing": 1
      },
      "boost_mode": "multiply",
      "score_mode": "multiply"
    }
  }
}
```

Common: boost newer documents with `gauss` decay on a date field.

---

## Sort instead of score

When relevance does not matter:

```http
GET /books/_search
{
  "query": { "match_all": {} },
  "sort": [
    { "amazon_rating": "desc" },
    { "release_date": "desc" }
  ]
}
```

Sorting by field sets `_score` to `null` unless you also sort by `_score`.

---

## `minimum_should_match` and operators

Tighten full-text matching so weak partial matches rank out:

```json
{
  "match": {
    "synopsis": {
      "query": "java concurrency practice",
      "operator": "and"
    }
  }
}
```

Or `"minimum_should_match": "75%"`.

---

## Practical tips

* Put filters in `bool.filter` so they do not distort BM25
* Boost **important** fields (`title`, `name`) over body text
* Use `explain` sparingly (expensive) while tuning
* For “newest first” + light text match, combine `function_score` or a `should` on recency with a must on text

---

## Summary

* `_score` ≈ BM25 relevance for scored queries
* Boost fields / clauses; use `function_score` for business signals
* Prefer `sort` when order is by field, not relevance
* `explain` helps debug surprising rankings
