# 16 — Text analysis

How text becomes tokens: analyzers = character filters + tokenizer + token filters.

[← Split / Shrink](./15-Split-Shrink.md) · [ELK index](./README.md) · [Next: Tokenizer →](./17-Tokenizer.md)

---

## Analysis pipeline

```
Original string
    → character filters   (e.g. strip HTML)
    → tokenizer           (split into tokens)
    → token filters       (lowercase, stop words, stemming, …)
    → terms on disk / query terms
```

**Index time** and **search time** should usually use compatible analyzers so query tokens match indexed tokens.

---

## Test with `_analyze`

```http
POST /_analyze
{
  "analyzer": "standard",
  "text": "The Quick Brown Fox!"
}
```

```http
POST /books/_analyze
{
  "field": "synopsis",
  "text": "Java reference book"
}
```

Inspect `tokens[].token` to see what actually gets indexed.

---

## Built-in analyzers

| Analyzer | Behavior |
| --- | --- |
| `standard` | Grammar-based tokenization + lowercase |
| `simple` | Non-letter split + lowercase |
| `whitespace` | Split on whitespace only |
| `keyword` | Entire string = one token |
| `english` | English stop words + stemming |
| `persian` | Persian-oriented analysis (see [19-Persian](./19-Persian.md)) |

---

## Custom analyzer (index settings)

```http
PUT /articles
{
  "settings": {
    "analysis": {
      "char_filter": {
        "strip_html": { "type": "html_strip" }
      },
      "filter": {
        "my_stop": {
          "type": "stop",
          "stopwords": ["_english_"]
        }
      },
      "analyzer": {
        "content_analyzer": {
          "type": "custom",
          "char_filter": ["strip_html"],
          "tokenizer": "standard",
          "filter": ["lowercase", "my_stop"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "body": {
        "type": "text",
        "analyzer": "content_analyzer",
        "search_analyzer": "content_analyzer"
      }
    }
  }
}
```

---

## `text` vs `keyword`

* **`text`** → analyzed → good for `match` / `match_phrase`
* **`keyword`** → not analyzed → good for `term`, sorting, aggs

Most string fields should expose **both** via multi-fields.

---

## Summary

* Analysis turns strings into searchable terms
* Always verify with `_analyze`
* Custom analyzers live in index settings; wire them in the mapping
* Next lessons: tokenizers in depth, then attaching analyzers per field / query
