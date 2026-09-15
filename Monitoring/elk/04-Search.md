# 04 — Search

The `_search` API: match everything, filter by ids, and read the response.

[← mget](./03-Mget.md) · [ELK index](./README.md) · [Next: Query →](./05-Query.md)

---

## Basic search

Search the whole index (default query is effectively “match all”, with a size limit):

```http
GET /users/_search
```

With an explicit body:

```http
GET /users/_search
{
  "query": {
    "match_all": {}
  }
}
```

---

## Search by document ids

```http
GET /users/_search
{
  "query": {
    "ids": {
      "values": ["1", "2", "7"]
    }
  }
}
```

Unlike `_mget`, this goes through the search API (scoring, `from`/`size`, aggregations can be added later).

---

## Response fields (what matters)

| Field | Meaning |
| --- | --- |
| `took` | Time in ms |
| `hits.total` | How many matched (object with `value` / `relation` in modern ES) |
| `hits.max_score` | Best relevance score in this page |
| `hits.hits[]._id` | Document id |
| `hits.hits[]._score` | Relevance for this hit |
| `hits.hits[]._source` | Original JSON |

---

## Size and from (pagination)

```http
GET /users/_search
{
  "from": 0,
  "size": 5,
  "query": {
    "match_all": {}
  }
}
```

Deep pagination (`from` + `size` large) is expensive — prefer `search_after` for large result sets later.

---

## URI search (quick filters)

Query string style (good for `_count` and simple checks):

```http
GET /users/_search?q=name:radin
```

Prefer Query DSL bodies for anything non-trivial (next lesson).

---

## Multi-index

```http
GET /users,books/_search
{
  "query": { "match_all": {} }
}
```

Wildcards work too: `GET /logs-*/_search`.

---

## Summary

* `_search` returns a **page** of hits, not one doc by id
* Start with `match_all` and `ids`
* Control page with `from` / `size`; inspect `hits.hits`
