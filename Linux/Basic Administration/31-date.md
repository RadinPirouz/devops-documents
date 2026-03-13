Here is a cleaned up, expanded, and more production-ready version of your **date and time manipulation** document, written from a DevOps / Linux system administration perspective and keeping it concise and accurate.

---

# Essential Date and Time Manipulation Commands

This document covers common shell commands for working with dates and times. These commands are frequently used in scripting, logging, monitoring, automation, and system administration tasks.

---

## 1. The `date` Command Overview

The `date` command is a standard Unix/Linux utility used to:

* Display the current system date and time
* Format timestamps
* Convert between human-readable dates and Unix epoch time
* Perform date arithmetic

Check system time:

```bash
date
```

---

## 2. Creating Epoch Timestamps

### Current Epoch Time (Seconds)

```bash
date +%s
```

Output example:

```
1737154200
```

### Current Epoch Time (Milliseconds)

```bash
date +%s%3N
```

Notes:

* `%s` → seconds since Unix epoch
* `%3N` → milliseconds (GNU date only)

---

### Convert Specific Date to Epoch (Milliseconds)

Convert a human-readable date to epoch time:

```bash
date -d "2026-01-13 14:31:26" +%s%3N
```

Common use cases:

* Log correlation
* API timestamps
* CI/CD pipeline timing
* Monitoring and alerting

---

## 3. Formatting Current Date and Time

Custom output formats are widely used in scripts and logs.

### Common Date Formats

| Command                     | Description           | Example Output               |
| --------------------------- | --------------------- | ---------------------------- |
| `date`                      | Default system format | Wed Jan 17 10:30:00 UTC 2026 |
| `date +'%Y-%m-%d %H:%M:%S'` | ISO-like format       | 2026-01-17 10:30:00          |
| `date +'%Y-%m-%d'`          | Date only             | 2026-01-17                   |
| `date +'%H:%M:%S'`          | Time only             | 10:30:00                     |
| `date +%s`                  | Epoch (seconds)       | 1737154200                   |

### Common Format Specifiers

| Specifier | Meaning         |
| --------- | --------------- |
| `%Y`      | Year (4 digits) |
| `%m`      | Month (01–12)   |
| `%d`      | Day (01–31)     |
| `%H`      | Hour (00–23)    |
| `%M`      | Minute (00–59)  |
| `%S`      | Second (00–60)  |
| `%N`      | Nanoseconds     |

---

## 4. Converting Epoch to Human-Readable Time

Convert epoch seconds to readable format:

```bash
date -d @1737154200
```

Using a variable:

```bash
EPOCH_TIME=1737154200
date -d @"$EPOCH_TIME"
```

Formatted output:

```bash
date -d @"$EPOCH_TIME" '+%Y-%m-%d %H:%M:%S'
```

---

## 5. Date Arithmetic

GNU `date` supports flexible date calculations.

### Relative Dates

| Command                 | Description             |
| ----------------------- | ----------------------- |
| `date -d "yesterday"`   | Previous day            |
| `date -d "tomorrow"`    | Next day                |
| `date -d "2 days ago"`  | Two days in the past    |
| `date -d "+1 hour"`     | One hour from now       |
| `date -d "+30 minutes"` | Thirty minutes from now |
| `date -d "+1 week"`     | One week from now       |
| `date -d "2 weeks ago"` | Two weeks ago           |

---

## 6. Date Arithmetic with Formatting

Example: date 7 days from now:

```bash
date -d "+7 days" '+%Y-%m-%d'
```

Example: timestamp 15 minutes ago (epoch):

```bash
date -d "-15 minutes" +%s
```

---

## 7. Working with UTC and Time Zones

Display current UTC time:

```bash
date -u
```

Format UTC time:

```bash
date -u '+%Y-%m-%d %H:%M:%S'
```

Convert date in a specific timezone:

```bash
TZ=UTC date
TZ=America/New_York date
```

---

## 8. Script-Friendly Usage Examples

Add timestamp to a log entry:

```bash
echo "$(date '+%Y-%m-%d %H:%M:%S') Application started"
```

Generate a timestamped filename:

```bash
backup_$(date +%Y%m%d_%H%M%S).tar.gz
```

Measure execution time:

```bash
start=$(date +%s)
# command here
end=$(date +%s)
echo "Duration: $((end - start)) seconds"
```

---

## 9. macOS Compatibility Notes

macOS uses BSD `date`, which differs from GNU `date`.

Example difference:

```bash
# GNU (Linux)
date -d "yesterday"

# BSD (macOS)
date -v -1d
```

Install GNU date on macOS:

```bash
brew install coreutils
gdate -d "yesterday"
```

---

## 10. Best Practices

* Use UTC for logs and distributed systems
* Store timestamps as epoch values when possible
* Format dates only at display time
* Avoid locale-dependent formats in scripts
* Be aware of GNU vs BSD `date` differences

---

If you want, I can:

* Add cron-specific date examples
* Add log rotation and backup use cases
* Provide a quick-reference cheat sheet
* Add cross-platform date handling strategies
