# 20 — Elasticsearch with Python

Use the official `elasticsearch` client for index, search, and bulk helpers.

[← Persian](./19-Persian.md) · [ELK index](./README.md) · [Next: Django →](./21-Django-Elastic.md)

---

## Install

```bash
pip install elasticsearch
```

For Elastic Cloud or API keys, also see the client docs for your major version (7.x vs 8.x APIs differ slightly).

---

## Connect

```python
from elasticsearch import Elasticsearch

es = Elasticsearch(
    "http://localhost:9200",
    # basic_auth=("elastic", "changeme"),
    # api_key="...",
)

print(es.info())
```

---

## Index and get

```python
es.indices.create(index="users", ignore=400)

es.index(
    index="users",
    id=1,
    document={"name": "radin", "age": 20},
)

doc = es.get(index="users", id=1)
print(doc["_source"])
```

On 7.x clients you may still see `body={...}` instead of `document=`.

---

## Search

```python
resp = es.search(
    index="users",
    query={
        "match": {
            "name": "radin"
        }
    },
    size=10,
)

for hit in resp["hits"]["hits"]:
    print(hit["_id"], hit["_score"], hit["_source"])
```

---

## Bulk helper

```python
from elasticsearch.helpers import bulk

actions = [
    {
        "_index": "books",
        "_id": i,
        "_source": {
            "title": title,
            "amazon_rating": rating,
        },
    }
    for i, (title, rating) in enumerate(
        [("Effective Java", 4.7), ("Head First Java", 4.3)],
        start=1,
    )
]

ok, errors = bulk(es, actions)
print(ok, errors)
```

Also useful: `streaming_bulk`, `parallel_bulk`, `scan` for scroll.

---

## Update and delete

```python
es.update(index="users", id=1, doc={"age": 21})
es.delete(index="users", id=1)
```

---

## mget

```python
es.mget(index="users", ids=[1, 2, 3])
```

---

## Tips

* Reuse one `Elasticsearch` client (connection pool)
* Check `resp.meta.status` / raise on errors as needed for your client version
* Prefer bulk helpers for more than a handful of docs
* Keep Query DSL as plain dicts — same bodies as Kibana Dev Tools

---

## Summary

* `pip install elasticsearch` → `Elasticsearch(...)`
* CRUD: `index` / `get` / `update` / `delete` / `search`
* `helpers.bulk` for loading datasets
* Same Query DSL JSON you practiced in earlier lessons
