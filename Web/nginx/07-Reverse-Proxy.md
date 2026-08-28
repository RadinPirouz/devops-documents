# 07 — Reverse Proxy

A reverse proxy sits in front of backend apps and forwards client requests. Nginx handles SSL, routing, headers, and load distribution while hiding backend details.

---

## Basic proxy

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

| Directive | Purpose |
| --------- | ------- |
| `proxy_pass` | Backend URL to forward requests to |
| `proxy_set_header Host` | Preserve original hostname |
| `X-Real-IP` | Client IP (single value) |
| `X-Forwarded-For` | Client IP chain through proxies |
| `X-Forwarded-Proto` | Original scheme (`http` / `https`) |

---

## Path rewriting with `proxy_pass`

The trailing slash is the key factor controlling how the URI is forwarded:

| Case | Config | Request | Upstream request |
| ---- | ------ | ------- | ---------------- |
| Trailing slash | `proxy_pass http://127.0.0.1:5000/;` | `/api/users` | `http://127.0.0.1:5000/users` |
| No trailing slash | `proxy_pass http://127.0.0.1:5000;` | `/api/users` | `http://127.0.0.1:5000/api/users` |
| Rewrite + proxy | `rewrite ^/api/(.*)$ /$1 break;` + `proxy_pass http://127.0.0.1:5000;` | `/api/users` | `http://127.0.0.1:5000/users` |

Recommended pattern — strip prefix with trailing slash:

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:5000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

---

## Multiple backends by path

Route different URL paths to different services:

```nginx
server {
    listen 80;
    server_name _;

    location /web1 {
        proxy_pass http://web1.com;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /web2 {
        proxy_pass http://web2.com;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    access_log /var/log/nginx/reverse-proxy-access.log;
    error_log /var/log/nginx/reverse-proxy-error.log;
}
```

Or by port on localhost:

```nginx
server {
    listen 80;
    server_name example.com;

    location /api/ {
        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /app/ {
        proxy_pass http://127.0.0.1:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable config:

```bash
sudo ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

See [19-WebSocket](19-WebSocket.md) for full WebSocket proxy details.

---

## WebSocket support

```nginx
location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
```

---

## HTTP/1.1 and keepalive to upstream

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

---

## Troubleshooting

| Error | Likely cause |
| ----- | ------------ |
| 502 Bad Gateway | Backend down or wrong address |
| Wrong path (e.g. `/api/api/users`) | Missing trailing slash on `proxy_pass` | Add `/` to `proxy_pass` target |
| Backend receives empty path | Bad rewrite or missing URI | Verify rewrite pattern, use `break` |
| Redirect loops | Missing `Host` header | Add `proxy_set_header Host $host` |
| HTTPS backend errors | Backend expects HTTPS | Use `proxy_pass https://...` |
| WebSocket fails | Missing `Upgrade` / `Connection` headers |

Test routing:

```bash
curl -v http://example.com/api/users
sudo nginx -t && sudo systemctl reload nginx
```

---

## Key takeaways

- Always set `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`
- Trailing slash on `proxy_pass` strips the location prefix
- Use `proxy_http_version 1.1` for WebSockets and upstream keepalive
