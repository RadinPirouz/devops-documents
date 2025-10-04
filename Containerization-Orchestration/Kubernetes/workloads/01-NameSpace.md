# Kubernetes Namespaces Guide

Kubernetes **namespaces** allow you to organize and isolate resources within your cluster.

---

## 🧾 Listing Namespaces

To list all namespaces:

```bash
kubectl get namespaces
```

or the shorthand:

```bash
kubectl get ns
```

---

## 🛠️ Creating a Namespace

Create a new namespace:

```bash
kubectl create namespace <namespace-name>
```

or:

```bash
kubectl create ns <namespace-name>
```

---

## 🗑️ Deleting a Namespace

Delete a namespace:

```bash
kubectl delete ns <namespace-name>
```

---

## ⚠️ Best Practices & Notes

* **Namespaces are isolated**, but they **can still communicate** with each other by default.
* It is **not recommended to create namespaces that start with `kube-`**, as those are typically reserved for system components.

---

## 📄 Creating a Namespace with a Manifest

You can define a namespace using a YAML manifest:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: namespace-test
```

Apply it using:

```bash
kubectl apply -f namespace.yaml
```

