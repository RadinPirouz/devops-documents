## 🕵️‍♂️ Monitoring Processes with `top`

The `top` command provides a simple, real-time overview of all running processes and system stats.

```bash
top
```

### Sample output header:

```bash
top - 21:28:31 up 10:05,  5 users,  load average: 0.19, 0.26, 0.23

Tasks: 382 total,   1 running, 381 sleeping,   0 stopped,   0 zombie

%Cpu(s):  8.0 us,  1.8 sy,  0.0 ni, 90.2 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st

MiB Mem :  19754.0 total,  14439.8 free,   3207.1 used,   2871.8 buff/cache

MiB Swap:   8192.0 total,   8192.0 free,      0.0 used.  16547.0 avail Mem
```

### What each part means:

| Item              | Description                                                                     |
| ----------------- | ------------------------------------------------------------------------------- |
| 🕒 `21:28:31`     | Current system time                                                             |
| ⏳ `up 10:05`      | System uptime — 10 hours and 5 minutes since last boot                          |
| 👥 `5 users`      | Number of users currently logged in                                             |
| 📈 `load average` | CPU load averages over 1, 5, and 15 minutes (fractions of total CPU cores used) |
|                   | — 0.19 = load in last 1 min                                                     |
|                   | — 0.26 = load in last 5 min                                                     |
|                   | — 0.23 = load in last 15 min                                                    |

