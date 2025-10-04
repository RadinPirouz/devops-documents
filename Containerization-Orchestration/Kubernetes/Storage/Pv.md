# 🌐 Kubernetes Persistent Volumes (PV) Cheat Sheet

## 📦 What is a Persistent Volume (PV)?

A **Persistent Volume (PV)** is a piece of storage in a Kubernetes cluster that can be:

- **Pre-provisioned** by an administrator, or  
- **Dynamically provisioned** using a **StorageClass**.

> PVs allow data to **persist beyond the lifecycle of individual Pods**.

---

## 📁 PV Storage Options

### 1. **HostPath**
- Mounts a file or directory from the host node’s filesystem into a Pod.
- Only suitable for **single-node testing or development** environments.

### 2. **Persistent Volume (PV) & Persistent Volume Claim (PVC)**
- **PV**: Represents the actual physical or virtual storage resource.
- **PVC**: A user's request for specific storage resources and access modes.

---

## 🧱 Kubernetes Storage Architecture

1. **Persistent Volume (PV)** – The actual storage unit, managed by the admin or provisioned dynamically.  
2. **Persistent Volume Claim (PVC)** – A user’s request for a certain amount and type of storage.

---

## 🔄 PV Lifecycle Phases

| **State**     | **Description**                             |
|---------------|---------------------------------------------|
| Provisioning  | PV is being created or initialized.         |
| Binding       | PV is bound to a PVC.                       |
| Using         | PV is in use by a Pod.                      |
| Releasing     | PVC is deleted; PV becomes unbound.         |
| Reclaiming    | Based on reclaim policy:                    |
|               | - `Delete`: Remove the storage.             |
|               | - `Recycle`: Basic scrub (deprecated).      |
|               | - `Retain`: Manual cleanup required.        |

---

## 🔒 PV Access Modes

| **Mode**   | **Description**                                 |
|------------|-------------------------------------------------|
| `RWO`      | **ReadWriteOnce** – One node can read/write.    |
| `ROX`      | **ReadOnlyMany** – Multiple nodes can read.     |
| `RWX`      | **ReadWriteMany** – Multiple nodes can read/write. |
| `RWOP`     | **ReadWriteOncePod** – Only one Pod can mount it with read/write access. |

---

## 🛠️ CLI Commands to Manage PVs & PVCs

```bash
# List all Persistent Volumes
kubectl get pv

# List all Persistent Volume Claims
kubectl get pvc

# Edit a PVC
kubectl edit pvc -n <namespace> <pvc-name>
```

---

## 🚀 Example: Deployment with `hostPath` Volume

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-1
  namespace: dev
spec:
  replicas: 3
  selector:
    matchLabels:
      name: nginx
  template:
    metadata:
      labels:
        name: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          ports:
            - containerPort: 80
          volumeMounts:
            - name: nginx-log
              mountPath: /var/log/nginx
      volumes:
        - name: nginx-log
          hostPath:
            path: /root/nginx/logs
            type: DirectoryOrCreate
```

### Valid `hostPath` Types:
- `DirectoryOrCreate`
- `Directory`
- `FileOrCreate`
- `File`
- `Socket`
- `CharDevice`
- `BlockDevice`

---

## 📄 Example: Static Persistent Volume (PV)

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv001
spec:
  capacity:
    storage: 128Mi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
```

---

## 📄 Example: Persistent Volume Claim (PVC)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-2
  namespace: db
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 64Mi
```

> ✅ To bind a PVC to a specific PV, add `volumeName: <pv-name>` in the PVC spec:
```yaml
volumeName: pv001
```

---

## 🌐 NFS-Based Persistent Volume

### Persistent Volume (PV)

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs-2
spec:
  capacity:
    storage: 128Mi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nginx-files
  mountOptions:
    - hard
    - nfsvers=4.2
  nfs:
    path: /root/Nginx_Files
    server: 192.168.6.160
```

### Persistent Volume Claim (PVC)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-1
  namespace: db
spec:
  volumeName: pv-nfs-2
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 64Mi
  storageClassName: nginx-files
```

---

## 🏗️ Static StorageClass for Pre-Provisioned Volumes

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nginx-files
provisioner: kubernetes.io/no-provisioner
```
