# Essential Date and Time Manipulation Commands 

This document outlines common shell commands used for working with dates and times, essential for scripting, logging, and system administration tasks.

## 1. Creating Epoch Timestamps

The `date` command is versatile for generating timestamps in various formats, most notably the Unix epoch time (seconds since 1970-01-01 00:00:00 UTC).

### Command to Create Epoch Time (Milliseconds Precision)

This command converts a specific human-readable date and time into the epoch time, including milliseconds (`%3N`).

```bash
date -d "2026-01-13 14:31:26" +%s%3N
```

## 2. Formatting Current Date and Time

Displaying the current date and time in a readable or specific format.

| Command | Description | Example Output (Varies) |
| :--- | :--- | :--- |
| `date` | Default display | Wed Jan 17 10:30:00 UTC 2026 |
| `date +'%Y-%m-%d %H:%M:%S'` | Standard ISO format | 2026-01-17 10:30:00 |
| `date +%s` | Current epoch time (seconds) | 1737154200 |

## 3. Converting Epoch to Human Readable

Converting a numeric epoch timestamp back into a readable format.

```bash
# Assuming $EPOCH_TIME holds a value like 1737154200
date -d @"$EPOCH_TIME"
```

## 4. Date Arithmetic

Calculating dates relative to the current time.

| Command | Description | Example Output (Varies) |
| :--- | :--- | :--- |
| `date -d "yesterday"` | The previous day | Tue Jan 16 ... |
| `date -d "2 weeks ago"` | Two weeks prior | Thu Jan 03 ... |
| `date -d "+1 hour"` | One hour from now | Wed Jan 17 11:30:00 UTC 2026 |