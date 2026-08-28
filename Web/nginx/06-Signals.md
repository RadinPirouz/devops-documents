# 06 — Signals

Nginx is controlled by sending **signals** to the master process. You can use `nginx -s <signal>` or `systemctl`.

---

## Process model recap

```
Master (PID in /run/nginx.pid)
  ├── Worker 1
  ├── Worker 2
  └── Worker N
```

Signals go to the **master process**, which coordinates workers.

---

## Nginx signals

| Signal | Command | Effect |
| ------ | ------- | ------ |
| `stop` | `nginx -s stop` | Fast shutdown — workers stop immediately |
| `quit` | `nginx -s quit` | Graceful shutdown — finish active requests first |
| `reload` | `nginx -s reload` | Reload config — new workers, old workers finish in-flight requests |
| `reopen` | `nginx -s reopen` | Reopen log files (after logrotate) |

Examples:

```bash
sudo nginx -s reload
sudo nginx -s quit
sudo nginx -s reopen
```

---

## systemctl equivalents

```bash
sudo systemctl start nginx      # start
sudo systemctl stop nginx       # stop (SIGTERM)
sudo systemctl reload nginx     # reload config
sudo systemctl restart nginx    # stop + start (brief downtime)
sudo systemctl status nginx     # check running state
sudo systemctl enable nginx     # start on boot
```

Prefer `reload` over `restart` in production — no dropped connections.

---

## Safe config workflow

```bash
# 1. Edit config
sudo vim /etc/nginx/sites-available/example.com

# 2. Test syntax
sudo nginx -t

# 3. Apply (only if test passes)
sudo systemctl reload nginx
```

If `nginx -t` fails, the running config is unchanged.

---

## What happens on reload

1. Master reads new config
2. If valid, master spawns new worker processes
3. Master signals old workers to exit gracefully
4. Old workers finish current requests, then stop

Failed reload leaves old workers running with the previous config.

---

## Log rotation

After `logrotate` renames log files, Nginx still writes to the old file descriptors. Reopen logs:

```bash
sudo nginx -s reopen
# or
sudo systemctl reload nginx
```

---

## Key takeaways

- `reload` applies config without dropping active connections
- Always run `nginx -t` before reload
- Use `reopen` after log rotation
