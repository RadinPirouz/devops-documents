# 18 — Specify analyzer

Attach analyzers on the field, override at search time, and keep index/search analysis aligned.

[← Tokenizer](./17-Tokenizer.md) · [ELK index](./README.md) · [Next: Persian →](./19-Persian.md)

---

## On the mapping

```http
PUT /posts
{
  "settings": {
    "analysis": {
      "analyzer": {
        "index_autocomplete": {
          "tokenizer": "edge_ngram_tok",
          "filter": ["lowercase"]
        },
        "search_autocomplete": {
          "tokenizer": "standard",
          "filter": ["lowercase"]
        }
      },
      "tokenizer": {
        "edge_ngram_tok": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 20
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "index_autocomplete",
        "search_analyzer": "search_autocomplete"
      },
      "body": {
        "type": "text",
        "analyzer": "english"
      }
    }
  }
}
```

* **`analyzer`** — used at **index** time (and at search if `search_analyzer` omitted)
* **`search_analyzer`** — used only when querying that field

 asymmetric index/search analyzers are common for autocomplete and stemming edge cases.

---

## Per-query analyzer override

```http
GET /posts/_search
{
  "query": {
    "match": {
      "body": {
        "query": "running quickly",
        "analyzer": "standard"
      }
    }
  }
}
```

Useful for debugging; prefer mapping defaults for production consistency.

---

## Multi-fields with different analyzers

```json
"content": {
  "type": "text",
  "analyzer": "standard",
  "fields": {
    "english": {
      "type": "text",
      "analyzer": "english"
    },
    "keyword": {
      "type": "keyword",
      "ignore_above": 256
    }
  }
}
```

Query `content.english` for stemmed English; aggregate on `content.keyword`.

---

## `_analyze` with a field

```http
POST /posts/_analyze
{
  "field": "title",
  "text": "elasticsearch"
}
```

Uses that field’s index analyzer. Add `"explain": true` on some versions for more detail.

---

## Checklist

1. Define analyzers under `settings.analysis`
2. Reference them from `mappings.properties`
3. Set `search_analyzer` when index-time tokens should not be reproduced at query time
4. Verify with `_analyze` before loading data
5. Changing analyzers on existing fields → **reindex**

---

## Summary

* Wire analyzers in the mapping; override search analyzer when needed
* Autocomplete pattern: n-gram index + standard search
* Multi-fields = multiple analysis strategies on one source value
