# 📦 Docker Swarm Documentation

Comprehensive guide to managing a **Docker Swarm** cluster. This document includes core commands, workflows, and best practices for maintaining a healthy and operational environment.

---

## 📚 Table of Contents

1. [🔧 Cluster Health & Manager Count](#-cluster-health--manager-count)
2. [🚀 Example Workflow: Setting Up Nginx](#-example-workflow-setting-up-nginx)
3. [⚙️ Cluster Initialization and Management](#️-cluster-initialization-and-management)
4. [🖥️ Node Management](#️-node-management)
5. [🛠️ Service Management](#️-service-management)
6. [🔑 Join Tokens & Node Configuration](#-join-tokens--node-configuration)

---

## 🔧 Cluster Health & Manager Count

A Docker Swarm cluster requires a **majority of manager nodes** to be functional for quorum.

> **Best Practice:** Always maintain **more than 50%** manager nodes online. Losing quorum will render the cluster non-operational.

---

## 🚀 Example Workflow: Setting Up Nginx

Docker Swarm handles service deployment through several internal components:

1. **API** – Receives service requests.
2. **Allocator** – Determines resource allocation.
3. **Dispatcher** – Assigns tasks to nodes.
4. **Scheduler** – Places tasks on optimal nodes.

This process ensures resilient and efficient service distribution.

---

## ⚙️ Cluster Initialization and Management

### 🔹 Initialize Cluster

```bash
docker swarm init
```

### 🔹 Initialize with Specific Interface

```bash
docker swarm init --advertise-addr <ip-or-interface>
```

### 🔹 Join Existing Cluster

```bash
docker swarm join
```

### 🔹 Leave Cluster

```bash
docker swarm leave
```

### 🔹 Unlock a Manager Node

```bash
docker swarm unlock
```

---

## 🖥️ Node Management

### 🔸 List Nodes

```bash
docker node ls
```

**Example Output:**

```
ID                            HOSTNAME   STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
8yw8jrjeqczaci0qkuy060g09 *   docker-1   Ready     Active         Leader           24.0.5
v4gvf7xenw0izmxgvhr6hb2rj     docker-2   Ready     Active                          24.0.5
kd3ujmt1ey3pw6v9189fouxfa     docker-3   Ready     Active         Reachable        24.0.5
tm1msy58ztcltt36rs1lb76p7     docker-4   Down      Active                          24.0.5
```

### 🔸 Remove a Node

```bash
docker node rm <node-id>
```

### 🔸 Promote to Manager

```bash
docker node promote <hostname-or-id>
```

### 🔸 Inspect a Node

```bash
docker node inspect <nodename>
```

### 🔸 Change Node Role

```bash
docker node update --role manager <nodename>
docker node update --role worker <nodename>
```

### 🔸 Change Node Availability

```bash
docker node update --availability active <nodename>
docker node update --availability pause <nodename>
docker node update --availability drain <nodename>
```

### 🔸 Add or Remove Labels

**Add:**

```bash
docker node update --label-add env=development <nodename>
docker node update --label-add env=testing <nodename>
```

**Remove:**

```bash
docker node update --label-rm env= <nodename>
docker node update --label-rm env <nodename>
```

**Use label constraints in service deployment:**

```yaml
deploy:
  placement:
    constraints:
      - node.labels.env == development
```

---

## 🛠️ Service Management

### 🔹 Show Tasks on a Node

```bash
docker node ps
```

### 🔹 List All Services

```bash
docker service ls
```

### 🔹 Create a New Service

```bash
docker service create --name <service-name> <image-name>
```

### 🔹 Scale a Service

```bash
docker service scale <service-name>=<replica-count>
```

**Example:**

```bash
docker service scale nginx=5
```

### 🔹 Inspect a Service

```bash
docker service inspect <service-name>
```

### 🔹 Create Service with Replicas, Env Vars, and Port Mapping

```bash
docker service create \
  --name <service-name> \
  --replicas <count> \
  --env <ENV_VAR=value> \
  --publish <host-port>:<container-port> \
  <image-name>
```

**Example:**

```bash
docker service create \
  --name nginx \
  --replicas 3 \
  --env MY_ENV_VAR=value \
  --publish 8080:80 \
  nginx
```

---

## 🔑 Join Tokens & Node Configuration

Securely add nodes to your Swarm using join tokens.

### 🔹 Get Worker Token

```bash
docker swarm join-token worker
```

### 🔹 Get Manager Token

```bash
docker swarm join-token manager
```

