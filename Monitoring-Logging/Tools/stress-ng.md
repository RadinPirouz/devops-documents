# Stress-ng: Hardware Stress Testing Tool

`stress-ng` is a powerful tool for performing various stress tests on your hardware components, including CPU, memory, and I/O. This utility helps in assessing hardware stability under heavy loads, making it useful for benchmarking or diagnosing hardware issues.

## Table of Contents
- [Installation](#installation)
- [CPU Stress Testing](#cpu-stress-testing)
- [Memory Stress Testing](#memory-stress-testing)
- [I/O Stress Testing](#io-stress-testing)
- [Full System Stress Testing](#full-system-stress-testing)

### Installation

To install `stress-ng` on Ubuntu or other Debian-based systems, run:
```bash
sudo apt install stress-ng
```

---

## CPU Stress Testing

Use `stress-ng` to test CPU performance under different configurations:

### 1. Run a CPU Test with a Specified Number of Threads

You can specify the number of threads to use during a CPU stress test. Using `0` as the thread number utilizes all available CPU cores, maximizing CPU usage.

```bash
stress-ng --cpu <thread-number>
```

**Example:**
```bash
stress-ng --cpu 4
```
This command uses 4 CPU threads to run the stress test.

### 2. Run a CPU Test for a Specified Duration

Specify both the number of CPU threads and a time limit for the test.

```bash
stress-ng --cpu <thread-number> --timeout <seconds>
```

**Example:**
```bash
stress-ng --cpu 2 --timeout 60s
```
This command uses 2 CPU threads and runs the test for 60 seconds.

### 3. Run a CPU Load Test at a Specific Percentage

You can control the CPU load by specifying a percentage, which is helpful for testing different levels of CPU usage.

```bash
stress-ng --cpu-load <percentage>
```

**Example:**
```bash
stress-ng --cpu-load 50
```
This command keeps the CPU load at approximately 50%.

---

## Memory Stress Testing

Stress test the system's memory by allocating and releasing blocks of memory. This can help evaluate memory stability and performance.

### 1. Basic Memory Stress Test

Run a memory test with a specified number of workers (processes) that continuously allocate and deallocate memory.

```bash
stress-ng --vm <workers>
```

**Example:**
```bash
stress-ng --vm 2
```
This command uses 2 workers to perform memory stress testing.

### 2. Run a Timed Memory Stress Test

Add a timeout option to run a memory test for a specific duration.

```bash
stress-ng --vm <workers> --timeout <seconds>
```

**Example:**
```bash
stress-ng --vm 2 --timeout 60s
```
This command uses 2 memory workers and runs the test for 60 seconds.

### 3. Allocate a Specific Amount of Memory

Specify the amount of memory to allocate per worker. 

```bash
stress-ng --vm <workers> --vm-bytes <size>
```

**Example:**
```bash
stress-ng --vm 1 --vm-bytes 512M
```
This command allocates 512 MB of memory for one worker.

---

## I/O Stress Testing

I/O testing evaluates the performance of your system’s storage by reading and writing files repeatedly. This is useful for identifying storage bottlenecks and stress-testing the I/O subsystem.

### 1. Basic I/O Stress Test

Run an I/O test with a specified number of workers performing file operations.

```bash
stress-ng --io <workers>
```

**Example:**
```bash
stress-ng --io 4
```
This command runs 4 I/O workers, continuously reading and writing data to test disk performance.

### 2. Timed I/O Stress Test

Specify a timeout to limit the duration of the I/O stress test.

```bash
stress-ng --io <workers> --timeout <seconds>
```

**Example:**
```bash
stress-ng --io 4 --timeout 60s
```
This command runs the I/O stress test for 60 seconds with 4 workers.

---

## Full System Stress Testing

For a comprehensive stress test, `stress-ng` allows you to stress multiple components at once, such as CPU, memory, and I/O. This puts a combined load on the system to simulate heavy usage conditions.

```bash
stress-ng --all --timeout <seconds>
```

**Example:**
```bash
stress-ng --all --timeout 10s
```
This command runs a 10-second full system stress test, targeting all components that `stress-ng` supports.

