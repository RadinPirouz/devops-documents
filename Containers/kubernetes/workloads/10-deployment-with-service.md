# Deployment with Service — Walkthrough

A single manifest that creates a namespace, a Deployment, and a ClusterIP Service. The Service routes port 80 to container port 8080 on Pods labeled `app: nginx`.

Full manifest: [manifests/deployment-with-service.yaml](./manifests/deployment-with-service.yaml)

```bash
kubectl apply -f manifests/deployment-with-service.yaml
kubectl get all -n ns
```

---

![Deploy an application with Deployment and Service](../images/module-first-app.png)


## 1. Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ns
```

Isolates all resources in this example under the `ns` namespace.

---

## 2. Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: ns
  labels:
    app: nginx
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

- `selector.app: nginx` must match Pod labels created by the Deployment.
- `port: 80` is what other Pods reach via DNS (`nginx-service.ns.svc.cluster.local`).
- `targetPort: 8080` is the port the container listens on.

---

## 3. Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: ns
  labels:
    app: nginx
spec:
  replicas: 2
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
          image: nginx:latest
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 250m
              memory: 256Mi
```

- `replicas: 2` keeps two Pods running; the ReplicaSet controller recreates failed Pods.
- `containerPort: 8080` must match the Service `targetPort`.
- Resource `requests` are used for scheduling; `limits` cap usage.

---

## Verify connectivity

```bash
# Check Pods and Service
kubectl get pods,svc -n ns

# Port-forward for local testing
kubectl port-forward -n ns svc/nginx-service 8080:80

# From another Pod in the cluster
kubectl run curl --rm -it --image=curlimages/curl -n ns -- \
  curl http://nginx-service/
```

---

## Related guides

- [Services](./09-services.md) — Service types, DNS, port-forwarding
- [Deployments](./04-deployments.md) — scaling, rollouts, rollbacks
- [Ingress](./14-ingress.md) — external HTTP/HTTPS access
