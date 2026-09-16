# MariaDB Docker Healthcheck — Access Denied

When a MariaDB container reports `unhealthy` with:

```text
Access denied for user 'healthcheck'
```

this is almost always a **healthcheck credential mismatch**, not an application-user problem.

The official MariaDB image creates these accounts automatically:

```text
healthcheck@localhost
healthcheck@127.0.0.1
healthcheck@::1
```

It generates a random password and stores it in:

```text
/var/lib/mysql/.my-healthcheck.cnf
```

With `MARIADB_AUTO_UPGRADE=1`, MariaDB can recreate the healthcheck users and regenerate `.my-healthcheck.cnf` when that file is missing.

---

## 1. Confirm the container is unhealthy

Replace `mariadb` with your container name.

```bash
docker ps
docker inspect --format='{{json .State.Health}}' mariadb | jq
```

Run the healthcheck manually:

```bash
docker exec mariadb healthcheck.sh --connect --innodb_initialized
echo $?
```

`Access denied for user 'healthcheck'` confirms this issue.

---

## 2. Check the healthcheck credentials file

```bash
docker exec mariadb sh -c '
if [ -f /var/lib/mysql/.my-healthcheck.cnf ]; then
    echo "healthcheck config exists"
    ls -l /var/lib/mysql/.my-healthcheck.cnf
else
    echo "healthcheck config MISSING"
fi
'
```

Do not print or share the file contents — it holds the generated healthcheck password.

---

## 3. Fix

### Compose configuration

```yaml
services:
  mariadb:
    image: mariadb:lts

    environment:
      MARIADB_ROOT_PASSWORD: ${MARIADB_ROOT_PASSWORD}
      MARIADB_AUTO_UPGRADE: "1"

    healthcheck:
      test:
        - CMD
        - healthcheck.sh
        - --connect
        - --innodb_initialized
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
```

`healthcheck.sh --connect --innodb_initialized` is the pattern documented for the official MariaDB Docker image.

### Regenerate healthcheck credentials

Rename the existing config so MariaDB recreates it:

```bash
docker exec mariadb \
  mv /var/lib/mysql/.my-healthcheck.cnf \
     /var/lib/mysql/.my-healthcheck.cnf.old
```

Recreate the container (**do not** remove the data volume):

```bash
docker compose up -d --force-recreate mariadb
```

Avoid:

```bash
docker compose down -v
```

`-v` can delete the MariaDB volume and your data.

---

## 4. Verify

```bash
docker logs -f mariadb
```

Look for healthcheck-user creation during startup, then:

```bash
docker exec mariadb healthcheck.sh --connect --innodb_initialized
echo $?
```

Expected exit code: `0`.

```bash
docker ps
```

should show:

```text
Up ... (healthy)
```

---

## Why this happens

```text
Old MariaDB container
       │
       ▼
existing /var/lib/mysql volume
       │
       ├── healthcheck DB users
       └── .my-healthcheck.cnf
                 │
                 ▼
        container/image updated
                 │
                 ▼
user password ≠ config password
                 │
                 ▼
Access denied for healthcheck
```

Common triggers:

- MariaDB image upgrade
- Restored or copied data directory
- Reused Docker volume across containers

Most initialization environment variables do **not** change an already-initialized datadir. `MARIADB_AUTO_UPGRADE` is an important exception.

---

## References

- [Using Healthcheck.sh](https://mariadb.com/docs/server/server-management/automated-mariadb-deployment-and-administration/docker-and-mariadb/using-healthcheck-sh)
- [MariaDB Docker environment variables](https://mariadb.com/docs/server/server-management/install-and-upgrade-mariadb/installing-mariadb/binary-packages/automated-mariadb-deployment-and-administration/docker-and-mariadb/mariadb-server-docker-official-image-environment-variables)
