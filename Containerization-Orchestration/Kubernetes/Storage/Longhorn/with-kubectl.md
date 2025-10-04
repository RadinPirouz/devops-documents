# 📦 Deploying Longhorn with `kubectl`

This guide walks you through installing **Longhorn**, a cloud-native distributed block storage solution for Kubernetes, using `kubectl`.

---

## 🚀 Prerequisites

* A Kubernetes cluster (v1.21 or newer recommended)
* `kubectl` configured and connected to your cluster
* Internet access for downloading manifests

---

## 🧩 Step 1: Apply Longhorn YAML

Apply the official Longhorn deployment manifest in the `longhorn-system` namespace:

```bash
kubectl apply -f https://raw.githubusercontent.com/longhorn/longhorn/v1.9.0/deploy/longhorn.yaml
```

This will create all required resources under the `longhorn-system` namespace.

---

## 🔍 Step 2: Monitor Longhorn Pods

Watch the pods being created to ensure Longhorn is deploying properly:

```bash
kubectl get pods \
--namespace longhorn-system \
--watch
```

Wait until all pods show a `Running` or `Completed` status.

---

## 📦 Step 3: Verify Storage Classes

Once Longhorn is running, verify that the storage classes have been registered:

```bash
kubectl get storageclasses
```

You should see a storage class named `longhorn`, which can now be used in your PersistentVolumeClaims (PVCs).

---

## ✅ Success!

Longhorn is now successfully deployed and ready to provide persistent block storage for your workloads.

For more information, visit the [official Longhorn documentation](https://longhorn.io/docs/).

