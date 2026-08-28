# 00 — Introduction

## What is Nginx?

**Nginx** (engine-x) is a popular open-source web server and reverse proxy. It uses an **event-driven, asynchronous architecture** to handle many concurrent connections efficiently — originally built to solve the **C10k problem** (10,000 simultaneous clients).

Key strengths: high performance, stability, low resource usage, SSL/TLS termination, load balancing, caching, and compression.

## What this course covers

A practical walkthrough of Nginx configuration — from basic web serving to reverse proxy, load balancing, security, and performance tuning.

| Lesson | Topic |
| ------ | ----- |
| 1 | Nginx basics — install, architecture, main config |
| 2 | `http` and `server` blocks |
| 3 | `location` matching |
| 4 | Logging |
| 5 | Custom error pages |
| 6 | Process signals and reload |
| 7 | Reverse proxy |
| 8 | Load balancing |
| 9 | Rate limiting |
| 10 | HTTP Basic Auth |
| 11 | IP allow/deny |
| 12 | Caching |
| 13 | Buffers |
| 14 | Gzip compression |
| 15 | Timeouts |
| 16 | URL rewrite |
| 17 | Events block |

See also: [18-SSL](18-SSL.md) · [19-WebSocket](19-WebSocket.md) · [20-File-Server](20-File-Server.md) · [Example-Config](Example-Config.md)

---

## Configuration file layout

On Debian/Ubuntu, Nginx config is split across several paths:

| Path | Purpose |
| ---- | ------- |
| `/etc/nginx/nginx.conf` | Main config — `events`, `http`, global settings |
| `/etc/nginx/sites-available/` | Site configs (not active until enabled) |
| `/etc/nginx/sites-enabled/` | Symlinks to enabled sites |
| `/etc/nginx/conf.d/` | Additional `.conf` snippets |
| `/etc/nginx/snippets/` | Reusable partial configs |

Typical top-level structure:

```nginx
# /etc/nginx/nginx.conf

user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 768;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    access_log /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

---

## Context hierarchy

Nginx config is nested in **contexts**. A directive is only valid in certain contexts.

```
main
├── events
└── http
    ├── upstream
    ├── server
    │   └── location
    └── map / geo / limit_req_zone ...
```

- **main** — global (worker processes, user, pid file)
- **events** — connection model (`worker_connections`, `use epoll`)
- **http** — HTTP-wide defaults (gzip, logging, mime types)
- **server** — virtual host (domain, SSL, root)
- **location** — URL path handling

---

## Essential commands

```bash
# Test syntax
sudo nginx -t

# Reload config (no dropped connections)
sudo systemctl reload nginx

# Restart (brief downtime)
sudo systemctl restart nginx

# Check status
sudo systemctl status nginx
```

Always run `nginx -t` before reloading.
