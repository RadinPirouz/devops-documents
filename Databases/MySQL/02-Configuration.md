# MySQL Performance and Administration Guide for DevOps

This document covers essential MySQL configuration parameters, monitoring practices, data integrity checks, slow query tuning, and useful command-line tools for database administration.

## Table of Contents

- [MySQL Performance and Administration Guide for DevOps](#mysql-performance-and-administration-guide-for-devops)
  - [Table of Contents](#table-of-contents)
  - [Configuration Parameters](#configuration-parameters)
    - [max\_allowed\_packet](#max_allowed_packet)
    - [Error and Slow Query Logs](#error-and-slow-query-logs)
    - [skip\_name\_resolve](#skip_name_resolve)
  - [Initial Root Password and Access Control](#initial-root-password-and-access-control)
  - [Monitoring](#monitoring)
    - [Performance Schema and Information Schema](#performance-schema-and-information-schema)
    - [Percona Monitoring and Management (PMM)](#percona-monitoring-and-management-pmm)
  - [Data Corruption Checking](#data-corruption-checking)
  - [Slow Query Configuration Details](#slow-query-configuration-details)
  - [Tools](#tools)
    - [pt-stalk](#pt-stalk)
    - [pt-diskstats](#pt-diskstats)
    - [pt-summary](#pt-summary)
    - [mysqlcheck](#mysqlcheck)

---

## Configuration Parameters

### max_allowed_packet

```ini
max_allowed_packet = 128M
```

- **Purpose**: Defines the maximum size of a single communication packet between the MySQL client and server.
- **Best Practice**: For large BLOB/ TEXT fields or large dumps, set to `1G`. Adjust according to workload and available memory.

### Error and Slow Query Logs

Place these directives under the `[mysqld]` section:

```ini
[mysqld]
log-error = /var/log/mysql/error.log
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
```

- `log-error`: Location of the error log file.
- `slow_query_log`: Enables slow query logging.
- `slow_query_log_file`: Path to the slow query log file.

### skip_name_resolve

```ini
skip_name_resolve
```

- **Effect**: Disables resolution of client hostnames to IP addresses.
- **Benefit**: Improves connection speed and reduces DNS overhead. Use when all users connect via IP addresses or CIDR ranges.

---

## Initial Root Password and Access Control

After the first initialization of MySQL, the temporary root password is stored in `/var/log/mysqld.log`. Use it to log in and change the password.

**Change root password:**

```sql
ALTER USER 'root'@'%' IDENTIFIED BY '123';
```

**Restrict access to a specific IP or range** (e.g., 192.168.1.0/24):

```sql
ALTER USER 'root'@'192.168.1.0/24' IDENTIFIED BY '123';
```

> Replace `'123'` with a strong password and adjust the subnet as needed.

---

## Monitoring

### Performance Schema and Information Schema

MySQL provides two built-in schemas for monitoring:

- **performance_schema**: Tracks server execution details at a low level (waits, events, statements, etc.).
- **information_schema**: Provides metadata about database objects (tables, columns, privileges, etc.).

### Percona Monitoring and Management (PMM)

PMM is an open-source monitoring solution that integrates with **Grafana** for dashboards and visualization. It collects metrics from MySQL, PostgreSQL, MongoDB, and system hosts.

**Key features**:
- Query analytics and slow query tracking.
- Real‑time performance dashboards.
- Historical data retention.

**How to use**:
1. Install PMM Server (Docker or package) on a dedicated host.
2. Install PMM Client on each MySQL host.
3. Connect the client to the server:  
   `pmm-admin config --server-url=https://<pmm-server-ip>:443`
4. Add MySQL service:  
   `pmm-admin add mysql --username=root --password=<pwd>`

---

## Data Corruption Checking

Use `mysqlcheck` to verify table integrity.

**Check all databases:**

```bash
mysqlcheck --check --all-databases -u root -p
```

**Check a specific database:**

```bash
mysqlcheck --check <database_name> -u root -p
```

The command will report any corrupted tables. For deeper repair, use `--repair` after verifying the need.

---

## Slow Query Configuration Details

Extended slow query log configuration:

```ini
slow_query_log = 1
slow_query_log_file = /var/log/mysql/mysql-slow.log
long_query_time = 2
```

- `long_query_time`: Queries that take more than `2` seconds are logged. Fractional seconds allowed (e.g., `0.5`).
- Additional useful parameters:
  - `log_queries_not_using_indexes = 1` – logs queries that do not utilise indexes.
  - `log_slow_admin_statements = 1` – logs slow administrative statements (OPTIMIZE, ANALYZE, ALTER).

After changes, restart MySQL: `sudo systemctl restart mysql`

---

## Tools

This section covers command-line tools from the **Percona Toolkit** (commonly used by DBAs and DevOps). The names in the original notes (`py-stals`, `py-disktats`, `pt-summery`) likely refer to `pt-stalk`, `pt-diskstats`, and `pt-summary`.

### pt-stalk

**Description**: Watches for a MySQL problem (e.g., high load, long lock wait) and collects diagnostic data when the problem occurs.

**Installation** (Ubuntu/Debian):

```bash
sudo apt-get install percona-toolkit
```

**Basic usage**:

```bash
pt-stalk --user=root --password=<pwd> --dest=/var/log/pt-stalk -- --defaults-file=/etc/mysql/my.cnf
```

- `--user`, `--password`: MySQL credentials.
- `--dest`: Directory where collected data will be stored.
- The `--` separates pt-stalk options from MySQL options.
- By default, the script runs as a daemon. Use `--run-time=30s` for a single collection cycle.

**How to use**:
1. Configure thresholds (disk free, processlist size, etc.) to trigger data collection.
2. Review collected files (tarballs) after an incident to diagnose root causes.

### pt-diskstats

**Description**: Analyzes disk I/O performance interactively, similar to `iostat`, but with more detailed per‑device statistics and latency histograms.

**Basic usage**:

```bash
pt-diskstats --interval=5 --iterations=10
```

- `--interval`: Seconds between samples.
- `--iterations`: Number of samples (omit for infinite).
- You can specify devices: `pt-diskstats --devices=sda,sdb`

**How to use**:
- Monitor disk latency and IOPS in real time to identify storage bottlenecks for MySQL.
- Redirect output to a file for later analysis: `pt-diskstats --interval=2 > /tmp/io.log`.

### pt-summary

**Description**: Collects and prints a system overview – CPU, memory, disk, network, and MySQL configuration.

**Basic usage**:

```bash
pt-summary
```

**How to use**:
- Run before and after changes to capture baseline system state.
- Combine with `pt-mysql-summary` for MySQL‑specific detail.
- The output helps quickly understand the environment when debugging performance issues.

### mysqlcheck

Already covered in the [Data Corruption Checking](#data-corruption-checking) section.

