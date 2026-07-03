# 🖥️ Mastering `screen` (Terminal Multiplexer)

`screen` is a **terminal multiplexer**. It allows you to:

✨ Start a terminal session that stays alive even if you disconnect.
✨ Run multiple shell sessions inside a single terminal.
✨ Detach and reattach to sessions later.

---

## 🚀 Basic Commands

### ▶️ Create a new shell

```bash
screen
```

### 📝 Create a new shell with a specific name

```bash
screen -S session_name
```

### 📜 Show all active sessions

```bash
screen -ls
```

### 🔗 Reattach to a session

```bash
screen -r session_name
```

---

## 🛑 Closing Sessions

### ❌ Exit a session (from inside)

```bash
exit
```

### 💣 Kill a specific session

```bash
screen -X -S session_name quit
```

---

## 🌟 Pro Tips

* You can **detach** from a session with `Ctrl + A` then `D`.
* Sessions keep running even if you **log out or disconnect**.
* Great for **long-running processes** (e.g., servers, builds, SSH tasks).

