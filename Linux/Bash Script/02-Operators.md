# 🖥️ Bash Operators

A quick reference guide to essential bash command operators and their usage.

---

## `>` — **Write to File (Overwrite)**

This operator **creates a new file** or **overwrites** the contents of an existing file.

```bash
echo "Hi" > file1
```

📄 *Creates* `file1` and writes `"Hi"` into it. If `file1` already exists, its content is replaced.

---

## `>>` — **Append to File**

Adds content to the **end of an existing file** without deleting what's already there.

```bash
echo "Hi" >> file1
```

📝 *Appends* `"Hi"` to the end of `file1`.

---

## `&&` — **AND Operator**

Runs the **second command only if the first succeeds**.

```bash
apt update && apt upgrade
```

🔗 `apt upgrade` runs only if `apt update` completes successfully.

---

## `;` — **Run Multiple Commands**

Executes **commands sequentially**, regardless of success or failure.

```bash
echo "Hi" > file1 ; cat file1
```

🔄 Both commands are executed one after the other.

---

## `|` — **Pipe Operator**

Takes the **output of the command on the left** and **uses it as input for the command on the right**.

```bash
ls -l | grep "txt"
```

🔗 Passes the output of `ls -l` to `grep "txt"` to filter and display only files containing "txt".

---

## `*` — **Wildcard (All Matching Files)**

Matches **all files** that meet the pattern.

```bash
cat file*
```

🌐 Displays the contents of all files starting with `file`.

---

## `[ ... ]` — **Specific Character Matching**

Reads files that match specific characters at the position defined in brackets.

```bash
cat file[1,2,3]
```

📚 Reads `file1`, `file2`, and `file3` (if they exist). Equivalent to:

```bash
cat file1 file2 file3
```
