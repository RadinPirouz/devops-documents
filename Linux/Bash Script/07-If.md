
# 🐚 Bash `if` Statement Guide

Conditional statements in Bash allow you to execute code based on specific conditions. Below is a comprehensive guide to `if` statements, their syntax, comparison operators, and examples.

---

## 🔹 Basic Syntax

```bash
if [[ condition ]]; then
    # commands if condition is true
fi
```

### With `else`

```bash
if [[ condition ]]; then
    # true
else
    # false
fi
```

### With `elif`

```bash
if [[ condition1 ]]; then
    # condition1 is true
elif [[ condition2 ]]; then
    # condition2 is true
else
    # none matched
fi
```

---

## ⚙️ Operators

### 🔢 Numeric Comparison

| Operator | Meaning          |
| -------- | ---------------- |
| `-eq`    | Equal to         |
| `-ne`    | Not equal        |
| `-lt`    | Less than        |
| `-le`    | Less or equal    |
| `-gt`    | Greater than     |
| `-ge`    | Greater or equal |

### 🔤 String Comparison

| Operator | Meaning          |
| -------- | ---------------- |
| `==`     | Equal to         |
| `!=`     | Not equal        |
| `-z`     | Empty string     |
| `-n`     | Not empty string |

### 📁 File Tests

| Operator | Meaning            |
| -------- | ------------------ |
| `-e`     | File exists        |
| `-d`     | Directory exists   |
| `-r`     | File is readable   |
| `-w`     | File is writable   |
| `-x`     | File is executable |

---

## 🧪 Practical Examples

### Example 1: Number Check

```bash
read -p "Enter Your Number: " number

if [[ $number -eq 0 ]]; then
    echo "Zero"
elif [[ $number -ge 1 ]]; then
    echo "Positive"
else
    echo "Negative"
fi
```

---

### Example 2: Number Range with Error Handling

```bash
read -p "Enter Your Number: " number

if [[ $number -eq 0 ]]; then
    echo "Zero"
elif [[ $number -ge 1 ]]; then
    echo "Positive"
elif [[ $number -le -1 ]]; then
    echo "Negative"
else 
    echo "Error: Invalid input"
    exit 1
fi
```

---

### Example 3: String Check

```bash
read -p "Enter Your String: " str

if [[ -n $str ]]; then
    if [[ $str == "hello" ]]; then
        echo "Hi"
    elif [[ $str != "hello" ]]; then
        echo "Ok"
    fi
else
    echo "Nothing to read"
    exit 1
fi
```

---

### Example 4: File Existence

```bash
file="script.sh"

if [[ -e $file ]]; then
    echo "File exists"
else
    touch "$file"
    echo "File created"
fi
```

---

### Example 5: File Permission Check

```bash
file="script50.sh"

if [[ -e $file ]]; then
    echo "File exists"

    if [[ ! -x $file ]]; then
        chmod +x "$file"
        echo "Executable permission added"
    fi

    if [[ ! -r $file ]]; then
        chmod +r "$file"
        echo "Read permission added"
    fi
else
    touch "$file"
    echo "File created"
fi
```

---

## ✅ Tips

* Always quote variables: `"$var"` to prevent word splitting.
* Use `[[ ... ]]` for conditional tests (preferred over `[ ... ]`).
* Prefer `read -r` to avoid backslash escapes.

