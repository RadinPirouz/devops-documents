# 05 — Query DSL

Full-text and term-level queries: `match`, `multi_match`, `prefix`, `match_phrase`, `fuzzy`, `term`, `range`.

[← Search](./04-Search.md) · [ELK index](./README.md) · [Next: Compound →](./06-Compound.md)

---

## Query vs filter (preview)

* **Query** context → relevance `_score` (full-text)
* **Filter** context → yes/no, cacheable, no score (see [06-Compound](./06-Compound.md) `bool.filter`)

Examples below mostly run in query context.

---

## `match` — analyzed full-text

Best default for text fields. Query string is analyzed like the field.

```http
GET /users/_search
{
  "query": {
    "match": {
      "name": "radin"
    }
  }
}
```

Multiple terms — default operator is `or` (any term can match):

```http
GET /users/_search
{
  "query": {
    "match": {
      "name": "radin abbas"
    }
  }
}
```

Require **all** terms (`and`):

```http
GET /users/_search
{
  "query": {
    "match": {
      "name": {
        "query": "radin abbas",
        "operator": "and"
      }
    }
  }
}
```

---

## `multi_match` — same query, several fields

```http
GET /users/_search
{
  "query": {
    "multi_match": {
      "query": "radin",
      "fields": ["name", "l_name"]
    }
  }
}
```

Boost a field: `"fields": ["name^3", "l_name"]`.

---

## `prefix` — starts with

```http
GET /users/_search
{
  "query": {
    "prefix": {
      "name": "rad"
    }
  }
}
```

Often used on `keyword` fields. On analyzed `text`, behavior depends on how terms were indexed — prefer `match_phrase_prefix` or completion suggesters for typeahead UX.

---

## `match_phrase` — terms in order

Good for exact phrases in text:

```http
GET /books/_search
{
  "query": {
    "match_phrase": {
      "synopsis": "Java reference"
    }
  }
}
```

Optional `"slop": 1` allows small word gaps / reordering.

---

## `fuzzy` — tolerate typos

```http
GET /books/_search
{
  "query": {
    "fuzzy": {
      "title": {
        "value": "kava",
        "fuzziness": 1
      }
    }
  }
}
```

`fuzziness`: `0`, `1`, `2`, or `"AUTO"`. Prefer `match` with `"fuzziness": "AUTO"` for most full-text cases.

---

## `term` — exact value (not analyzed)

Use on **keyword** / numeric / boolean fields — not on analyzed `text`:

```http
GET /books/_search
{
  "query": {
    "term": {
      "edition": {
        "value": 2
      }
    }
  }
}
```

For several exact values: `terms` query.

---

## `range` — numbers and dates

```http
GET /books/_search
{
  "query": {
    "range": {
      "amazon_rating": {
        "gte": 2,
        "lte": 5
      }
    }
  }
}
```

Operators: `gt`, `gte`, `lt`, `lte`. Dates accept ISO strings and date math (`now-7d`).

---

## Sample data reminder

The `books` examples assume the bulk load from [02-Index](./02-Index.md). Reload with `POST _bulk` if the index is empty.

---

## Cheat sheet

| Query | Use when |
| --- | --- |
| `match` | Full-text on one field |
| `multi_match` | Full-text across fields |
| `match_phrase` | Exact phrase |
| `prefix` | Starts-with on keyword-like data |
| `fuzzy` | Typos / approximate terms |
| `term` / `terms` | Exact keyword / id / enum |
| `range` | Numbers, dates, versions |
| `ids` | Known document ids |
| `match_all` | Everything |

Next: combine these with `bool` (must / should / filter / must_not).
