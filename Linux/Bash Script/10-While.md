# Bash `while` Loop Guide

A clear, concise, and visually pleasant reference for using `while` loops in Bash.

---

## 1. Overview

The `while` loop in Bash repeatedly executes a block of commands **as long as a condition evaluates to true**. It is a fundamental control structure for iteration when the number of repetitions is not known in advance.

### General form

```bash
while [ condition ]
do
  command1
  command2
  ...
done
```

* The condition is evaluated before each iteration. If it returns a zero (truthy) exit status, the loop body runs. Otherwise, the loop exits.
* Square brackets (`[ ... ]`) are a synonym for the `test` command; spacing matters.

---

## 2. Examples

### 2.1 Simple counter

Counts from 1 to 5 and prints the current value.

```bash
counter=1

while [ $counter -le 5 ]
do
  echo "Counter: $counter"
  ((counter++))
done
```

**What it does:**

* Initializes `counter` to 1.
* The loop continues while `counter` is less than or equal to 5.
* Prints and increments the counter each iteration.

### 2.2 Waiting for a file to appear

Polls for the existence of `/tmp/myfile.txt` once per second.

```bash
while [ ! -f /tmp/myfile.txt ]
do
  echo "Waiting for file..."
  sleep 1
done

echo "File exists!"
```

**What it does:**

* Checks if the file does **not** exist (`! -f`).
* Sleeps for one second between checks to avoid busy-waiting.
* When the file appears, exits the loop and prints confirmation.

### 2.3 Interactive prompt with exit condition

Keeps prompting the user until they type `q`.

```bash
while true
do
  read -p "Type 'q' to quit: " input
  if [ "$input" = "q" ]; then
    break
  fi
done
```

**What it does:**

* Uses an infinite loop (`while true`).
* Prompts the user each time.
* Exits the loop when the input equals `q` using `break`.

---

## 3. Tips & Best Practices

* **Quote variables** to avoid word splitting and issues when they are empty: `[ "$foo" = "bar" ]`.
* **Use arithmetic expressions** with `(( ... ))` when dealing with numbers (`((counter++))` is more concise than `counter=$((counter + 1))`).
* **Avoid busy loops:** if waiting on external state, insert a `sleep` to reduce CPU usage.
* **Use `set -u` and `set -e`** in scripts to catch undefined variables and stop on errors, but be careful when using them with conditional tests.
* **Test conditions explicitly:** e.g., use `-f`, `-d`, `-r`, `-s`, etc., for file-related checks.

---

## 4. Common Pitfalls

* Missing spaces inside `[ ]` — `while [$counter -le 5]` is invalid; it must be `[ $counter -le 5 ]`.
* Forgetting to initialize loop variables, leading to unexpected behavior when using them in tests.
* Using `read` without handling empty input; consider providing a default or validating.
* Infinite loops without an exit strategy (e.g., missing `break` or condition never false).

---

## 5. Variations

* **Until loop:** opposite of `while` — runs until a condition becomes true.

  ```bash
  until [ -f /tmp/myfile.txt ]
  do
    echo "Waiting..."
    sleep 1
  ```

done

- **Command-based condition:** you can use any command whose exit status matters.

```bash
while ping -c1 example.com >/dev/null 2>&1
do
  echo "Host is reachable"
  sleep 5
done
````

---

## 6. Summary

Use `while` loops when the number of iterations depends on dynamic conditions (user input, file existence, external services). Combine with proper quoting, sleeping, and exit strategies to write robust and readable scripts.

