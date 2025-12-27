# Kubernetes (K8s) – Technical Documentation

## 1. Overview

**Kubernetes (K8s)** is an open-source container orchestration platform that automates the deployment, scaling, networking, and lifecycle management of containerized applications. It provides declarative configuration and self-healing capabilities to maintain the desired state of workloads.

Kubernetes follows a **control plane / worker node** architecture and is designed to run reliably at scale.

---

## 2. Kubernetes Architecture

A Kubernetes cluster consists of:

* **Control Plane nodes** – manage cluster state
* **Worker nodes** – run application workloads

---

## 3. Control Plane

The **Control Plane** is responsible for managing the overall cluster state. It does not normally run application workloads.

### 3.1 Control Plane Components

#### kube-apiserver

* Entry point to the Kubernetes cluster
* Exposes the Kubernetes REST API
* Validates requests and persists state to etcd
* All components communicate through the API server

#### etcd

* Distributed, consistent key-value store
* Stores all cluster state and configuration
* Uses the **Raft consensus algorithm**
* Requires an **odd number of members (3, 5, …)** to maintain quorum
* Minimum recommended production setup: **3 etcd members**

#### kube-scheduler

* Assigns Pods to nodes
* Makes scheduling decisions based on:

  * Resource requests and limits
  * Node affinity / anti-affinity
  * Taints and tolerations
  * Pod affinity rules

#### kube-controller-manager

* Runs multiple controllers, including:

  * Node Controller
  * ReplicaSet Controller
  * Deployment Controller
  * Job Controller
* Ensures the actual cluster state matches the desired state

---

## 4. Worker Nodes

Worker nodes run application containers and system workloads.

### 4.1 Worker Node Components

#### kubelet

* Node agent running on each worker
* Responsibilities:

  * Register the node with the API server
  * Create and manage Pods
  * Monitor Pod and container health
  * Report node and Pod status
  * Manage DaemonSet Pods
* Communicates with the container runtime via CRI

#### kube-proxy

* Handles networking and service routing
* Maintains iptables or IPVS rules
* Enables Service abstraction and load balancing
* Usually runs as a **DaemonSet**

#### Container Runtime

* Responsible for running containers
* Must be **CRI-compliant**
* Common runtimes:

  * containerd (recommended)
  * CRI-O

---

## 5. Container Runtime Interface (CRI)

**CRI (Container Runtime Interface)** is a Kubernetes API that allows kubelet to communicate with container runtimes.

Important clarification:

* CRI is **not a registry**
* It is an interface between kubelet and the container runtime

---

## 6. Cluster Networking & DNS

### 6.1 CoreDNS

* Kubernetes internal DNS service
* Runs as a **Deployment** (not DaemonSet in modern clusters)
* Provides service discovery inside the cluster

#### Default cluster domain

```
cluster.local
```

#### DNS formats

* Service:

```
<service-name>.<namespace>.svc.cluster.local
```

* Pod:

```
<pod-ip>.<namespace>.pod.cluster.local
```

---

## 7. Administration Tools

### kubeadm

* Tool for bootstrapping Kubernetes clusters
* Used to initialize control plane and join worker nodes

### kubectl

* Command-line interface to interact with Kubernetes API
* Used for deployment, debugging, inspection, and administration

### Lens

* Client-side GUI for Kubernetes
* Requires kubeconfig access

### Kubernetes Dashboard

* Server-side web UI
* Runs inside the cluster
* Requires RBAC configuration for access

---

## 8. Kubernetes Version & Runtime Compatibility

| Kubernetes Version | Docker Support                               |
| ------------------ | -------------------------------------------- |
| ≤ 1.23             | Docker supported via dockershim              |
| 1.24+              | Docker shim removed                          |
| 1.25+              | Docker only usable indirectly via containerd |

**Recommendation:** Use `containerd` directly.

---

## 9. Node Roles & High Availability

### Control Plane

* Requires **odd number of nodes** (1, 3, 5…)
* Necessary for etcd quorum and fault tolerance

### Worker Nodes

* Can scale horizontally without restrictions
* Do not participate in control decisions

---

## 10. Pod Lifecycle Hooks

### postStart

* Executed immediately after container creation
* Runs asynchronously with container startup
* Failure causes container restart

### preStop

* Executed before container termination
* Commonly used for graceful shutdown
* Kubernetes waits for completion (within termination grace period)

---

## 11. Static Pods

* Managed directly by kubelet
* Defined via local manifest files
* Do **not** require API server scheduling
* Commonly used for core components:

  * kube-apiserver
  * etcd
  * kube-controller-manager

---

## 12. Workload Types

Common Kubernetes workloads:

* Deployment
* ReplicaSet
* StatefulSet
* DaemonSet
* Job
* CronJob

Examples:
[https://k8s-examples.container-solutions.com/](https://k8s-examples.container-solutions.com/)

---

## 13. Scheduling Behavior

Pod scheduling is **skipped** for:

* **DaemonSet Pods**
* **Static Pods**

These are directly bound to nodes.

---

## 14. Scaling

### Horizontal Scaling

* Adjust replica count
* Manual or automatic

### Vertical Scaling

* Adjust CPU and memory resources
* Requires Pod restart

---

## 15. Autoscaling Components

### Horizontal Pod Autoscaler (HPA)

* Scales replicas based on:

  * CPU
  * Memory
  * Custom metrics

### Vertical Pod Autoscaler (VPA)

Components:

1. **Recommender** – calculates resource recommendations
2. **Updater** – evicts Pods if needed
3. **Admission Controller** – applies recommendations at Pod creation

### Cluster Autoscaler (CA)

* Scales worker nodes up/down
* Integrates with cloud providers or node groups

---

## 16. Resource Management

### ResourceQuota

* Limits total resource usage per namespace
* Controls CPU, memory, object count, etc.

### LimitRange

* Sets default and maximum limits per Pod or container
* Applies at namespace level

---

## 17. Finalizers

* Prevent resource deletion until cleanup is complete
* Common use cases:

  * External resource cleanup
  * Storage detachment
* Object remains in `Terminating` state until finalizer is removed

---

## 18. Deployment Update Strategies

### Recreate

* Terminates old Pods before creating new ones
* Causes downtime

### RollingUpdate

* Gradual replacement
* Zero or minimal downtime
* Default for Deployments

### Blue-Green Deployment

* Two environments (blue and green)
* Traffic switched after validation

### Canary Deployment

* Gradual traffic increase to new version
* Used for risk reduction

### A/B Testing

* Traffic split between versions
* Used for experimentation

### Shadow Testing

* New version receives production traffic without user impact
* Used for performance and behavior analysis

---

## 19. Services

### Service

* Provides stable networking and load balancing
* Uses label selectors to target Pods

### Headless Service

* No virtual IP
* Direct Pod DNS resolution
* Commonly used with StatefulSets (e.g., databases)

---

## 20. Summary

Kubernetes provides a highly scalable, self-healing platform for running modern workloads. Understanding control plane behavior, scheduling, networking, scaling, and deployment strategies is essential for operating production-grade clusters reliably.

This documentation can be used as:

* Internal DevOps reference
* Onboarding material
* Interview preparation
* Production architecture baseline

If you want, I can also:

* Convert this into Markdown/PDF
* Add diagrams
* Create a learning roadmap
* Add real-world production best practices
