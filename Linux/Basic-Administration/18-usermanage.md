# 🧑‍💻 Linux User & Group Management Cheat Sheet

---

## 🔍 Viewing User Info from `/etc/shadow`

```bash
cat /etc/shadow
```

Example entry:

```bash
radin:$y$j9T$gxn.Bgl/nVnzPEeWn0Hrz.$CEeQGtg1TlZ/jwu9Zsz2kkIq3dBtbhJ/bzhVT7cJ1.9:20270:0:99999:7:::
```

| Field             | Description                                  | Example                                         |
| ----------------- | -------------------------------------------- | ----------------------------------------------- |
| 👤 Username       | User’s login name                            | `radin`                                         |
| 🔒 Password Hash  | Encrypted password                           | `$y$j9T$gxn.Bgl/nVnzPEeWn0Hrz.$CEeQGtg1TlZ/...` |
| 🗓️ Last Changed  | Days since Jan 1, 1970 when password changed | `20270` (which is 20270 + 1970 = year)          |
| ⏳ Min Age         | Minimum days between password changes        | `0`                                             |
| ⏰ Max Age         | Maximum days before password must be changed | `99999`                                         |
| ⚠️ Warning Period | Days before expiration user is warned        | `7`                                             |

---

## 🛡️ Viewing Groups from `/etc/group`

```bash
cat /etc/group
```

Example:

```bash
radin:x:1000:
sudo:x:27:radin
```

| Field         | Description                          | Example         |
| ------------- | ------------------------------------ | --------------- |
| 👥 Group Name | Name of the group                    | `radin`, `sudo` |
| 🔑 Password   | Password (usually `x` means none)    | `x`             |
| 🆔 GID        | Group ID                             | `1000`, `27`    |
| 👤 Users      | Users in the group (comma-separated) | `radin`         |

---

## 👥 Check Groups for a User

```bash
groups <username>
```

---

## 🆔 View User and Group IDs

```bash
id <username>
```

Example output:

```bash
uid=1000(radin) gid=1000(radin) groups=1000(radin),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),100(users),114(lpadmin)
```

---

## ➕ Adding Users

| Command                                | Description                               |
| -------------------------------------- | ----------------------------------------- |
| `useradd <username>`                   | Add user without home directory           |
| `useradd -m <username>`                | Add user **with** home directory          |
| `useradd -s /bin/bash -m <username>`   | Add user with bash shell & home directory |
| `useradd -G group1,root -m <username>` | Add user with home and extra groups       |

---

## 🔑 Changing Password

```bash
passwd <username>
```

---

## ❌ Deleting Users

| Command                 | Description                          |
| ----------------------- | ------------------------------------ |
| `userdel <username>`    | Delete user                          |
| `userdel -r <username>` | Delete user and their home directory |
| `userdel -f <username>` | Force delete user                    |

---

## 🔧 Modifying Users (`usermod`)

| Command                                  | Description                               |
| ---------------------------------------- | ----------------------------------------- |
| `usermod [options] username`             | Modify user with various options          |
| `usermod -l <newusername> <oldusername>` | Rename user                               |
| `usermod -d <dir> -m <username>`         | Change user home directory and move files |
| `usermod -G <groups> <username>`         | Set new groups (replaces old groups)      |
| `usermod -aG <group> <username>`         | Add user to a supplementary group         |
| `usermod -s <shell> <username>`          | Change user login shell                   |

