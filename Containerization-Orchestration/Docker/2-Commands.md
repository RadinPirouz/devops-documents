# **Docker Commands Guide**

## **1. Docker Data Directories**
Docker stores essential data, including images, containers, and volumes, in specific directories.

- **`/var/lib/docker/`**: Main directory for Docker's data, including images, containers, and volumes.
- **`/var/lib/docker/containers/`**: Stores configuration files for individual containers.
- **`/var/lib/docker/volumes/`**: Stores data for Docker volumes, which persist beyond the container’s lifecycle.

---

## **2. Installing Docker on Ubuntu**

### **Step 1: Update Package List and Install Dependencies**
```bash
sudo apt update && sudo apt install -y ca-certificates curl
```
- **`sudo apt update`**: Refreshes the package list.
- **`sudo apt install -y ca-certificates curl`**: Installs certificates and `curl` to securely download Docker packages.

### **Step 2: Add Docker’s GPG Key**
```bash
sudo install -m 0755 -d /etc/apt/keyrings 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc 
sudo chmod a+r /etc/apt/keyrings/docker.asc
```
- **`install -m 0755 -d /etc/apt/keyrings`**: Creates the `/etc/apt/keyrings` directory with appropriate permissions.
- **`curl -fsSL <url> -o <file>`**: Downloads Docker’s GPG key.
- **`chmod a+r`**: Grants read permissions for all users to the GPG key.

### **Step 3: Add Docker’s Official Repository**
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
- Adds Docker’s repository to the Apt sources list.

### **Step 4: Install Docker**
```bash
sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
- **`docker-ce`**: Installs Docker Community Edition.
- **`docker-ce-cli`**: Docker command-line interface.
- **`containerd.io`**: Container runtime.
- **`docker-buildx-plugin`**: Provides advanced build functionality.
- **`docker-compose-plugin`**: Manages multi-container applications.

---

## **3. Docker CLI Commands**

### **3.1 Authentication**
```bash
docker login
```
- **`docker login`**: Logs into Docker Hub or a private registry by prompting for credentials.

### **3.2 Image Management**
- **Download an image:**
  ```bash
  docker pull <repo-addr>
  ```
  - Downloads an image from a repository.

- **List images:**
  ```bash
  docker images
  ```
  - Displays all available images.

- **Remove an image:**
  ```bash
  docker rmi -f <image-id>
  ```
  - Forcefully removes a specific image.

- **Save an image as a `.tar` file:**
  ```bash
  docker save -o <file-location-and-name> <image-name>
  ```

- **Load an image from a `.tar` file:**
  ```bash
  docker load -i <file-location>
  ```

### **3.3 Container Management**
- **Run a container:**
  ```bash
  docker run <options> <image-name>
  ```

- **Run an interactive container with a terminal:**
  ```bash
  docker run -it <image-name>
  ```

- **Run a container in detached mode:**
  ```bash
  docker run -dit <image-name>
  ```

- **Set a container to always restart:**
  ```bash
  docker run -dit --restart=always <image-name>
  ```

- **Name a container:**
  ```bash
  docker run -dit --name <container-name> <image-name>
  ```

- **Assign a hostname:**
  ```bash
  docker run -dit --hostname=<hostname> <image-name>
  ```

- **Set environment variables:**
  ```bash
  docker run -dit -e var1=data --name <container-name> --hostname=<hostname> <image-name>
  ```

- **Map host and container ports:**
  ```bash
  docker run -dit -p <host-port>:<container-port> <image-name>
  ```

- **Run a container with memory and CPU limits:**
  ```bash
  docker run -dit --name nginx --memory-reservation 150m --memory 500m nginx
  ```
  - Limits memory reservation to 150MB and usage to a maximum of 500MB.

  ```bash
  docker run -dit --name nginx --cpus 2 --cpu-shares 100 nginx
  ```
  - Limits the container to 2 CPUs.

- **Stream container logs in real-time:**
  ```bash
  docker logs -f <container-name>
  ```

- **Access a container’s terminal:**
  ```bash
  docker exec -it <container-name> /bin/bash
  ```

- **Stop a container:**
  ```bash
  docker stop <container-name>
  ```

- **Remove a container:**
  ```bash
  docker rm <container-name>
  ```

- **Forcefully remove a running container:**
  ```bash
  docker rm -f <container-name>
  ```

- **List all container IDs (including stopped):**
  ```bash
  docker ps -aq
  ```

- **Prune stopped containers:**
  ```bash
  docker container prune
  ```

- **Commit a container to an image:**
  ```bash
  docker commit <container-name> <new-image-name>
  ```

- **Inspect container details:**
  ```bash
  docker inspect <container-name>
  ```

- **Copy files between host and container:**
  ```bash
  docker cp <file-on-local> <container-name>:/<container-path>
  ```

  ```bash
  docker cp <container-name>:/<container-path> <local-path>
  ```

- **View real-time container resource usage:**
  ```bash
  docker stats
  ```

- **Build an image from a Dockerfile:**
  ```bash
  docker build -t <app-name>:<app-version> <path-to-dockerfile>
  ```

---

## **4. Volume Management**
Volumes store data that persists even when a container is deleted.

- **List all volumes:**
  ```bash
  docker volume ls
  ```

- **Create a volume:**
  ```bash
  docker volume create <volume-name>
  ```

- **Inspect a volume:**
  ```bash
  docker volume inspect <volume-name>
  ```

- **Mount a volume to a container:**
  ```bash
  docker run -dit --name <container-name> -v <volume-name>:<container-path> <image-name>
  ```

- **Mount a file with read-only access:**
  ```bash
  docker run -dit --name nginx -v /etc/resolv.conf:/etc/resolv.conf:ro nginx
  ```

- **Mount temporary filesystem in memory:**
  ```bash
  docker run -dit --name nginx --tmpfs /opt:100M nginx
  ```

---

## **5. Network Management**
Docker networks allow communication between containers.

- **List all networks:**
  ```bash
  docker network ls
  ```

- **Create a network:**
  ```bash
  docker network create <network-name>
  ```

- **Create a custom network with subnet and gateway:**
  ```bash
  docker network create --subnet <subnet> --gateway <gateway-ip> --driver=<network-type> <network-name>
  ```

- **Run a container on a specific network:**
  ```bash
  docker run -dit --name <container-name> --network <network-name> <image-name>
  ```

- **Connect a running container to a network:**
  ```bash
  docker network connect <network-name> <container-name>
  ```

- **Disconnect a container from a network:**
  ```bash
  docker network disconnect <network-name> <container-name>
  ```

  ---

## **6. System Commands**

- **Show Docker Disk usage:**
  ```bash
    docker system df 
  ```
- **Remove Unuse Cache,Container And More**
- ```bash
-   docker system prune
- ```
-
-
