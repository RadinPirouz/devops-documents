# 📘 Disk Partitioning Guide: MBR & GPT using `fdisk` and `gdisk`

## 🔹 Overview

* Use `**fdisk**` for **MBR (Master Boot Record)** partitioning.
* For **GPT (GUID Partition Table)**, the recommended tool is `**gdisk**`, but `fdisk` also supports GPT.

---

## 🧰 Disk Partitioning with `fdisk`

### 🔍 List Partitions

| Command    | Description                         |
| ---------- | ----------------------------------- |
| `fdisk -l` | Show list of available partitions   |
| `fdisk -x` | Show list with extended information |

### ⚙️ Launch `fdisk`

```bash
fdisk /dev/sdX
```

Replace `/dev/sdX` with your actual disk name (e.g., `/dev/sdb`).

---

### 📖 Inside `fdisk`

Once inside the `fdisk` prompt:

| Key | Function                          |
| --- | --------------------------------- |
| `m` | Show help                         |
| `p` | Print partition table (disk info) |
| `n` | Create new partition              |
| `t` | Change partition type             |
| `w` | Write changes and exit            |

#### ➕ Creating a Partition (`n`)

* Choose **`p`** for **primary** or **`e`** for **extended** partition.
* MBR allows **4 primary** partitions. One of them can be **extended**, which can hold **logical** partitions.

#### 📏 Define Partition Size

Example:

```bash
+512M
```

---

## 🧱 Create Filesystem

To format the partition with `ext4`:

```bash
mkfs.ext4 /dev/sdb1
```

---

## 🔗 Get Partition UUID

Option 1: After formatting, the UUID is shown in output.
Option 2: Use `blkid` to retrieve it:

```bash
blkid
```

---

## 📝 Mount Using `/etc/fstab`

1. Open the `fstab` configuration file:

```bash
vim /etc/fstab
```

2. Add the following line:

```
/dev/disk/by-uuid/<UUID> <mount_path> <filesystem> defaults 0 1
```

### Example:

```
/dev/disk/by-uuid/1eb043d2-f2ee-4a69-a7c4-13c283c3ccc6 /test ext4 defaults 0 1
```

This ensures the partition is mounted automatically at boot.

---

## ✅ Summary

| Task               | Command/Action        |
| ------------------ | --------------------- |
| List partitions    | `fdisk -l`            |
| Start partitioning | `fdisk /dev/sdX`      |
| Format partition   | `mkfs.ext4 /dev/sdX1` |
| Get UUID           | `blkid`               |
| Edit fstab         | `vim /etc/fstab`      |

