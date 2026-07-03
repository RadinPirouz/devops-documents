
The **MinIO Client (`mc`)** provides a modern alternative to UNIX commands for interacting with S3-compatible object storage.
This guide summarizes commonly used commands.

---

## Aliases (`mc alias`)

Aliases are used to manage S3 server connections.

* **List all aliases:**

```bash
mc alias ls
```

* **List a specific alias:**

```bash
mc alias ls <mc-server>
```

* **Remove an alias:**

```bash
mc alias rm <mc-server>
```

* **Set a new alias:**

```bash
mc alias set <object-storage-name> <url> <access-key> <secret-key> --api <s3-version>
```

* **Export alias to JSON:**

```bash
mc alias export <mc-server> | tee object-st.json
```

* **Import alias from JSON:**

```bash
mc alias import <object-storage-name> <json-file>
```

---

## Listing Objects (`mc ls`)

* **List bucket contents:**

```bash
mc ls <mc-server>/<bucket>/<dir>/
```

* **List with versions:**

```bash
mc ls --versions <mc-server>/<bucket>/<dir>/
```

---

## Copying Files (`mc cp`)

* **Upload file to bucket:**

```bash
mc cp <file-onlocal> <mc-server>/<bucket>/<dir>/
```

* **Download file from bucket:**

```bash
mc cp <mc-server>/<bucket>/<dir> <file-onlocal>
```

* **Download specific version:**

```bash
mc cp --version-id <version-uuid> <mc-server>/<bucket>/<dir> <file-onlocal>
```

---

## Viewing Files (`mc cat`)

* **View file contents:**

```bash
mc cat <mc-server>/<bucket>/<dir>
```

---

## Moving Files (`mc mv`)

* **Move from local to bucket:**

```bash
mc mv <file-onlocal> <mc-server>/<bucket>/<dir>/
```

* **Move specific version from bucket:**

```bash
mc mv --version-id <version-uuid> <mc-server>/<bucket>/<dir> <file-onlocal>
```

---

## Removing Files (`mc rm`)

* **Remove file:**

```bash
mc rm <mc-server>/<bucket>/<dir>/file
```

* **Force remove specific version:**

```bash
mc rm --force --version-id <version-uuid> <mc-server>/<bucket>/<dir>/file
```

---

## Creating Buckets (`mc mb`)

* **Create a bucket:**

```bash
mc mb <mc-server>/<bucket-name>
```

* **Create a bucket with versioning:**

```bash
mc mb --with-versioning <mc-server>/<bucket-name>
```

* **Create a bucket with object lock:**

```bash
mc mb --with-lock <mc-server>/<bucket-name>
```

---

## Removing Buckets (`mc rb`)

* **Remove a bucket:**

```bash
mc rb <mc-server>/<bucket-name>
```

* **Force remove a bucket:**

```bash
mc rb --force <mc-server>/<bucket-name>
```

---

## Health Check (`mc ping`)

* **Ping a server:**

```bash
mc ping <mc-server> --count <count-of-ping>
```

---

## Tree View (`mc tree`)

* **Display bucket tree structure:**

```bash
mc tree <mc-server>/<bucket>
```

