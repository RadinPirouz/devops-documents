# PostgreSQL Installation and Configuration Guide

Follow these steps to install and configure PostgreSQL on your system:

## Step 1: Update System Packages
Ensure your system's package list is up-to-date:

```bash
sudo apt update
```

## Step 2: Install PostgreSQL
Install PostgreSQL and its additional utilities:

```bash
sudo apt install postgresql postgresql-contrib
```

## Step 3: Start PostgreSQL Service
Start the PostgreSQL service:

```bash
sudo systemctl start postgresql.service
```

## Step 4: Enable PostgreSQL to Start on Boot
Enable the PostgreSQL service to start automatically on system boot:

```bash
sudo systemctl enable postgresql.service
```

## Step 5: Switch to the PostgreSQL User
Switch to the `postgres` system user to perform database administration tasks:

```bash
sudo -i -u postgres
```

## Step 6: Access the PostgreSQL Command-Line Interface
Start the `psql` command-line interface:

```bash
psql
```

## Step 7: Configure PostgreSQL
Edit the PostgreSQL configuration file:

```bash
vim /etc/postgresql/14/main/postgresql.conf
```

---

**Note:** Replace `14` in the file path above with your PostgreSQL version number, if it's different.
