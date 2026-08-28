# 10 — HTTP Basic Authentication

Protect locations with username/password using HTTP Basic Auth.

---

## Configuration

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/example.com/html;

    location / {
        auth_basic "Restricted Area";
        auth_basic_user_file /etc/nginx/.htpasswd;
        try_files $uri $uri/ =404;
    }
}
```

| Directive | Purpose |
| --------- | ------- |
| `auth_basic "..."` | Enables auth; string is the browser prompt title |
| `auth_basic_user_file` | Path to password file (must be outside web root) |

Protect only part of a site:

```nginx
location /admin/ {
    auth_basic "Admin Panel";
    auth_basic_user_file /etc/nginx/.htpasswd;
    try_files $uri $uri/ =404;
}
```

---

## Create password file

Install `htpasswd`:

```bash
sudo apt install apache2-utils
```

Create file with first user (`-c` creates new file — use only once):

```bash
sudo htpasswd -c /etc/nginx/.htpasswd admin
```

Add more users (no `-c`):

```bash
sudo htpasswd /etc/nginx/.htpasswd developer
```

Set permissions:

```bash
sudo chmod 640 /etc/nginx/.htpasswd
sudo chown root:www-data /etc/nginx/.htpasswd
```

---

## Test and reload

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Browser will prompt for username and password when accessing the protected location.

---

## HTTPS + Basic Auth

Combine SSL with password protection (see [18-SSL](18-SSL.md) for certificate setup):

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    root /var/www/example.com/html;

    location / {
        auth_basic "Admin";
        auth_basic_user_file /etc/nginx/.htpasswd;
        try_files $uri $uri/ =404;
    }
}
```

---

## Combine with IP restriction

Require both valid IP **and** password:

```nginx
location /admin/ {
    satisfy all;
    allow 192.168.1.0/24;
    deny all;

    auth_basic "Admin";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

Or either IP **or** password:

```nginx
satisfy any;
```

---

## Security notes

- Passwords are hashed in `.htpasswd`, but credentials are sent base64-encoded — **always use HTTPS** in production
- Store `.htpasswd` outside the document root
- Suitable for admin panels, staging sites, and internal tools — not a replacement for app-level auth

---

## Key takeaways

- `auth_basic` + `auth_basic_user_file` enable password protection
- Create users with `htpasswd`
- Use HTTPS; restrict file permissions on `.htpasswd`
