# 12 — Caching

Nginx can cache responses from upstream servers and set browser cache headers for static files.

---

## Browser caching (static files)

Tell clients to cache assets locally:

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2?)$ {
    expires 7d;
    add_header Cache-Control "public, no-transform";
    access_log off;
}
```

| Directive | Purpose |
| --------- | ------- |
| `expires 7d` | Sets `Expires` and `Cache-Control: max-age` |
| `add_header Cache-Control` | Fine-grained cache policy |
| `access_log off` | Skip logging high-volume static requests |

Time units: `s`, `m`, `h`, `d`, `M` (month), `y`.

---

## Proxy cache (upstream responses)

Cache backend responses on the Nginx server:

```nginx
http {
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m
                     max_size=1g inactive=60m use_temp_path=off;

    server {
        location / {
            proxy_pass http://127.0.0.1:8080;
            proxy_cache my_cache;
            proxy_cache_valid 200 10m;
            proxy_cache_valid 404 1m;
            proxy_cache_use_stale error timeout updating;
            add_header X-Cache-Status $upstream_cache_status;
        }
    }
}
```

| Directive | Purpose |
| --------- | ------- |
| `proxy_cache_path` | Cache storage location and zone definition |
| `keys_zone=my_cache:10m` | Shared memory for cache keys (10 MB) |
| `max_size=1g` | Max disk usage |
| `inactive=60m` | Remove entries not accessed in 60 minutes |
| `proxy_cache_valid` | How long to cache by status code |
| `$upstream_cache_status` | `HIT`, `MISS`, `BYPASS`, `EXPIRED`, etc. |

Create cache directory:

```bash
sudo mkdir -p /var/cache/nginx
sudo chown www-data:www-data /var/cache/nginx
```

---

## Skip cache for certain requests

```nginx
# Don't cache POST or authenticated requests
proxy_cache_methods GET HEAD;
proxy_no_cache $cookie_session $http_pragma $http_authorization;
proxy_cache_bypass $cookie_session $http_pragma $http_authorization;
```

---

## Cache by URL or args

```nginx
proxy_cache_key "$scheme$request_method$host$request_uri";
```

Default key is `$scheme$proxy_host$request_uri`.

---

## FastCGI cache (PHP)

```nginx
fastcgi_cache_path /var/cache/nginx/fastcgi levels=1:2 keys_zone=php_cache:10m;

location ~ \.php$ {
    fastcgi_pass unix:/run/php/php8.2-fpm.sock;
    fastcgi_cache php_cache;
    fastcgi_cache_valid 200 5m;
    add_header X-Cache-Status $upstream_cache_status;
}
```

---

## Purge cache

Nginx open-source has no built-in purge. Options:

- Delete files under `/var/cache/nginx/` and reload
- Use `proxy_cache_purge` (commercial Nginx Plus)
- Set short `proxy_cache_valid` TTLs during development

---

## Key takeaways

- `expires` / `Cache-Control` for browser-side caching of static files
- `proxy_cache_path` + `proxy_cache` for server-side upstream caching
- Check `$upstream_cache_status` header to verify cache hits
