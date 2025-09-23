# MinIO Admin: Site-to-Site Replication 

The **`mc admin replication`** and **`mc admin replicate`** commands manage replication between MinIO servers.

---

## Checking Replication

* **Get replication configuration info:**

```bash
mc admin replication info <mc-server>
```

* **Check replication status:**

```bash
mc admin replication status <mc-server>
```

---

## Adding Replication

* **Add a replication between servers (default mode):**

```bash
mc admin replicate add <mc-server1> <mc-server2> <mc-server3>
```

* **Add replication in synchronous mode:**

```bash
mc admin replicate add <mc-server1> <mc-server2> <mc-server3> --mode sync
```

* **Add replication in asynchronous mode:**

```bash
mc admin replicate add <mc-server1> <mc-server2> <mc-server3> --mode async
```

---

## Removing Replication

* **Remove all replication rules on a server:**

```bash
mc admin replication rm <mc-server1> --all --force
```

* **Remove specific replication between servers:**

```bash
mc admin replication rm <mc-server1> <mc-server2> <mc-server3> --force
```

