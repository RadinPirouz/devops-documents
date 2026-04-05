# 02. Commands – Practical `hping3` Usage

This document explains common `hping3` commands and what they do at a packet/protocol level.  
Replace `<target>` with an IP or hostname, and `<port>` with a TCP/UDP port number.

> Use these commands only on systems and networks you are authorized to test.

---

## 1. ICMP “Normal Ping”
```bash
hping3 -1 <target>
```
- `-1`: Use **ICMP mode** (type 8 echo request), similar to the standard `ping` command.
- Behavior:
  - Sends ICMP echo request packets to `<target>`.
  - Measures round-trip time (RTT) and indicates packet loss.
- Use case:
  - Basic connectivity check when you want to use `hping3` instead of `ping`.
  - Helpful if you want later to switch to more advanced testing without changing tools.

---

## 2. Send TCP ACK Packets

```bash
hping3 -A <target>
```

- `-A`: Set the **ACK** flag in TCP packets.
- Behavior:
  - Sends TCP packets with the ACK flag set to the default port (0 unless `-p` is specified).
- Use case:
  - Test firewall rules related to **established** connections (many firewalls allow ACK packets but block SYN).
  - Map which hosts respond to unsolicited ACK packets and how (RST/no response).

To target a specific port (for example, 80):

```bash
hping3 -A <target> -p 80
```
---

## 3. Send TCP SYN Packets

```bash
hping3 -S <target>
```

- `-S`: Set the **SYN** flag in TCP packets.
- Behavior:
  - Sends SYN packets to the default port (0 unless `-p` is specified).
- Use case:
  - Test how the target responds to connection attempts.
  - When combined with `-p`, this becomes a basic SYN scan for that port.

With a specific port:

```bash
hping3 -S <target> -p <port>
```
---

## 4. Send TCP FIN Packets

```bash
hping3 -F <target>
```
- `-F`: Set the **FIN** flag in TCP packets.
- Behavior:
  - Sends packets that look like “finish” requests for a connection.
- Use case:
  - Perform **FIN scans** (when combined with `-p`) to check firewall behavior:
- Closed ports typically respond with `RST`.
- Open ports often send no response.
  - Useful for testing how devices treat non-SYN traffic.

Example with a port:

```bash
hping3 -F <target> -p 80
```
---

## 5. Send TCP RST (Reset) Packets

```bash
hping3 -R <target>
```
- `-R`: Set the **RST** flag in TCP packets.
- Behavior:
  - Sends packets that instruct the receiver to immediately terminate a connection.
- Use case:
  - Observe how the target or firewall handles unexpected RST packets.
  - In controlled tests, can be used to tear down test connections.

With a specific port:

```bash
hping3 -R <target> -p 80
```
---

## 6. Send TCP URG (Urgent) Packets

```bash
hping3 -U <target>
```
- `-U`: Set the **URG** flag in TCP packets.
- Behavior:
  - Marks data as “urgent” (though most modern applications rarely use it).
- Use case:
  - Test how TCP stacks and firewalls handle **uncommon flags**.
  - Validate logging/alerting for rare or suspicious traffic patterns.

Example with a port:

```bash
hping3 -U <target> -p 80
```
---

## 7. Send XMAS Packets

```bash
hping3 -X <target>
```
- `-X`: Send **XMAS** packets (commonly FIN + PSH + URG flags set).
- Behavior:
  - Creates “Christmas tree” packets with multiple flags lit.
- Use case:
  - **XMAS scans**:
- Closed ports usually respond with `RST`.
- Open ports often do not respond.
  - Test firewall/IDS handling of obviously suspicious packets.

Example with a port:

```bash
hping3 -X <target> -p 80
```
---

## 8. Send SYN Packet to a Destination Port

```bash
hping3 -S <target> -p <port>
```

- `-S`: SYN flag.
- `-p <port>`: Destination port.
- Behavior:
  - Sends a TCP SYN packet to the specified `<port>` on `<target>`.
- Use case:
  - Simple port check:
- Open port: typically responds with SYN/ACK.
- Closed port: typically responds with RST.
  - Validate firewall rules for a specific service port.

---

## 9. Send SYN Packets with Random Source Address

```bash
hping3 -S <target> --rand-source
```

- `-S`: SYN flag.
- `--rand-source`: Randomize the **source IP address** for each packet.
- Behavior:
  - Target sees SYN packets as if they are coming from many different IPs.
- Use case (legitimate, controlled testing):
  - Test how firewalls, load balancers, or DDoS protection handle **spoofed** or distributed-looking traffic.
  - Validate rate-limiting or connection limiting across “different” clients.

Note: Because of IP spoofing, responses will not come back to you; this is for observing target-side behavior/logs.

---

## 10. SYN Flood with Random Source

```bash
hping3 -S <target> --rand-source --flood
```
- `-S`: SYN flag.
- `--rand-source`: Randomize source IP per packet.
- `--flood`: Send packets as fast as possible, no output per packet.
- Behavior:
  - High-rate SYN traffic with spoofed source IPs.
- Use case:
  - **Stress testing** and **capacity testing** of firewalls/load balancers/IPS in a lab or authorized environment.
- Warning:
  - This can severely impact services and look like a SYN flood attack.
  - Use only with explicit permission and monitoring in place.

---

## 11. ICMP Flood with Spoofed Source Address

```bash
hping3 -1 <target> -a <src-address> --flood
```
> Note: Your original example used `-i`, but for ICMP mode it should be `-1`.

- `-1`: ICMP mode (echo requests).
- `-a <src-address>`: Spoof **source IP** as `<src-address>`.
- `--flood`: Send packets as fast as possible.
- Behavior:
  - Sends a high-rate ICMP echo request flood to `<target>` with a fake source IP.
- Use case:
  - Test how devices handle **ICMP flood** conditions and spoofed traffic (in a controlled environment).
- Warning:
  - Can consume bandwidth and trigger DDoS protections or rate limits.
  - Only for authorized stress testing.

If you really meant `-i` (interval), that changes send rate instead of protocol:

```bash
hping3 -1 <target> -a <src-address> --flood
# or with custom interval (e.g., 10 ms):
hping3 -1 <target> -a <src-address> -i u10000
```
---

## 12. Check If Port 22 (SSH) Is Open

```bash
hping3 -S <target> -p 22 -c 1
```

- `-S`: SYN flag (start of TCP handshake).
- `-p 22`: Destination port 22 (typically SSH).
- `-c 1`: Send only **one** packet.
- Behavior:
  - Sends a single SYN to port 22 on `<target>`.
- How to interpret:
  - If you see a **SYN/ACK** response, port 22 is likely open and reachable.
  - If you see a **RST**, port 22 is closed or actively refused.
  - If there is **no response**, the port may be filtered by a firewall or silently dropped.

---

## Summary

- `-1`: ICMP mode (ping-like).
- `-S`, `-A`, `-F`, `-R`, `-U`, `-X`: Control which TCP flags are set (SYN, ACK, FIN, RST, URG, XMAS).
- `-p <port>`: Target a specific port.
- `--rand-source`: Spoof/randomize source IPs.
- `-a <src-address>`: Spoof a specific source IP.
- `--flood`: Send packets as fast as possible (for stress testing).
- `-c <count>`: Limit number of packets sent.

