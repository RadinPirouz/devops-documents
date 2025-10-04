# 🧩 DaemonSet in Kubernetes

A **DaemonSet** ensures that a copy of a specific pod runs on **every (or some) node** in the cluster. It’s typically used for background system-level services like log collection, monitoring, or networking tools.

---

## 📌 Key Characteristics

- Automatically deploys one pod per worker node.
- Ensures the pod stays on each node as long as the DaemonSet exists.
- Automatically adds pods to new nodes when they join the cluster.

---

## 📄 Example DaemonSet YAML

Below is a simple DaemonSet example that deploys `nginx` to every node in the `web` namespace:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: nginx
  namespace: web
  labels:
    app: web-servers
spec:
  selector:
    matchLabels:
      app: web-servers
  template:
    metadata:
      labels:
        app: web-servers
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
````

