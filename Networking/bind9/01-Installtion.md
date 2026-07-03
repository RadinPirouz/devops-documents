# BIND9 DNS Forwarder Configuration Guide

## 1. Installing BIND9

```bash
sudo apt install bind9
```

### Explanation

BIND9 (Berkeley Internet Name Domain) is one of the most widely used DNS servers. In this setup, it will act as a **DNS forwarder**, meaning it forwards DNS queries to upstream servers instead of resolving them recursively from root servers.

---

## 2. Configuration Overview

The configuration snippet defines how BIND9 behaves as a DNS server. It is typically located in:

```
/etc/bind/named.conf.options
```

---

## 3. Detailed Configuration Breakdown

### Global Options Block

```conf
options {
    directory "/var/cache/bind";
```

* `directory`: Specifies where BIND stores cache and zone files.
* `/var/cache/bind`: Default working directory for cached DNS data.

---

### Forwarders

```conf
    forwarders {
        192.168.1.10;
        8.8.8.8;
        1.1.1.1;
    };
```

* Defines upstream DNS servers to which queries are forwarded.
* `192.168.1.10`: Likely an internal DNS server (e.g., corporate or local network).
* `8.8.8.8`: Public DNS server provided by Google.
* `1.1.1.1`: Public DNS server provided by Cloudflare.

**Behavior:**

* Queries that BIND cannot resolve locally are sent to these servers.

---

### DNSSEC Validation

```conf
    dnssec-validation no;
```

* Disables DNSSEC (DNS Security Extensions) validation.
* DNSSEC ensures DNS responses are authentic and not tampered with.

**Why disable it?**

* Simplicity in lab or internal environments.
* Avoid issues if upstream servers or zones are misconfigured.

**Production note:**

* It is generally recommended to enable DNSSEC in secure environments.

---

### Listening Interfaces

```conf
    #listen-on { any; };
    # listen-on-v6 { any; };

    listen-on port 53 { 127.0.0.1; };
    listen-on-v6 { none; };
```

* `listen-on port 53 { 127.0.0.1; };`

  * BIND listens only on the loopback interface (localhost).
  * This means only the local machine can query this DNS server.

* `listen-on-v6 { none; };`

  * Disables IPv6 listening.

* Commented lines:

  * `#listen-on { any; };` would allow all IPv4 interfaces.
  * `#listen-on-v6 { any; };` would enable IPv6 support.

**Implication:**

* This configuration is suitable for a **local DNS resolver**, not a network-wide DNS server.

---

### Forwarding Mode

```conf
    forward only;
```

* Forces BIND to **only use forwarders**.
* It will not attempt full recursive resolution if forwarders fail.

**Behavior:**

* If all forwarders fail → DNS resolution fails.

---

### Query Access Control

```conf
    allow-query { any; };
```

* Allows any client to query the DNS server.

**Note:**

* Safe here because the server only listens on `127.0.0.1`.

---

### Recursion Settings

```conf
    recursion yes;
    allow-recursion { any; };
```

* `recursion yes;`

  * Enables recursive DNS resolution (required for a caching resolver).

* `allow-recursion { any; };`

  * Allows all clients to use recursion.

**Important:**

* In public-facing servers, unrestricted recursion can lead to abuse (e.g., DNS amplification attacks).
* In this case, it is safe due to localhost restriction.

---

## 4. Summary of Behavior

This configuration sets up BIND9 as:

* A **local DNS forwarder**
* Listening only on **localhost (127.0.0.1)**
* Forwarding queries to:

  * Internal DNS: `192.168.1.10`
  * Public DNS: `8.8.8.8`, `1.1.1.1`
* Performing recursion via forwarders only
* Not using DNSSEC validation
* Not exposed to external clients

---

## 5. Typical Use Cases

* Local development environments
* Caching DNS resolver for a single machine
* Forwarding DNS queries inside containers or VMs
* Acting as a DNS proxy for internal services

---

## 6. Recommendations for Production

* Enable DNSSEC validation:

  ```conf
  dnssec-validation auto;
  ```

* Restrict recursion:

  ```conf
  allow-recursion { trusted_network; };
  ```

* Bind to specific internal interfaces instead of localhost if needed:

  ```conf
  listen-on { 192.168.1.0/24; };
  ```

* Implement logging for observability

---

## 7. Restarting the Service

After making changes:

```bash
sudo systemctl restart bind9
```

To check status:

```bash
sudo systemctl status bind9
```

---

## 8. Testing DNS Resolution

```bash
dig google.com @127.0.0.1
```

* Confirms that the local BIND server is resolving queries correctly via forwarders.

