# 📦 Linux Libraries & Package Management

This guide provides a quick overview of **library types**, **package sources**, and **Debian-based package management** commands using `apt`.

---

## 📚 Library Types

Linux supports two main types of libraries:

1. **Static Libraries (`.a`)**  
   - Linked at **compile-time**  
   - Included in the final binary  
   - Larger file size, faster execution

2. **Shared Libraries (`.so`)**  
   - Linked at **run-time**  
   - Saved separately from the binary  
   - Saves space and allows updates without recompiling

---

## 📦 Package Sources

### ✅ Official Packages  
Provided and maintained by the distribution (e.g., Debian, Ubuntu, Red Hat).

### 🌐 Third-Party Packages  
Created by external developers or organizations. Use with caution and verify trustworthiness.

---

## 🏬 Linux Package Managers

### 📦 Debian-based Systems
- **Package Manager**: `apt`
- **Low-level Tool**: `dpkg`
- **Package Format**: `.deb`

### 📦 Red Hat-based Systems
- **Package Manager**: `yum` or `dnf` (newer)
- **Low-level Tool**: `rpm`
- **Package Format**: `.rpm`

---

## 🌍 Package Mirrors

Mirrors are alternative download sources for package repositories, often closer geographically for faster updates.
