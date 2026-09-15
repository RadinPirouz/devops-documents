# 15 — Split and shrink

Change primary shard count safely: **shrink** (fewer shards) or **split** (more shards).

[← Index template](./14-Index-Template.md) · [ELK index](./README.md) · [Next: Text analysis →](./16-Text-Analysis.md)

---

## Why?

`number_of_shards` is set at index creation. Too many small shards waste memory; too few huge shards limit parallelism. Shrink and split create a **new** index with a different primary count (then you alias-swap).

---

## Shrink — fewer primaries

Target shard count must be a **factor** of the current count (e.g. 6 → 3, 2, or 1).

1. Make the index read-only and relocate shards onto one node:

```http
PUT /books/_settings
{
  "settings": {
    "index.routing.allocation.require._name": "node-1",
    "index.blocks.write": true
  }
}
```

2. Shrink:

```http
POST /books/_shrink/books_shrunk
{
  "settings": {
    "index.number_of_shards": 1,
    "index.number_of_replicas": 1
  },
  "aliases": {
    "books_current": {}
  }
}
```

3. Clear allocation require / write block on the new index as needed; delete the old index when ready.

---

## Split — more primaries

Target must be a **multiple** of the current primary count (e.g. 1 → 2, 3, …).

```http
PUT /books/_settings
{
  "settings": {
    "index.blocks.write": true
  }
}
```

```http
POST /books/_split/books_split
{
  "settings": {
    "index.number_of_shards": 3
  }
}
```

Index must be read-only; Elasticsearch documents health/green requirements — check cluster docs for your version if the call fails.

---

## Clone (same shard count)

```http
POST /books/_clone/books_copy
```

Fast copy of metadata + hard links when on the same node (filesystem permitting). Still needs write block.

---

## Practical notes

* Prefer planning shard count via templates over frequent split/shrink
* After shrink/split, use aliases so apps keep a stable name
* Shrink needs all primaries on one node — disruptive; schedule a window
* For time-based indices, create the next index with the right shard count instead of rewriting history

---

## Summary

| API | Direction | Constraint |
| --- | --- | --- |
| `_shrink` | Fewer shards | Factor of current |
| `_split` | More shards | Multiple of current |
| `_clone` | Same count | Copy index |

All require a write block (and shrink needs co-located shards).
