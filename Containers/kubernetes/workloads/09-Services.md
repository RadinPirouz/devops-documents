# 🔗 **Kubernetes Services (SVC)**

A **Service** in Kubernetes provides a stable network endpoint to access a set of Pods. It abstracts access through selectors and DNS names, enabling loose coupling between client applications and Pods.

---

## 🌐 **Service Basics**

### 📌 **Service Flow**

```
Service ➡️ Endpoint ➡️ Pods
```

* Services **group Pods** behind a single access point.
* They get a **cluster-wide DNS name** automatically.
* Use **label selectors** to forward traffic to matching Pods.

---

## 🧭 **Types of Services**

1. **ClusterIP** (default)

   * Only reachable within the cluster.

2. **NodePort**

   * Exposes the service via a static port on each node.

3. **LoadBalancer**

   * Creates an external IP address using a cloud provider.

---

## 🧪 **Useful Commands**

### 🔍 Get Endpoints

```bash
kubectl get ep -n <namespace>
```

### 📄 Get Services

```bash
kubectl get svc -n <namespace>
```


```bash
kubectl expose deployment web-server-dep -n dev --port 80 
```



---

## 🔁 **Port Forwarding**

To access a service from your local machine, forward a local port to the service port:

```bash
kubectl port-forward -n <namespace> svc/<service-name> <local-port>:<target-port>
```

> **Example:**
> Forward local port `8080` to port `80` of `my-service` in the `mynamespace` namespace:
>
> ```bash
> kubectl port-forward -n mynamespace svc/my-service 8080:80
> ```

You can also bind to all network interfaces:

```bash
kubectl port-forward -n <namespace> svc/nginx 80:80 --address 0.0.0.0
```

> 🌐 **DNS format:**
> `<service-name>.<namespace>.svc.cluster.local`

---

## 🧾 **Example Service Manifest**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  namespace: ns
  labels:
    app: web-server
spec:
  type: ClusterIP  # Options: ClusterIP, NodePort, LoadBalancer
  selector:
    app: nginx
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

> 🔍 **Note:** The `selector` must match the labels of the target Pods.
> 🧠 **Tip:** Use `kubectl describe svc <service-name>` to inspect the service and verify connectivity.



```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  namespace: ns
  labels:
    app: web-server
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: db-svc
  namespace: db
spec:
  type: NodePort
  ports:
    - name: sql
      port: 3306
      targetPort: 3306
      nodePort: 30000
  selector:
    app: db
```