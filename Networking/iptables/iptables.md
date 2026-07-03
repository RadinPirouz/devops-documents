# 🛡️ Iptables & Netfilter Guide


## 🌐 Overview

**iptables** works with **Netfilter** to manage and control network traffic on Linux systems.

---

## 🔗 Connection Types

1. **NEW** – A new connection being initiated
2. **ESTABLISHED** – An existing, ongoing connection
3. **RELATED** – A new connection related to an existing one

---

## 🧰 iptables-persistent

Install iptables and save the rules to a file for persistence across reboots.

---

## 📂 Default Path

```plaintext
/etc/iptables
```

---

## ⚙️ Command Format

```bash
iptables -t <table-name> <option> <chain-name> <match> -j <action>
```

---

## 🏷️ Table Names

| Table Name | Purpose                          |
| ---------- | -------------------------------- |
| filter     | Default – Filtering Packets      |
| nat        | Network Address Translation      |
| mangle     | Packet alteration/editing        |
| raw        | Pre-processing packets before OS |

---

## 🔄 Chains

| Table  | Chains                                          |
| ------ | ----------------------------------------------- |
| filter | INPUT, OUTPUT, FORWARD                          |
| nat    | PREROUTING, OUTPUT, POSTROUTING                 |
| mangle | PREROUTING, INPUT, FORWARD, OUTPUT, POSTROUTING |
| raw    | PREROUTING, OUTPUT                              |

---

## 🚦 Chain Functions

| Chain       | Description                                              |
| ----------- | -------------------------------------------------------- |
| INPUT       | Incoming connections to the server                       |
| OUTPUT      | Outgoing packets from the server                         |
| FORWARD     | Packets routed through the server to other destinations  |
| PREROUTING  | Edit packets before routing                              |
| POSTROUTING | Edit packets after routing and before exiting the server |

---

## 🔧 Options

| Option | Meaning     |
| ------ | ----------- |
| `-A`   | Append rule |
| `-I`   | Insert rule |
| `-D`   | Delete rule |

---

## 🎯 Actions

| Action     | Description                                  |
| ---------- | -------------------------------------------- |
| ACCEPT     | Accept the packet                            |
| DROP       | Drop the packet silently (no response)       |
| REJECT     | Drop the packet and send a rejection message |
| LOG        | Log the packet details                       |
| MASQUERADE | Perform NAT masquerading                     |

---

## 🧩 iptables Command Examples & Explanations

---

### 1️⃣ Save Current Rules to a File

```bash
iptables-save >> <file_path>
```

💾 **Explanation:**
This command saves the current iptables rules to a file (`<file_path>`). Useful for backing up or persisting your firewall rules.

---

### 2️⃣ List Rules in Default Filter Table

```bash
iptables -nL
```

📜 **Explanation:**
Lists all rules in the default `filter` table, showing rules without resolving IPs to names (`-n` speeds it up).

---

### 3️⃣ List Rules in NAT Table

```bash
iptables -t nat -nL
```

🔄 **Explanation:**
Lists all NAT table rules. NAT is used for modifying packets, like translating IP addresses.

---

### 4️⃣ Allow Traffic from a Specific IP (Insert Rule)

```bash
iptables -t filter -I INPUT -s 192.168.1.100 -j ACCEPT
```

✅ **Explanation:**
Inserts (`-I`) a rule at the top of the `INPUT` chain to ACCEPT all packets coming from IP `192.168.1.100`.

---

### 5️⃣ Drop All Incoming Packets (Insert Rule)

```bash
iptables -t filter -I INPUT -j DROP
```

⛔ **Explanation:**
Inserts a rule to DROP all incoming packets on the `INPUT` chain, effectively blocking all new inbound traffic.

---

### 6️⃣ Append Drop Rule at End of INPUT Chain

```bash
iptables -t filter -A INPUT -j DROP
```

⏳ **Explanation:**
Appends (`-A`) a rule at the end of the `INPUT` chain to drop packets that don’t match previous ACCEPT rules.

---

### 7️⃣ Allow Incoming TCP Traffic on Port 22 (SSH)

```bash
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

🔓 **Explanation:**
Allows incoming TCP traffic on port 22, which is commonly used for SSH connections.

---

### 8️⃣ Drop Incoming TCP Traffic on Port 22 (SSH)

```bash
iptables -I INPUT -p tcp --dport 22 -j DROP
```

🚫 **Explanation:**
Inserts a rule to DROP all incoming TCP traffic destined for port 22, blocking SSH access.

---

### 9️⃣ Drop TCP Traffic From a Specific IP

```bash
iptables -A INPUT -p tcp -s 192.168.1.100 -j DROP
```

📵 **Explanation:**
Drops all incoming TCP packets coming from IP `192.168.1.100`.

---

### 🔟 Allow Incoming TCP Traffic on Port 443 (HTTPS)

```bash
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

🔐 **Explanation:**
Allows incoming TCP traffic on port 443, used for secure HTTPS connections.

---

### 1️⃣1️⃣ Allow Multiple Ports Using Multiport Module

```bash
iptables -A INPUT -p tcp -m multiport --dports 22,443,80,3306 -j ACCEPT
```

🎯 **Explanation:**
Accepts incoming TCP traffic on multiple ports at once: SSH (22), HTTPS (443), HTTP (80), and MySQL (3306).

---

### 1️⃣2️⃣ Allow Multiple Ports From a Specific Subnet

```bash
iptables -A INPUT -p tcp -m multiport --dports 22,443,80,3306 -s 192.168.10.0/24 -j ACCEPT
```

🏠 **Explanation:**
Allows TCP traffic on ports 22, 443, 80, and 3306 but only if it originates from the subnet `192.168.10.0/24`.

---

### 1️⃣3️⃣ Limit Incoming Connections on Port 80

```bash
iptables -A INPUT -p tcp --dport 80 -m limit --limit 100/minute --limit-burst 200 -j ACCEPT
```

🚦 **Explanation:**
Limits HTTP (port 80) incoming connections to 100 per minute with a burst of 200, helping prevent DoS attacks.

---

### 1️⃣4️⃣ Redirect HTTP Traffic to HTTPS on Interface `ens33`

```bash
iptables -t nat -A PREROUTING -i ens33 -p tcp --dport 80 -j REDIRECT --to-port 443
```

🔄 **Explanation:**
In the `nat` table's PREROUTING chain, this redirects all HTTP traffic (port 80) arriving on interface `ens33` to HTTPS port 443.

## 🎉 Summary

* **iptables** is a powerful Linux firewall tool
* Works by managing **tables**, **chains**, and **rules**
* Supports filtering, NAT, packet mangling, and raw processing
* Persistence through `iptables-persistent` package
* Flexible commands for network security and traffic control
