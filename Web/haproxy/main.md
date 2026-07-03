# HAProxy Configuration Guide

## Overview

**HAProxy** (High Availability Proxy) is an open-source TCP/HTTP load balancer and proxying solution designed to improve the performance and reliability of server environments by distributing incoming requests across multiple servers. HAProxy can be deployed on Linux, macOS, and FreeBSD, and it’s widely used by large-scale platforms, including GitHub, Instagram, and Twitter, for load balancing and failover purposes.

This guide will help you install and configure HAProxy, set up load balancing rules, and enable monitoring for your HAProxy instance.

---

## Installation

Install HAProxy using the following commands:
```bash
sudo apt update && sudo apt install haproxy -y
```

Once installed, HAProxy’s primary configuration file is located at `/etc/haproxy/haproxy.cfg`.

---

## Configuration Structure

HAProxy’s configuration file is divided into multiple sections, each with specific settings:

- **Global**: Contains settings that affect the HAProxy process as a whole.
- **Defaults**: Applies default settings for other sections, such as timeout values and mode (HTTP or TCP).
- **Frontend**: Defines the entry points for traffic (IP addresses and ports where clients connect).
- **Backend**: Specifies server pools that handle the requests from the frontend.
- **Listen**: Combines frontend and backend functions for simple setups or specific server groups.
  
### Step 1: Configuring Defaults

Open the configuration file with a text editor:
```bash
sudo vim /etc/haproxy/haproxy.cfg
```

Define default settings for HAProxy:

```conf
defaults
    mode http
    timeout client 5s
    timeout connect 5s
    timeout server 5s
    timeout http-request 5s
```

#### Explanation of Key Parameters:

- **mode**: Sets the mode to either `http` (for HTTP traffic) or `tcp` (for raw TCP traffic). Use `http` for web traffic.
- **timeout client**: Time HAProxy waits for data from the client.
- **timeout connect**: Time to establish a connection with a backend server.
- **timeout server**: Time HAProxy waits for the server to send data.
- **timeout http-request**: Time HAProxy waits for a complete HTTP request from the client.

Adjust these values based on your needs to optimize performance and prevent timeouts.

---

### Step 2: Setting Up the Frontend

The `frontend` section defines how HAProxy receives incoming connections.

Example configuration:

```conf
frontend my_frontend
    bind 127.0.0.1:80
    default_backend my_backend
```

- **bind**: Specifies the IP address and port where HAProxy listens for incoming requests.
- **default_backend**: Defines the backend that handles requests sent to this frontend.

---

### Step 3: Configuring Backend Servers

The `backend` section defines the pool of servers that will handle requests from the frontend.

Example configuration:

```conf
backend my_backend
    balance leastconn
    server server1 127.0.0.1:8001 check
    server server2 127.0.0.1:8002 check
```

- **balance**: The load-balancing algorithm. Here, `leastconn` ensures that new requests go to the server with the fewest active connections.
- **server**: Defines a backend server with IP, port, and optional health check parameters (`check` enables health checks for each server).

---

### Step 4: Advanced Load-Balancing Rules with Conditions

To implement conditional routing, define multiple backend groups with conditional statements:

```conf
frontend my_frontend
    bind 127.0.0.1:81, 127.0.0.1:82, 127.0.0.1:83
    use_backend first if { dst_port = 81 }
    use_backend second if { dst_port = 82 }
    default_backend third

backend first
    server server1 127.0.0.1:8001 check

backend second
    server server2 127.0.0.1:8002 check

backend third
    server server3 127.0.0.1:8003 check
```

- **use_backend**: Redirects requests to specific backends based on conditions, such as destination port.
  
---

### Step 5: Enabling Monitoring and Statistics

HAProxy includes a built-in statistics module, allowing you to monitor server health and traffic in real-time.

To enable monitoring, add a `listen` section:

```conf
global
    stats socket /run/haproxy/admin.sock mode 660 level admin

defaults
    mode http
    timeout client 10s
    timeout connect 5s
    timeout server 10s
    timeout http-request 10s

frontend my_frontend
    bind 127.0.0.1:80
    default_backend my_backend

backend my_backend
    balance leastconn
    server server1 127.0.0.1:8001 check
    server server2 127.0.0.1:8002 check

listen stats
    bind :8000
    stats enable
    stats uri /monitoring
    stats auth username:password
```

- **stats socket**: Specifies the Unix socket for administrative commands.
- **stats uri**: Sets the URI endpoint for monitoring (e.g., `http://localhost:8000/monitoring`).
- **stats auth**: Enables basic authentication for the monitoring interface. Replace `username:password` with your desired credentials.

---

### Finalizing and Testing the Configuration

1. **Check HAProxy Configuration Syntax**:
   Run the following command to validate your configuration file:
   ```bash
   sudo haproxy -c -f /etc/haproxy/haproxy.cfg
   ```

2. **Restart HAProxy**:
   If there are no syntax errors, restart HAProxy to apply the new configuration:
   ```bash
   sudo systemctl restart haproxy
   ```

3. **Access Monitoring Dashboard**:
   Open a web browser and go to `http://your_server_ip:8000/monitoring`. Use the credentials you set in `stats auth` to log in and view real-time statistics.

