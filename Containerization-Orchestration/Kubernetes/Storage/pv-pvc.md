# Kubernetes Persistent Volumes (PV) Cheat Sheet

## What is a Persistent Volume (PV)?

A **Persistent Volume (PV)** is a piece of storage in a Kubernetes cluster that can be:

* **Pre-provisioned** by an administrator, or
* **Dynamically provisioned** using a **StorageClass**.

PVs allow data to **persist beyond the lifecycle of individual Pods**.

---

## PV Storage Options

### 1. HostPath

* Mounts a file or directory from the host node’s filesystem into a Pod.
* Suitable **only for local development or single-node clusters** such as Minikube or Kind.
* Not recommended for production workloads.

### 2. NFS

* Network File System; allows multiple Pods and nodes to share storage.
* Recommended for shared or distributed environments.

### 3. Cloud Volumes

* **AWS:** `awsElasticBlockStore`
* **GCP:** `gcePersistentDisk`
* **Azure:** `azureDisk` or `azureFile`
* **CSI Drivers:** Preferred modern approach for all major clouds and on-prem solutions.

---

## Kubernetes Storage Architecture

1. **Persistent Volume (PV)** – Represents the actual storage resource, managed by the cluster admin or a dynamic provisioner.
2. **Persistent Volume Claim (PVC)** – A user request for storage with specific size and access requirements.
3. **StorageClass** – Defines how dynamic provisioning should occur (provisioner, reclaim policy, parameters).

---

## PV Lifecycle Phases

| State         | Description                                              |
| ------------- | -------------------------------------------------------- |
| **Available** | PV is ready to be bound.                                 |
| **Bound**     | PV is bound to a PVC.                                    |
| **Released**  | PVC was deleted; PV is unbound but data may still exist. |
| **Failed**    | Automatic cleanup failed.                                |

### Reclaim Policies:

* **Delete:** Removes the underlying storage resource.
* **Retain:** Keeps data for manual recovery.
* **Recycle:** Deprecated (previously used to scrub the volume).

---

## PV Access Modes

| Mode                      | Description                                                          |
| ------------------------- | -------------------------------------------------------------------- |
| `ReadWriteOnce` (RWO)     | One node can read/write.                                             |
| `ReadOnlyMany` (ROX)      | Many nodes can read.                                                 |
| `ReadWriteMany` (RWX)     | Many nodes can read/write.                                           |
| `ReadWriteOncePod` (RWOP) | Only one Pod can mount it with read/write access (Kubernetes ≥1.22). |

---

## CLI Commands to Manage PVs & PVCs

```bash
# List all Persistent Volumes
kubectl get pv

# List all Persistent Volume Claims
kubectl get pvc -A

# Describe a specific PV or PVC
kubectl describe pv <pv-name>
kubectl describe pvc <pvc-name> -n <namespace>

# Delete a PV or PVC
kubectl delete pv <pv-name>
kubectl delete pvc <pvc-name> -n <namespace>
```

---

## Example: Deployment with `hostPath` Volume

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
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
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

**Valid `hostPath` Types:**
`DirectoryOrCreate`, `Directory`, `FileOrCreate`, `File`, `Socket`, `CharDevice`, `BlockDevice`

---

## Example: Static Persistent Volume (PV)

**Important:** A PV **must specify a volume source type** (this was the cause of your validation error).
For example, this corrected PV uses `hostPath`:

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
  storageClassName: manual
  hostPath:
    path: /mnt/data/pv001
```

---

## Example: Persistent Volume Claim (PVC)

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
  storageClassName: manual
```

To bind this PVC to a specific PV manually:

```yaml
volumeName: pv001
```

---

## NFS-Based Persistent Volume

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

## Static StorageClass for Pre-Provisioned Volumes

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nginx-files
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Retain
```

---

## Recommended Additions

1. **Always include `storageClassName`** to ensure predictable binding.
2. **Set `volumeBindingMode: WaitForFirstConsumer`** in StorageClasses for node-aware provisioning.
3. **Avoid using `hostPath` in multi-node clusters**; use NFS or CSI drivers.
4. **Check events** for troubleshooting PV/PVC binding:

   ```bash
   kubectl describe pvc <pvc-name> -n <namespace>
   ```
5. **Automate cleanup** with proper reclaim policies or storage lifecycle controllers.

