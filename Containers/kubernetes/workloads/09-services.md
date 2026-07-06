# Kubernetes Services

A **Service** provides a stable network endpoint for a set of Pods. It uses label selectors to route traffic and gets a cluster-internal DNS name automatically.

```
Client → Service (stable IP/DNS) → Endpoints → Pods
```

---

## Service types

| Type | Scope | Use case |
| --- | --- | --- |
| `ClusterIP` | In-cluster only | Default; internal microservice communication |
| `NodePort` | External via node IP + port | Testing, bare-metal without cloud LB |
| `LoadBalancer` | External via cloud LB | Production external access (cloud) |
| Headless (`clusterIP: None`) | DNS returns Pod IPs directly | StatefulSets, databases, custom service discovery |

**DNS format:** `<service-name>.<namespace>.svc.cluster.local`

---

## Commands

```bash
# List Services and Endpoints
kubectl get svc -n <namespace>
kubectl get endpoints -n <namespace>

# Create a Service from an existing Deployment
kubectl expose deployment <deployment-name> --port=80 -n <namespace>

# Inspect
kubectl describe svc <service-name> -n <namespace>
```

---

## Port forwarding

Access a Service from your local machine:

```bash
kubectl port-forward -n <namespace> svc/<service-name> <local-port>:<service-port>
```

Bind to all interfaces (not just localhost):

```bash
kubectl port-forward -n <namespace> svc/<service-name> 80:80 --address 0.0.0.0
```

---

## Example: ClusterIP

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  namespace: web
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

`selector` labels must match the target Pods. `port` is the Service port; `targetPort` is the container port.

---

## Example: NodePort

```yaml
apiVersion: v1
kind: Service
metadata:
  name: db-svc
  namespace: db
spec:
  type: NodePort
  selector:
    app: db
  ports:
    - name: sql
      port: 3306
      targetPort: 3306
      nodePort: 30000
```

Access via `<any-node-ip>:30000`. `nodePort` must be in range 30000–32767.

---

## Example: LoadBalancer

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-lb
  namespace: web
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

---

## Example: Headless Service

No virtual IP — DNS resolves directly to Pod IPs. Required for StatefulSet stable network identity.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-headless
  namespace: db
spec:
  clusterIP: None
  selector:
    app: mysql
  ports:
    - port: 3306
      targetPort: 3306
```

---

## Related

- [Deployment with Service walkthrough](./10-deployment-with-service.md)
- [Ingress](./14-ingress.md) — HTTP/HTTPS routing from outside the cluster
