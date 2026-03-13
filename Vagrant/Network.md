# Vagrant Networking Configuration Guide (DevOps Oriented)

This document provides a structured reference for configuring Vagrant virtual machine networking, focusing on private, public, and forwarded port configurations commonly used in DevOps workflows.

---

## 1. Types of Networks

Vagrant supports multiple networking modes. This guide focuses on two primary types:

### 1.1 Private Network

A private network allows the VM to communicate only with the host or other VMs on the same private network. Often used for internal service communication or NAT-style layouts.

**NAT-based private network:**

```ruby
config.vm.network "private_network", type: "dhcp"
```

**Static IP private network:**

```ruby
config.vm.network "private_network", ip: "192.168.50.4"
```

**Static IP with manual configuration (no auto-config):**

```ruby
config.vm.network "private_network", ip: "192.168.50.4", auto_config: false
```

**IPv6 private network:**

```ruby
config.vm.network "private_network", ip: "fde4:8dba:82e1::c4"
```

---

### 1.2 Public Network

A public network bridges the VM directly to the physical network, making it appear as a full-fledged device on the LAN, similar to the host.

**Basic public network:**

```ruby
config.vm.network "public_network"
```

**Use DHCP-assigned default route:**

```ruby
config.vm.network "public_network", use_dhcp_assigned_default_route: true
```

**Static IP assignment:**

```ruby
config.vm.network "public_network", ip: "192.168.0.17"
```

**Specify network bridge interface:**

```ruby
config.vm.network "public_network", bridge: "en1: Wi-Fi (AirPort)"
```

**Multiple bridge options:**

```ruby
config.vm.network "public_network", bridge: [
  "en1: Wi-Fi (AirPort)",
  "en6: Broadcom NetXtreme Gigabit Ethernet Controller",
]
```

---

## 2. Port Forwarding

Port forwarding maps ports from the host machine to the guest VM, allowing external access to services running inside the VM.

### 2.1 Basic Port Forwarding

```ruby
config.vm.network "forwarded_port", guest: 80, host: 8080
```

### 2.2 Port Forwarding with Protocol Selection

```ruby
config.vm.network "forwarded_port", guest: 2003, host: 12003, protocol: "tcp"
config.vm.network "forwarded_port", guest: 2003, host: 12003, protocol: "udp"
```

### 2.3 Auto Correcting Port Conflicts

```ruby
config.vm.network "forwarded_port", guest: 80, host: 8080, auto_correct: true
```

### 2.4 Define a Usable Host Port Range

Useful when Vagrant must auto-correct ports within a controlled range.

```ruby
config.vm.usable_port_range = 8000..8999
```

