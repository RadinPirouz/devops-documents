## 🖥️ Viewing Memory Usage with `free`

The `free` command shows your system’s memory usage.

```bash
free
```

For **human-readable** output (MB, GB, etc.):

```bash
free -h
```

**📊 Explanation of columns:**

| Column           | Description                                                        |
| ---------------- | ------------------------------------------------------------------ |
| **💾 total**     | Total physical memory (RAM) available in the system.               |
| **📂 used**      | Memory currently used by processes and the system.                 |
| **🆓 free**      | Completely unused RAM (not allocated to anything).                 |
| **🔄 shared**    | Memory shared between multiple processes.                          |
| **⚡ buff/cache** | Memory used for file buffers and cache to improve performance.     |
| **✅ available**  | Estimated memory available for starting new apps without swapping. |

💡 **Pro Tip:**

* `✅ available` is more useful than `🆓 free` for knowing how much memory you can actually use, since Linux keeps unused memory in cache for speed.

