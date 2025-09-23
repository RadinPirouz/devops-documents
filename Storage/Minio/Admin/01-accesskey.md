# MinIO Admin: Access Key Management (`mc admin accesskey`)

The **`mc admin accesskey`** command set is used to manage users and access keys on a MinIO server.

---

## Listing Access Keys

* **List all access keys:**

```bash
mc admin accesskey ls
```

* **List access keys for a specific user:**

```bash
mc admin accesskey ls <user>
```

---

## Creating Access Keys

* **Create a new access key with default settings:**

```bash
mc admin accesskey create <mc-server>
```

* **Create a new access key with custom access and secret keys:**

```bash
mc admin accesskey create <mc-server> --access-key <custom-access> --secret-key <custom-secret>
```

* **Create a user with temporary expiry duration (e.g., 24 hours):**

```bash
mc admin accesskey create <mc-server> miniouser --expiry-duration 24h
```

* **Create a user with a specific expiry date:**

```bash
mc admin accesskey create <mc-server> --expiry 2026-01-15
```

* **Create a user with expiry date and custom policy:**

```bash
mc admin accesskey create <mc-server> --expiry 2026-01-15 --policy /path/to/policy.json
```

---

## Enabling and Disabling Access Keys

* **Disable an access key:**

```bash
mc admin accesskey disable <mc-server> <access-key>
```

* **Enable a disabled access key:**

```bash
mc admin accesskey enable <mc-server> <access-key>
```

---

## Access Key Information

* **Get detailed info about an access key:**

```bash
mc admin accesskey info <mc-server> <access-key>
```

---

## Removing Access Keys

* **Remove an access key:**

```bash
mc admin accesskey rm <mc-server> <access-key>
```

