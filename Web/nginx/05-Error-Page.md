# 05 — Error Pages

The `error_page` directive maps HTTP status codes to custom responses — HTML files, redirects, or named locations.

---

## Custom HTML pages

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/example.com/html;

    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;

    location = /404.html {
        internal;
    }

    location = /50x.html {
        internal;
    }
}
```

Place files in the site root (e.g. `/var/www/example.com/html/404.html`).

`internal` prevents direct browser access — the page is only served via internal redirect from `error_page`.

---

## Redirect on error

```nginx
error_page 404 =301 /new-location;
error_page 404 =301 https://example.com/not-found;
```

The `=` prefix changes the response code.

---

## Named location fallback

```nginx
error_page 502 503 504 @maintenance;

location @maintenance {
    root /var/www/maintenance;
    rewrite ^ /maintenance.html break;
}
```

---

## Change response code (soft 404)

```nginx
# Returns 200 with 404 page body — use carefully for SEO
error_page 404 =200 /404.html;
```

---

## Per-location error pages

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8080/;
    error_page 502 503 /api-error.json;
}

location = /api-error.json {
    internal;
    default_type application/json;
    return 503 '{"error":"Service unavailable"}';
}
```

---

## Upstream errors (reverse proxy)

By default Nginx passes backend error responses through. Enable interception:

```nginx
location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_intercept_errors on;
    error_page 502 503 504 /50x.html;
}
```

---

## Complete example

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.html;

    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8080/;
        proxy_intercept_errors on;
        error_page 502 503 504 /50x.html;
    }

    location = /404.html { internal; }
    location = /50x.html { internal; }
}
```

---

## Key takeaways

- `error_page` maps status codes to URIs, named locations, or redirects
- Mark error page locations as `internal`
- Use `proxy_intercept_errors on` to handle backend 5xx errors
