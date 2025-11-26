# 🗡️ Kill Command

The `kill` command is used to **send signals to processes**, typically to terminate or control them.

```bash
kill [options] <PID>
```

📌 Replace `<PID>` with the Process ID of the target process.

---

## 🚦 Common `kill` Usage Examples

### 💤 Graceful Termination — `SIGTERM` (Signal 15)

```bash
kill 123
```

✅ Politely asks the process to terminate.
*Allows the process to clean up before exiting.*

---

### 🪓 Force Kill — `SIGKILL` (Signal 9)

```bash
kill -9 123
```

💥 **Immediate termination**.
*Doesn’t allow cleanup — use only when necessary.*
🗡️ *Think of it as the "katana" of kill commands.*

### 📑 Multi Process Kill

```bash
pidof <ps-name> | xargs kill -9 
```

---

### ⌨️ Interrupt — `SIGINT` (Signal 2)

```bash
kill -2 123
```

🛑 Mimics pressing `Ctrl + C`.
*Often used to stop processes gracefully from the terminal.*

---

### 🔄 Hangup — `SIGHUP` (Signal 1)

```bash
kill -1 123
```

♻️ Requests the process to **reload or restart**.
*Commonly used for daemons or services to reload configs.*

---

## 📋 Summary of Signals

| Signal | Name      | Description                    |
| ------ | --------- | ------------------------------ |
| `1`    | `SIGHUP`  | Reload configuration / restart |
| `2`    | `SIGINT`  | Interrupt (like Ctrl + C)      |
| `9`    | `SIGKILL` | Force kill (cannot be ignored) |
| `15`   | `SIGTERM` | Graceful termination (default) |

