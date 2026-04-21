# BIND9 Zone File and SOA Configuration Guide

## 1. What is a Zone File

A **zone file** defines DNS records for a specific domain. It maps domain names to IP addresses and other resources.

In this example, we are configuring a zone for:

```
test.com
```

---

## 2. SOA (Start of Authority) Record

### Example

```conf id="soa-example"
$TTL 120

@ IN SOA test.com. admin.test.com ( 
    1;
    86400;
    7200;
    57600;
    3600);
```

### Explanation

#### `$TTL 120`

* Default Time To Live for all records in this zone.
* Value is in seconds (120 seconds = 2 minutes).
* Controls how long DNS responses are cached.

---

### SOA Record Structure

```
@ IN SOA <primary-ns> <admin-email> (
    <serial>
    <refresh>
    <retry>
    <expire>
    <minimum>
)
```

#### Fields Breakdown

* `@`

  * Refers to the root of the zone (`test.com`).

* `IN`

  * Internet class (standard for DNS).

* `SOA`

  * Start of Authority record. Defines the authoritative source for the zone.

---

### SOA Parameters

* **Primary Nameserver**

  ```
  test.com.
  ```

  * The authoritative DNS server for this zone.
  * Must be a fully qualified domain name (FQDN).

* **Admin Email**

  ```
  admin.test.com
  ```

  * Represents `admin@test.com`.
  * The `@` is replaced with a dot in DNS format.

---

### Timing Parameters

* **Serial**

  ```
  1;
  ```

  * Version number of the zone.
  * Must be incremented on every change.
  * Secondary DNS servers use this to detect updates.

* **Refresh (86400 seconds = 24 hours)**

  * How often secondary servers check for updates.

* **Retry (7200 seconds = 2 hours)**

  * Retry interval if refresh fails.

* **Expire (57600 seconds = 16 hours)**

  * Time after which secondary servers discard the zone if they cannot reach the primary.

* **Minimum TTL (3600 seconds = 1 hour)**

  * Default negative caching time (NXDOMAIN responses).

---

## 3. DNS Records in the Zone

### Example Zone File

```conf id="zone-file"
@ IN NS test.com. 

@ IN A 10.10.30.1

www IN CNAME docs.test.com
docs IN A 10.10.20.1
```

---

### NS Record

```conf id="ns-record"
@ IN NS test.com.
```

* Defines the authoritative nameserver for the domain.
* `test.com.` must resolve to an IP (via an A record).

---

### A Record

```conf id="a-record-root"
@ IN A 10.10.30.1
```

* Maps `test.com` → `10.10.30.1`.

---

### CNAME Record

```conf id="cname-record"
www IN CNAME docs.test.com
```

* `www.test.com` becomes an alias of `docs.test.com`.
* DNS queries for `www` will resolve to the IP of `docs`.

---

### Additional A Record

```conf id="a-record-docs"
docs IN A 10.10.20.1
```

* Maps `docs.test.com` → `10.10.20.1`.

---

## 4. The Trailing Dot in DNS

### Example

```
test.com.
```

### Explanation

* The trailing dot (`.`) indicates a **fully qualified domain name (FQDN)**.
* Without the dot, BIND appends the current zone name.

#### Example Behavior

* `docs.test.com` (no dot)
  → interpreted as `docs.test.com.test.com`

* `docs.test.com.` (with dot)
  → interpreted correctly as `docs.test.com`

**Rule:**

* Always use a trailing dot for absolute domain names in zone files.

---

## 5. Zone Configuration in BIND

### File: `/etc/bind/named.conf.local`

```conf id="named-conf-local"
zone 'test.com' IN {
    type master;
    file "/etc/bind/zones/test.com.zone";
};
```

### Explanation

* `zone 'test.com'`

  * Declares the domain being managed.

* `type master`

  * This server is the authoritative source for the zone.

* `file`

  * Path to the zone file.

---

## 6. Validating the Zone File

```bash id="check-zone"
named-checkzone test.com /etc/bind/zones/test.com.zone
```

### Purpose

* Validates syntax and logic of the zone file.
* Detects:

  * Missing dots
  * Invalid records
  * Formatting errors

---

## 7. Applying Configuration Changes

### Reconfigure BIND

```bash id="rndc-reconfig"
rndc reconfig
```

* Reloads BIND configuration files.
* Detects new or modified zones.

---

### Reload Specific Zone

```bash id="rndc-reload"
rndc reload test.com
```

* Reloads only the `test.com` zone.
* Faster and more efficient than restarting the entire service.

---

## 8. Key Operational Notes

* Always increment the **serial number** after modifying the zone.
* Use `named-checkzone` before applying changes.
* Prefer `rndc reload` over full service restart for production systems.
* Ensure proper file permissions for `/etc/bind/zones/`.

---

## 9. Summary

This setup defines:

* A **master DNS zone** for `test.com`
* Authoritative records:

  * Root domain (`test.com`)
  * `docs.test.com`
  * Alias `www.test.com`
* Proper SOA configuration for synchronization
* DNS validation and reload workflow using BIND tools

