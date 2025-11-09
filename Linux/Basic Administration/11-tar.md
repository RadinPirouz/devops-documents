# Linux Compression & Archiving Cheatsheet

## Tar Command Basics

The `tar` command is used to create, extract, and manage archive files.

**Syntax:**

```bash
tar [options] [archive_name.tar] [file(s)/directory]
```

---

### Create a `.tar` Archive

```bash
tar -cf archive_file.tar file1 file2 dir1
```

**Options:**

* `-c`: Create a new archive
* `-f`: Specify the archive file name

### Create with Verbose Output

```bash
tar -cvf archive_file.tar file1 file2 dir1
```

* `-v`: Verbose mode (shows progress)

### Extract a `.tar` Archive

```bash
tar -xf archive_file.tar
```

or

```bash
tar -xvf archive_file.tar
```

* `-x`: Extract files

---

## Gzip Compression

**Gzip** (GNU zip) is a fast and widely used compression tool.

### Create a `.tar.gz` Archive

```bash
tar -czf archive_file.tar.gz file1 file2 dir1
```

* `-z`: Compress using gzip

### Verbose Creation

```bash
tar -czvf archive_file.tar.gz file1 file2 dir1
```

### Extract `.tar.gz`

```bash
tar -xzf archive_file.tar.gz
```

or

```bash
tar -xzvf archive_file.tar.gz
```

---

## Bzip2 Compression

**Bzip2** provides better compression than gzip but at the cost of speed.

### Create a `.tar.bz2` Archive

```bash
tar -cjf archive_file.tar.bz2 file1 file2 dir1
```

* `-j`: Compress using bzip2

### Verbose Creation

```bash
tar -cjvf archive_file.tar.bz2 file1 file2 dir1
```

### Extract `.tar.bz2`

```bash
tar -xjf archive_file.tar.bz2
```

or

```bash
tar -xjvf archive_file.tar.bz2
```

---

## XZ Compression

**XZ** offers the best compression ratio but is the slowest option.

### Create a `.tar.xz` Archive

```bash
tar -cJf archive_file.tar.xz file1 file2 dir1
```

* `-J`: Compress using xz

### Verbose Creation

```bash
tar -cJvf archive_file.tar.xz file1 file2 dir1
```

### Extract `.tar.xz`

```bash
tar -xJf archive_file.tar.xz
```

or

```bash
tar -xJvf archive_file.tar.xz
```

---

## Compression Format Comparison

| Feature             | gzip        | bzip2      | xz        |
| ------------------- | ----------- | ---------- | --------- |
| Compression Speed   | Fast        | Slow       | Slowest   |
| Decompression Speed | Fast        | Slower     | Moderate  |
| Compression Ratio   | Good        | Better     | Best      |
| File Extension      | `.tar.gz`   | `.tar.bz2` | `.tar.xz` |
| Common Use          | General/Web | Backups    | Archival  |

