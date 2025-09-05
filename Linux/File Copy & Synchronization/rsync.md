# 🔄 Rsync

`rsync` is a powerful command-line tool for syncing files and directories between systems over SSH.
Here are some useful commands 👇

---

## 📌 Basic Syntax

```bash
rsync [options] <file_or_dir> <user>@<host>:<target-dir>
```

or

```bash
rsync [options] <user>@<host>:<source-dir_or_file> <target-dir>
```

---

## 📥 Copy from Local ➝ Remote

```bash
rsync file1.txt radin@192.168.1.10:/home/radin
```

Verbose mode (shows details):

```bash
rsync -v file1.txt radin@192.168.1.10:/home/radin
```

---

## 📤 Copy from Remote ➝ Local

```bash
rsync -v radin@192.168.1.10:/home/radin/file1.txt /opt
```

---

## 📦 Archiving

Archive mode (preserves permissions, symlinks, etc.):

```bash
rsync -va file1.txt radin@192.168.1.10:/home/radin
```

Archive + compress (gzip):

```bash
rsync -vaz file1.txt radin@192.168.1.10:/home/radin
```

With progress bar:

```bash
rsync -vaz --progress file1.txt radin@192.168.1.10:/home/radin
```

---

## 🔐 Custom SSH Port

```bash
rsync -e 'ssh -p 8090' -vaz file1.txt radin@192.168.1.10:/home/radin
```

---

## 🗑️ Sync with Delete (mirror directories)

Deletes files on destination that don’t exist on source:

```bash
rsync -vaz --delete dir_test/ radin@192.168.1.10:/home/radin
```

---

## 🚫 Excluding Files

Exclude `.img` files:

```bash
rsync -va dir_test/ --exclude '*.img' radin@192.168.1.10:/home/radin
```

---

## ⚡ Bandwidth Control

Limit transfer speed (in KB/s):

```bash
rsync -v --bwlimit=2048 file1.txt radin@192.168.1.10:/home/radin
```

---

## 🧹 Move Instead of Copy

Remove source file after transfer:

```bash
rsync -v --remove-source-file file1.txt radin@192.168.1.10:/home/radin
```

---

## ⛔ Ignore Existing Files

Skip already existing files:

```bash
rsync -v --ignore-existing file1.txt radin@192.168.1.10:/home/radin
```

---

## 🧹⛔ Combine Options

Remove source + ignore existing:

```bash
rsync -v --remove-source-file --ignore-existing file1.txt radin@192.168.1.10:/home/radin
```

