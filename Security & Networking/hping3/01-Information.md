# 01. Information – What is `hping3`?

## Overview

`hping3` is a powerful network tool used primarily for:

- Crafting and sending custom TCP/IP packets  
- Testing firewalls and intrusion detection systems (IDS/IPS)  
- Network scanning, mapping, and discovery  
- Performance and connectivity testing (latency, MTU, path issues)

From a DevOps/SRE perspective, `hping3` is like a “Swiss Army knife” for low‑level network troubleshooting and security‑oriented testing. It allows you to send packets with very precise control over headers and flags, which goes far beyond what tools like `ping` or `traceroute` can do.

> Note: `hping3` should be used only on networks and systems you are authorized to test. It can easily be mistaken for malicious traffic.

---

## Key Capabilities

### 1. Custom Packet Crafting

`hping3` lets you build packets with specific parameters:

- **IP layer**:
  - Source/destination IP
  - TTL, fragmentation, IP ID
- **TCP layer**:
  - Source/destination port
  - Flags (SYN, ACK, FIN, RST, PSH, URG)
  - Sequence/ack numbers
- **UDP & ICMP**:
  - Custom payloads
  - Port selection (UDP)
  - ICMP type and code

This is useful for:

- Reproducing odd traffic patterns seen in logs  
- Simulating client behavior at the packet level  
- Testing how devices and middleboxes handle specific combinations of flags

---

### 2. Stateful Firewall & IDS Testing

Because `hping3` can manipulate flags and headers, it is commonly used to test:

- Firewall rules (ingress/egress)  
- NAT behavior  
- IDS/IPS detection and blocking

Examples of what you can validate:

- Whether SYN packets to certain ports are correctly blocked or allowed  
- How a firewall responds to fragmented packets  
- Whether “stealth” scans are detected by security tooling

---

### 3. Port Scanning and Host Discovery

`hping3` can act as a flexible port scanner:

- TCP SYN scans on specific ports or ranges  
- FIN/XMAS/NULL scans to observe firewall behavior  
- Host discovery based on custom probes (TCP/UDP/ICMP)

While tools like `nmap` are more convenient for general scanning, `hping3` is useful when you need precise control over how probes are sent or you want to emulate specific traffic patterns.

---

### 4. Network Performance & Path Testing

`hping3` can be used to measure:

- Round-trip time (RTT) for various protocols and ports  
- Packet loss and jitter under different conditions  
- MTU/path issues with fragmentation control

Typical use cases:

- Measuring latency to a specific TCP port (e.g., 443) instead of relying on ICMP `ping`  
- Determining whether ICMP is blocked and testing alternative paths with TCP/UDP  
- Debugging connectivity problems through stateful devices that treat ICMP differently from TCP

---

### 5. Traceroute-like Functionality

`hping3` can perform traceroute‑style path discovery, but using TCP or UDP instead of ICMP:

- Helps when ICMP is filtered or rate-limited  
- Shows how TCP packets to specific ports traverse the network

This is useful when:

- ICMP-based `traceroute` doesn’t give meaningful results  
- You need path information for application ports (e.g., 80, 443, 5432)

---

## Why DevOps/SRE Engineers Care

In modern environments (cloud, containers, microservices), networking problems often involve:

- Security groups, NACLs, firewalls  
- Load balancers and proxies  
- Overlay networks (e.g., Kubernetes CNI)  
- Complex routing or NAT

`hping3` helps you:

- Validate security rules (e.g., between Kubernetes nodes, across VPCs/VNETs)  
- Troubleshoot weird connectivity issues that don’t show up with `ping`  
- Investigate asymmetrical routing or stateful filtering  
- Reproduce network conditions reported by applications or logs

It is especially valuable when standard utilities (`ping`, `curl`, `telnet`, `nc`) aren’t enough to reveal how packets are handled in transit.

---

## TCP Flags & Special Packets (FIN, URG, RST, XMAS) and Flooding

`hping3` gives you direct control over TCP flags. Understanding these is crucial for using it correctly and interpreting responses.

### FIN (Finish) flag / FIN packet

- **What it is**:  
  The FIN flag indicates that the sender has finished sending data and wants to gracefully close the TCP connection.
- **Normal use**:  
  Used at the end of a TCP session as part of the connection teardown (FIN/ACK, ACK).
- **In scanning/testing**:  
  - A **FIN scan** sends packets with only the FIN flag set to a port.  
  - On a **closed port**, the target should respond with `RST`.  
  - On an **open port**, many TCP/IP stacks ignore the packet (no response).  
  This behavior is used to infer whether ports are open/filtered without sending SYN packets that might be logged more aggressively.

### URG (Urgent) flag / URG packet

