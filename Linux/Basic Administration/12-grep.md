# 📘 **Using `grep` in Linux/Unix**

`grep` (Global Regular Expression Print) is a powerful command-line utility used to search for text patterns in files. Below are common variations of the `grep` command with examples and explanations.

---

## 🔍 Basic Search

```bash
grep "hello" file1
```

**Description**:
Searches for lines containing the word `hello` in `file1`. The search is **case-sensitive**.

---

## 🔍 Case-Insensitive Search

```bash
grep -i "hello" file1
```

**Description**:
Performs a **case-insensitive** search for `hello` in `file1`. Matches `hello`, `Hello`, `HELLO`, etc.

---

## 🔢 Show Line Numbers

```bash
grep -n "hello" file1
```

**Description**:
Displays matching lines **with their line numbers**.

---

## 🔢 Case-Insensitive with Line Numbers

```bash
grep -in "hello" file1
```

**Description**:
Combines `-i` and `-n` to show line numbers and ignore case.

---

## 🚫 Invert Match

```bash
grep -v "hello" file1
```

**Description**:
Shows lines that **do NOT** contain the word `hello`.

---

## 🚫 Invert, Ignore Case, and Show Line Numbers

```bash
grep -ivn "hello" file1
```

**Description**:
Combines all the above:

* `-i`: Ignore case
* `-v`: Invert match
* `-n`: Show line numbers
  Shows all lines that **don’t contain** `hello`, regardless of case, and includes line numbers.

---

## ✅ Summary of Flags

| Flag | Description                |
| ---- | -------------------------- |
| `-i` | Ignore case                |
| `-n` | Show line numbers          |
| `-v` | Invert the match (exclude) |

