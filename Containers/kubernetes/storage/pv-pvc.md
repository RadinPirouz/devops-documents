# 🌐 Kubernetes: Persistent Volumes (PV) Cheat Sheet

## 📦 What is a Persistent Volume (PV)?

A **Persistent Volume** is a piece of storage in a Kubernetes cluster that has been provisioned by an administrator or dynamically provisioned using **StorageClasses**.

---

## 📁 PV Storage Options

1. **HostPath**

   * Mounts a file or directory from the host node’s filesystem into your Pod.

2. **Using PV and PVC**

   * **PV (Persistent Volume):** The actual storage resource.
   * **PVC (Persistent Volume Claim):** A request for storage by a user.

---

## 🧱 Kubernetes Storage Layers

1. **Persistent Volume (PV)**
2. **Persistent Volume Claim (PVC)**

---

## 🔄 PV Lifecycle States

| State        | Description                                          |
| ------------ | ---------------------------------------------------- |
| Provisioning | Kubernetes is preparing the PV.                      |
| Binding      | The PV is bound to a PVC.                            |
| Using        | The bound PV is being used by a Pod.                 |
| Releasing    | PVC is deleted; PV is no longer bound.               |
| Reclaiming   | PV is reclaimed using one of the following policies: |
|              |     • `Delete` – Remove the storage                  |
|              |     • `Recycle` – Basic scrub (deprecated)           |
|              |     • `Retain` – Manual reclaim                      |

---

## 🔒 PV Access Modes

| Mode   | Description                                 |
| ------ | ------------------------------------------- |
| `RWO`  | **ReadWriteOnce** – One node can read/write |
| `ROX`  | **ReadOnlyMany** – Many nodes read-only     |
| `RWX`  | **ReadWriteMany** – Many nodes read/write   |
| `RWOP` | **ReadWriteOncePod** – One Pod only         |

---

## 🛠️ Check PVs via CLI

```bash
kubectl get pv
```

```bash
kubectl get pvc
```


---

## 🚀 Example: Deployment using HostPath Volume

```yaml
apiVersion: apps/v1
kind: Deployment
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
          ports:
            - containerPort: 80
          volumeMounts:
            - name: nginx-log
              mountPath: /var/log/nginx  
      volumes:
        - name: nginx-log
          hostPath:
            path: /root/nginx/logs
```

---

## 📂 Example: PersistentVolume with NFS

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv1
spec:
  capacity: 
    storage: 5Gi
  volumeMode: Filesystem
  accessModes: 
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: custom-name
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    path: /nfs/data
    server: 192.168.1.10
```




```yaml
apiVersion: apps/v1
kind: Deployment
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
          ports:
            - containerPort: 80
          volumeMounts:
            - name: nginx-log
              mountPath: /var/log/nginx  
          volumes:
            - name: nginx-log
              persisentVolumeClaim:
                claimName: pv1
---

apiVersion: v1
kind: persisentVolumeClaim
metadata:
    name: pvc1
    namespace: ns-test
spec:
    accessModes: 
        - ReadWriteMany
    resources:
        requests:
            storage: 1Gi
        limits:
            storage: 2Gi        
    storageClassName: custom-name
```

