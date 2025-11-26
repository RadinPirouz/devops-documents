# **Nginx Optimization Guide**

This document provides recommended configurations to optimize **Nginx performance** for high concurrency, low latency, and efficient resource usage.

---

## **1. Core Performance Configuration**

```nginx
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 8192;   
    multi_accept on;          
    use epoll;                 
}
```

### **Explanation:**

| Directive                    | Description                                                                                                     |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `worker_processes auto`      | Automatically sets the number of worker processes to match CPU cores. Best practice: match number of CPU cores. |
| `worker_rlimit_nofile 65535` | Increases the number of file descriptors (FD) Nginx can handle, supporting higher connections.                  |
| `worker_connections 8192`    | Maximum number of simultaneous connections a worker can handle.                                                 |
| `multi_accept on`            | Allows a worker to accept multiple new connections at once. Improves performance but increases CPU usage.       |
| `use epoll`                  | Uses the epoll event model (Linux only). Highly scalable and efficient for non-blocking I/O.                    |

---

## **2. HTTP Optimization**

```nginx
http {
    sendfile on;               
    tcp_nopush on;             
    tcp_nodelay on;            
    keepalive_timeout 65;      
    keepalive_requests 10000;  

    client_max_body_size 50M;  
    server_tokens off;         

    # Compression
    gzip on;
    gzip_comp_level 5;         
    gzip_min_length 256;
    gzip_proxied any;
    gzip_types text/plain text/css application/json application/javascript application/xml+rss;
}
```

### **Explanation:**

| Directive                  | Description                                                                                           |
| -------------------------- | ----------------------------------------------------------------------------------------------------- |
| `sendfile on`              | Sends files directly from disk to network (zero-copy). Reduces CPU usage and improves response time.  |
| `tcp_nopush on`            | Sends headers and body together in a single packet for better network efficiency.                     |
| `tcp_nodelay on`           | Sends small TCP packets immediately, reducing latency for small responses.                            |
| `keepalive_timeout 65`     | Keeps connections open for 65 seconds after a request (adjustable).                                   |
| `keepalive_requests 10000` | Maximum number of requests allowed per keepalive connection.                                          |
| `client_max_body_size 50M` | Limits maximum upload size to prevent DoS attacks.                                                    |
| `server_tokens off`        | Hides Nginx version in headers and error pages for security.                                          |
| `gzip on`                  | Enables gzip compression of responses to reduce bandwidth.                                            |
| `gzip_comp_level 5`        | Compression level (1 = fast, low compression; 9 = slow, maximum compression). 5 is a balanced choice. |
| `gzip_min_length 256`      | Only compress responses larger than 256 bytes.                                                        |
| `gzip_proxied any`         | Enable compression even behind reverse proxies.                                                       |
| `gzip_types`               | Defines content types eligible for compression.                                                       |

---

## **3. Static File Caching**

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2?)$ {
    expires 7d;
    access_log off;
    add_header Cache-Control "public, no-transform";
}
```

### **Explanation:**

| Directive                                         | Description                                               |     |     |     |     |    |           |                                                               |
| ------------------------------------------------- | --------------------------------------------------------- | --- | --- | --- | --- | -- | --------- | ------------------------------------------------------------- |
| `~* .(jpg                                         | jpeg                                                      | png | gif | ico | css | js | woff2?)$` | Regex to match static files (images, styles, scripts, fonts). |
| `expires 7d`                                      | Sets browser caching for 7 days to reduce server load.    |     |     |     |     |    |           |                                                               |
| `access_log off`                                  | Disables logging for static files to improve performance. |     |     |     |     |    |           |                                                               |
| `add_header Cache-Control "public, no-transform"` | Ensures files are cacheable by clients and proxies.       |     |     |     |     |    |           |                                                               |

---

## **Summary of Best Practices**

1. **Worker & Connection Optimization:** Match workers to CPU cores, increase FD limits, and configure events for high concurrency.
2. **TCP & HTTP Tweaks:** Enable `sendfile`, `tcp_nopush`, and `tcp_nodelay` for low latency and efficient transfers.
3. **Connection Reuse:** Use `keepalive_timeout` and `keepalive_requests` to reduce overhead of repeated connections.
4. **Compression:** Enable gzip with balanced compression for reduced bandwidth usage.
5. **Security & Limits:** Hide Nginx version and set client upload limits to prevent abuse.
6. **Static Content Caching:** Cache static files with long expiry and disable unnecessary logging.

