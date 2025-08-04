# 📘 **Using `less` in Linux/Unix**

`less` is a terminal pager program used to view the content of files one screen at a time. It's especially useful for viewing large files or logs.

---

## 📂 Basic Usage

```bash
less file
```

**Description**:
Opens `file` for viewing.

```bash
less /var/log/syslog
```

**Description**:
Opens the system log file for reading. Useful for examining system logs line by line.

---

## ⌨️ Common Keyboard Shortcuts

Here are the most frequently used keyboard shortcuts when using `less`:

| Key/Command | Action                               |
| ----------- | ------------------------------------ |
| `space`     | Scroll **down** one screen           |
| `b`         | Scroll **up** one screen             |
| `q`         | **Quit** `less`                      |
| `/pattern`  | **Search** forward for `pattern`     |
| `n`         | Go to the **next** match of pattern  |
| `N`         | Go to the **previous** match         |
| `g`         | Go to the **first line** of the file |
| `G`         | Go to the **last line** of the file  |

---

## ✅ Summary

`less` is a vital tool for system administrators, developers, and anyone dealing with large text files. With simple navigation and powerful search capabilities, it makes file reading efficient and user-friendly.

