# S5CMD Reference Guide

`s5cmd` is a fast and efficient S3 and local filesystem command-line tool optimized for large-scale data operations.

---

## Command Syntax

```bash
s5cmd [global options] <command> [command options] [arguments...]
```

---

## Global Options

| Option                  | Description                                    |
| ----------------------- | ---------------------------------------------- |
| `--aws-profile string`  | AWS profile to use                             |
| `--endpoint-url string` | Custom S3 endpoint                             |
| `--no-sign-request`     | Do not sign requests (for public buckets)      |
| `--numworkers int`      | Number of parallel workers (**default: 256**)  |
| `--retry-count int`     | Number of retries for failed requests          |
| `--json`                | Output logs in JSON format                     |
| `--log string`          | Log level: `info`, `warning`, `error`, `debug` |
| `--dry-run`             | Show operations without executing              |

---

## Common Commands

### List Buckets/Objects

```bash
s5cmd ls s3://bucket_2/
```

### Bucket Management

```bash
s5cmd mb s3://new-bucket       # Create bucket
s5cmd rb s3://bucket-name      # Remove bucket
```

### Upload Files

```bash
s5cmd cp local.txt s3://bucket/file.txt
```

### Download Files

```bash
s5cmd cp s3://bucket/file.txt ./local.txt
s5cmd cp s3://bucket/*.jpg ./photos/
```

### Move/Rename Files

```bash
s5cmd mv s3://bucket/old.txt s3://bucket/new.txt
```

### Remove Files

```bash
s5cmd rm s3://bucket/file.txt
s5cmd rm --all-versions s3://bucket/file.txt
```

### Synchronization

```bash
s5cmd sync ./localdir/ s3://bucket/targetdir/
s5cmd sync s3://bucket/targetdir/ ./localdir/
```

### Read File Content

```bash
s5cmd cat s3://bucket/file.txt
```

### Disk Usage

```bash
s5cmd du s3://bucket/*
```

### Query with S3 Select

```bash
s5cmd select "select * from s3object s limit 10" s3://bucket/data.csv
```
