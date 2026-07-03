# InnoDB Storage Engine:

This document provides an in-depth explanation of the InnoDB storage engine, its on-disk structures, memory management mechanisms (buffer pool), and change buffering. The target audience is database administrators and DevOps engineers who need to understand and tune InnoDB for performance and reliability.

## Table of Contents

1. What is InnoDB?
2. MySQL Data Directories Related to InnoDB
3. Pages in InnoDB
4. Index Pages
5. Tablespaces
6. Buffer and Buffer Pool
   - Buffer Pool Metrics
   - Configuration Example
7. Change Buffering
   - Configuration Parameters

---

## 1. What is InnoDB?

InnoDB is a storage engine for MySQL that provides:

- ACID compliance (Atomicity, Consistency, Isolation, Durability)
- Row-level locking
- Foreign key constraints
- Crash recovery
- Multi-version concurrency control (MVCC)

It is the default storage engine for MySQL since version 5.5. InnoDB stores data in tablespaces, which are composed of pages.

---

## 2. MySQL Data Directories Related to InnoDB

In a typical MySQL installation, several directories are used to store InnoDB‑related files. Understanding their purpose helps with backup, recovery, and capacity planning.

| Directory           | Description                                                                                     |
|---------------------|-------------------------------------------------------------------------------------------------|
| `innodb_redo`       | Contains redo log files. Redo logs record changes made to InnoDB data to ensure durability.     |
| `innodb_temp`       | Stores temporary tablespaces used for internal temporary tables and on‑disk temporary objects. |
| `mysql`             | The system schema that holds metadata (database names, tables, privileges, etc.).               |

Even though `mysql` is not exclusively InnoDB, many system tables now use InnoDB by default.

---

## 3. Pages in InnoDB

A page is the smallest unit of storage in InnoDB. All data (table rows, indexes, etc.) is stored in pages.

- **Default page size**: 16 KB (can be configured to 4 KB, 8 KB, 32 KB, or 64 KB via `innodb_page_size`).
- **Structure**: Each page contains a header, a trailer (checksum), and the actual data.
- When a page is full, InnoDB allocates a new page to hold more data.

Pages are read from disk into memory (the buffer pool) and written back to disk when modified.

---

## 4. Index Page in InnoDB

An **index page** is a special type of page that stores index entries. InnoDB uses a B‑tree data structure for both primary and secondary indexes.

- **Primary key index (clustered index)**: The leaf pages contain the actual row data for the table. The entire table is organised as a B‑tree based on the primary key.
- **Secondary index**: Leaf pages contain the indexed column value and the primary key value (which is used to look up the full row in the clustered index).

Index pages are also 16 KB by default. Each index page contains pointers to child pages (for non‑leaf levels) or row pointers (for leaf levels).

---

## 5. Tablespace

A tablespace is a logical storage container that holds InnoDB data. There are several types of tablespaces:

| Tablespace Type          | Description                                                                        |
|--------------------------|------------------------------------------------------------------------------------|
| System tablespace        | Contains the data dictionary, doublewrite buffer, change buffer, and undo logs.    |
| File‑per‑table tablespace| Each table has its own `.ibd` file (controlled by `innodb_file_per_table`).        |
| General tablespaces      | User‑created tablespaces that can hold multiple tables.                            |
| Undo tablespace          | Stores undo logs for MVCC and transaction rollback.                                |
| Temporary tablespace     | Stores temporary tables created during queries or sessions (non‑persistent).      |

Each tablespace is divided into pages. The system tablespace (usually `ibdata1`) starts at 12 MB and grows as needed.

---

## 6. Buffer and Buffer Pool

### What is a Buffer?

A buffer is a memory area that temporarily holds data read from disk to reduce the number of direct disk I/O operations. In InnoDB, the main buffer is called the **buffer pool**.

### Buffer Pool

When a query requests data, InnoDB first checks whether the required pages are already present in the buffer pool:

- **If yes (cache hit)**: The data is returned directly from memory (extremely fast).
- **If no (cache miss)**: InnoDB reads the relevant pages from disk into the buffer pool, then serves the data from memory.

