# 🚢 Understanding Dockerfile: A Complete Guide

---

## 📄 What is a Dockerfile?

A **Dockerfile** is a simple text file containing instructions to create a **Docker image**. Docker images provide a consistent, reproducible environment to run applications inside containers. By defining dependencies, configurations, and the operating system, Dockerfiles automate image creation, ensuring version-controlled and portable environments.

---

### 🔑 Key Concepts:

* 🏗️ **Base Image**: The foundational layer of your image, usually an official OS like Ubuntu, CentOS, or Alpine Linux.
* 📝 **Instructions**: Commands that tell Docker what to install, how the image behaves, and which files to include.

Common instructions include:

| Instruction | Description                                                      |
| ----------- | ---------------------------------------------------------------- |
| 🏃‍♂️ `RUN` | Executes commands inside the container (e.g., install software). |
| 📁 `COPY`   | Copies files from your local machine to the image.               |
| ▶️ `CMD`    | Specifies the default command when the container starts.         |

---

## 🛠️ Step-by-Step Guide to Creating a Dockerfile

---

### 1️⃣ Create a File Named `Dockerfile`

Create a file called `Dockerfile` in your project directory. If named differently, specify the filename during build.

#### Example Dockerfile:

```dockerfile
# 🐧 Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# 🏷️ Add metadata such as version information
LABEL version="0.0.1"

# 🔄 Update package lists and install essential tools
RUN apt update && apt install -y bash vim curl

# 🌐 Install Nginx web server
RUN apt install -y nginx
```

**Explanation:**

* `FROM ubuntu:22.04` — Use Ubuntu 22.04 as the base image.
* `LABEL version="0.0.1"` — Adds version metadata.
* `RUN` — Executes commands inside the container to install tools and software.

---

### 2️⃣ Example Using Alpine Linux

Alpine Linux is lightweight and creates smaller images.

```dockerfile
# 🐧 Use Alpine as the base image
FROM alpine

# 🏷️ Add version metadata
LABEL version="0.0.1"

# 🔄 Update package lists and install essential tools
RUN apk update && apk add bash vim curl
```

Perfect for a compact, minimalistic image.

---

### 3️⃣ Complex Dockerfile with a Script

```dockerfile
# 🐧 Start with Alpine as the base image
FROM alpine

# 🏷️ Add metadata
LABEL version="0.0.1"

# 🔄 Update packages and install essential tools
RUN apk update && apk add bash vim curl iputils-ping

# 📂 Copy the script into the image
COPY <local-file-path> <container-destination-path>

# 🏠 Set working directory
WORKDIR <container-destination-path>

# 🌿 Add environment variables
ENV API_KEY="123445"

# 👤 Set user and expose ports
USER deploy
EXPOSE 3210

# ⚙️ Make the script executable
RUN chmod +x app.sh

# ▶️ Default command to run
CMD ["./app.sh"]
# Alternatively, ENTRYPOINT ensures always running the executable
ENTRYPOINT ["bash", "./app.sh"]
```

---

### ❤️ Health Check Setup

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
```

* ⏲️ **interval**: time between checks
* ⏳ **timeout**: fail if check takes longer than 5 seconds
* 🔄 **retries**: mark container unhealthy after failed attempts
* 🛡️ **start-period**: grace period before counting failures

---

### 4️⃣ Build Your Docker Image

```bash
docker build -t <app-name> <path-to-dockerfile>
```

**Examples:**

* Build with Dockerfile in current directory:

  ```bash
  docker build -t app-test .
  ```
* Use custom Dockerfile name:

  ```bash
  docker build -t app-test -f <CustomDockerfile> .
  ```
* Build without cache:

  ```bash
  docker build -t app-test:v1 -f <Custom-Dir> . --no-cache
  ```

---

## 📋 Summary

A **Dockerfile** is a powerful tool for automating Docker image creation:

1. 📝 **Create a Dockerfile**: Define the image with `FROM`, `RUN`, `COPY`, and `CMD`.
2. 🏗️ **Build the Image**: Use `docker build` to generate your image.
3. 🚀 **Run the Container**: Use `docker run` to start your container.

