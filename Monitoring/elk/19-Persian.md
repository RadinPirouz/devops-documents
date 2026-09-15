# 19 — Persian analysis

Indexing and searching Persian (Farsi) text in Elasticsearch.

[← Specify analyzer](./18-Specify-Analyzer.md) · [ELK index](./README.md) · [Next: Elastic Py →](./20-Elastic-Py.md)

---

## Built-in `persian` analyzer

Elasticsearch ships a **persian** analyzer (stemmer + stop words suited to Persian). Test it:

```http
POST /_analyze
{
  "analyzer": "persian",
  "text": "کتاب‌های برنامه‌نویسی جاوا"
}
```

Compare with `standard` on the same string to see tokenization differences.

---

## Index mapping example

```http
PUT /articles_fa
{
  "settings": {
    "analysis": {
      "analyzer": {
        "fa_text": {
          "type": "persian"
        },
        "fa_autocomplete": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "persian_stop", "edge_ngram_fa"]
        }
      },
      "filter": {
        "persian_stop": {
          "type": "stop",
          "stopwords": ["_persian_"]
        },
        "edge_ngram_fa": {
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
        "analyzer": "fa_text",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      },
      "body": {
        "type": "text",
        "analyzer": "fa_text"
      }
    }
  }
}
```

Adjust custom filters to your ES version — check that `persian` / `_persian_` stopword set exists in your release.

---

## Character normalization tips

Persian text often needs normalization **before** or **inside** analysis:

* Arabic Yeh / Kaf vs Persian ی / ک
* Zero-width non-joiner (ZWNJ, `\u200c`) in compound words
* Digits: Western `0-9` vs Eastern `۰-۹`

Options:

* Normalize in the application before index/search
* `mapping` character filter for simple char replacements
* Ingest pipeline processors for cleanup

Example mapping char filter:

```json
"char_filter": {
  "fa_yeh_kaf": {
    "type": "mapping",
    "mappings": [
      "ي => ی",
      "ك => ک"
    ]
  }
}
```

Wire `fa_yeh_kaf` into your custom analyzer’s `char_filter` list.

---

## Querying

Use the same analyzer path as the field:

```http
GET /articles_fa/_search
{
  "query": {
    "match": {
      "body": "برنامه‌نویسی"
    }
  }
}
```

For exact titles/tags, query the `.keyword` subfield with `term`.

---

## Mixed Persian + English

Use multi-fields or `multi_match` across language-specific subfields:

```json
"body": {
  "type": "text",
  "analyzer": "persian",
  "fields": {
    "en": { "type": "text", "analyzer": "english" }
  }
}
```

---

## Summary

* Start with the built-in `persian` analyzer and `_analyze`
* Normalize Yeh/Kaf, ZWNJ, and digits for consistent matches
* Keep a `keyword` multi-field for exact operations
* Reindex after analyzer changes
