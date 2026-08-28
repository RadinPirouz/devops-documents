# 15 — Timeouts

Timeouts control how long Nginx waits during connections, requests, and upstream communication. Misconfigured timeouts cause 504 Gateway Timeout or hung connections.

---

## Client timeouts

```nginx
http {
    keepalive_timeout 65;          # idle keepalive connection (seconds)
    keepalive_requests 1000;       # max requests per keepalive connection
    send_timeout 60;               # timeout sending response to client
    client_body_timeout 60;        # timeout reading client request body
    client_header_timeout 60;      # timeout reading client request headers
}
```

| Directive | Purpose |
| --------- | ------- |
| `keepalive_timeout` | Close idle client connections after N seconds |
| `keepalive_requests` | Max requests before closing keepalive connection |
| `send_timeout` | Time between successive write operations to client |
| `client_body_timeout` | Time to read entire request body |
| `client_header_timeout` | Time to read request headers |

---

## Proxy timeouts (reverse proxy)

```nginx
location / {
    proxy_pass http://127.0.0.1:8080;

    proxy_connect_timeout 10s;     # time to connect to upstream
    proxy_send_timeout 60s;        # time to send request to upstream
    proxy_read_timeout 60s;        # time to read response from upstream
}
```

| Directive | Default | Purpose |
| --------- | ------- | ------- |
| `proxy_connect_timeout` | 60s | Max time to establish upstream connection |
| `proxy_send_timeout` | 60s | Max time between writes to upstream |
| `proxy_read_timeout` | 60s | Max time between reads from upstream |

**504 Gateway Timeout** usually means `proxy_read_timeout` was exceeded — backend took too long.

For long-running API calls or reports:

```nginx
location /api/report/ {
    proxy_pass http://127.0.0.1:8080;
    proxy_read_timeout 300s;
    proxy_send_timeout 300s;
}
```

---

## FastCGI timeouts (PHP)

```nginx
location ~ \.php$ {
    fastcgi_pass unix:/run/php/php8.2-fpm.sock;
    fastcgi_connect_timeout 10s;
    fastcgi_send_timeout 60s;
    fastcgi_read_timeout 60s;
}
```

---

## Upstream keepalive

Keep connections open to backends (reduces connect overhead):

```nginx
upstream backend {
    server 127.0.0.1:8080;
    keepalive 32;
}

location / {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
}
```

`keepalive_timeout` in `upstream` (Nginx 1.1.4+) controls idle upstream connection lifetime.

---

## WebSocket / long-lived connections

WebSockets need long read timeouts:

```nginx
location /ws {
    proxy_pass http://127.0.0.1:8080;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 3600s;
}
```

---

## Quick reference

| Symptom | Likely fix |
| ------- | ---------- |
| 504 Gateway Timeout | Increase `proxy_read_timeout` |
| Upload fails on large files | Increase `client_body_timeout` and `client_max_body_size` |
| Connections pile up | Lower `keepalive_timeout` |
| Slow backend connect | Check `proxy_connect_timeout` and backend health |

---

## Key takeaways

- Client timeouts control browser ↔ Nginx; proxy timeouts control Nginx ↔ backend
- 504 errors → increase `proxy_read_timeout`
- WebSockets and streaming need extended read timeouts
