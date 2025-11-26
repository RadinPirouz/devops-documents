# **crictl: CLI for CRI-Compatible Container Runtimes**

## Overview

`crictl` is a **command-line interface** for **Container Runtime Interface (CRI)**–compatible runtimes such as **containerd** and **CRI-O**, primarily used within Kubernetes environments.

It provides node-level visibility and control over pods, containers, and images. While it resembles Docker CLI in syntax, it is designed for **debugging** and **inspection**, not for managing workloads outside Kubernetes control.

`crictl` is part of the **[cri-tools](https://github.com/kubernetes-sigs/cri-tools)** project, which also includes `critest`.

---

## Installation

1. Navigate to the [cri-tools releases page](https://github.com/kubernetes-sigs/cri-tools/releases) to find the version compatible with your Kubernetes or CRI runtime.
2. Download and install `crictl`:

   ```bash
   VERSION="v1.33.0"
   wget https://github.com/kubernetes-sigs/cri-tools/releases/download/$VERSION/crictl-$VERSION-linux-amd64.tar.gz
   tar zxvf crictl-$VERSION-linux-amd64.tar.gz
   sudo mv crictl /usr/local/bin/
   ```

   *(Adjust version and architecture as needed.)*
3. Clean up the tarball if desired.
4. Verify installation:

   ```bash
   crictl --version
   ```

---

## Configuration and Endpoints

`crictl` communicates with CRI runtimes using socket endpoints.

### Configuration Methods

You can configure endpoints via:

* **Command-line flags**: `--runtime-endpoint`, `--image-endpoint`
* **Environment variables**:
  `CONTAINER_RUNTIME_ENDPOINT`, `IMAGE_SERVICE_ENDPOINT`
* **Configuration file**: Default path `/etc/crictl.yaml`
* **Custom config file**: Use `--config=<path>`

### Example `/etc/crictl.yaml`

```yaml
runtime-endpoint: unix:///var/run/containerd/containerd.sock
image-endpoint:  unix:///var/run/containerd/containerd.sock
timeout: 10
debug: true
```

If no endpoint is provided, `crictl` attempts to connect to a list of known sockets, which can slow operations.

### Modifying Configuration

```bash
crictl config --set debug=true
crictl config --get debug
```

Additional configuration parameters include:

* `pull-image-on-create`
* `disable-pull-on-run`

---

## Global Options

| Flag                        | Description                                |
| --------------------------- | ------------------------------------------ |
| `-h`, `--help`              | Display help and usage information         |
| `-v`, `--version`           | Display crictl and runtime version details |
| `--runtime-endpoint <path>` | Specify CRI runtime socket                 |
| `--image-endpoint <path>`   | Specify CRI image service socket           |
| `--timeout <duration>`      | Connection timeout (e.g., `5s`)            |
| `-D`, `--debug`             | Enable verbose output                      |
| `--config <path>`           | Specify a custom config file               |

---

## Common Commands

### Status and Information

| Command          | Description                                           |
| ---------------- | ----------------------------------------------------- |
| `crictl version` | Display version and runtime API info                  |
| `crictl info`    | Show runtime health, plugin states, and configuration |

### Pods / Pod Sandboxes

| Command                             | Description                        |
| ----------------------------------- | ---------------------------------- |
| `crictl pods`                       | List all pod sandboxes on the node |
| `crictl inspectp <POD_ID>`          | Inspect a specific pod sandbox     |
| `crictl runp <sandbox-config.json>` | Create a new pod sandbox           |
| `crictl stopp <POD_ID>`             | Stop a pod sandbox                 |
| `crictl rmp <POD_ID>`               | Remove a pod sandbox               |

### Containers

| Command                                                                | Description                              |
| ---------------------------------------------------------------------- | ---------------------------------------- |
| `crictl ps` / `crictl ps -a`                                           | List running / all containers            |
| `crictl inspect <CONTAINER_ID>`                                        | Inspect a specific container             |
| `crictl create <POD_ID> <container-config.json> <sandbox-config.json>` | Create a container in a pod              |
| `crictl start <CONTAINER_ID>`                                          | Start a container                        |
| `crictl exec -i -t <CONTAINER_ID> <command>`                           | Execute a command inside a container     |
| `crictl stop <CONTAINER_ID>`                                           | Stop a running container                 |
| `crictl rm <CONTAINER_ID>`                                             | Remove a stopped container               |
| `crictl stats`                                                         | Show CPU and memory usage for containers |

### Images

| Command                   | Description                   |
| ------------------------- | ----------------------------- |
| `crictl images`           | List available images         |
| `crictl inspecti <IMAGE>` | Inspect image metadata        |
| `crictl pull <IMAGE>`     | Pull an image from a registry |
| `crictl rmi <IMAGE>`      | Remove an image               |
| `crictl load <tarball>`   | Load an image from a tar file |

---

## Best Practices and Caveats

* **Kubelet cleanup:** Containers or pods created manually with `crictl` may be removed by the kubelet since they’re not managed by the Kubernetes control plane. Use for debugging only.
* **Permissions:** Root privileges or socket access are often required to communicate with the runtime.
* **Version compatibility:** Always match your `crictl` version to your Kubernetes or CRI runtime.
* **Timeout tuning:** Adjust `--timeout` or configuration to avoid connection failures.
* **Not a Docker replacement:** Although similar in command structure, `crictl` interacts directly with the CRI layer and may not support all Docker features.

---

## Example Debugging Workflow

1. SSH into a Kubernetes node.
2. Check runtime health:

   ```bash
   crictl info
   crictl version
   ```
3. List pod sandboxes:

   ```bash
   crictl pods
   ```
4. Inspect a pod:

   ```bash
   crictl inspectp <POD_ID>
   ```
5. List and inspect containers:

   ```bash
   crictl ps -a
   crictl inspect <CONTAINER_ID>
   ```
6. Execute into or inspect logs:

   ```bash
   crictl exec -it <CONTAINER_ID> sh
   ```
7. Clean up stuck containers or unused images:

   ```bash
   crictl stop <CONTAINER_ID>
   crictl rm <CONTAINER_ID>
   crictl rmi <IMAGE>
   ```

This workflow is typically used for **node-level debugging**, especially when `kubectl` cannot access or display runtime state.