#### Recommended Size

A common best practice is to set the buffer pool size to approximately 75% of the available system memory on a dedicated database server. For shared servers, reduce the percentage accordingly.

### Configuration Example

In MySQL configuration file (`my.cnf` or `my.ini`):

```ini
[mysqld]
innodb_buffer_pool_size = 1G
```

Alternatively, change it dynamically at runtime (MySQL 8.0+):

```sql
SET PERSIST innodb_buffer_pool_size = 1073741824;   -- value in bytes
```

### Buffer Pool Metrics

These status variables help monitor buffer pool efficiency. Query them with:

```sql
SHOW GLOBAL STATUS LIKE 'innodb_buffer_pool%';
```

| Metric                              | Description                                                                                          |
|-------------------------------------|------------------------------------------------------------------------------------------------------|
| `Innodb_buffer_pool_reads`          | Number of times InnoDB had to read a page from disk because it was not available in the buffer pool. High values indicate a shortage of buffer pool memory. |
| `Innodb_buffer_pool_read_requests`  | Total number of logical read requests (page accesses) made to the buffer pool.                       |
| `Innodb_buffer_pool_wait_free`      | Count of times a thread had to wait for a clean page to become available. Non‑zero values suggest the buffer pool is under pressure (e.g., dirty page flushing is slow). |
| `Innodb_buffer_pool_pages_free`     | Number of free pages currently in the buffer pool. Low values mean the buffer pool is nearly full.   |

#### Interpreting Metrics

- **Cache hit ratio** = `(Innodb_buffer_pool_read_requests - Innodb_buffer_pool_reads) / Innodb_buffer_pool_read_requests`. Aim for >99%.
- If `Innodb_buffer_pool_wait_free` keeps increasing, consider increasing the buffer pool size or tuning flushing behaviour (`innodb_io_capacity`, `innodb_max_dirty_pages_pct`).
- Low `Innodb_buffer_pool_pages_free` alone is not a problem; it just shows the buffer pool is actively used.

---

## 7. Change Buffering

Change buffering is a feature that delays writing changes to secondary index pages. Instead of immediately updating the index pages on disk when a non‑unique secondary index is modified, InnoDB records the change in a special area called the **change buffer** (which is part of the system tablespace). Later, when the index pages are read into the buffer pool by other queries, the buffered changes are merged (applied) to the pages.

This reduces random disk I/O and improves performance for workloads with many Data Manipulation Language (DML) operations (INSERT, UPDATE, DELETE) that affect secondary indexes.

### Configuration Parameters

Both parameters are set in the MySQL configuration file.

#### `innodb_change_buffering`

Controls which operations are buffered. Possible values:

| Value     | Description                                                              |
|-----------|--------------------------------------------------------------------------|
| `none`    | Do not buffer any changes.                                               |
| `inserts` | Buffer only insert operations.                                           |
| `deletes` | Buffer only delete operations (including purge operations).              |
| `changes` | Buffer inserts and delete‑marking operations (but not actual purges).    |
| `purges`  | Buffer only the physical deletion of rows that occur during background purge. |
| `all`     | Buffer inserts, delete‑marking, and purges (default value).              |

Example configuration:

```ini
[mysqld]
innodb_change_buffering = all
```

#### `innodb_change_buffer_max_size`

Specifies the maximum size of the change buffer as a percentage of the total buffer pool size. The default is 25 (meaning 25% of the buffer pool). Valid range is 0 to 50.

Increasing this value allows more space for buffered changes, which can help workloads with heavy DML on secondary indexes, but it reduces the space available for cached data pages.

Example:

```ini
[mysqld]
innodb_change_buffer_max_size = 30
```

### When to Tune Change Buffering

- **Write‑heavy OLTP**: Keep `innodb_change_buffering = all` and possibly increase `innodb_change_buffer_max_size` to 30–40.
- **Read‑only or mostly reads**: Set `innodb_change_buffering = none` to avoid wasting buffer pool memory.
- **Unique indexes**: Change buffering does not apply to unique secondary indexes because uniqueness checks require immediate disk access.
