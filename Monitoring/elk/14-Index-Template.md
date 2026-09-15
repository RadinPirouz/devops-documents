# 14 — Index templates

Apply settings, mappings, and aliases automatically when new indices match a pattern.

[← Alias](./13-Alias.md) · [ELK index](./README.md) · [Next: Split / Shrink →](./15-Split-Shrink.md)

---

## Composable index template (modern)

```http
PUT /_index_template/books_template
{
  "index_patterns": ["books-*"],
  "priority": 200,
  "template": {
    "settings": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    },
    "mappings": {
      "properties": {
        "title": {
          "type": "text",
          "fields": {
            "keyword": { "type": "keyword" }
          }
        },
        "amazon_rating": { "type": "float" },
        "release_date": { "type": "date" }
      }
    },
    "aliases": {
      "books-all": {}
    }
  }
}
```

Creating `books-2024` now picks up this template. Higher **`priority`** wins when several templates match.

---

## Component templates

Reuse building blocks:

```http
PUT /_component_template/books_mappings
{
  "template": {
    "mappings": {
      "properties": {
        "title": { "type": "text" }
      }
    }
  }
}
```

```http
PUT /_index_template/books_template
{
  "index_patterns": ["books-*"],
  "composed_of": ["books_mappings"],
  "priority": 200,
  "template": {
    "settings": {
      "number_of_replicas": 1
    }
  }
}
```

---

## Data streams (logs / metrics)

For append-only time series, prefer **data streams** + lifecycle policies. An index template with `"data_stream": {}` backs `PUT /_data_stream/logs-app`.

---

## Simulate

```http
POST /_index_template/_simulate_index/books-demo
```

Shows which template would apply and the resolved settings/mappings.

---

## Legacy templates

Older clusters used `PUT /_template/name`. Prefer composable `_index_template` + `_component_template` on 7.8+.

---

## List / delete

```http
GET /_index_template/books_template
```

```http
DELETE /_index_template/books_template
```

---

## Summary

* Templates enforce consistent schema for `logs-*`, `books-*`, etc.
* Compose reusable component templates
* Set `priority` deliberately when patterns overlap
* Simulate before rolling out
