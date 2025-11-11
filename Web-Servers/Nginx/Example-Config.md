# Nginx Reverse Proxy Configuration
## Overview

This Nginx configuration serves two main purposes:

1. **Static file listing** from `/srv/files/` under the `/nginx-files/` path.
2. **Reverse proxy to MinIO** running on `http://127.0.0.1:9001` for all other requests.

The configuration also sets headers to ensure proper client information forwarding, support for WebSockets, and correct host resolution.

---

## Server Block

```nginx
server {
    listen 80;
    server_name example.com;

    error_log /var/log/nginx/file-error.log warn;
    access_log /var/log/nginx/file-access.log;
```

* **listen 80;** — The server listens on HTTP port 80.
* **server_name example.com;** — Responds to requests for this domain.
* **error_log** and **access_log** — Define custom log files for debugging and access tracking.

---

## Location `/nginx-files/` — Static File Listing

```nginx
location /nginx-files/ {
    alias /srv/files/;
    autoindex on;
    autoindex_exact_size off;
    autoindex_localtime on;
}
```

* **alias /srv/files/;** — Maps the URL path `/nginx-files/` to the filesystem path `/srv/files/`.
* **autoindex on;** — Enables directory listing.
* **autoindex_exact_size off;** — Shows file sizes in human-readable format instead of exact bytes.
* **autoindex_localtime on;** — Displays file modification times in the server’s local timezone.

---

## Location `/` — MinIO Reverse Proxy

```nginx
location / {
    proxy_pass http://127.0.0.1:9001;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### proxy_pass

* **proxy_pass [http://127.0.0.1:9001](http://127.0.0.1:9001);** — Forwards all requests to the MinIO server running on localhost port 9001.

### proxy_http_version

* **proxy_http_version 1.1;** — Ensures the proxy uses HTTP/1.1, required for WebSocket support and persistent connections.

### proxy_set_header

1. **Upgrade $http_upgrade;**

   * Passes the `Upgrade` header from the client, needed for WebSocket connections.
   * Allows MinIO (or any WebSocket-enabled service) to handle protocol upgrades properly.

2. **Connection "upgrade";**

   * Indicates that the connection may be upgraded (e.g., to WebSocket).
   * Works with the `Upgrade` header to maintain persistent connections.

3. **Host $host;**

   * Sends the original `Host` header from the client to the upstream server.
   * Ensures that MinIO knows which hostname was requested and can generate correct URLs.

4. **X-Real-IP $remote_addr;**

   * Forwards the client’s IP address to the upstream server.
   * Useful for logging, rate limiting, and IP-based access control.

5. **X-Forwarded-For $proxy_add_x_forwarded_for;**

   * Maintains a list of all IP addresses the request has passed through (client → proxy → upstream).
   * Helps upstream services identify the original client IP when multiple proxies are involved.

6. **X-Forwarded-Proto $scheme;**

   * Passes the original protocol (`http` or `https`) used by the client.
   * Important for generating correct links, redirects, or enforcing HTTPS in the upstream service.

---

### Summary

This configuration ensures:

* Efficient serving of static files with directory listing.
* Proper reverse proxying to MinIO with support for WebSockets.
* Accurate client information forwarding for logging and security.
* Compatibility with applications that depend on the original `Host` and protocol.


