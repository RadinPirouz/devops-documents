# 11 — Deny IP

Control access by client IP using `allow` and `deny` directives.

---

## Block specific IPs

```nginx
server {
    listen 80;
    server_name example.com;

    deny 192.168.1.100;
    deny 10.0.0.0/8;
    allow all;

    location / {
        root /var/www/html;
    }
}
```

Rules are evaluated **in order**. First match wins.

---

## Allow only specific IPs

```nginx
location /admin/ {
    allow 192.168.1.0/24;
    allow 93.127.222.112;
    deny all;

    root /var/www/admin;
}
```

Only listed networks can access `/admin/`; everyone else gets 403 Forbidden.

---

## Per-location rules

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        root /var/www/html;    # public
    }

    location /internal/ {
        allow 10.0.0.0/8;
        deny all;
        proxy_pass http://127.0.0.1:8080;
    }
}
```

---

## Combine with auth (`satisfy`)

**Both IP and password required:**

```nginx
location /admin/ {
    satisfy all;
    allow 192.168.1.0/24;
    deny all;

    auth_basic "Admin";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

**Either IP or password:**

```nginx
satisfy any;
allow 192.168.1.0/24;
deny all;
auth_basic "Admin";
auth_basic_user_file /etc/nginx/.htpasswd;
```

---

## Using `geo` for complex rules

Define a variable based on IP, then use it elsewhere:

```nginx
geo $blocked {
    default 0;
    192.168.1.100 1;
    10.0.0.0/8    1;
}

server {
    if ($blocked) {
        return 403;
    }
}
```

Prefer `allow`/`deny` in `location` blocks when possible — `if` in Nginx has caveats.

---

## Real IP behind a proxy

If Nginx sits behind another proxy/CDN, `$remote_addr` may be the proxy IP. Use `real_ip` module:

```nginx
set_real_ip_from 10.0.0.0/8;
real_ip_header X-Forwarded-For;
real_ip_recursive on;
```

Then `allow`/`deny` evaluate the actual client IP.

---

## Key takeaways

- `allow` / `deny` rules are processed top to bottom; first match wins
- End with `deny all` when whitelisting
- Use `satisfy` to combine IP rules with Basic Auth
