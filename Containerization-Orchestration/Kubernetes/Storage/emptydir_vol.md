
## 📦 Pod Volume Lifecycle & `emptyDir` Usage in Kubernetes

This document describes how volumes work in the context of Kubernetes Pods, focusing on `emptyDir` and its lifecycle behavior.

---

### 🔁 Pod Lifecycle & Volumes

* **Volumes are defined at the Pod level.**
  They are not tied to a specific container, but can be shared among containers within the same Pod.

* **Volumes are attached to containers through `volumeMounts`.**
  This enables containers to access the volume’s filesystem at the specified `mountPath`.

* **Data in `emptyDir` volumes is ephemeral.**
  The volume is created when the Pod starts and **deleted when the Pod is removed**, erasing all stored data.

---

### ⚠️ Visibility Across Pods & Containers

* A **Pod cannot access another Pod’s volume**, even if it's of type `emptyDir`.
  For example:

  * Pod A cannot see Pod B’s `emptyDir`.
* However, **containers within the same Pod can share and access the same `emptyDir`** volume.

---

### 🧪 Example: Pod with `emptyDir` Volume in Memory

```yaml
apiVersion: v1
kind: Pod
metadata:
  namespace: ns-test
  name: pod-tests
spec:
  containers:
    - name: nginx
      image: nginx
      resources:
        limits:
          memory: "150Mi"
          cpu: "500m"
      volumeMounts:
        - name: nginx-log
          mountPath: /var/log/nginx
  volumes:
    - name: nginx-log
      emptyDir:
        medium: Memory  # Uses memory for faster read/write operations
        sizeLimit: 64Mi # Volume size limited to 64Mi
```

---

### 🧠 Key Points

* `emptyDir` is ideal for temporary storage like logs, scratch space, or caches.
* Using `medium: Memory` stores data in memory (RAM) instead of disk, offering higher performance.
* `sizeLimit` restricts the amount of memory that the `emptyDir` can consume.

