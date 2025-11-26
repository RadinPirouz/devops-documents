
# 📘 MariaDB Replication Setup Guide

This guide walks you through setting up **Master-Slave Replication** using MariaDB.

---

## 🛠️ Step 1: Install MariaDB

Install MariaDB on both the **master** and **slave** servers.

```bash
sudo apt update
sudo apt install mariadb-server
```

---

## ⚙️ Step 2: Configure the Master Server

Edit the MariaDB configuration file:

```bash
sudo vim /etc/mysql/mariadb.conf.d/50-server.cnf
```

Add or modify the following under the `[mariadb]` section:

```cnf
[mariadb]
log-bin
server_id=1
log-basename=master1
binlog-format=mixed
```

🔁 **Also**, change the `bind-address` to allow external connections:

```cnf
bind-address = 0.0.0.0
```

---

## 🔐 Step 3: Create Replication User

Access the MariaDB shell:

```bash
sudo mysql
```

Then run:

```sql
CREATE USER 'radin'@'%' IDENTIFIED BY '123';
GRANT REPLICATION SLAVE ON *.* TO 'radin'@'%';
FLUSH PRIVILEGES;
```

---

## 📈 Step 4: Check Master Status

Still inside the MariaDB shell, run:

```sql
FLUSH TABLES WITH READ LOCK;
SHOW MASTER STATUS;
```

Take note of:

* `File`: The binary log file name (e.g., `db-master1-bin.000003`)
* `Position`: The log position (e.g., `347`)

Then, in a separate terminal, unlock tables:

```sql
UNLOCK TABLES;
```

---

## 🛠️ Step 5: Configure the Slave Server

Edit the config file on the slave:

```bash
sudo vim /etc/mysql/mariadb.conf.d/50-server.cnf
```

Set the following:

```cnf
[mariadb]
log-bin
server_id=2
log-basename=slave1
binlog-format=mixed
```

---

## 🔄 Step 6: Set Up Slave Replication

Access the MariaDB shell on the slave server:

```bash
sudo mysql
```

Run the following (replace values as needed):

```sql
CHANGE MASTER TO
  MASTER_HOST='192.168.6.160',
  MASTER_USER='radin',
  MASTER_PASSWORD='123',
  MASTER_PORT=3306,
  MASTER_LOG_FILE='db-master1-bin.000003',
  MASTER_LOG_POS=347,
  MASTER_CONNECT_RETRY=10;
```

Start the slave:

```sql
START SLAVE;
```

Check slave status:

```sql
SHOW SLAVE STATUS\G
```

Look for:

* `Slave_IO_Running: Yes`
* `Slave_SQL_Running: Yes`

---

## 🔁 Resetting the Slave

To reset the slave configuration:

```sql
STOP SLAVE;
RESET SLAVE ALL;
```

