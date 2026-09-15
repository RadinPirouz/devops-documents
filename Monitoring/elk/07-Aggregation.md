# 07 — Aggregations

Summarize search results: metrics, buckets, and simple pipelines.

[← Compound](./06-Compound.md) · [ELK index](./README.md) · [Next: Relevance →](./08-Relevance.md)

---

## Idea

A search returns **hits**. An **aggregation** returns **analytics** over the same (or filtered) document set — averages, histograms, top terms, etc.

```http
GET /books/_search
{
  "size": 0,
  "query": {
    "match": { "synopsis": "java" }
  },
  "aggs": {
    "avg_rating": {
      "avg": { "field": "amazon_rating" }
    }
  }
}
```

`"size": 0` skips hits when you only care about aggs.

---

## Metric aggregations

```http
GET /books/_search
{
  "size": 0,
  "aggs": {
    "avg_rating": { "avg": { "field": "amazon_rating" } },
    "max_rating": { "max": { "field": "amazon_rating" } },
    "min_edition": { "min": { "field": "edition" } },
    "sum_edition": { "sum": { "field": "edition" } },
    "stats_rating": { "stats": { "field": "amazon_rating" } }
  }
}
```

`stats` returns count, min, max, avg, sum in one agg.

---

## Bucket: `terms`

Top values for a **keyword** field (or numeric):

```http
GET /books/_search
{
  "size": 0,
  "aggs": {
    "by_author": {
      "terms": {
        "field": "author.keyword",
        "size": 10
      }
    }
  }
}
```

If `author` is only `text`, you need a `.keyword` multi-field or a `keyword` mapping — see [09-Mapping](./09-Mapping.md).

---

## Bucket: `range` / `histogram`

```http
GET /books/_search
{
  "size": 0,
  "aggs": {
    "rating_ranges": {
      "range": {
        "field": "amazon_rating",
        "ranges": [
          { "to": 4.0 },
          { "from": 4.0, "to": 4.5 },
          { "from": 4.5 }
        ]
      }
    }
  }
}
```

```http
GET /books/_search
{
  "size": 0,
  "aggs": {
    "editions": {
      "histogram": {
        "field": "edition",
        "interval": 1
      }
    }
  }
}
```

Date fields: `date_histogram` with `"calendar_interval": "month"`.

---

## Sub-aggregations

Nest metrics inside buckets:

```http
GET /books/_search
{
  "size": 0,
  "aggs": {
    "by_edition": {
      "terms": { "field": "edition", "size": 20 },
      "aggs": {
        "avg_rating": { "avg": { "field": "amazon_rating" } }
      }
    }
  }
}
```

---

## Filter aggregation

Agg over a subset without changing the main query hits:

```http
GET /books/_search
{
  "size": 0,
  "aggs": {
    "high_rated": {
      "filter": {
        "range": { "amazon_rating": { "gte": 4.5 } }
      },
      "aggs": {
        "avg_edition": { "avg": { "field": "edition" } }
      }
    }
  }
}
```

---

## Summary

| Type | Examples |
| --- | --- |
| Metrics | `avg`, `sum`, `min`, `max`, `stats`, `cardinality` |
| Buckets | `terms`, `range`, `histogram`, `date_histogram`, `filter` |
| Nesting | Put `aggs` inside a bucket agg |

Use `size: 0` for analytics-only responses.
