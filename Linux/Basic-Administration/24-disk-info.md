# 💽 **Disk Partition Types & Commands Guide**

## 🗂 **Partition Types**

### 1️⃣ **MBR (Master Boot Record)**

* 📏 **Max Disk Size:** 2 TB
* 📦 **Partition Entries:** 4

---

### 2️⃣ **GPT (GUID Partition Table)**

* 📏 **Max Disk Size:** 9 ZB (zettabytes)
* 📦 **Partition Entries:** 128

---

## 📊 **Disk Space & Usage Commands**

### 🖥 **`df` – Show Disk Space Usage**

The `df` command displays information about available and used disk space.

| Command               | Description                              |
| --------------------- | ---------------------------------------- |
| `df`          | 📄 Show disk space in default format     |
| `df -h`       | 🧍 Human-readable sizes (e.g., GB, MB)   |
| `df -T`       | 📂 Show file system type                 |
| `df -i`       | 🔢 Show inode usage                      |
| `df -h /home` | 🏠 Show usage for `/home` directory only |

---

### 📦 **`du` – Show Disk Usage**

The `du` command shows how much space files and directories take up.

| Command                       | Description                              |
| ----------------------------- | ---------------------------------------- |
| `du`                  | 📄 Show disk usage in blocks             |
| `du -h`               | 🧍 Human-readable sizes                  |
| `du -sh`              | 📊 Summary of current directory          |
| `du -h --max-depth=1` | 📂 Usage per subdirectory (1 level deep) |

---

## 🔍 **Disk & Partition Information Commands**

### 💿 **`lsblk`**

Shows partitions, disks, sizes, and mount points.

```bash
lsblk
```

---

### 🆔 **`blkid`**

Displays partition UUIDs and types.

```bash
blkid
```

