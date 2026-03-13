# diff Command Reference

The `diff` command is a standard Unix/Linux utility used to compare files line by line. It is commonly used in development, DevOps, and system administration to identify changes between configuration files, source code, logs, or generated outputs.

---

## 1. Basic File Comparison

Compare two files line by line:

```bash
diff file1 file2
```

### Output Behavior

* Shows only the lines that differ
* Uses symbols to indicate changes:

  * `<` line from `file1`
  * `>` line from `file2`
  * `c` change
  * `a` addition
  * `d` deletion

---

## 2. Side-by-Side Comparison

Display files next to each other:

```bash
diff -y file1 file2
```

### Notes

* Useful for human-readable comparison
* Differences are shown in two columns
* Change indicators appear in the middle

Limit output width:

```bash
diff -y --width=120 file1 file2
```

Suppress common lines:

```bash
diff -y --suppress-common-lines file1 file2
```

---

## 3. Unified Diff Format (Most Common)

Generate a unified diff:

```bash
diff -u file1 file2
```

### Why Unified Diff

* Standard format used by Git, patch, and code reviews
* Shows context before and after changes
* Easier to read and apply

Example output markers:

* `+` added lines
* `-` removed lines
* `@@` line numbers and context

---

## 4. Save Diff Output to a File

Redirect diff output to a file:

```bash
diff -u file1 file2 > different.diff
```

Common use cases:

* Code reviews
* Patch creation
* Change tracking
* CI/CD artifact storage

---

## 5. Recursive Directory Comparison

Compare directories:

```bash
diff -r dir1 dir2
```

Unified recursive diff:

```bash
diff -ru dir1 dir2
```

Ignore missing files:

```bash
diff -rq dir1 dir2
```

---

## 6. Ignore Differences

Ignore whitespace:

```bash
diff -w file1 file2
```

Ignore blank lines:

```bash
diff -B file1 file2
```

Ignore case differences:

```bash
diff -i file1 file2
```

---

## 7. Apply a Diff as a Patch

Create a patch:

```bash
diff -u oldfile newfile > change.patch
```

Apply patch:

```bash
patch < change.patch
```

Dry-run patch:

```bash
patch --dry-run < change.patch
```

---

## 8. diff vs Git diff

| diff                 | git diff                        |
| -------------------- | ------------------------------- |
| Compares any files   | Compares Git-tracked files      |
| Works without Git    | Requires Git repository         |
| Produces patch files | Integrated with version control |

---

## 9. Best Practices

* Use `-u` format for readability and compatibility
* Store diff files with `.diff` or `.patch` extensions
* Avoid committing generated diff files unless required
* Use `diff` for system configuration audits
* Use `git diff` inside Git repositories

---

## 10. Quick Reference

```bash
diff file1 file2
diff -y file1 file2
diff -u file1 file2
diff -ru dir1 dir2
diff -u file1 file2 > change.diff
```

