# 📦 Managing Packages with `rpm` on RHEL/CentOS

The `rpm` command (RPM Package Manager) is the **low-level package management tool** used on **Red Hat-based** systems such as RHEL, CentOS, Fedora, and others. Unlike `yum`, `rpm` does not resolve dependencies automatically and is best used for advanced or manual package management.

Below are the core `rpm` commands categorized and explained.

---

## 📥 1. Installing Packages

### `rpm -i <file.rpm>`

### `rpm --install <file.rpm>`

Installs a new `.rpm` package file. This command will **fail if the package's dependencies are not already installed**.

```bash
rpm -i <file.rpm>
```

or

```bash
rpm --install <file.rpm>
```

> 💡 Tip: Use `yum localinstall` or `dnf install` instead for dependency resolution.

---

## 🔄 2. Upgrading Packages

### `rpm -U <file.rpm>`

### `rpm --upgrade <file.rpm>`

Upgrades an existing package if it is already installed. If the package is not already present, this command will install it.

```bash
rpm -U <file.rpm>
```

or

```bash
rpm --upgrade <file.rpm>
```

---

## ❌ 3. Removing Packages

### `rpm -e <package>`

### `rpm --erase <package>`

Removes a package from the system by name (not the filename). Note that this command also does **not resolve dependencies**, so it may break things if you're not careful.

```bash
rpm -e <package>
```

or

```bash
rpm --erase <package>
```

> ⚠️ Caution: Always check what depends on a package before removing it.

---

## 🔍 4. Querying Packages

### `rpm -q <package>`

Query whether a package is installed, and show its version.

```bash
rpm -q <package>
```

---

### `rpm -qa`

List **all installed packages**.

```bash
rpm -qa
```

---

### `rpm -qi <package>`

Displays detailed **information** about a specific installed package.

```bash
rpm -qi <package>
```

---

### `rpm -ql <package>`

Lists all files installed by a package.

```bash
rpm -ql <package>
```

---

### `rpm -qf <file>`

Finds out **which package** owns a specific file.

```bash
rpm -qf /usr/bin/wget
```

---

### `rpm -qp <file.rpm>`

Query a package file (without installing it) to see its metadata.

```bash
rpm -qp <file.rpm>
```

---

### `rpm -K <file.rpm>`

Verifies the **signature and integrity** of an RPM package file.

```bash
rpm -K <file.rpm>
```

---

## 🛠️ 5. Verifying and Checking

### `rpm -V <package>`

Verifies installed package files against their original metadata (modifications, corruption, etc.).

```bash
rpm -V <package>
```

---

### `rpm --test -i <file.rpm>`

Simulates an install without actually installing the package — useful for testing.

```bash
rpm --test -i <file.rpm>
```

---

## ✅ Final Notes

* `rpm` is a **powerful low-level tool**, but not recommended for resolving dependencies.
* For **automated dependency handling**, prefer using `yum` or `dnf`.
* Use `rpm` when you need precise control over the package management process or are working with standalone `.rpm` files.

