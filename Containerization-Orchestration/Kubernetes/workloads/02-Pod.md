# 🌐 Kubernetes Pod Management Guide

A concise guide for managing Kubernetes Pods using `kubectl` and YAML manifests.

---

## 📋 Listing Pods

### 🔹 Default Namespace

List all Pods in the **default** namespace:

```bash
kubectl get pods
```

### 🔹 Wide Output (More Info)

List Pods with extended details (e.g., IP, node, etc.):

```bash
kubectl get pods -o wide
```

### 🔹 Specific Namespace

List Pods in a specific namespace:

```bash
kubectl get pods -o wide -n <namespace-name>
```

---

## 🚀 Running a Pod

> **Note:** `kubectl run` is ideal for quick tests or running **single** Pods. For production workloads, use **YAML manifests** or **Deployments**.

### 🔹 Run a Pod in Default Namespace

```bash
kubectl run <pod-name> --image=<image-name>
```

### 🔹 Run a Pod in a Specific Namespace

```bash
kubectl run <pod-name> --image=<image-name> -n <namespace>
```

---

## ❌ Deleting Pods

### 🔹 Standard Delete

```bash
kubectl delete pod <pod-name> -n <namespace-name>
```

### 🔹 Force Delete

```bash
kubectl delete pod <pod-name> -n <namespace-name> --force
```

### 🔹 Immediate Force Delete (No Grace Period)

```bash
kubectl delete pod <pod-name> -n <namespace-name> --force --grace-period=0
```

---

## ✏️ Editing a Pod

> **Warning:** Pods are **not directly editable**. Attempting to edit a running pod will result in a temporary patch but not persistent changes.

```bash
kubectl edit pod -n <namespace> <pod-name>
```

---

## 🔧 Executing into a Pod

Use this to start a shell or run commands inside a container:

```bash
kubectl exec -it -n <namespace> <pod-name> -- <command>
```

Example for a shell:

```bash
kubectl exec -it -n dev my-pod -- /bin/bash
```

---

## 🧾 Example Pod YAML Manifest

A multi-container Pod with resource limits and node selector:

```yaml
apiVersion: v1
kind: Pod
metadata:
  namespace: dev
  name: pod-1
  labels:
    label1: test
    label2: test2
    app.kubernetes.io/label3: test3
    app.kubernetes.io/label4: test4
spec:
  containers:
    - name: nginx-server
      image: nginx

    - name: nginx-exporter
      image: nginx-exporter

    - name: ubuntu-c0
      image: ubuntu
      command: ["/bin/bash", "-c", "while true; do echo hello-world; sleep 5; done"]
      resources:
        limits:
          memory: "256Mi"
          cpu: "250m"
        requests:
          memory: "128Mi"
          cpu: "125m"
  nodeSelector:
    hostname: k3s
    app.kubernetes.io/disk: ssd
```

