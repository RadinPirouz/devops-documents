# Node Management

Commands for listing nodes and performing maintenance (cordon, drain, uncordon).

---

## 📋 Listing Nodes

### 🔹 Show All Nodes
```bash
kubectl get nodes
```

### 🔹 Show Nodes with Labels

```bash
kubectl get nodes --show-labels
```

---

## 🔧 Node Maintenance (Cordon / Drain)

### 🚫 Cordon a Node

Prevent new pods from being scheduled on the node.

```bash
kubectl cordon <node-name>
```

### ✅ Uncordon a Node

Mark the node as schedulable again.

```bash
kubectl uncordon <node-name>
```

### 🧹 Drain a Node

Evict all pods from the node (excluding those managed by DaemonSets).

* Forcefully drain the node:

  ```bash
  kubectl drain <node-name> --ignore-daemonsets --force
  ```

* Drain and delete local data:

  ```bash
  kubectl drain <node-name> --ignore-daemonsets --delete-local-data
  ```

#### 🔄 Undo Drain (Uncordon)

```bash
kubectl uncordon <node-name>
```

> ⚠️ **Warning:** Draining a node will evict running pods. Ensure that this is planned to avoid service disruption.

