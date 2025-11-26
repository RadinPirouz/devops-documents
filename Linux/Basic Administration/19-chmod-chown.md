# 📁 Linux File Permissions: A Quick & Clear Guide

---

## 🔍 Example: Output of `ls -lh`

Run this command in your terminal:

```bash
ls -lh
```

Example output:

```bash
drwxr-xr-x 3 root root 4.0K Jul  1 22:22 dir1
-rw-r--r-- 1 root root 2.0G Jul  1 21:59 test2.tar
```

---

## 🧠 Understanding the Output Columns

| Column               | Description                             |
| -------------------- | --------------------------------------- |
| `d` / `-`            | File type (`d` = directory, `-` = file) |
| `rwxr-xr-x`          | Permissions (user, group, others)       |
| `3`                  | Number of hard links                    |
| `root`               | Owner (user)                            |
| `root`               | Group                                   |
| `4.0K` / `2.0G`      | File size                               |
| `Jul 1 22:22`        | Last modification date                  |
| `dir1` / `test2.tar` | File or directory name                  |

---

## 🔤 First Character: File Type Indicator

* `d` → Directory 📂
* `-` → Regular file 📄

---

## 🔠 File Permissions Breakdown

```
drwxr-xr-x
│││ │ │ │
│││ │ │ └─ Permissions for Others (o)
│││ │ └── Permissions for Group (g)
│││ └──── Permissions for User (u)
│└──────── File type (d = directory, - = file)
└───────── Read (r), Write (w), Execute (x)
```

---

## 🔐 Permission Symbols Explained

| Symbol | Meaning |
| ------ | ------- |
| `r`    | Read    |
| `w`    | Write   |
| `x`    | Execute |

---

## 👥 Permission Entities

| Symbol | Meaning      |
| ------ | ------------ |
| `u`    | User (owner) |
| `g`    | Group        |
| `o`    | Others       |
| `a`    | All          |

---

## 🔢 Numeric Permission Values (Octal)

| Value | Binary | Permissions | Meaning                |
| ----- | ------ | ----------- | ---------------------- |
| 0     | 000    | ---         | No permissions         |
| 1     | 001    | --x         | Execute only           |
| 2     | 010    | -w-         | Write only             |
| 3     | 011    | -wx         | Write + Execute        |
| 4     | 100    | r--         | Read only              |
| 5     | 101    | r-x         | Read + Execute         |
| 6     | 110    | rw-         | Read + Write           |
| 7     | 111    | rwx         | Read + Write + Execute |

---

## 🛠️ Changing Permissions with `chmod`

### Syntax:

```bash
chmod [permissions] [filename]
```

### Example (numeric):

```bash
chmod 755 myscript.sh
```

### What does `755` mean?

| Entity | Value | Permission                 |
| ------ | ----- | -------------------------- |
| User   | 7     | rwx (read, write, execute) |
| Group  | 5     | r-x (read, execute)        |
| Others | 5     | r-x (read, execute)        |

### Recursive permission change:

```bash
chmod -R <permission> <directory>
```

---

## 👑 Changing Ownership with `chown`

### Syntax:

```bash
chown [options] owner[:group] file
```

### Examples:

Change owner only:

```bash
sudo chown radin file.txt
```

Change owner and group:

```bash
sudo chown radin:dev file.txt
```

Change owner and group recursively (for directories):

```bash
sudo chown -R radin:dev files/
```
