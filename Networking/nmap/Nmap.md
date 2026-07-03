### How to Install Nmap and Use Nmap for Scanning

1. **Update your system:**
```bash
sudo apt-get update
```

2. **Install Nmap:**
```bash
sudo apt install nmap
```

3. **Scan a single IP address:**
```bash
nmap [your_IP]
```

4. **Scan multiple IP addresses:**
```bash
nmap [your_IP1,your_IP2]
```

5. **Scan a range of IP addresses:**
```bash
nmap [your_IP1-your_IP100]
```

6. **Scan targets from a text file:**
```bash
nmap -iL filename.txt
```

7. **Check for live systems:**
```bash
nmap -sn [your_IP]
```

8. **Ping sweep:**
```bash
nmap -sP [your_IP]
```

9. **If ICMP is blocked:**
```bash
nmap -PN [your_IP]
```

10. **Scan specific port:**
```bash
nmap -p [your_port] [your_IP]
```
If ICMP is blocked:
```bash
nmap -PN [your_IP] -p [your_port]
```

11. **Scan multiple ports:**
```bash
nmap -p [port1,port2,port3-port6] [your_IP]
```

12. **Specify protocol:**
```bash
nmap -p http,https,ftp [your_IP]
```

13. **Scan TCP ports:**
```bash
nmap -p T:[port,port2] [your_IP]
```

14. **Get more information:**
```bash
nmap -p [your_port] -sV [your_IP]
```

15. **Detect operating system:**
```bash
nmap -O [your_IP] -p [your_port]
```

16. **Fast scan (top 100 ports):**
```bash
nmap -F [your_IP]
```

17. **Aggressive scan:**
```bash
nmap -A [your_IP] -p [your_port]
```

18. **Whois lookup:**
```bash
nmap -p [your_port] --script whois-ip [your_IP_or_domain]
```

19. **IP geolocation:**
```bash
nmap -p [your_port] --script ip-geolocation-* [IP]
```

20. **Detect Web Application Firewall (WAF):**
```bash
nmap -p [your_port] --script http-waf-detect [your_domain]
```

21. **Save results to a text file:**
```bash
nmap -Pn -p [your_port] [your_IP] -oN your_filename.txt
```

22. **Save results to an XML file:**
```bash
nmap -Pn -p [your_port] [your_IP] -oX filename.xml
```

23. **Save results to a grepable file:**
```bash
nmap -Pn -p [your_port] [your_IP] -oG filename.gnmap
```

24. **Save results to all formats:**
```bash
nmap -Pn -p [your_port] [your_IP] -oA filename
```

25. **Scan top ports:**
```bash
nmap --top-ports [number] [your_domain]
```

26. **Scan top ports and show open ones:**
```bash
nmap --top-ports [number] [your_domain] --open
```

27. **Check for open ports using different scan types:**
```bash
nmap -sT [your_IP]    # TCP Scan
nmap -sS [your_IP]    # SYN Scan
nmap -sX [your_IP]    # XMAS Scan
nmap -sF [your_IP]    # FIN Scan
nmap -sN [your_IP]    # Null Scan
```
