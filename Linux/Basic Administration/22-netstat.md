# 🌐 `netstat` and `ss` Command Documentation

This guide provides essential usage examples for the `netstat` and `ss` commands to monitor network connections, listening ports, and socket statistics in Linux.

---

## 📡 `netstat` – Network Statistics

`netstat` is a legacy tool used for displaying network connections, routing tables, interface statistics, masquerade connections, and multicast memberships.

> ⚠️ `netstat` may be deprecated on some systems. Consider using `ss` as a modern replacement.

### 🔍 Show All Active Network Connections

```bash
netstat
```

* Displays all active sockets (both listening and non-listening).
* Includes TCP, UDP, UNIX domain sockets, etc.

---

### 🎧 Show Listening Ports

```bash
netstat -l
```

* Lists all **listening** ports (TCP and UDP).
* Useful for checking which services are waiting for incoming connections.

---

### 🔒 Show Listening TCP Ports

```bash
netstat -lt
```

* Lists only **TCP** ports in the **listening** state.

---

### 📡 Show Listening UDP Ports

```bash
netstat -lu
```

* Lists only **UDP** ports in the **listening** state.

---

### 🧠 Show Listening TCP/UDP Ports with Process Info

```bash
netstat -tulpn
```

* Shows all listening **TCP/UDP** ports.
* Includes **process ID (PID)** and **program name**.
* Useful for identifying which service is using a specific port.

---

## ⚡ `ss` – Socket Statistics (Modern Alternative)

`ss` is a faster and more powerful alternative to `netstat` for displaying socket statistics.

### Common `ss` Options

| Option | Description                                  |
| ------ | -------------------------------------------- |
| `-t`   | Show TCP sockets                             |
| `-u`   | Show UDP sockets                             |
| `-l`   | Show only listening sockets                  |
| `-n`   | Show numerical addresses (no DNS resolution) |
| `-p`   | Show process using the socket                |
| `-a`   | Show all sockets                             |

### Example – Show Listening TCP/UDP with Process Info

```bash
ss -tulpn
```

* Equivalent to `netstat -tulpn`
* Recommended for modern Linux distributions.

---

## ✅ Summary

| Task                                | `netstat` Command | `ss` Equivalent |
| ----------------------------------- | ----------------- | --------------- |
| Show all connections                | `netstat`         | `ss -a`         |
| Show listening ports                | `netstat -l`      | `ss -l`         |
| Show listening TCP ports            | `netstat -lt`     | `ss -lt`        |
| Show listening UDP ports            | `netstat -lu`     | `ss -lu`        |
| Show listening TCP/UDP with process | `netstat -tulpn`  | `ss -tulpn`     |

