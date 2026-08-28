# 17 — Events Block

The `events` block configures how Nginx handles connections. It sits at the top level alongside `http` — not inside it.

---

## Basic events block

```nginx
# /etc/nginx/nginx.conf

user www-data;
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 1024;
    multi_accept on;
    use epoll;
}

http {
    # ...
}
```

---

## Directives

| Directive | Purpose |
| --------- | ------- |
| `worker_connections` | Max simultaneous connections per worker |
| `multi_accept on` | Accept multiple connections at once when ready |
| `use epoll` | Event method (Linux — efficient for high concurrency) |
| `accept_mutex off` | Disable accept mutex (default off in recent versions) |

---

## Event methods (`use`)

| Method | Platform |
| ------ | -------- |
| `epoll` | Linux (recommended) |
| `kqueue` | FreeBSD, macOS |
| `select` / `poll` | Generic fallback |

On Linux, `epoll` is selected automatically if available. Explicit `use epoll` documents intent.

---

## Connection capacity

Maximum concurrent clients:

```
max_clients = worker_processes × worker_connections
```

Example:

```
worker_processes auto   → 4 cores
worker_connections 1024
max = 4 × 1024 = 4096 concurrent connections
```

Also limited by OS file descriptor limits:

```nginx
worker_rlimit_nofile 65535;
```

Check system limits:

```bash
ulimit -n
cat /proc/sys/fs/file-max
```

`/etc/security/limits.conf`:

```
www-data soft nofile 65535
www-data hard nofile 65535
```

---

## Tuning for high traffic

```nginx
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 8192;
    multi_accept on;
    use epoll;
}
```

| Setting | Notes |
| ------- | ----- |
| `worker_processes auto` | Match CPU cores |
| `worker_connections 8192` | Increase for high concurrency (watch memory) |
| `multi_accept on` | Reduces latency under load; slightly higher CPU |
| `worker_rlimit_nofile` | Must exceed `worker_connections` × 2 (approx) |

Each connection uses memory — don't set `worker_connections` excessively high without testing.

---

## Relationship to `http` block

```
main context
├── events { }     ← how workers accept connections
└── http { }       ← HTTP protocol handling
    └── keepalive_timeout, sendfile, etc.
```

- **events** — connection acceptance model
- **http** — protocol-level settings (keepalive, buffers, gzip)

---

## Key takeaways

- `events` is required — Nginx won't start without it
- `worker_connections` × `worker_processes` = max concurrent clients
- On Linux use `epoll`; raise `worker_rlimit_nofile` with connection limits
