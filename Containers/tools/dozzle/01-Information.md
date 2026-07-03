# **Dozzle – Real-Time Docker Log Viewer**

## **Overview**

**Dozzle** is an open-source, lightweight, web-based log viewer designed to simplify monitoring and debugging Docker containers. Sponsored by **Docker OSS** and actively maintained by **Amir Raminfar**, Dozzle provides real-time log streaming with an intuitive and efficient UI.

Optimized for developers, DevOps engineers, and system administrators, Dozzle offers:

* **Live log streaming** directly from containers
* **Search and filtering capabilities**
* **JSON log support** with intelligent color coding
* **A minimal footprint**, making it ideal for any environment

Dozzle is distributed under the **MIT license**, ensuring free and open use across development and production workflows.

---

## **Key Features**

### **🔹 Real-Time Log Streaming**

Instantly view logs as they are generated, enabling faster debugging and container monitoring.

### **🔹 Web-Based Interface**

No need for additional CLI commands—open your browser and start exploring logs immediately.

### **🔹 Lightweight & Fast**

Runs with minimal resource usage, suitable for both development setups and production Docker hosts.

### **🔹 Simple Installation**

Deployable with a single Docker command or via Docker Compose. No complex setup required.

### **🔹 Secure Local Access**

Works by reading the Docker daemon socket (`/var/run/docker.sock`), ensuring direct and secure interaction with local containers.

---

## **Installation & Setup**

### **Using Docker CLI (Recommended)**

The simplest way to run Dozzle is by mounting the Docker socket file:

* The Docker socket is typically located at:
  **`/var/run/docker.sock`**
* Dozzle listens on **port 8080** by default, but you can remap it using `-p` if needed.

```bash
docker run -d \
  --name dozzle \
  -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  amir20/dozzle:latest
```

Once running, access Dozzle at:
➡️ **[http://localhost:8080](http://localhost:8080)**

---

## **Using Docker Compose**

For environments managed with Compose, use the following configuration:

```yaml
services:
  dozzle:
    image: amir20/dozzle:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - 8080:8080
```

Start the service:

```bash
docker compose up -d
```

---

## **Swarm Deployment**

Dozzle can also be deployed as a Swarm service for distributed environments.

