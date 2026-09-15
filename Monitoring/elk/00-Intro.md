# 00 — Intro

What Elasticsearch is, how you talk to it, and the first cluster checks.

[ELK index](./README.md) · [Next: Architecture →](./01-Architecture.md)

---

## What is Elasticsearch?

Elasticsearch is a distributed **search and analytics** engine built on Apache Lucene. You store JSON **documents** in **indices**, then search and aggregate them over a REST API.

Typical uses:

* Full-text search (apps, sites, logs)
* Log and metrics analytics (with Logstash / Beats / Kibana)
* Near real-time filtering and aggregations

---

## How you send requests

Use **Kibana Dev Tools** (Console) or any HTTP client. Pattern:

```http
<METHOD> <api>
{
  ...optional JSON body...
}
```

Examples:

```http
GET /
```

```http
GET /_cluster/health
```

```http
GET /_nodes/stats
```

`GET /` returns cluster name, version, and tagline. `_cluster/health` shows green / yellow / red status and shard counts.

---

## Core vocabulary

| Concept | Meaning |
| --- | --- |
| **Cluster** | One or more nodes working together |
| **Node** | A single Elasticsearch process / server |
| **Index** | Logical collection of documents (like a DB) |
| **Document** | One JSON object (`_source`) with an `_id` |
| **Shard** | Horizontal slice of an index (primary + replicas) |
| **Mapping** | Schema: field names and types |

Compare with a relational DB:

| Traditional DB | Elasticsearch |
| --- | --- |
| Database | Index |
| Table | Index (types deprecated) |
| Row | Document |
| Column | Field |
| Primary key | Document `_id` |

---

## Cat APIs (human-friendly)

`_cat` endpoints print tabular text — handy in the console:

```http
GET /_cat/indices?v=true
```

```http
GET /_cat/indices?v=true&help=true
```

`v=true` adds a header row; `help=true` lists available columns.

Other useful ones: `/_cat/nodes?v`, `/_cat/shards?v`, `/_cat/health?v`.

---

## Summary

* Talk to ES with HTTP: `METHOD` + path + optional JSON body
* Start with `/`, `/_cluster/health`, and `/_cat/indices?v`
* Data lives as JSON documents inside indices, split across shards
