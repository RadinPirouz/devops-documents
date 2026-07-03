```markdown
# Benchmarking MySQL Performance

## Introduction

As a DevOps engineer, understanding MySQL performance under various workloads is critical for capacity planning, query optimization, and infrastructure tuning. Benchmarking provides repeatable, measurable insights into how your database behaves under stress. This document outlines standard methodologies, tools, and metrics for benchmarking MySQL effectively.

## Key Performance Metrics

Before running benchmarks, focus on these core metrics:

- **Throughput** - Transactions per second (TPS) or queries per second (QPS)
- **Latency** - Average, 95th, and 99th percentile response times
- **Concurrency** - How performance scales with increasing connections
- **Resource Utilization** - CPU, memory, disk I/O, and network usage on database host
- **Transaction Consistency** - Ensure ACID properties hold under load

## Benchmarking Tools

### Sysbench

The most common and flexible tool. Supports OLTP workloads, point selects, random reads/writes, and more.

Installation:
```bash
# Ubuntu/Debian
sudo apt install sysbench

# RHEL/CentOS
sudo yum install sysbench
```

### mysqlslap

Built-in MySQL utility for simulating client load. Simple but less customizable.

```bash
mysqlslap --host=localhost --user=root --password=secret \
  --auto-generate-sql --concurrency=50 --iterations=3
```

### Other Tools

- **HammerDB** - Graphical TPC-C style benchmarking
- **tcpdump + pt-query-digest** - Analyze real production traffic
- **dbt2** - Open source TPC-C implementation

## Benchmark Methodology

### Prerequisites

1. **Isolate the environment** - Use a dedicated database server or cloud instance. Disable OS background services (backups, cron, monitoring) that interfere.
2. **Configure MySQL** - Match production settings (buffer pool, log file sizes, innodb_flush_log_at_trx_commit, etc.).
3. **Prepare data** - Use realistic data volumes. For sysbench, typically 10-100 million rows per table.
4. **Warm up the buffer pool** - Run a trial workload before measuring.

### Phases

1. **Plan** - Define workload type (read-heavy, write-heavy, mixed), duration, and concurrency levels.
2. **Prepare** - Create test tables and data.
3. **Run** - Execute benchmark with monitoring tools active (e.g., `htop`, `iostat`, `mysqladmin status`).
4. **Cleanup** - Remove test databases.
5. **Analyze** - Compare results against baseline.

## Example: Sysbench OLTP Benchmark

### 1. Prepare Data

Create 4 tables with 1 million rows each:

```bash
sysbench oltp_read_write \
  --mysql-host=127.0.0.1 \
  --mysql-port=3306 \
  --mysql-user=sysbench \
  --mysql-password=bench123 \
  --mysql-db=testdb \
  --tables=4 \
  --table-size=1000000 \
  prepare
```

### 2. Run the Benchmark

Execute with varying concurrency (e.g., 1, 4, 8, 16, 32, 64 threads):

```bash
sysbench oltp_read_write \
  --mysql-host=127.0.0.1 \
  --port=3306 \
  --user=sysbench \
  --password=bench123 \
  --db=testdb \
  --tables=4 \
  --table-size=1000000 \
  --threads=32 \
  --time=300 \
  --report-interval=10 \
  run
```

Parameters explained:
- `--threads` - Number of concurrent clients
- `--time` - Benchmark duration in seconds (300 = 5 minutes)
- `--report-interval` - Print intermediate stats every N seconds

### 3. Clean Up

```bash
sysbench oltp_read_write \
  --mysql-host=127.0.0.1 \
  --mysql-user=sysbench \
  --mysql-password=bench123 \
  --mysql-db=testdb \
  cleanup
```

## Analyzing Results

### Key Output from Sysbench

After a run, sysbench outputs:

```
SQL statistics:
    queries performed:
        read:                            1091424
        write:                           311836
        other:                           155918
        total:                           1559178
    transactions:                        77958   (259.83 per sec.)
    queries:                             1559178 (5196.67 per sec.)
    ignored errors:                      0       (0.00 per sec.)
    reconnects:                          0       (0.00 per sec.)

General statistics:
    total time:                          300.0050s
    total number of events:              77958

Latency (ms):
         min:                                    4.01
         avg:                                  123.07
         max:                                 1152.19
         95th percentile:                      210.56
         sum:                              9591283.90
```

Critical metrics:
- **Transactions per second** - Primary throughput indicator
- **95th percentile latency** - Important for SLOs
- **Avg latency** - General responsiveness

### Interpreting Results

| Observation | Potential Cause |
|-------------|----------------|
| TPS scales linearly with threads up to a point | Healthy system, then bottleneck may shift |
| Latency spikes after certain concurrency | Contention on locks, mutexes, or I/O queue saturation |
| Dropping TPS at high concurrency | Context switching overhead or connection limits |
| High 95th vs avg latency | Occasional stalls (checkpointing, swapping, network latency) |

