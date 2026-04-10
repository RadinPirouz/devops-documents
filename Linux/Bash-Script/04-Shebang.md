
# 🌟 Understanding the **Shebang** (`#!`)

A **shebang** (also known as a **hashbang**) is the character sequence:

```
#!<interpreter_path>
```

It appears **at the very top** of a script file and tells the operating system **which interpreter** should execute the file.

---

## 📌 What It Looks Like

```bash
#!/usr/bin/python3
print("Hello, world!")
```

### Breakdown:

* `#!` — This is the **shebang**.
* `/usr/bin/python3` — This tells the OS to use **Python 3** to run the script.

---

## 🧠 Why It Matters

When you make a script **executable**:

```bash
chmod +x script.py
```

And run it directly:

```bash
./script.py
```

The OS reads the **shebang line** and uses the specified interpreter to execute the file. This works for any script type, like:

```bash
./script.sh   # for a Bash script
./script.py   # for a Python script
```

---

## 💡 Common Shebang Examples

| Language | Shebang               |
| -------- | --------------------- |
| Bash     | `#!/bin/bash`         |
| Python   | `#!/usr/bin/python3`  |
| Node.js  | `#!/usr/bin/env node` |
| Perl     | `#!/usr/bin/perl`     |

---

## 🚀 Pro Tip: Use `env` for Portability

Instead of hardcoding the interpreter path, use:

```bash
#!/usr/bin/env python3
```

This makes your script more **portable**, as it locates `python3` using the user's `PATH` environment.

---

## ✅ Summary

* The **shebang** defines the script interpreter.
* Place it on **the first line** of your script.
* Make the script executable with `chmod +x`.
* Use `/usr/bin/env` for better portability across systems.

