# tcpdump

## Overview

`tcpdump` is a powerful command-line packet analyzer used to capture and inspect network traffic in real time. It is widely used by DevOps engineers, network administrators, and security professionals for troubleshooting, monitoring, and debugging network-related issues.

It works by intercepting packets flowing through a network interface and displaying them based on defined filters.

---

## How tcpdump Works

### Packet Capture Mechanism

`tcpdump` relies on the **libpcap** library to capture packets. The process involves:

1. **Network Interface Access**
   - tcpdump attaches to a network interface (e.g., `eth0`, `ens33`, `wlan0`).

2. **Promiscuous Mode**
   - By default, tcpdump can enable promiscuous mode, allowing it to capture all packets on the network segment, not just those addressed to the host.

3. **Kernel-Level Filtering**
   - Uses Berkeley Packet Filter (BPF) to filter packets efficiently in the kernel space before sending them to user space.

4. **Packet Decoding**
   - Captured packets are decoded and printed in a human-readable format.

---

## Installation

### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install tcpdump
````

### Linux (RHEL/CentOS)

```bash
sudo yum install tcpdump
```

### macOS

```bash
brew install tcpdump
```

---

## Basic Syntax

```bash
tcpdump [options] [filter expression]
```

---

## Common Options

| Option              | Description                           |
| ------------------- | ------------------------------------- |
| `-i <interface>`    | Specify network interface             |
| `-c <count>`        | Capture a specific number of packets  |
| `-n`                | Disable hostname resolution           |
| `-nn`               | Disable hostname and port resolution  |
| `-v`, `-vv`, `-vvv` | Increase verbosity                    |
| `-X`                | Show packet contents in hex and ASCII |
| `-A`                | Display packet contents in ASCII      |
| `-w <file>`         | Write output to file                  |
| `-r <file>`         | Read packets from file                |
| `-s <snaplen>`      | Set capture size                      |
| `-D`                | List available interfaces             |

---

## Common Use Cases

### 1. Capture Packets on an Interface

```bash
tcpdump -i eth0
```

### 2. Capture a Limited Number of Packets

```bash
tcpdump -i eth0 -c 10
```

### 3. Disable Name Resolution (Faster Output)

```bash
tcpdump -nn -i eth0
```

### 4. Capture and Save to File

```bash
tcpdump -i eth0 -w capture.pcap
```

### 5. Read from a Capture File

```bash
tcpdump -r capture.pcap
```

---

## Filtering with BPF (Berkeley Packet Filter)

Filters are the most powerful feature of tcpdump.

### Basic Structure

```bash
tcpdump [options] 'filter expression'
```

### Filter Types

#### Host Filter

```bash
tcpdump host 192.168.1.1
```

#### Source/Destination Filter

```bash
tcpdump src 192.168.1.1
tcpdump dst 192.168.1.1
```

#### Port Filter

```bash
tcpdump port 80
tcpdump src port 443
tcpdump dst port 22
```

#### Protocol Filter

```bash
tcpdump tcp
tcpdump udp
tcpdump icmp
```

#### Network Filter

```bash
tcpdump net 192.168.1.0/24
```

---

## Combining Filters

### Logical Operators

| Operator | Meaning                    |
| -------- | -------------------------- |
| `and`    | Both conditions must match |
| `or`     | Either condition matches   |
| `not`    | Negates the condition      |

### Examples

```bash
tcpdump tcp and port 80
tcpdump host 192.168.1.1 and port 22
tcpdump not port 22
tcpdump tcp and (port 80 or port 443)
```

---

## Packet Output Interpretation

Example output:

```
14:32:10.123456 IP 192.168.1.10.54321 > 93.184.216.34.80: Flags [S], seq 123456, win 65535
```

### Breakdown

| Field       | Description                     |
| ----------- | ------------------------------- |
| Timestamp   | Packet capture time             |
| Protocol    | IP, ARP, etc.                   |
| Source      | Source IP and port              |
| Destination | Destination IP and port         |
| Flags       | TCP flags (SYN, ACK, FIN, etc.) |
| seq         | Sequence number                 |
| win         | Window size                     |

---

## TCP Flags

| Flag | Meaning                |
| ---- | ---------------------- |
| SYN  | Connection initiation  |
| ACK  | Acknowledgment         |
| FIN  | Connection termination |
| RST  | Reset connection       |
| PSH  | Push data immediately  |
| URG  | Urgent data            |

---

## Advanced Usage

### 1. Capture HTTP Traffic

```bash
tcpdump -i eth0 -A port 80
```

### 2. Capture HTTPS Traffic (Metadata Only)

```bash
tcpdump -i eth0 port 443
```

### 3. Capture DNS Queries

```bash
tcpdump -i eth0 port 53
```

### 4. Capture Traffic Between Two Hosts

```bash
tcpdump host 192.168.1.1 and 192.168.1.2
```

### 5. Capture Large Packets Fully

```bash
tcpdump -i eth0 -s 0
```

---

## Writing and Analyzing PCAP Files

### Capture to File

```bash
tcpdump -i eth0 -w traffic.pcap
```

### Analyze with tcpdump

```bash
tcpdump -r traffic.pcap
```

### Integration with Wireshark

* Export `.pcap` files and analyze using GUI tools like Wireshark.

---

## Performance Considerations

* Use `-n` or `-nn` to reduce DNS lookups.
* Apply filters to minimize captured data.
* Avoid capturing full packets unless necessary (`-s 0`).
* Use `-c` to limit capture size.

---

## Security and Permissions

* Requires root or sudo privileges:

```bash
sudo tcpdump -i eth0
```

* Be cautious when capturing sensitive data (credentials, tokens).

---

## Troubleshooting Scenarios

### 1. Debugging Connectivity Issues

```bash
tcpdump -i eth0 host <target-ip>
```

### 2. Checking Open Ports

```bash
tcpdump -i eth0 tcp port 22
```

### 3. Investigating Packet Loss

* Look for retransmissions and duplicate ACKs.

### 4. Diagnosing DNS Problems

```bash
tcpdump -i eth0 port 53
```

---

## Best Practices

* Always filter traffic to reduce noise.
* Capture only what is necessary.
* Store captures securely.
* Use rotation when capturing long sessions:

```bash
tcpdump -i eth0 -w file_%Y%m%d%H%M%S.pcap
```

---

## Limitations

* Cannot decrypt encrypted traffic (e.g., HTTPS).
* High traffic environments may drop packets.
* Output can become overwhelming without filters.

---

## Alternatives and Complementary Tools

* `tshark` (CLI version of Wireshark)
* `wireshark` (GUI packet analyzer)
* `ngrep` (network grep tool)
* `iftop` / `nload` (bandwidth monitoring)

---

## Summary

`tcpdump` is an essential tool in a DevOps engineer’s toolkit for low-level network inspection. Mastery of filtering, efficient capture strategies, and output interpretation enables effective debugging and monitoring of complex distributed systems.

