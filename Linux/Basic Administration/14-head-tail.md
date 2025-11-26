# 📘 **Using `head` and `tail` Commands in Linux/Unix**

Both `head` and `tail` are essential commands for viewing specific portions of a file quickly, without opening the entire file.

---

## 🔝 `head` — Show the Top of a File

The `head` command displays the beginning part of a file.

### Syntax

```bash
head [options] file
```

### Examples

```bash
head file1
```

**Description**:
Displays the first 10 lines of `file1` (default behavior).

```bash
head -n 5 file1
```

**Description**:
Shows the first 5 lines of `file1`.

---

## 🔚 `tail` — Show the Bottom of a File

The `tail` command displays the end part of a file.

### Syntax

```bash
tail [options] file
```

### Examples

```bash
tail file1
```

**Description**:
Displays the last 10 lines of `file1` (default behavior).

```bash
tail -n 20 file1
```

**Description**:
Shows the last 20 lines of `file1`.

```bash
tail -f file1
```

**Description**:
Follows the file as it grows — useful for watching logs in real-time.

---

## ✅ Summary of Options

| Command | Option        | Description                                 |
| ------- | ------------- | ------------------------------------------- |
| `head`  | `-n <number>` | Show the first `<number>` lines             |
| `tail`  | `-n <number>` | Show the last `<number>` lines              |
| `tail`  | `-f`          | Follow the file in real-time (live updates) |

