# 🔗 **Linux Links: Soft Link vs Hard Link**

## 📝 **Types of Links**

In Linux, there are **two types** of links:

1. 🪶 **Soft Link** (Symbolic Link)
2. 🪨 **Hard Link**

---

## ⚙️ **Commands**

### 🪶 **Soft Link (Symbolic Link)**

Acts like a **shortcut** pointing to the original file.

```bash
ln -s <base-file> <link-file>
```

💡 **Example:**

```bash
ln -s file.txt file_link.txt
```

---

### 🪨 **Hard Link**

Points directly to the file's **inode** (physical data on disk).

```bash
ln <base-file> <link-file>
```

💡 **Example:**

```bash
ln file.txt file_hard.txt
```

---

## 📊 **Soft Link vs Hard Link**

| 🏷️ Feature               | 🪶 Soft Link (Symbolic)           | 🪨 Hard Link                  |
| ------------------------- | --------------------------------- | ----------------------------- |
| 🔢 **Inode Number**       | Different from the original file  | Same as original file         |
| 🗂 **Cross Filesystem**   | ✅ Yes                             | ❌ No                          |
| ❌ **If Original Deleted** | Link breaks (becomes invalid)     | File still exists             |
| 📦 **Storage**            | Stores path to original file      | Stores actual data reference  |
| 🔄 **Update**             | Reflects changes in original file | Reflects changes (same inode) |

---

## 🧠 **Quick Notes**

* **Soft Link** → Think *shortcut* 📎
* **Hard Link** → Think *clone reference* 📀
* If you delete the **base file**:

  * 🪶 Soft Link → ❌ Broken link
  * 🪨 Hard Link → ✅ Still works (data intact)

