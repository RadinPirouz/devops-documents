# 12 — Settings

Index settings: shards, replicas, refresh, analyzers, and dynamic updates.

[← Update](./11-Update.md) · [ELK index](./README.md) · [Next: Alias →](./13-Alias.md)

---

## Get settings

```http
GET /books/_settings
```

```http
GET /books/_settings/index.number_of_replicas
```

---

## Create with settings

```http
PUT /logs-2024
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "refresh_interval": "5s"
  }
}
```

* **`number_of_shards`** — fixed after create (use split/shrink to change — [15-Split-Shrink](./15-Split-Shrink.md))
* **`number_of_replicas`** — change anytime
* **`refresh_interval`** — how often new docs become searchable (`-1` disables; useful during bulk load)

---

## Update dynamic settings

```http
PUT /books/_settings
{
  "index": {
    "number_of_replicas": 2,
    "refresh_interval": "1s"
  }
}
```

---

## Bulk-load pattern

1. Set `"refresh_interval": "-1"` and optionally `"number_of_replicas": 0`
2. Bulk index
3. Restore refresh / replicas
4. `POST /books/_refresh` or wait for interval

```http
PUT /books/_settings
{
  "index": {
    "refresh_interval": "-1",
    "number_of_replicas": 0
  }
}
```

---

## Analysis settings

Custom analyzers live under index settings (details in [16–18](./16-Text-Analysis.md)):

```http
PUT /articles
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "body": {
        "type": "text",
        "analyzer": "my_analyzer"
      }
    }
  }
}
```

Changing analyzers on existing fields usually requires **reindex**.

---

## Blocks and read-only

Disk watermark can flip an index to read-only. Clear after freeing disk:

```http
PUT /books/_settings
{
  "index.blocks.read_only_allow_delete": null
}
```

---

## Cluster settings (related)

```http
GET /_cluster/settings?include_defaults=true
```

Persistent example:

```http
PUT /_cluster/settings
{
  "persistent": {
    "action.auto_create_index": "true"
  }
}
```

---

## Summary

* Set shard count carefully at create time
* Tune replicas and refresh for write-heavy loads
* Analysis config is part of settings + mapping
* Prefer index templates ([14](./14-Index-Template.md)) for consistent settings across many indices
