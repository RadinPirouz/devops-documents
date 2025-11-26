## 1. Purpose

This document describes how **NGINX handles route mapping** when used as a reverse proxy.
It explains how `location`, `proxy_pass`, and related directives determine the **final upstream URL** sent to backend services.

---

## 2. Core Directives

### 2.1 `location`

Defines which incoming request path should be matched.

**Example**

```nginx
location /api/ { ... }
```

This block is triggered for any request beginning with `/api/`, such as `/api/users` or `/api/data/info`.

---

### 2.2 `proxy_pass`

Defines the target backend (upstream) to which the request will be forwarded.

The **syntax of `proxy_pass`** determines how the URI is rewritten.
This is the most important aspect of route handling.

---

## 3. URI Rewriting Logic

The effect of `proxy_pass` depends on the **presence of a trailing slash `/`** after the upstream URL.

| Case                          | Configuration                                                      | Example Request | Upstream Request                  | Result                                                                  |
| ----------------------------- | ------------------------------------------------------------------ | --------------- | --------------------------------- | ----------------------------------------------------------------------- |
| **A. Trailing Slash Present** | `proxy_pass http://127.0.0.1:5000/;`                               | `/api/users`    | `http://127.0.0.1:5000/users`     | Keeps the part after `/api/`. **Recommended** for most reverse proxies. |
| **B. No Trailing Slash**      | `proxy_pass http://127.0.0.1:5000;`                                | `/api/users`    | `http://127.0.0.1:5000/api/users` | Appends the full location path; can cause incorrect routing.            |
| **C. Using Rewrite**          | `rewrite ^/api/(.*)$ /$1 break; proxy_pass http://127.0.0.1:5000;` | `/api/users`    | `http://127.0.0.1:5000/users`     | Manually removes `/api` prefix before forwarding.                       |

---

## 4. Recommended Routing Pattern

A clean and predictable configuration for separate routes:

```nginx
server {
    listen 80;
    server_name example.com;

    # Route for API
    location /api/ {
        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Route for Frontend
    location /app/ {
        proxy_pass http://127.0.0.1:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

This configuration ensures:

* `/api/...` → backend at port `5000`
* `/app/...` → frontend at port `3000`
* Path components after `/api/` or `/app/` are preserved correctly.

---

## 5. Common Routing Issues

| Symptom                                             | Likely Cause                                               | Fix                                           |
| --------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------- |
| Backend receives wrong path (e.g. `/api/api/users`) | Missing trailing slash in `proxy_pass`                     | Add `/` to the end of the `proxy_pass` target |
| Backend receives empty path                         | Using `rewrite` incorrectly or missing URI in `proxy_pass` | Verify the rewrite pattern and use `break`    |
| Redirects loop or wrong host in backend             | Missing `proxy_set_header Host $host;`                     | Include required proxy headers                |
| HTTPS backend errors                                | Backend expects HTTPS but `proxy_pass` uses HTTP           | Use `proxy_pass https://...;`                 |

---

## 6. Testing Routing

Use `curl` to validate routing:

```bash
curl -v http://example.com/api/users
```

Check the backend logs to confirm that the incoming path matches the expected `/users`.

Test configuration before reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## 7. Summary

* The `location` directive defines which incoming route to match.
* The `proxy_pass` directive determines how the URI is forwarded.
* The **presence of a trailing slash** in `proxy_pass` is the key factor controlling route rewriting.
* Optional `rewrite` rules can further customize paths.
* Always test with `nginx -t` and verify backend behavior.

