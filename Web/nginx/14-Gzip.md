# 14 — Gzip Compression

Gzip reduces response size by compressing text-based content before sending it to the client.

---

## Enable gzip

```nginx
http {
    gzip on;
    gzip_comp_level 5;
    gzip_min_length 256;
    gzip_proxied any;
    gzip_vary on;
    gzip_types
        text/plain
        text/css
        text/xml
        application/json
        application/javascript
        application/xml
        application/xml+rss
        image/svg+xml;
}
```

| Directive | Purpose |
| --------- | ------- |
| `gzip on` | Enable compression |
| `gzip_comp_level` | Compression level 1–9 (5 is a good balance) |
| `gzip_min_length` | Don't compress responses smaller than this |
| `gzip_proxied` | Compress proxied responses (`any`, `off`, `expired`, etc.) |
| `gzip_vary on` | Adds `Vary: Accept-Encoding` for caches |
| `gzip_types` | MIME types to compress (HTML is always compressed) |

---

## Compression levels

| Level | Speed | Compression |
| ----- | ----- | ----------- |
| 1 | Fastest | Lowest |
| 5 | Balanced | Good (recommended) |
| 9 | Slowest | Highest |

Higher levels use more CPU. Level 5 is typical for production.

---

## Don't compress already-compressed formats

Gzip is for text. Skip binary formats that are already compressed:

- `jpg`, `png`, `gif`, `webp`
- `mp4`, `zip`, `gz`

Only list compressible types in `gzip_types`. Nginx never gzip-compresses `image/*` by default.

---

## Precompressed static files

Serve pre-built `.gz` files if they exist:

```nginx
gzip_static on;    # requires ngx_http_gzip_static_module
```

Nginx serves `file.js.gz` when client accepts gzip and the file exists on disk.

---

## Verify compression

```bash
curl -H "Accept-Encoding: gzip" -I http://example.com/style.css
```

Look for:

```
Content-Encoding: gzip
Vary: Accept-Encoding
```

---

## Behind reverse proxy / CDN

If Nginx is behind a CDN that also compresses, avoid double compression — either compress at CDN or at Nginx, not both.

Use `gzip_proxied any` when Nginx compresses responses from upstream backends.

---

## Key takeaways

- Enable gzip for text, JSON, CSS, JS, SVG
- Level 5 is a good CPU/size tradeoff
- Set `gzip_min_length` to skip tiny responses
- Verify with `curl -H "Accept-Encoding: gzip"`
