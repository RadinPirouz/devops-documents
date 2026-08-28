# 13 — Buffers

Buffers control how Nginx reads and stores request/response data in memory before sending it. Proper buffer sizing prevents disk I/O and improves proxy performance.

---

## Why buffers matter

Without enough buffer space, Nginx writes temporary data to disk — slower and more I/O intensive. Buffers are especially important for reverse proxy and file upload scenarios.

---

## Client request buffers

```nginx
http {
    client_body_buffer_size 16k;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 8k;
    client_max_body_size 50m;
}
```

| Directive | Purpose |
| --------- | ------- |
| `client_body_buffer_size` | Buffer for request body (POST uploads) |
| `client_header_buffer_size` | Buffer for request headers |
| `large_client_header_buffers` | Extra buffers for large headers (cookies, JWT) |
| `client_max_body_size` | Max upload size (returns 413 if exceeded) |

---

## Proxy buffers (upstream response)

```nginx
location / {
    proxy_pass http://127.0.0.1:8080;

    proxy_buffering on;              # default: on
    proxy_buffer_size 4k;              # first chunk of response (headers)
    proxy_buffers 8 4k;              # 8 buffers of 4k for response body
    proxy_busy_buffers_size 8k;      # max size of buffers sending to client
}
```

| Directive | Purpose |
| --------- | ------- |
| `proxy_buffering on` | Buffer full response before sending to client |
| `proxy_buffer_size` | Buffer for response headers |
| `proxy_buffers` | Number and size of buffers for response body |
| `proxy_busy_buffers_size` | Limit on buffers actively sent to client |

**Disable buffering** for streaming/SSE (send data immediately):

```nginx
location /stream/ {
    proxy_pass http://127.0.0.1:8080;
    proxy_buffering off;
    proxy_cache off;
}
```

---

## FastCGI buffers (PHP)

```nginx
location ~ \.php$ {
    fastcgi_pass unix:/run/php/php8.2-fpm.sock;
    fastcgi_buffer_size 16k;
    fastcgi_buffers 4 16k;
    fastcgi_busy_buffers_size 32k;
}
```

---

## Temporary file thresholds

When buffers are full, Nginx writes to disk:

```nginx
proxy_max_temp_file_size 1024m;    # max temp file size (0 = disable disk)
proxy_temp_file_write_size 64k;    # chunk size when writing to temp file
```

For high-throughput proxying, increase `proxy_buffers` to avoid disk writes.

---

## Recommended starting point

```nginx
http {
    client_max_body_size 50m;
    client_body_buffer_size 128k;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
    }
}
```

Tune based on typical response sizes and upload requirements.

---

## Key takeaways

- Increase proxy/fastcgi buffers for large responses to avoid disk temp files
- Set `client_max_body_size` to control upload limits
- Disable `proxy_buffering` for streaming endpoints
