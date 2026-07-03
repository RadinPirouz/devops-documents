# MinIO Admin: User Management (`mc admin user`)

The **`mc admin user`** command set is used to manage users on a MinIO server.

---

## Listing Users

* **List all users on a server:**

```bash
mc admin user ls <mc-server>
```

* **Get detailed info about a specific user:**

```bash
mc admin user info <mc-server> <user>
```

---

## Adding Users

* **Add a new user with a secret key:**

```bash
mc admin user add <mc-server> <newuser> <newusersecret>
```

---

## Removing Users

* **Remove an existing user:**

```bash
mc admin user rm <mc-server> <user>
```

---

## Enabling and Disabling Users

* **Disable a user:**

```bash
mc admin user disable <mc-server> <user>
```

* **Enable a previously disabled user:**

```bash
mc admin user enable <mc-server> <user>
```
