# `find` — quick reference & practical documentation

This is a compact, practical reference for the Unix/Linux `find` command aimed at DevOps engineers and system administrators. It covers common options, tests, actions, operators, examples (safe and practical) and performance tips.

---

# Synopsis

```
find [path...] [expression]
```

If no `path` is given, `find` searches the current directory (`.`). `expression` is evaluated left-to-right and can contain tests, actions and operators.

---

# Basic behaviour

* `find` walks directory trees recursively by default.
* An *expression* evaluates to true/false; when true, the default action `-print` (or whatever action is specified) is executed.
* You can control traversal order with `-depth` and `-maxdepth`/`-mindepth`.
* `-prune` prevents descending into directories.

---

# Common options and switches

* `-H` : follow symbolic links specified on the command line.
* `-L` : follow all symbolic links.
* `-P` : never follow symbolic links (default).
* `-xdev` : don't descend into directories on other filesystems (useful when walking `/`).
* `-mindepth N` : do not apply tests/actions to files at depth < N.
* `-maxdepth N` : do not descend past depth N.
* `-depth` : process directory contents before the directory itself (useful for safe deletes).
* `-mount` : same as `-xdev` (GNU find).

---

# Common tests (predicates)

* `-name pattern` : match basename with shell globbing (case-sensitive). Pattern uses shell wildcards (`*`, `?`, `[]`).
* `-iname pattern` : case-insensitive `-name`.
* `-path pattern` : match the whole path (slash-separated) with shell globbing.
* `-ipath pattern` : case-insensitive `-path`.
* `-regex pattern` : match full path with regular expression (syntax differs by `find` implementation; GNU `find` defaults to Emacs regex).
* `-type c` : file type; `f` = regular file, `d` = directory, `l` = symlink, `c` = character device, `b` = block device, `p` = FIFO, `s` = socket.
* `-perm mode` : file permission test. Modes:

  * octal: `-perm 0644` (exact)
  * symbolic: `-perm -u=w` (any of the bits), `-perm /u=w` (any), `-perm -0644` (all bits set)
  * GNU `find` also accepts `/mode` to mean "any of the bits".
* `-user name` / `-uid uid` : owner.
* `-group name` / `-gid gid` : group.
* `-size n[cwbk]` : file size; default 512-byte blocks for some `find` versions; most use 1K blocks for `k`. GNU `find` suffixes:

  * `c` = bytes
  * `k` = kilobytes
  * `M` = megabytes
  * `G` = gigabytes
  * `+n` = greater than n, `-n` = less than n, `n` = exactly n
* `-mtime n` / `-atime n` / `-ctime n` : modified / accessed / changed time in 24-hour periods; `-mtime +7` older than 7 days, `-mtime -7` less than 7 days, `-mtime 7` exactly 7.
* `-mmin n`, `-amin n`, `-cmin n` : minutes.
* `-newer file` : newer than file (can be combined with `!` to negate).
* `-empty` : empty file or directory.
* `-links n` : number of hard links.
* `-readable` / `-writable` / `-executable` : access checks from running user perspective.

---

# Common actions

* `-print` : print path (often default; some implementations require explicit `-print` with complex expressions).
* `-print0` : print paths separated by NUL (safe with whitespace/newlines).
* `-ls` : list file using `ls -dils` style.
* `-exec command {} \;` : run `command` once per matched file. `{}` is replaced by the current path. The `\;` terminator must be escaped or quoted.
* `-exec command {} +` : optimized form; appends multiple matches to command arguments like `xargs` (more efficient).
* `-ok command {} \;` : like `-exec` but prompts the user before each execution.
* `-delete` : delete matched files/directories (be careful; obeys ordering and `-depth`).
* `-prune` : exclude directory from descent (returns true; often used with `-o`).
* `-quit` : stop after first match (very efficient when used with `-print`).
* `-mindepth N`, `-maxdepth N` already described; they behave like tests.

---

# Operator precedence (GNU `find` style)

* Parentheses `(` `)` group expressions. They must be escaped or quoted: `\( ... \)` or `'(' ... ')'`.
* `!` or `-not` : logical NOT (unary).
* `-a` or implicit concatenation : logical AND.
* `-o` or `-or` : logical OR.
* Evaluation is left-to-right; `-a` has higher precedence than `-o`. Use parentheses to be explicit.
* Common pitfall: mixing `-prune` and `-o` requires careful grouping:
  Example pattern to exclude `dir`:

  ```
  find . -path ./dir -prune -o -print
  ```

  This means: if path is `./dir` prune it (and `-prune` returns true) otherwise (`-o`) `-print`.

---

# Typical practical examples

Search examples assume `bash` shell; escape parentheses and semicolons as needed.

1. Find files by name (case-sensitive)

```
find /var/log -type f -name "syslog*"
```

2. Case-insensitive:

```
find /home -type f -iname "*.jpg"
```

3. Find empty directories:

```
find /path -type d -empty
```

4. Delete `*.tmp` files safely (print first, then delete)

```
find /data -type f -name "*.tmp" -print
find /data -type f -name "*.tmp" -delete
```

Or safer with confirmation:

```
find /data -type f -name "*.tmp" -ok rm {} \;
```

5. Find and remove files older than 30 days (safe: use `-print` first)

```
find /var/log -type f -mtime +30 -print
find /var/log -type f -mtime +30 -exec rm -- {} +
```

Prefer `-exec ... +` over `-exec ... \;` for efficiency.

6. Remove directories older than 30 days (use `-depth` to ensure files inside are removed first)

