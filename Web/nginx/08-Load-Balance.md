# 08 — Load Balancing

Nginx distributes traffic across multiple backend servers using an `upstream` block and `proxy_pass`.

---

## Basic round-robin

```nginx
upstream backend_servers {
    server 10.10.10.1;
    server 10.10.10.2;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

By default Nginx uses **round-robin** — requests rotate across servers in order.

---

## Load balancing methods

**Least connections** — send to server with fewest active connections:

```nginx
upstream backend_servers {
    least_conn;
    server 10.10.10.1;
    server 10.10.10.2;
}
```

**IP hash** — same client IP always hits the same server (session stickiness):

```nginx
upstream backend_servers {
    ip_hash;
    server 10.10.10.1;
    server 10.10.10.2;
}
```

**Weighted round-robin** — more traffic to stronger servers:

```nginx
upstream backend_servers {
    server 10.10.10.1 weight=3;
    server 10.10.10.2 weight=1;
}
```

---

## Server states

```nginx
upstream backend_servers {
    server 10.10.10.1;
    server 10.10.10.2;
    server 10.10.10.3 backup;    # used only when primary servers are down
    server 10.10.10.4 down;      # marked permanently unavailable
}
```

| Parameter | Effect |
| --------- | ------ |
| `weight=N` | Relative load (default 1) |
| `backup` | Only used when all primaries fail |
| `down` | Temporarily disabled |
| `max_fails=N` | Failures before marking unhealthy |
| `fail_timeout=T` | Time server is considered down |

---

## Health checks (passive)

Nginx marks a server down after `max_fails` failed requests within `fail_timeout`:

```nginx
upstream backend_servers {
    server 10.10.10.1 max_fails=3 fail_timeout=30s;
    server 10.10.10.2 max_fails=3 fail_timeout=30s;
}
```

For active health checks, use Nginx Plus or an external health checker.

---

## Enable and test

```bash
sudo vim /etc/nginx/sites-available/load_balancer.conf
sudo ln -s /etc/nginx/sites-available/load_balancer.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Access `http://your-server-ip/` — requests should rotate across backend servers.

---

## Troubleshooting

| Issue | Fix |
| ----- | --- |
| 502 Bad Gateway | Backend unreachable — verify IPs and that services are running |
| Permission denied on logs | `sudo chown www-data:www-data /var/log/nginx/load_balancer_access.log` |
| Config errors | Run `nginx -t` before reload |

---

## Keepalive to upstreams

Reuse connections to backends:

```nginx
upstream backend_servers {
    server 10.10.10.1;
    server 10.10.10.2;
    keepalive 32;
}

location / {
    proxy_pass http://backend_servers;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
}
```

---

## Key takeaways

- `upstream` defines the server pool; `proxy_pass http://pool_name` uses it
- Default is round-robin; use `least_conn`, `ip_hash`, or `weight` as needed
- Use `backup` and `max_fails` for resilience
