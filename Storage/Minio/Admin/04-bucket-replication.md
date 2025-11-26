# MinIO Bucket Replication Guide

MinIO bucket replication allows you to synchronize objects across multiple MinIO servers. **Replication requires versioning** to be enabled on all participating buckets.

---

## 1. One-Way Bucket Replication

**Scenario:** `ms-sv1` → `ms-sv2`

**Command:**

```bash
mc replicate add ms-sv-1/BUCKET \
   --remote-bucket 'https://USER:PASSWORD@ms-sv-2/BUCKET' \
   --replicate "delete,delete-marker,existing-objects"
```

This sets up replication from `ms-sv1` to `ms-sv2`. Changes on `ms-sv1` will be mirrored to `ms-sv2`.

---

## 2. Two-Way Bucket Replication

**Scenario:** `ms-sv1` ↔ `ms-sv2`

**Commands:**

```bash
mc replicate add ms-sv-1/BUCKET \
   --remote-bucket 'https://USER:PASSWORD@ms-sv-2/BUCKET' \
   --replicate "delete,delete-marker,existing-objects"
```

```bash
mc replicate add ms-sv-2/BUCKET \
   --remote-bucket 'https://USER:PASSWORD@ms-sv-1/BUCKET' \
   --replicate "delete,delete-marker,existing-objects"
```

This ensures bidirectional synchronization between `ms-sv1` and `ms-sv2`.

---

## 3. Multi-Node Replication

**Scenario:** `ms-sv1`, `ms-sv2`, `ms-sv3`

Set up replication rules for each pair of servers:

**ms-sv1 rules:**

```bash
mc replicate add ms-sv-1/BUCKET \
   --remote-bucket 'https://USER:PASSWORD@ms-sv-2/BUCKET' \
   --replicate "delete,delete-marker,existing-objects"

mc replicate add ms-sv-1/BUCKET \
   --remote-bucket 'https://USER:PASSWORD@ms-sv-3/BUCKET' \
   --replicate "delete,delete-marker,existing-objects"
```

**ms-sv2 rules:**

```bash
mc replicate add ms-sv-2/BUCKET \
   --remote-bucket 'https://USER:PASSWORD@ms-sv-1/BUCKET' \
   --replicate "delete,delete-marker,existing-objects"

mc replicate add ms-sv-2/BUCKET \
   --remote-bucket 'https://USER:PASSWORD@ms-sv-3/BUCKET' \
   --replicate "delete,delete-marker,existing-objects"
```

**ms-sv3 rules:**

```bash
mc replicate add ms-sv-3/BUCKET \
   --remote-bucket 'https://USER:PASSWORD@ms-sv-1/BUCKET' \
   --replicate "delete,delete-marker,existing-objects"

mc replicate add ms-sv-3/BUCKET \
   --remote-bucket 'https://USER:PASSWORD@ms-sv-2/BUCKET' \
   --replicate "delete,delete-marker,existing-objects"
```

**Notes:**

* Each MinIO deployment has a replication rule for every other node.
* This setup ensures that any change in one bucket is synchronized across all nodes.
