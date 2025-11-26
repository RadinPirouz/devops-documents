# 🧾 Linux Exit Codes Cheat Sheet

Every command in Linux returns an **exit status code** upon completion. You can check this code using:

```bash
command
echo $?
```

These codes are helpful for debugging scripts or understanding command behavior.

---

## ✅ Common Exit Codes & Their Meanings

| Exit Code | Meaning                                         |
| --------- | ----------------------------------------------- |
| `0`       | ✅ Success                                       |
| `1`       | ❌ General Error                                 |
| `2`       | ⚠️ Misuse of Shell Built-in (bad options, etc.) |
| `126`     | 🚫 Command Found but Cannot Execute             |
| `127`     | ❓ Command Not Found                             |
| `130`     | ⌨️ Terminated by `Ctrl+C`                       |
| `137`     | 💀 Killed (e.g., `kill -9`)                     |

---

## 🔍 Exit Code Examples

### `0` — Success

```bash
echo "Hello"
echo $?    # ➜ 0
```

---

### `1` — General Error

```bash
grep "text" non_existing_file.txt
echo $?    # ➜ 1
```

---

### `2` — Misuse of Shell Built-in

```bash
ls --wrongoption
echo $?    # ➜ 2
```

---

### `126` — Command Found but Not Executable

```bash
touch myscript.sh
chmod -x myscript.sh
./myscript.sh
echo $?    # ➜ 126
```

---

### `127` — Command Not Found

```bash
nonexistentcommand
echo $?    # ➜ 127
```

---

### `130` — Script Terminated by `Ctrl+C`

```bash
sleep 10
# Press Ctrl+C while it sleeps
echo $?    # ➜ 130
```

---

### `137` — Killed by `kill -9`

```bash
sleep 100 &
kill -9 $!
wait
echo $?    # ➜ 137
```

