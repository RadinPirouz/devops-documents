# 🐧 Linux Runlevels Guide

This guide provides a concise overview of traditional **runlevels** in Linux systems, particularly for **Red Hat** and **Debian**-based distributions. Runlevels define specific states of system operation, historically managed by the `init` system.

---

## 🔄 System Boot Sequence

```plaintext
BIOS → Bootloader → Kernel → init
```

* **BIOS**: Performs hardware checks via **POST** (Power-On Self Test).
* **Bootloader**: Loads the kernel.
* **Kernel**: Initializes system and mounts the root filesystem.
* **init**: Launches system processes based on the selected runlevel.

---

## 📊 Runlevels Comparison

| Runlevel | Description                         | Red Hat          | Debian          |
| -------- | ----------------------------------- | ---------------- | --------------- |
| 0        | Halt / Shutdown                     | ✅ Supported      | ✅ Supported     |
| 1        | Single-User Mode                    | ✅ Supported      | ✅ Supported     |
| 2        | Multi-User (No Network)             | ❌ (Includes Net) | ✅ Supported     |
| 3        | Multi-User (Network, No GUI)        | ✅ Supported      | ✅ Supported     |
| 4        | User-Defined / Custom               | ✅ Supported      | ✅ Supported     |
| 5        | GUI Mode / *(Halt on some systems)* | ✅ GUI Mode       | ⚠️ Custom/Halt? |
| 6        | Reboot                              | ✅ Supported      | ✅ Supported     |

> 💡 **Notes**:
> • **Runlevel 5** on Red Hat typically launches a full graphical environment (GUI).
> • On Debian, runlevels 2–5 are often configured identically and can be customized.
> • Runlevel behavior is configurable via `/etc/inittab` (SysVinit systems).

---

## 🔧 Useful Commands

### ✅ Check Current Runlevel

```bash
runlevel
```

### 🔁 Change Runlevel

```bash
telinit <runlevel>
```

or

```bash
init <runlevel>
```

> ⚠️ **Caution**: Switching runlevels may stop services or terminate user sessions. Use carefully on production systems.

---

## 🚀 Modern Systems: systemd Targets

Most modern Linux distributions use **systemd**, which replaces runlevels with **targets**.

| Runlevel | systemd Target      |
| -------- | ------------------- |
| 0        | `poweroff.target`   |
| 1        | `rescue.target`     |
| 3        | `multi-user.target` |
| 5        | `graphical.target`  |
| 6        | `reboot.target`     |

### 📌 Common systemd Commands

```bash
# Show default target
systemctl get-default

# Change to graphical mode
systemctl isolate graphical.target
```

