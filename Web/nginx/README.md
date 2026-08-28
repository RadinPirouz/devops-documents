# Nginx Documentation

Unified guide covering the video course (lessons 0–17) plus supplementary topics.

## Course (video series)

| # | Video | Doc |
| - | ----- | --- |
| 0 | intro | [00-Intro.md](00-Intro.md) |
| 1 | nginx | [01-Nginx.md](01-Nginx.md) |
| 2 | http | [02-Http.md](02-Http.md) |
| 3 | location | [03-Location.md](03-Location.md) |
| 4 | logging | [04-Logging.md](04-Logging.md) |
| 5 | error page | [05-Error-Page.md](05-Error-Page.md) |
| 6 | signals | [06-Signals.md](06-Signals.md) |
| 7 | reverse proxy | [07-Reverse-Proxy.md](07-Reverse-Proxy.md) |
| 8 | load balance | [08-Load-Balance.md](08-Load-Balance.md) |
| 9 | limit | [09-Limit.md](09-Limit.md) |
| 10 | auth basic | [10-Auth-Basic.md](10-Auth-Basic.md) |
| 11 | deny ip | [11-Deny-IP.md](11-Deny-IP.md) |
| 12 | cache | [12-Cache.md](12-Cache.md) |
| 13 | buffer | [13-Buffer.md](13-Buffer.md) |
| 14 | gzip | [14-Gzip.md](14-Gzip.md) |
| 15 | timeout | [15-Timeout.md](15-Timeout.md) |
| 16 | rewrite | [16-Rewrite.md](16-Rewrite.md) |
| 17 | events | [17-Events.md](17-Events.md) |

## Supplementary

| Doc | Topic |
| --- | ----- |
| [18-SSL.md](18-SSL.md) | HTTPS with Let's Encrypt / Certbot |
| [19-WebSocket.md](19-WebSocket.md) | WebSocket proxy configuration |
| [20-File-Server.md](20-File-Server.md) | File server with directory listing |
| [21-openssl.md](21-openssl.md) | Self-signed certificates with OpenSSL |
| [Example-Config.md](Example-Config.md) | Full reverse proxy + static files example |

## Config hierarchy

```
main context          → /etc/nginx/nginx.conf
├── events { }        → see 17-Events.md
└── http { }          → see 02-Http.md
    ├── upstream { }  → see 08-Load-Balance.md
    └── server { }    → virtual host
        └── location  → see 03-Location.md
```

After every config change:

```bash
sudo nginx -t
sudo systemctl reload nginx
```
