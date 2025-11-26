# 🧩 Kubernetes ReplicaSet Management

A guide to working with **ReplicaSets** in Kubernetes, including inspection, editing behavior, and configuration examples.

---

## 📦 Listing Pods and ReplicaSets

### 🔹 List Pods in a Namespace

```bash
kubectl get pod -n <namespace>
```

### 🔹 List ReplicaSets in a Namespace

```bash
kubectl get rs -n <namespace>
```

---

## ✏️ Editing a ReplicaSet

You can attempt to edit a ReplicaSet:

```bash
kubectl edit rs -n <namespace> <replica-set-name>
```

> ⚠️ **Note:**
> Editing the **image** in a ReplicaSet directly will not automatically update existing Pods.
> This is because ReplicaSets do not perform **rolling updates**.
> Pods will only use the new image **after the old ones are deleted and new ones are created**.

**To apply image changes effectively:**

1. **Delete existing Pods** manually:

   ```bash
   kubectl delete pod -l <label-selector> -n <namespace>
   ```

2. **Or**, use a higher-level controller like a **Deployment** for image updates and rolling behavior.

---

## 🧾 Example ReplicaSet YAML

Below is a minimal and clear ReplicaSet configuration:

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: app-1
  namespace: dev
  labels:
    label1: test1
    app.kubernetes.io/label2: test2
spec:
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/label2: test2
  template:
    metadata:
      labels:
        app.kubernetes.io/label2: test2
        os: linux
    spec:
      containers:
        - name: nginx
          image: nginx
```

> ✅ **Tip:**
> Ensure that the `template.metadata.labels` **matches exactly** with `spec.selector.matchLabels`.
> This is critical for proper ReplicaSet Pod matching.

