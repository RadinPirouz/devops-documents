# 🧮 Bash Variables

In **Bash scripting**, **variables** are used to store values like text or numbers. They allow scripts to be dynamic and reusable.

---

## ✍️ Defining Variables

Variables are created **without spaces** around the `=` sign:

```bash
user="ali"
age=21
```

* `user` is assigned the value `"ali"`.
* `age` is assigned the value `21`.

> ✅ Tip: No `let` or `var` is needed like in other programming languages.

---

## 📢 Using Variables

You can **access variables** by prefixing them with `$`:

```bash
user="radin"
echo "Welcome, $user"
```

**Output:**

```
Welcome, radin
```

---

## 🧪 Full Script Example

Here's a complete Bash script using variables:

```bash
#!/bin/bash

user="mmd"
age=25

echo "$user is $age years old."
```

**Output:**

```
mmd is 25 years old.
```

---

## 📌 Notes

* Variable names are **case-sensitive** (`User` and `user` are different).
* Avoid spaces around `=` when assigning.
* Enclose variable values in quotes if they contain spaces.

---

## ✅ Summary

| Task            | Syntax                       |
| --------------- | ---------------------------- |
| Define variable | `name="value"`               |
| Use variable    | `$name`                      |
| Print value     | `echo "$name"`               |
| With script     | Use `#!/bin/bash` at the top |

