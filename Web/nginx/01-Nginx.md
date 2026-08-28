# 01 — Nginx Basics

## What is Nginx?

**Nginx** (engine-x) is a high-performance web server, reverse proxy, and load balancer. It uses an **event-driven, asynchronous** architecture to handle many concurrent connections with low memory usage — originally built to solve the **C10k problem** (10,000 simultaneous clients).

Common roles:

- Serve static files (HTML, images, CSS, JS)
- Reverse proxy to app servers (Node, Python, PHP-FPM)
- Load balance across multiple backends
- Terminate SSL/TLS
- Cache and compress responses

---

## Architecture

```
         Master process
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
 Worker 1  Worker 2  Worker N
    │         │         │
  handles   handles   handles
  requests  requests  requests
```

- **Master process** — reads config, manages workers, handles signals
- **Worker processes** — actually serve requests (one per CPU core is typical)

---

## Installation

### Debian/Ubuntu

```bash
sudo apt update
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

### Red Hat/CentOS/Fedora

```bash
sudo yum install epel-release   # if needed
sudo yum install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Firewall

```bash
# Debian/Ubuntu
sudo ufw allow 'Nginx Full'

# Red Hat
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

Verify in browser: `http://<server-ip>` — you should see the default welcome page.

---

## Main configuration

`/etc/nginx/nginx.conf` — top-level settings:

```nginx
user www-data;
worker_processes auto;        # one worker per CPU core
pid /run/nginx.pid;
error_log /var/log/nginx/error.log;

events {
    worker_connections 768;
}

http {
    # all HTTP settings and server blocks
    include /etc/nginx/sites-enabled/*;
}
```

| Directive | Purpose |
| --------- | ------- |
| `user` | Unix user workers run as |
| `worker_processes` | Number of worker processes (`auto` = CPU count) |
| `pid` | PID file location |
| `error_log` | Global error log (can be overridden per server) |

---

## First server block

Create `/etc/nginx/sites-available/example.com`:

```nginx
server {
    listen 80;
    server_name example.com;

    root /var/www/example.com/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Set up web directory, enable site, and reload:

```bash
sudo mkdir -p /var/www/example.com/html
sudo chown -R $USER:$USER /var/www/example.com/html
sudo chmod -R 755 /var/www/example.com

echo "<html><head><title>Welcome</title></head>
<body><h1>Success! Nginx is serving your website.</h1></body></html>" \
  | sudo tee /var/www/example.com/html/index.html

sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Troubleshooting

| Issue | Fix |
| ----- | --- |
| 403 Forbidden | Check permissions — `chmod 755` on dirs, Nginx user (`www-data`) must read files |
| 404 Not Found | Verify `index.html` exists and `try_files` is correct |
| Config errors | Always run `nginx -t` before reload |
| Package not found (RHEL) | Install `epel-release` first |

---

## Key takeaways

- Nginx config is hierarchical: `main → events → http → server → location`
- One master process manages multiple worker processes
- Always test with `nginx -t` before reload
