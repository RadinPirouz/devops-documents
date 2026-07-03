### **1st Document: Namespace**

```yaml
apiVersion: v1
```

* Specifies the API version used. Here, it's version 1 of the core Kubernetes API.

```yaml
kind: Namespace
```

* Declares the resource type. This is a **Namespace**, which logically isolates groups of resources.

```yaml
metadata:
  name: ns
```

* Metadata block.

  * `name: ns` sets the name of the namespace to `ns`.

---

### **2nd Document: Service**

```yaml
---
```

* Separates multiple documents in the YAML file.

```yaml
apiVersion: v1
```

* Uses the core v1 API again.

```yaml
kind: Service
```

* Declares a **Service** resource, which provides stable networking to access pods.

```yaml
metadata:
  name: nginx-service
  namespace: ns
  labels:
    app: nginx
```

* Metadata block:

  * `name: nginx-service`: name of the Service.
  * `namespace: ns`: places this service in the previously created `ns` namespace.
  * `labels`: key-value pairs used for organizing and selecting resources. Here, `app: nginx`.

```yaml
spec:
  type: ClusterIP
```

* `spec` describes the behavior.

  * `type: ClusterIP`: exposes the service internally within the cluster using a virtual IP.

```yaml
  selector:
    app: nginx
```

* This selects pods with the label `app: nginx` to receive traffic from this service.

```yaml
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

* Defines port configuration:

  * `name: http`: a name for the port (optional but useful for readability).
  * `port: 80`: the port that the service exposes internally.
  * `targetPort: 8080`: the port on the pod that receives the traffic.

---

### **3rd Document: Deployment**

```yaml
---
```

* Separates from the previous document.

```yaml
apiVersion: apps/v1
```

* Uses the `apps/v1` API group, suitable for deployments and other controllers.

```yaml
kind: Deployment
```

* Declares a **Deployment**, which ensures a specified number of pod replicas are running.

```yaml
metadata:
  name: nginx-deployment
  namespace: ns
  labels:
    app: nginx
```

* Metadata block:

  * `name: nginx-deployment`: name of the deployment.
  * `namespace: ns`: places this in the `ns` namespace.
  * `labels: app: nginx`: used for matching with selectors.

```yaml
spec:
  replicas: 2
```

* Desired number of pod replicas to run: 2.

```yaml
  selector:
    matchLabels:
      app: nginx
```

* Tells the deployment which pods to manage, by matching labels (`app: nginx`).

```yaml
  template:
    metadata:
      labels:
        app: nginx
```

* Template for creating new pods:

  * Each pod created will have `app: nginx` label.

```yaml
    spec:
      containers:
        - name: nginx
          image: nginx:latest
```

* Pod spec:

  * One container named `nginx`, using the latest official Nginx image.

```yaml
          ports:
            - containerPort: 8080
```

* The container exposes port 8080 (must match the `targetPort` in the Service).

```yaml
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "250m"
              memory: "256Mi"
```

* **Resource management**:

  * `requests`: the minimum guaranteed resources.

    * `cpu: 100m` = 0.1 CPU core.
    * `memory: 128Mi` = 128 MiB RAM.
  * `limits`: the maximum resources the container can use.

    * `cpu: 250m` = 0.25 CPU core.
    * `memory: 256Mi` = 256 MiB RAM.

