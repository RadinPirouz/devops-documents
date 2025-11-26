# 🚢 Kubernetes (K8s) Documentation

## 🌐 Overview
**Kubernetes (K8s)** is an open-source container orchestration platform designed to automate the deployment, scaling, and operation of containerized applications.

---

## 🧠 Control Plane (CP)
The **Control Plane** is the core management component of a Kubernetes cluster. It makes global decisions about the cluster (e.g., scheduling) and maintains the desired state of the cluster by managing workloads and directing communication within the system.

> 💡 **Note:** By default, the Control Plane does not directly manage or run application containers.

### 🔑 Key Components of the Control Plane

- **API Server (`kube-apiserver`)**  
  Exposes the Kubernetes API and serves as the cluster's entry point. It handles communication between internal components and external clients.

- **Scheduler (`kube-scheduler`)**  
  Assigns workloads (e.g., Pods) to nodes based on resource availability and defined policies.

- **Controller Manager (`kube-controller-manager`)**  
  Runs controllers that monitor and regulate the cluster's state, such as the Node Controller and Replication Controller.

- **etcd**  
  A consistent and highly available key-value store that stores all cluster data, configurations, and state. This is the "database" of Kubernetes.

---

## 🧱 Worker Nodes
**Worker nodes** are the machines where containerized applications run. Each node contains essential components for managing containers.

### 🔧 Key Components of a Worker Node

- **Kubelet**  
  An agent that ensures containers run as specified in their Pod definitions. It communicates with the Control Plane to execute assigned tasks.

- **Kube Proxy**  
  Maintains network rules and manages routing for communication within the cluster and with external systems.

---

## 🔄 Data Flow
- **Kubelet** and **Kube Proxy** on each worker node interact with the **API Server** to perform operations and update resource states.
- The **Scheduler** selects suitable nodes for pod placement based on available resources.
- The **Controller Manager** ensures the actual state of the cluster matches the desired state.

---

## 🛠️ Administration Tools

- **`kubeadm`**  
  A command-line tool to bootstrap and configure Kubernetes clusters. It streamlines the setup of both the Control Plane and worker nodes.

- **`kubectl`**  
  The CLI for interacting with the Kubernetes API. It's used to deploy apps, inspect cluster resources, and manage configurations.

---

## 🧩 Kubernetes Version Compatibility

### Kubernetes and Container Runtimes

- **Kubernetes ≤ 1.23**  
  ✅ Compatible with **Docker** as the default container runtime.

- **Kubernetes 1.24 – 1.25**  
  ❌ Docker is **not supported** directly. Use `containerd` or another CRI-compliant runtime.

- **Kubernetes ≥ 1.25**  
  ⚠️ Docker may be installed on the system but must be used **indirectly** through `containerd` or another supported CRI.

---

## 👥 Kubernetes Roles

- **Control Plane (Manager)**  
  Requires an **odd number** of nodes for high availability (e.g., 1, 3, 5, ...). This ensures quorum in distributed consensus.

- **Worker (none)**  
  These nodes run application workloads and do not participate in control decisions.


image pull policy in kubernetes:


example of all work loads:
https://k8s-examples.container-solutions.com/