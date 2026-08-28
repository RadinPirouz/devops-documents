# 04 — Logging

Nginx has two log types: **access logs** (one line per request) and **error logs** (diagnostics and errors).

---

## Basic setup

```nginx
http {
    access_log /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log warn;

    server {
        listen 80;
        server_name example.com;

        access_log /var/log/nginx/example.com-access.log;
        error_log  /var/log/nginx/example.com-error.log notice;
    }
}
```

| Directive | Purpose |
| --------- | ------- |
| `access_log` | Records each request (IP, URI, status, bytes, time) |
| `error_log` | Records warnings and errors |

Logs can be set at `http`, `server`, or `location` level. Child contexts override parent settings.

---

## Error log levels

From most to least verbose:

| Level | Use |
| ----- | --- |
| `debug` | Deep debugging (needs debug build) |
| `info` | General information |
| `notice` | Normal significant events |
| `warn` | Warnings (common default) |
| `error` | Errors |
| `crit` | Critical failures |
| `alert` | Immediate action needed |
| `emerg` | System unusable |

```nginx
error_log /var/log/nginx/error.log warn;
```

---

## Custom access log format

Define in `http`, reference by name:

```nginx
http {
    log_format main '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';

    log_format upstream '$remote_addr [$time_local] "$request" '
                        '$status rt=$request_time '
                        'urt="$upstream_response_time"';

    access_log /var/log/nginx/access.log main;
}
```

Useful variables:

| Variable | Meaning |
| -------- | ------- |
| `$remote_addr` | Client IP |
| `$request` | Full request line |
| `$status` | HTTP status code |
| `$body_bytes_sent` | Response size |
| `$request_time` | Total request time (seconds) |
| `$upstream_response_time` | Backend response time |

---

## Disable or filter logging

**Turn off for static assets / health checks:**

```nginx
location = /health {
    access_log off;
    return 200;
}

location ~* \.(css|js|png|jpg|gif|ico)$ {
    access_log off;
}
```

**Log only errors (skip 2xx/3xx):**

```nginx
map $status $loggable {
    ~^[23]  0;
    default 1;
}

access_log /var/log/nginx/access.log main if=$loggable;
```

**Buffered logging (high traffic):**

```nginx
access_log /var/log/nginx/access.log main buffer=32k flush=5s;
```

---

## Log rotation

Nginx does not rotate logs. Use `logrotate`:

```bash
sudo logrotate -f /etc/logrotate.d/nginx
```

After rotation, reopen log files:

```bash
sudo nginx -s reopen
# or
sudo systemctl reload nginx
```

---

## Key takeaways

- Access log = per-request; error log = problems and diagnostics
- Define custom formats with `log_format`
- Disable logging on high-volume static paths to reduce I/O
