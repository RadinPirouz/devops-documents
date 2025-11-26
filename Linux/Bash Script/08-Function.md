# 🐚 Bash Function Syntax & Examples

Bash functions allow you to group reusable logic in shell scripts. Below are clear examples and explanations to help you understand how to define and use them effectively.

---

## 🔧 Defining a Function

You can define a Bash function in two main ways:

### Option 1: Classic Syntax

```bash
function_name () {
    # commands
}
```

### Option 2: With the `function` Keyword

```bash
function function_name () {
    # commands
}
```

> 💡 Both syntaxes are valid. The use of the `function` keyword is optional and mostly stylistic.

---

## 📥 Passing Arguments

Bash functions accept arguments just like scripts. These are accessed via `$1`, `$2`, etc.

### Example: Single Argument

```bash
func1() {
    echo "Arg: $1"
}

func1 "Test"
```

**Output:**

```
Arg: Test
```

---

## ➕ Multiple Arguments & Calculation

You can perform operations using passed arguments, like arithmetic:

```bash
summery() {
    local sum=$(( $1 + $2 ))
    echo $sum
}

summery 5 7
```

**Output:**

```
12
```

> 📌 `local` ensures `sum` is scoped within the function.

---

## ✅ Best Practices

* Use `local` to avoid polluting the global scope.
* Quote variables when dealing with strings.
* Use descriptive names for clarity.

---

## 🧪 Try It Yourself

Add these examples to a `.sh` file and run it with:

```bash
bash script.sh
```
