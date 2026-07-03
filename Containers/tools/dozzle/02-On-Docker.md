# **Dozzle Deployment Modes**

Dozzle offers multiple deployment modes to support a variety of architectures—from single-host setups to distributed multi-node clusters. Depending on your environment, you can run Dozzle in one of the following modes:

* **Standard Mode (default)** – Local logs from the Docker engine
* **Agent Mode** – Remote hosts exposed securely via TLS
* **Swarm Mode** – Distributed mesh network for Docker Swarm clusters
* **Hybrid (Swarm + Standalone Agents)** – Combine both for maximum flexibility

This section explains how each mode works and provides production-ready deployment examples.

---

# **1. Agent Mode**

Agent mode allows a Dozzle instance to expose its host’s container logs to other Dozzle servers over a secure **TLS-encrypted channel**. This is ideal for:

* Managing multiple remote Docker hosts
* Viewing logs from distributed machines in a single Dozzle UI
* Secure cross-host communication without VPNs

In agent mode, Dozzle runs with the `agent` subcommand and listens for remote connections.

---

## **Deploying a Dozzle Agent**

```yaml
services:
  dozzle-agent:
    image: amir20/dozzle:latest
    command: agent
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    ports:
      - 7007:7007
```

### **Customizing Agent Identity**

Agents can be assigned human-readable names using the `DOZZLE_HOSTNAME` variable:

```yaml
environment:
  - DOZZLE_HOSTNAME=my-special-name
```

---

## **Connecting a Dozzle Instance to One or More Agents**

Define the remote agents in the `DOZZLE_REMOTE_AGENT` variable. Multiple agents should be comma-separated.

```yaml
services:
  dozzle:
    image: amir20/dozzle:latest
    environment:
      - DOZZLE_REMOTE_AGENT=agent1:7007,agent2:7007
    ports:
      - 8080:8080
```

Once launched, the UI will display the remote agent hosts alongside local containers.

---

# **2. Swarm Mode**

Dozzle supports a special **Swarm Mode** designed for distributed Docker Swarm environments. When enabled, Dozzle automatically forms a **secure, fully encrypted mTLS mesh network** between all Dozzle nodes in the cluster.

### **Key features of Swarm Mode**

* Automatic discovery of all Dozzle instances
* Encrypted communication using mTLS
* Support for grouping logs by:

  * Docker stacks (`com.docker.stack.namespace`)
  * Docker Compose projects (`com.docker.compose.project`)
  * Swarm services (`com.docker.swarm.service.name`)

Swarm Mode is the recommended deployment method for multi-node clusters.

---

## **Deploying Dozzle in Swarm Mode**

Use `mode: global` to deploy Dozzle on every node:

```yaml
services:
  dozzle:
    image: amir20/dozzle:latest
    environment:
      - DOZZLE_MODE=swarm
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - 8080:8080
    networks:
      - dozzle
    deploy:
      mode: global
networks:
  dozzle:
    driver: overlay
```

### **Important:**

**Swarm mode cannot use Docker socket-proxy.**
This is a Docker limitation—Swarm services cannot directly access individual proxy instances, and Dozzle requires that direct access.

---

# **3. Adding Standalone Agents to Swarm Mode (v8.8.x+)**

Starting with **v8.8.x**, Dozzle allows you to mix **standalone agents** with a **Swarm-mode deployment**. Remote agents will appear as additional nodes in the Dozzle UI.

Example configuration:

```yaml
services:
  dozzle:
    image: amir20/dozzle:latest
    environment:
      - DOZZLE_MODE=swarm
      - DOZZLE_REMOTE_AGENT=agent:7007
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - 8080:8080
    networks:
      - dozzle
    deploy:
      mode: global
networks:
  dozzle:
    driver: overlay
```

This hybrid approach is ideal when part of your infrastructure runs in Swarm and other nodes run standalone Docker.

---

# **Summary**

| Mode                        | Best For                         | Key Features                         |
| --------------------------- | -------------------------------- | ------------------------------------ |
| **Standard**                | Single-host setups               | Local logs, simplest deployment      |
| **Agent Mode**              | Remote nodes, non-Swarm clusters | TLS-secured remote access            |
| **Swarm Mode**              | Multi-node Swarm clusters        | mTLS mesh networking, auto-discovery |
| **Hybrid (Swarm + Agents)** | Mixed environments               | Combine Swarm nodes + remote agents  |