```
find /tmp -depth -type d -mtime +30 -exec rm -rf -- {} +
```

`-delete` may also be used but beware of ordering; `-depth` ensures children processed before parent.

7. Find files with spaces and handle them safely:

```
find /srv -type f -name "*.conf" -print0 | xargs -0 grep -H "pattern"
```

8. Find files larger than 100 MiB:

```
find / -type f -size +100M -print
```

9. Find files newer than a reference file:

```
find /web -type f -newer /tmp/deploy_marker -print
```

10. Find and run a command on many files (batching):

```
find /data -type f -name "*.log" -exec gzip -- {} +
```

11. Exclude a directory (`dir_to_skip`) while listing everything else:

```
find . -path "./dir_to_skip" -prune -o -print
```

12. Only search one level (non-recursive):

```
find . -maxdepth 1 -type f -print
```

13. Find broken symlinks:

```
find / -xtype l -print
```

Note: `-xtype` tests the target type; `-L` changes behavior of `-type`.

14. Use `-printf` to customize output (GNU find):

```
find . -type f -printf "%p\t%k KB\t%TY-%Tm-%Td %TH:%TM:%TS\n"
```

`-printf` supports format sequences (`%p` path, `%s` bytes, `%k` KB blocks, `%TY` year, ...). Exact spec depends on implementation (GNU has extensive options).

15. Stop at first match (fast):

```
find /usr -type f -name "passwd" -print -quit
```

16. Find files modified within last 15 minutes:

```
find /var -type f -mmin -15
```

---

# Safe deletion checklist

* Always `-print` or `-ls` first to verify matches.
* Prefer `-exec rm -- {} +` or use `-delete` with `-depth` if required.
* Watch out for `-maxdepth`/`-mindepth` to avoid accidental top-level deletions.
* Use `-print0` + `xargs -0` when passing to other utilities.
* Consider using `-ok` for destructive changes in interactive contexts.

---

# Performance & scalability tips

* Limit scope: pass explicit starting paths instead of `.` or `/` when possible.
* Use `-maxdepth` and `-mindepth` to reduce traversal.
* Use `-xdev` to avoid crossing filesystem boundaries (speeds up root scans).
* Combine fast tests early (e.g., `-type f -name "*.log"` rather than `-name` alone) because find evaluates left-to-right; short-circuiting happens when possible.
* Prefer `-exec ... +` to `-exec ... \;` to reduce process spawn overhead.
* Use `-prune` to skip large tree branches that aren’t needed.
* On very large trees consider tools optimized for indexing (e.g., `locate` / `mlocate`, `fd`, or ripgrep for content search). `find` is always consistent but traverses the disk each run.

---

# Portability notes

* Behavior, available tests/actions and argument formats vary slightly between implementations (GNU `find` vs BSD `find` vs BusyBox). Examples above assume GNU `find` when using `-printf`, `-delete`, `-quit` or suffixes like `M`/`G` for sizes.
* When writing scripts for mixed environments, try to stick to portable tests: `-name`, `-type`, `-mtime`, `-print`, `-exec ... \;`. Check `/usr/bin/find --version` or `man find` on target hosts.

---

# Gotchas & common pitfalls

* Shell globbing vs `find` globbing: `-name "*.txt"` is matched by `find` and must be quoted to prevent shell expansion.
* `-perm` exact vs any-bit semantics differ across versions; test on target system.
* `-regex` matches the whole path, not just basename; regex dialect differs (use `-regextype posix-extended` on GNU `find` to set type).
* `-delete` will fail if used before tests that select children (order matters). Use `-depth` or test ordering appropriately.
* Beware of running `find` as root with `-exec rm -rf {}` — very dangerous if expression is wrong. Always verify output.
* `-maxdepth`/`-mindepth` may not be supported in very old `find` implementations.

---

# Exit status

* `0` : at least one match and command completed successfully.
* `1` : no matches were found (behavior can vary).
* `>1` : an error occurred (e.g., permission errors or malformed expression).
  Note: exact meanings can depend on implementation.

---

# Useful combinations

* Find files and preserve relative paths for tar:

```
cd /path && find . -type f -name "*.conf" -print0 | tar --null -T - -czf confs.tar.gz
```

* Find and change ownership or permissions:

```
find /srv/www -type f -name "*.php" -exec chown www-data:www-data {} +
find /srv/www -type d -exec chmod 755 {} +
```

* Search content in matched files:

```
find /app -type f -name "*.py" -print0 | xargs -0 grep -n "TODO"
```

---

# Related commands/tools

* `locate` / `mlocate` : fast filename lookup (uses database).
* `fd` : simpler, faster user-friendly alternative to `find` (not always installed).
* `xargs` : pass batches of arguments to commands (careful with spaces; use `-print0` + `xargs -0`).
* `stat` : detailed file metadata for a single file.
* `rm`, `tar`, `gzip`, `chown`, `chmod`, `rsync` : commonly used alongside `find`.

---

# Quick cheatsheet (most-used patterns)

* Find files by name: `find /path -type f -name "pattern"`
* Case-insensitive: `-iname`
* Size bigger than 100M: `-size +100M`
* Modified > 7 days: `-mtime +7`
* Delete old files: `find /dir -type f -mtime +30 -exec rm -- {} +`
* Print NUL-separated: `-print0`
* Safe prune: `find . -path ./skip -prune -o -print`
* Batch exec: `-exec cmd {} +`
* Stop on first: `-print -quit`