- **What it is**:  
  URG marks that some of the data in the TCP segment is “urgent” and should be prioritized by the receiving host.
- **Normal use**:  
  Rarely used in modern applications. Historically used for things like interrupt signals.
- **In scanning/testing**:  
  Setting the URG flag along with other flags can:
  - Stress or test how TCP stacks handle unusual or rarely seen combinations  
  - Help detect middleboxes that mishandle or log such packets  
  Tools like `hping3` can create URG packets to see how targets or firewalls react.

### RST (Reset) flag / RST packet

- **What it is**:  
  The RST flag instructs the receiver to immediately terminate the TCP connection.
- **Normal use**:  
  - Sent when a packet arrives for a port where no service is listening.  
  - Used to abort a connection abruptly (e.g., when a process crashes or refuses a connection).
- **In scanning/testing**:  
  - When you send a SYN to a **closed** port, a typical response is a `RST` packet.  
  - Tools use the presence or absence of RST to determine whether a port is open or closed.  
  - You can also send RST packets to tear down existing connections (for testing, in controlled environments).

### XMAS packet

- **What it is**:  
  A “XMAS” (Christmas tree) packet is a TCP packet with multiple flags set at once, commonly: **FIN, PSH, URG**.
- **Why the name**:  
  It’s called a “Christmas tree” packet because many flags are “lit up” at the same time, like lights on a tree.
- **In scanning/testing**:
  - Used for **XMAS scans**.  
  - Similar to FIN scans:
    - On **closed** ports, the host often responds with `RST`.  
    - On **open** ports, many stacks send no reply.  
  - Some older or non-standard TCP/IP stacks respond differently, leaking information about OS type or configuration.
- **Firewall/IDS behavior**:  
  XMAS packets are unusual and often treated as suspicious, so many devices log or drop them, which can be useful for testing detection.

---

## What is a Flood?

In the context of `hping3` and network testing, a **flood** means sending a very high rate of packets to a target, typically as fast as possible.

- **Purpose in legitimate testing**:
  - Stress-test network devices (firewalls, load balancers, routers).  
  - Identify bottlenecks or performance limits in network paths.  
  - Observe how systems behave under heavy packet load (Do they drop packets? Do they rate-limit?).
- **Types of floods (conceptually)**:
  - **SYN flood**: flood of TCP SYN packets to a port.  
  - **ICMP flood**: flood of ICMP echo requests.  
  - **UDP flood**: flood of UDP packets.
- **Use in `hping3`**:
  - `hping3` can send packets in “flood mode” (no delays between packets).  
  - This is powerful and potentially disruptive: packet floods can consume bandwidth and CPU, degrade service, or trigger protective mechanisms.
- **Operational considerations**:
  - Only perform flood tests on infrastructure you control and where such testing is explicitly allowed.  
  - Coordinate with network and security teams.  
  - Monitor carefully (CPU, memory, bandwidth, and logs) during tests to avoid unintended outages.

---

## Typical Usage Contexts

- **On-prem / data center**:  
  Test firewalls, routers, and IDS, validate segmentation between environments (e.g., prod vs. non‑prod).

- **Cloud environments (AWS/Azure/GCP/etc.)**:  
  - Verify security group/NACL behavior at the packet level.  
  - Test connectivity between VPCs/VNETs, on‑prem VPNs, and cloud workloads.

- **Kubernetes & containerized apps**:  
  - Validate node-to-node or pod-to-pod connectivity.  
  - Test ingress/egress rules in CNIs and service meshes.  
  - Debug why a service is reachable via one path but not another.

---

## Limitations & Considerations

- Requires appropriate privileges (often root) to craft raw packets.  
- Can generate traffic patterns similar to port scans or attacks, so:
  - Always get proper authorization.  
  - Coordinate with security teams to avoid false alarms.
- Not designed as a full replacement for higher-level tools (e.g., `nmap`, `iperf`, `traceroute`), but as a complementary low-level tool.
- Behavior may differ slightly across OSes and network stacks.

---

## Installation (High-Level)

Availability varies by distribution, but generally:

- **Debian/Ubuntu**: via `apt` (package usually named `hping3`)  
- **RHEL/CentOS/Fedora**: via `yum`/`dnf` or EPEL  
- **macOS**: via Homebrew (if available) or compile from source  
- **Others**: typically built from source from the official repository

(Installation instructions can be detailed in a separate document.)

---

## Summary

`hping3` is a low-level TCP/IP packet crafting and analysis tool used by DevOps/SRE and security engineers to:

- Test and validate firewall and network security policies  
- Perform targeted port scans (including FIN/XMAS-style scans) and host discovery  
- Troubleshoot complex connectivity and performance issues  
- Generate controlled floods for stress tests (in authorized environments)
