# 09 — Rate Limiting

Nginx limits request rates using the **leaky bucket** algorithm via `limit_req_zone` and `limit_req`.

---

## Real-world example (file server)

```nginx
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=1r/s;

server {
    server_name files.example.com;
    root /srv/files;

    location / {
        autoindex on;
        limit_req zone=mylimit burst=4 nodelay;
    }
}
```

---

## Basic rate limit

```nginx
http {
    limit_req_zone $binary_remote_addr zone=mylimit:10m rate=1r/s;

    server {
        location / {
            limit_req zone=mylimit burst=4 nodelay;
        }
    }
}
```

| Directive | Purpose |
| --------- | ------- |
| `limit_req_zone` | Define shared zone (key + memory + rate) |
| `$binary_remote_addr` | Rate-limit key (client IP, 4 bytes) |
| `zone=mylimit:10m` | Named zone, 10 MB (~160k IPs) |
| `rate=1r/s` | Sustained rate (also `10r/m` for per-minute) |
| `burst=4` | Allow short bursts above the rate |
| `nodelay` | Reject excess immediately (no queue delay) |

---

## Burst with delay (two-stage)

```nginx
limit_req zone=mylimit burst=4 delay=2;
```

- Requests within rate + burst → served immediately
- Requests beyond burst → delayed
- Requests beyond burst + delay queue → rejected (503 by default)

---

## Custom status and logging

```nginx
location / {
    limit_req zone=mylimit burst=4 nodelay;
    limit_req_status 429;
    limit_req_log_level warn;
}

error_log /var/log/nginx/rate-error.log warn;
```

---

## Connection limiting

Limit simultaneous connections per IP:

```nginx
limit_conn_zone $binary_remote_addr zone=connlimit:10m;

server {
    location / {
        limit_conn connlimit 10;
    }
}
```

---

## Whitelist IPs

Skip rate limiting for trusted networks:

```nginx
geo $limit {
    default 1;
    10.0.0.0/8       0;
    192.168.0.0/24   0;
    93.127.222.112   0;
}

map $limit $limit_key {
    0 "";
    1 $binary_remote_addr;
}

limit_req_zone $limit_key zone=mylimit:10m rate=2r/s;

server {
    location / {
        limit_req zone=mylimit burst=3 delay=1;
    }
}
```

Empty key in `limit_req_zone` = no limit applied for that request.

---

## Key takeaways

- Define zones in `http` context; apply with `limit_req` in `location`
- `burst` handles traffic spikes; `nodelay` vs `delay` controls queuing
- Combine `geo` + `map` to whitelist trusted IPs
