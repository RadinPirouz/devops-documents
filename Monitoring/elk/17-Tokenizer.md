# 17 — Tokenizer

The tokenizer splits (and sometimes merges) character streams into tokens.

[← Text analysis](./16-Text-Analysis.md) · [ELK index](./README.md) · [Next: Specify analyzer →](./18-Specify-Analyzer.md)

---

## Role in the analyzer

Character filters run first; the **tokenizer** emits the initial token list; token filters refine them (lowercase, n-grams, synonyms, …).

---

## Common tokenizers

### `standard`

Unicode text segmentation — default for the `standard` analyzer.

```http
POST /_analyze
{
  "tokenizer": "standard",
  "text": "You're emailing user@example.com"
}
```

### `whitespace`

```http
POST /_analyze
{
  "tokenizer": "whitespace",
  "text": "one-two three"
}
```

Tokens: `one-two`, `three`.

### `keyword`

No split — one token for the whole string (same idea as `keyword` field type).

### `pattern`

Split on a regex:

```http
POST /_analyze
{
  "tokenizer": {
    "type": "pattern",
    "pattern": ","
  },
  "text": "red,green,blue"
}
```

### `ngram` / `edge_ngram`

Partial matching / autocomplete-style tokens:

```http
PUT /suggest
{
  "settings": {
    "analysis": {
      "analyzer": {
        "autocomplete": {
          "tokenizer": "autocomplete_tok",
          "filter": ["lowercase"]
        }
      },
      "tokenizer": {
        "autocomplete_tok": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 15,
          "token_chars": ["letter", "digit"]
        }
      }
    }
  }
}
```

Often: **edge_ngram at index time**, plain tokenizer at search time (see next lesson).

### `uax_url_email`

Keeps URLs and emails as single tokens — better than `standard` for those.

### `path_hierarchy`

```http
POST /_analyze
{
  "tokenizer": {
    "type": "path_hierarchy",
    "delimiter": "/"
  },
  "text": "/usr/local/bin"
}
```

Emits `/usr`, `/usr/local`, `/usr/local/bin`.

---

## Try before you map

```http
POST /_analyze
{
  "tokenizer": "standard",
  "filter": ["lowercase"],
  "text": "Sample TEXT"
}
```

Iterate tokenizer + filters here, then lock them into index settings.

---

## Summary

| Tokenizer | Typical use |
| --- | --- |
| `standard` | General language text |
| `whitespace` | Simple space split |
| `keyword` | Exact whole-string token |
| `pattern` | Custom delimiters |
| `edge_ngram` | Prefix / typeahead |
| `uax_url_email` | URLs & emails intact |
| `path_hierarchy` | File / URL paths |
