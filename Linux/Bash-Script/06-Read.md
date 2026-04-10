# 📝 Bash `read` Command

The `read` command in **Bash** is used to **take user input** from the terminal. It stores the input into one or more **variables**.

---

## 🔤 Basic Syntax

```bash
read [options] variable
```

---

## 📘 Simple Example

```bash
echo "What is your name?"
read name
echo "Hello, $name!"
```

* `read name` takes input from the user and stores it in the variable `name`.
* The script then greets the user with the stored input.

---

## 🎯 Prompt Inline with `-p`

```bash
read -p "What is your name? " name
echo "Hello, $name!"
```

* `-p` allows you to show the prompt **on the same line** as the user input.

---

## 🔒 Silent Input with `-s` (e.g., Passwords)

```bash
read -sp "Enter your password: " password
echo $password >> pass.txt
```

* `-s` hides the user’s input while typing (useful for passwords).
* `>> pass.txt` appends the password to a file (⚠️ For demonstration only—**avoid storing passwords in plain text**!).

---

## ⏳ Set a Timeout with `-t`

```bash
read -t 5 -p "Enter something in 5 seconds: " data
```

* `-t 5` gives the user **5 seconds** to input something.
* If no input is given in time, the script moves on.

---

## 🧠 Summary Table

| Option | Description           | Example                      |
| ------ | --------------------- | ---------------------------- |
| `-p`   | Show prompt inline    | `read -p "Name: " name`      |
| `-s`   | Silent (hidden input) | `read -sp "Password: " pass` |
| `-t`   | Timeout (in seconds)  | `read -t 10 var`             |

---

## ✅ Quick Recap

* Use `read` to get **interactive input** in your Bash scripts.
* Combine options (`-sp`, `-tp`, etc.) for powerful input control.
* Avoid exposing sensitive data—use secure handling practices.

