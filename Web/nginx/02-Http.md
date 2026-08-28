# 02 — HTTP Block

The `http` block wraps all HTTP-related settings. Directives here apply to every `server` block unless overridden.

---

## Basic structure

```nginx
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    keepalive_timeout 65;

    access_log /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log warn;

    gzip on;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

---

## Common http-level directives

| Directive | Purpose |
| --------- | ------- |
| `include mime.types` | Maps file extensions to MIME types |
| `default_type` | Fallback MIME type when unknown |
| `sendfile on` | Zero-copy file transfer (efficient static serving) |
| `tcp_nopush on` | Send headers and body in one packet with sendfile |
| `tcp_nodelay on` | Send small packets immediately (lower latency) |
| `keepalive_timeout` | How long to keep idle connections open |
| `keepalive_requests` | Max requests per keepalive connection |
| `client_max_body_size` | Max upload size (default 1m) |
| `server_tokens off` | Hide Nginx version in headers |

---

## Server block

Each `server { }` is a virtual host — one site or app.

```nginx
server {
    listen 80;
    listen [::]:80;                    # IPv6
    server_name example.com www.example.com;

    root /var/www/example.com/html;
    index index.html index.htm;

    charset utf-8;

    access_log /var/log/nginx/example.com-access.log;
    error_log  /var/log/nginx/example.com-error.log warn;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Key server directives

| Directive | Purpose |
| --------- | ------- |
| `listen` | IP:port to bind (default port 80) |
| `server_name` | Hostnames this block responds to |
| `root` | Document root for this server |
| `index` | Default file when URI is a directory |
| `charset` | Response character set |

### `server_name` matching order

1. Exact name (`example.com`)
2. Longest wildcard starting with `*` (`.example.com`)
3. Longest wildcard ending with `*` (`example.*`)
4. First matching regex
5. Default server (first `listen` with `default_server`)

Catch-all:

```nginx
server {
    listen 80 default_server;
    server_name _;
    return 444;   # close connection without response
}
```

---

## Multiple sites on one server

```nginx
# /etc/nginx/sites-available/site-a
server {
    listen 80;
    server_name site-a.com;
    root /var/www/site-a;
}

# /etc/nginx/sites-available/site-b
server {
    listen 80;
    server_name site-b.com;
    root /var/www/site-b;
}
```

Enable each with a symlink to `sites-enabled/`.

---

## Include pattern

Split config into reusable files:

```nginx
http {
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}

# Inside a server block:
include snippets/ssl-params.conf;
```

This keeps the main file clean and makes snippets shareable across sites.

---

## Key takeaways

- `http` = global HTTP defaults; `server` = one virtual host
- `listen` + `server_name` determine which block handles a request
- Use `include` to organize config across multiple files
