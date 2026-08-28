# 16 — Rewrite

Nginx can rewrite URLs, redirect clients, and route requests using `rewrite`, `return`, and `try_files`.

---

## `return` — simple redirects and responses

```nginx
# Permanent redirect
location /old-page {
    return 301 /new-page;
}

# Temporary redirect
return 302 https://example.com/maintenance;

# Plain response
location = /health {
    return 200 "OK\n";
    add_header Content-Type text/plain;
}

# Drop connection
return 444;
```

| Code | Meaning |
| ---- | ------- |
| `301` | Permanent redirect |
| `302` | Temporary redirect |
| `404` | Not found |
| `444` | Close connection (Nginx-specific) |

---

## `rewrite` — regex URL rewriting

```nginx
rewrite regex replacement [flag];
```

Flags:

| Flag | Effect |
| ---- | ------ |
| `last` | Restart location search with new URI |
| `break` | Stop rewrite processing, continue in current location |
| `redirect` | 302 redirect to new URI |
| `permanent` | 301 redirect to new URI |

Examples:

```nginx
# Remove www
server {
    server_name www.example.com;
    return 301 $scheme://example.com$request_uri;
}

# Strip /api prefix before proxy
location /api/ {
    rewrite ^/api/(.*)$ /$1 break;
    proxy_pass http://127.0.0.1:8080;
}

# Force trailing slash
rewrite ^(/images/[^/]+)$ $1/ permanent;

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```

---

## `try_files` — filesystem lookup

```nginx
location / {
    try_files $uri $uri/ /index.html;
}

location / {
    try_files $uri $uri/ =404;
}
```

Checks each path in order:

1. `$uri` — exact file
2. `$uri/` — directory (may trigger index)
3. Fallback — last argument (URI, named location, or status code)

Named location fallback:

```nginx
location / {
    try_files $uri $uri/ @backend;
}

location @backend {
    proxy_pass http://127.0.0.1:3000;
}
```

---

## `rewrite` vs `try_files`

| Use case | Prefer |
| -------- | ------ |
| Static file serving | `try_files` |
| Redirect to another URL | `return 301` |
| Strip prefix for proxy | `rewrite ... break` or trailing slash on `proxy_pass` |
| SPA fallback | `try_files $uri $uri/ /index.html` |

---

## Common patterns

**HTTPS redirect:**

```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```

**Remove double slashes:**

```nginx
merge_slashes off;
rewrite ^/(.*//+)(.*)$ /$2 permanent;
```

**Legacy URL migration:**

```nginx
rewrite ^/blog/(.*)$ /articles/$1 permanent;
```

---

## Caution with `if`

Avoid complex logic with `if` inside `location` — it can behave unexpectedly. Prefer `return`, `rewrite`, `map`, or separate `location` blocks.

```nginx
# Prefer this:
location = /old {
    return 301 /new;
}

# Over this:
if ($uri = /old) {
    rewrite ^ /new permanent;
}
```

---

## Key takeaways

- `return` for simple redirects and fixed responses
- `rewrite` for regex-based URL transformation
- `try_files` for static content and SPA routing
- Prefer `return`/`try_files` over `if` when possible
