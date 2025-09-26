# Nginx Rate Limiting Guide

Nginx can control request rates using the **Leaky Bucket algorithm**. This helps prevent abuse, protect resources, and manage traffic efficiently.

---

## Basic Configuration

```nginx
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=1r/s;

server {
    server_name files.usethelinux.shop;
    root /srv/files;

    location / {
        autoindex on;
        limit_req zone=mylimit burst=4 nodelay;
    }
}
```

### Explanation:

* `$binary_remote_addr` → Client IP Address
* `10m` → Zone memory size (10MB) can handle approximately 160,000 addresses
* `1r/s` → 1 request per second
* `burst=4` → Allows a peak of 4 requests without delay
* `nodelay` → Rejects requests immediately when the limit is exceeded

> The rate can also be set lower, e.g., `10r/min` (10 requests per minute)

---

## Two-Stage Configuration (Smooth Bursting)

```nginx
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=5r/s;

server {
    server_name files.usethelinux.shop;
    root /srv/files;

    location / {
        autoindex on;
        limit_req zone=mylimit burst=4 delay=2;
    }
}
```

### Behavior:

* Requests 1–7 → Handled at full speed
* Requests 8–9 → Handled with delay
* Requests above 9 → Rejected

---

## Advanced Configuration

```nginx
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=3r/s;

server {
    server_name files.usethelinux.shop;
    root /srv/files;

    location / {
        autoindex on;
        limit_req zone=mylimit burst=4 delay=2;
        limit_req_status 403;
        limit_req_log_level warn;
    }

    error_log /var/log/nginx/rate-error.log warn;
}
```

### Additional Options:

* `limit_req_status` → Status code returned when requests are rejected (e.g., 403)
* `limit_req_log_level` → Logging level for rate-limit warnings (requires `error_log` configured)

---

## Whitelist Specific IPs

```nginx
geo $limit {
    default 1;
    10.0.0.0/8 0;
    192.168.0.0/24 0;
    93.127.222.112/32 0;
}

map $limit $limit_key {
    0 "";
    1 $binary_remote_addr;
}

limit_req_zone $limit_key zone=mylimit:10m rate=2r/s;

server {
    server_name files.usethelinux.shop;
    root /srv/files;

    location / {
        autoindex on;
        limit_req zone=mylimit burst=3 delay=1;
        limit_req_status 403;
        limit_req_log_level warn;
    }

    error_log /var/log/nginx/rate-error.log warn;
}
```

### Explanation:

* `geo` → Defines a variable with default `1` (all clients)
* `map` → Applies `limit_req_zone` only to non-whitelisted IPs
* Whitelisted IPs (value `0`) are not limited, others follow rate limits

---

## Summary

* **`limit_req_zone`** → Defines the rate-limiting key and storage
* **`limit_req`** → Applies the rate limit to a location
* **Burst & Delay** → Control traffic spikes smoothly
* **Whitelist** → Exclude trusted IPs from rate limiting
* **Logging & Status** → Monitor and handle rejected requests efficiently


