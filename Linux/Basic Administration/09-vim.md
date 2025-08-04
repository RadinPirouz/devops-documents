# Getting Started with Vim 📝

## 1. Installing Vim

To install Vim on a Debian‑based system (like Ubuntu), run:

```bash
sudo apt update
sudo apt install vim
```

---

## 2. Opening Files or Directories

* **Open a file**

  ```bash
  vim <filename>
  ```

* **Open a directory**

  ```bash
  vim <directory_name>
  ```

  (This opens Vim’s file browser—helpful for navigating and editing multiple files.)

---

## 3. Vim Modes

Vim works in multiple modes—here are the core ones:

1. **Normal mode** – The default mode; used for navigation and commands.
2. **Insert mode** – For editing text; enter it by pressing `i`, `a`, or `o`.
3. **Visual mode** – For selecting text; enter it with `v`, `V`, or `Ctrl+v`.

---

## 4. Essential Commands

(Type these in **Normal mode** and then press Enter when needed)

| Command     | Description                               |
| ----------- | ----------------------------------------- |
| `:w`        | Save (write changes to the current file)  |
| `:w <name>` | Save changes to a specified file `<name>` |
| `:wq`       | Save and quit Vim                         |
| `:q`        | Quit (only if no unsaved changes exist)   |
| `:q!`       | Quit without saving (discard all changes) |

---

## 5. Handy Shortcuts

These are core shortcuts used in **Normal mode**:

| Shortcut | Action                           |
| -------- | -------------------------------- |
| `dd`     | Delete (cut) the current line    |
| `yy`     | Yank (copy) the current line     |
| `p`      | Paste after the cursor           |
| `u`      | Undo the last change             |
| `gg`     | Go to the first line of the file |

---

## 6. Quick Usage Flow

1. **Start Vim**:

   ```bash
   vim example.txt
   ```

2. **Insert text**:
   Press `i` → type your content → press `Esc` to return to **Normal mode**.

3. **Save your work**:
   Type `:w` in Normal mode and press Enter.

4. **Make edits**:

   * Use `dd` to delete a line
   * Use `yy` to copy (yank) a line
   * Move the cursor to a new location, then hit `p` to paste
   * Press `u` to undo any mistake

5. **Navigate quickly**:

   * `gg` to jump to the beginning
   * Use arrow keys or `h`, `j`, `k`, `l` for navigation

6. **Finish editing**:

   * `:wq` to save and exit
   * `:q!` to exit without saving

---

## 7. Tips & Tricks

* **Visual mode**:
  Press `v` to start selecting character by character, `V` for line selection, or `Ctrl+v` for block-wise selection.

* **Other navigation**:

  * Use `G` to go to the end of the file
  * Use a number before a command, e.g., `5dd` deletes 5 lines

---

### Summary

Vim may feel different at first, but once you get comfortable switching between **Insert**, **Normal**, and **Visual** modes, you'll find it’s a powerful and efficient editor.
Happy Vimming! 😊

