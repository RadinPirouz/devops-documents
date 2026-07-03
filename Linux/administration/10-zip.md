# 🗜️ ZIP Compression Cheatsheet

The `zip` command is a widely used tool for compressing files and folders into a `.zip` archive. It is cross-platform and supports features like encryption and customizable compression levels.

---

## 📦 Basic Syntax

```bash
zip [options] archive.zip files
```

---

## 🔧 Create a ZIP Archive

```bash
zip archive.zip file1 file2
```

* Compresses `file1` and `file2` into `archive.zip`

---

## 📈 Maximum Compression

```bash
zip -9 archive.zip file1 file2
```

* `-9`: Use maximum compression (slower, but smaller file size)

---

## 🔐 Create a Password-Protected ZIP

```bash
zip -e archive.zip file1 file2
```

* `-e`: Prompts for password encryption on the archive

---

## 📋 List Files in a ZIP Archive

```bash
unzip -l archive.zip
```

* `-l`: Lists contents of the ZIP without extracting

---

## 📂 Extract ZIP Archive

```bash
unzip archive.zip
```

* Extracts contents into the current directory

### 📁 Extract to Custom Directory

```bash
unzip archive.zip -d <custom-dir>
```

* `-d <custom-dir>`: Extracts files into the specified folder

