iptable work with net filter

connection type:
1. new
2. stablished
3. Related 

iptable-persitant --> install iptables and save in iptables file 


defualt path --> /etc/iptables

command format

```bash
iptables -t <table-names> <option> <chain-name> <match> -j <action>
```
table name: 
1. filter (default) --> Filtering Packets
2. nat --> Nating Service
3. mangel --> Edit Packets
4. raw --> edit packets before prossecc by os

chains: 

1. filter:
    1. INPUT
    2. OUTPUT
    3. Forward
2. nat
    1. OUTPUT
    2. PREROUTING
    3. PASTROUTING
3. mangle
    1. INPUT
    2. OUTPUT
    3. Forward
    4. PREROUTING
    5. PASTROUTING
4. raw
    1. OUTPUT
    2. PREROUTIUNG

INPUT : Connection Incomming into Server
OUTPUT : Packets Outgoiing From server
FORWARD : Packer incomming to server but the target is not server (routing)
PREROUTING : EDIT Packets Before Routing 
PASTROUTING : Edit Packet After Routing And Before Exit From Server

option:
1. `-A`: Append
2. `-I`: Insert
3. `-D`: Delete

actions:
ACCEPT: accept the packet
DROP: drop the packer without any msg
REJECT: drop the packet with send message to packet sender
LOG: Log The Packet 
MASQUERADE: Nating

```bash
iptables-save >> <file_dir>
```

```bash
iptables -nL
```
```bash
iptables -t nat -nL
```

```bash
iptables -t filter -I INPUT -s 192.168.1.100 -j ACCEPT 
```

```bash
iptables -t filter -I INPUT -j DROP 
```

```bash
iptables -t filter -A INPUT -j DROP 
```

```bash
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

```bash
iptables -I INPUT -p tcp --dport 22 -j DROP 
```

```bash
iptables -A INPUT -p tcp -s 192.168.1.100 -j DROP
```
```bash
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

```bash
les -A INPUT -p tcp -m multiport --dport 22,443,80,3306 -j ACCEPT
```

```bash
iptables -A INPUT -p tcp -m multiport --dport 22,443,80,3306 -d 192.168.10.0/24 -j ACCEPT
```

```bash
iptables -A INPUT -p tcp --dport 80 -m limit --limit 100/minute --limit-burst 200 -j ACCEPT
```

```bash
iptables -t NAT -A PREROUTING -i ens33 -p tcp --dport 80 -j REDIRECT --to-port 443
```
