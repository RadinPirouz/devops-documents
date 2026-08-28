# 03 — Location

The `location` directive matches request URIs and defines how Nginx handles them. Multiple `location` blocks can exist inside one `server`.

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8080/;
    }

    location = /health {
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }

    location ~* \.(jpg|jpeg|png|gif|css|js)$ {
        expires 30d;
        access_log off;
    }
}
```

---

## Match types

| Modifier | Syntax | Behavior |
| -------- | ------ | -------- |
| *(none)* | `location /api/` | **Prefix** — URI starts with path |
| `=` | `location = /login` | **Exact** — URI must match exactly |
| `^~` | `location ^~ /static/` | **Prefix, no regex** — stops search if matched |
| `~` | `location ~ \.php$` | **Regex** (case-sensitive) |
| `~*` | `location ~* \.(jpg\|png)$` | **Regex** (case-insensitive) |

---

## Selection order

1. Exact match (`=`)
2. Longest prefix with `^~`
3. Longest regular prefix
4. First matching regex (`~` / `~*`), in config order

If `^~` matches, regex locations are skipped.

---

## Common patterns

**SPA fallback**

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

**Static assets (skip regex for performance)**

```nginx
location ^~ /assets/ {
    root /var/www/static;
    expires 7d;
}
```

**PHP via FastCGI**

```nginx
location ~ \.php$ {
    include snippets/fastcgi-php.conf;
    fastcgi_pass unix:/run/php/php8.2-fpm.sock;
}
```

**Named location (internal only)**

```nginx
location / {
    try_files $uri @backend;
}

location @backend {
    proxy_pass http://127.0.0.1:3000;
}
```

Named locations (`@name`) cannot be hit directly by clients — only via `try_files`, `error_page`, etc.

---

## `root` vs `alias`

| Directive | Config | Request | Filesystem |
| --------- | ------ | ------- | ---------- |
| `root` | `location /images/ { root /srv; }` | `/images/logo.png` | `/srv/images/logo.png` |
| `alias` | `location /images/ { alias /srv/photos/; }` | `/images/logo.png` | `/srv/photos/logo.png` |

Use `alias` when the URL path should **not** be appended to the disk path. Keep trailing slashes consistent when serving directories.

---

## Key takeaways

- Prefix locations are the default; `=`, `^~`, `~`, `~*` modify matching
- Longest prefix wins among prefix locations
- `root` appends the location path; `alias` replaces it
