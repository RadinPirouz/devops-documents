## 📊 Network Monitoring with `nload`

```bash
nload [options] [interface]
```

* If no interface is specified, `nload` lists available interfaces and lets you choose one.
* Displays **two graphs**:
  🔽 Incoming traffic
  🔼 Outgoing traffic

---

### ⚙️ Options

| Option              | Description                                                                                           |
| ------------------- | ----------------------------------------------------------------------------------------------------- |
| `-u <unit>`         | Set unit for data rates (bits, bytes, kilobits, etc.) Options: `b`, `B`, `k`, `m`, `g` (default: `b`) |
| `-t <milliseconds>` | Refresh interval in milliseconds (default: 500 ms)                                                    |
| `-m`                | Show minimum and maximum network usage statistics                                                     |
| `-a`                | Show average network usage statistics                                                                 |
| `-q`                | Quiet mode — no graphical output, only numeric data                                                   |
| `-V`                | Show version info and exit                                                                            |
| `-h`                | Show help message and exit                                                                            |

---

### 💡 Examples

**Monitor a specific interface (e.g., eth0):**

```bash
nload eth0
```

**Use bytes per second as unit:**

```bash
nload -u B eth0
```

**Set refresh interval to 1 second:**

```bash
nload -t 1000 eth0
```

