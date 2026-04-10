
# 📦 `dpkg` – Debian Package Manager

`dpkg` is the package manager for Debian-based Linux distributions. It is used to install, remove, and manage `.deb` packages directly.

### 📘 Basic Syntax

```bash
dpkg [<option>...] <command>
```

---

## 🌐 Finding Packages

You can browse and search for Debian packages at [pkgs.org](https://pkgs.org).

---

## 📋 Listing Installed Packages

```bash
dpkg -l
dpkg --list
```

---

## 📥 Installing a Package

```bash
dpkg -i <package.deb>
dpkg --install <package.deb>
```

> ⚠️ If there are missing dependencies, run:

```bash
apt install -f
```

---

## 📂 Viewing Package Contents

```bash
dpkg -c <package.deb>
dpkg --contents <package.deb>
```

---

## ℹ️ Getting Package Info

```bash
dpkg -I <package.deb>
dpkg --info <package.deb>
```

---

## 📁 Listing Installed Files

```bash
dpkg -L <package-name>
dpkg --listfiles <package-name>
```

---

## 🧹 Removing a Package (and its config files)

```bash
dpkg -p <package-name>
dpkg --purge <package-name>
```

---

## 📝 Checking Package Status

```bash
dpkg -s <package-name>
dpkg --status <package-name>
```

---

## 🔧 Reconfiguring a Package

```bash
dpkg-reconfigure <package-name>
```

