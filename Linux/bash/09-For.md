# Bash `for` Loop Cheat Sheet

A clear and concise reference for using `for` loops in Bash, with syntax variations, examples, and best practices.

---

## 1. Basic `for` Loop (List Iteration)

Iterates over a fixed list of items.

**Syntax:**

```bash
for VARIABLE in ITEM1 ITEM2 ITEM3 ...
do
  commands
DONE
done
```

**Example:**

```bash
for color in red green blue
do
  echo "Color: $color"
done
```

*Output:*

```
Color: red
Color: green
Color: blue
```

---

## 2. Numeric Iteration Using a List

When you explicitly list out numbers.

**Example:**

```bash
for i in 1 2 3 4 5
do
  echo "Number: $i"
done
```

*Output:*

```
Number: 1
Number: 2
Number: 3
Number: 4
Number: 5
```

---

## 3. C-style `for` Loop (Arithmetic)

Similar to loops in C-style languages: initialize, condition, increment.

**Syntax:**

```bash
for (( init; condition; increment ))
do
  commands
ndone
```

**Example:**

```bash
for (( i=0; i<5; i++ ))
do
  echo "Index: $i"
done
```

*Output:*

```
Index: 0
Index: 1
Index: 2
Index: 3
Index: 4
```

---

## 4. Looping Over Files (Globbing)

Use shell glob patterns to iterate over matching filenames.

**Example:**

```bash
for file in *.txt
do
  echo "Found text file: $file"
done
```

```
# If the directory contains a.txt and notes.txt, output might be:
Found text file: a.txt
Found text file: notes.txt
```

---

## Summary

| Style             | Purpose                                    | Notes                                 |
| ----------------- | ------------------------------------------ | ------------------------------------- |
| `for var in list` | Iterate over a static list or glob results | Most common in shell scripting        |
| `for (( ... ))`   | Numeric / arithmetic loops                 | C-style syntax, powerful for counters |

