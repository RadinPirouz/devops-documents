# 01 — Architecture

How a cluster is built: nodes, roles, shards, and request flow.

[← Intro](./00-Intro.md) · [ELK index](./README.md) · [Next: Index →](./02-Index.md)

---

## Cluster and nodes

A **cluster** is one or more **nodes** that share the same `cluster.name`. Nodes discover each other and hold a copy of the **cluster state** (which indices exist, where shards live, etc.).

```
Client / Kibana
      │
      ▼
┌─────────────┐
│ Coordinating│  (often every node can do this)
└──────┬──────┘
       │
   ┌───┴───┐
   ▼       ▼
 Data    Data     (+ dedicated master, ingest, …)
```

For production role layouts (master, hot/warm/cold, ingest, ML), see [Node-Types.md](./Node-Types.md). For the wider ELK pipeline (Beats → Logstash → ES → Kibana), see [Stack-Overview.md](./Stack-Overview.md).

---

## Shards and replicas

Each index is split into **primary shards**. Each primary can have **replica** copies on other nodes.

| Setting | Role |
| --- | --- |
| `number_of_shards` | How many primary shards (set at index creation; hard to change later) |
| `number_of_replicas` | How many copies of each primary (can change anytime) |

* Writes go to the primary, then sync to replicas
* Searches can run on primaries or replicas
* Yellow health usually means primaries are fine but some replicas are unassigned (common on a single-node cluster)

---

## Index vs document

```
Index: users
├── Document _id: 1   { "name": "radin", "age": 20 }
├── Document _id: 2   { "name": "ali",   "age": 25 }
└── ...
```

Documents are JSON. Elasticsearch indexes fields according to the **mapping** so they can be searched and aggregated efficiently.

---

## Request path (search)

1. Client hits any node (coordinating role).
2. Coordinating node fans the query out to shards that hold the data.
3. Each shard runs the query locally (Lucene).
4. Coordinating node merges hits, sorts by score / sort fields, returns the response.

Indexing follows a similar pattern: coordinating node → primary shard → replicas.

---

## Near real-time

A document is searchable after the next **refresh** (default ~1s), not instantly after the write ACK. For forced visibility in demos:

```http
POST /users/_refresh
```

---

## Summary

* Cluster = nodes + shared cluster state
* Index data is split into primary shards + optional replicas
* Any node can coordinate; dedicated roles scale production clusters
* Search is distributed; refresh makes new docs searchable
