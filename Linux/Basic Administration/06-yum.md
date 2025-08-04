# 🍽️ Managing Packages with `yum` on RHEL/CentOS

`yum` (Yellowdog Updater, Modified) is the traditional package manager for RPM-based Linux distributions such as **Red Hat Enterprise Linux (RHEL)** and **CentOS**. Below is a breakdown of commonly used `yum` commands, categorized and explained in detail.

---

## 🔄 1. Updating the System

### `yum update`

Fetches the latest package metadata and installs available updates for all packages currently installed on the system.

```bash
yum update
```

---

### `yum upgrade`

Performs the same function as `yum update`. In older versions of `yum`, `upgrade` was used for more aggressive upgrades, but in recent versions, they are functionally equivalent.

```bash
yum upgrade
```

---

## 📥 2. Installing and Reinstalling Packages

### `yum install <pkg-name>`

Installs a new package along with any required dependencies.

```bash
yum install <pkg-name>
```

---

### `yum reinstall <pkg-name>`

Reinstalls an already installed package, which is useful if system files have been corrupted or modified.

```bash
yum reinstall <pkg-name>
```

---

### `yum localinstall <file-dir>`

Installs a `.rpm` package from a local file path while resolving dependencies using remote repositories.

```bash
yum localinstall <file-dir>
```

---

## ❌ 3. Removing Packages

### `yum remove <pkg-name>`

Uninstalls the specified package from the system, including any dependencies no longer required.

```bash
yum remove <pkg-name>
```

---

## 🔍 4. Querying and Searching

### `yum list`

Lists all available, installed, and updatable packages.

```bash
yum list
```

---

### `yum info <pkg>`

Displays detailed information about the specified package, including version, repository, summary, and description.

```bash
yum info <pkg>
```

---

### `yum search`

Searches for a keyword in package names and descriptions. Add the search term to complete the command.

```bash
yum search <keyword>
```

Example:

```bash
yum search python
```

---

### `yum deplist <pkg>`

Shows the list of dependencies for a given package.

```bash
yum deplist <pkg>
```

---

## 🕓 5. Package History and Transactions

### `yum history`

Displays a history of all yum transactions (installs, updates, removals), which can be reviewed or undone if needed.

```bash
yum history
```

---

## 💾 6. Downloading Packages (Without Installing)

### `yum download <pkg>`

Downloads an RPM package file without installing it. Useful for transferring or offline installations. Requires the `yum-utils` package.

```bash
yum download <pkg>
```

> 💡 **Note:** If you get an error, try installing `yum-utils`:
>
> ```bash
> yum install yum-utils
> ```

---

## ✅ Final Notes

* `yum` has been replaced by `dnf` in newer distributions (e.g., RHEL 8+), but still widely used in older systems.
* Always run `yum update` before installing new packages.
* Combine with `yum history` to review or undo changes when troubleshooting.

