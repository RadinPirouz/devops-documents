# **Kubernetes Persistent Volumes (PV) – Technical Reference Guide**

## **1. Overview**

A **Persistent Volume (PV)** is a storage resource in Kubernetes that allows data to persist beyond the lifecycle of Pods.
Persistent Volumes can be:

* **Pre-provisioned** by a cluster administrator, or
* **Dynamically provisioned** using a **StorageClass**.

---

## **2. PV Storage Options**

### **2.1 HostPath**

* Mounts a directory or file from the host node’s filesystem into a Pod.
* Suitable only for **local development** or **single-node clusters** (e.g., Minikube, Kind).
* **Not recommended** for production environments.

### **2.2 NFS**

* Uses Network File System (NFS) to allow multiple Pods and nodes to share storage.
* Recommended for **shared or distributed** setups.

### **2.3 Cloud Volumes**

* **AWS:** `awsElasticBlockStore`
* **GCP:** `gcePersistentDisk`
* **Azure:** `azureDisk` or `azureFile`
* **CSI Drivers:** Preferred for all modern cloud and on-prem environments.

---

## **3. Kubernetes Storage Architecture**

1. **Persistent Volume (PV):** Represents the actual storage resource, either statically created or dynamically provisioned.
2. **Persistent Volume Claim (PVC):** A user request for storage of specific size and access modes.
3. **StorageClass:** Defines dynamic provisioning behavior (provisioner, reclaim policy, parameters).

---

## **4. PV Lifecycle Phases**

| **State**     | **Description**                                  |
| ------------- | ------------------------------------------------ |
| **Available** | PV is ready to be bound to a claim.              |
| **Bound**     | PV is bound to a PVC.                            |
| **Released**  | PVC was deleted; PV is unbound but retains data. |
| **Failed**    | Automatic cleanup failed.                        |

### **Reclaim Policies**

* **Delete:** Deletes the underlying storage resource.
* **Retain:** Keeps the data for manual recovery.
* **Recycle:** Deprecated (was used to scrub the volume).

---

## **5. PV Access Modes**

| **Access Mode**           | **Description**                                             |
| ------------------------- | ----------------------------------------------------------- |
| `ReadWriteOnce` (RWO)     | Volume can be mounted as read-write by a single node.       |
| `ReadOnlyMany` (ROX)      | Volume can be mounted read-only by multiple nodes.          |
| `ReadWriteMany` (RWX)     | Volume can be mounted as read-write by multiple nodes.      |
| `ReadWriteOncePod` (RWOP) | Volume can be mounted read-write by a single Pod. (≥ v1.22) |

---

## **6. CLI Commands**

```bash
# List all Persistent Volumes
kubectl get pv

# List all Persistent Volume Claims (across all namespaces)
kubectl get pvc -A

# Describe a specific PV or PVC
kubectl describe pv <pv-name>
kubectl describe pvc <pvc-name> -n <namespace>

# Delete a PV or PVC
kubectl delete pv <pv-name>
kubectl delete pvc <pvc-name> -n <namespace>
```

---

## **7. Example: Deployment with HostPath Volume**

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

**Valid `hostPath` types:**
`DirectoryOrCreate`, `Directory`, `FileOrCreate`, `File`, `Socket`, `CharDevice`, `BlockDevice`

---

## **8. Example: Static Persistent Volume (PV)**

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

## **9. Example: Persistent Volume Claim (PVC)**

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
  volumeName: pv001
```

---

## **10. Example: NFS-Based PV and PVC**

### **Persistent Volume (PV)**

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

### **Persistent Volume Claim (PVC)**

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

## **11. Example: Static StorageClass**

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

## **12. Example: Nginx Deployment Using PVC**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  namespace: web-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app_type: nginx-web
  template:
    metadata:
      labels:
        app_type: nginx-web
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
          volumeMounts:
            - name: nginx-configs-volume
              mountPath: /etc/nginx/conf.d/default.conf
              subPath: reverse_proxy.conf
            - name: nginx-logs-volume
              mountPath: /var/log/nginx
      volumes:
        - name: nginx-configs-volume
          configMap:
            name: nginx-configs
        - name: nginx-logs-volume
          persistentVolumeClaim:
            claimName: nginx-pvc
```

---

## **13. Best Practices and Recommendations**

1. **Always specify `storageClassName`** for predictable PV/PVC binding.
2. **Use `volumeBindingMode: WaitForFirstConsumer`** to ensure node-aware provisioning.
3. **Avoid `hostPath`** in multi-node or production clusters; use NFS or CSI drivers instead.
4. **Monitor events** for troubleshooting binding issues:

   ```bash
   kubectl describe pvc <pvc-name> -n <namespace>
   ```
5. **Implement proper reclaim policies** or automated cleanup mechanisms for storage lifecycle management.

