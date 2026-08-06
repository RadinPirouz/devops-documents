# Ingress

An **Ingress** exposes HTTP and HTTPS routes from outside the cluster to Services inside it. It provides host-based and path-based routing, TLS termination, and load balancing — typically through an **Ingress controller** (NGINX, Traefik, HAProxy, etc.).

```
Internet → Ingress Controller → Ingress rules → Service → Pods
```

> Ingress only defines routing rules. You must install an Ingress controller separately for rules to take effect.

---

![Ingress routes HTTP(S) traffic to Services](../images/ingress.png)

![Ingress fan-out routing to multiple Services](../images/ingress-fanout.png)


## Prerequisites

1. A running Ingress controller in the cluster.
2. A Service that matches the backend you want to expose.

**NGINX Ingress Controller** (common choice):

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.3/deploy/static/provider/cloud/deploy.yaml
```

Verify:

```bash
kubectl get pods -n ingress-nginx
```

---

## Commands

```bash
# List Ingress resources
kubectl get ingress -n <namespace>

# Inspect routing rules and backend Services
kubectl describe ingress <name> -n <namespace>

# Delete
kubectl delete ingress <name> -n <namespace>
```

---

## Example: path-based routing

Routes `/` to an nginx Service and `/api` to an API Service:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: web
spec:
  ingressClassName: nginx
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nginx-service
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 8080
```

---

## Example: TLS termination

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-ingress
  namespace: web
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls-secret
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nginx-service
                port:
                  number: 80
```

Create the TLS Secret (or use cert-manager for automatic certificates):

```bash
kubectl create secret tls app-tls-secret \
  --cert=path/to/tls.crt \
  --key=path/to/tls.key \
  -n web
```

---

## Ingress vs Service types

| Approach | Use when |
| --- | --- |
| `ClusterIP` + Ingress | HTTP/HTTPS routing with host/path rules (recommended for web apps) |
| `NodePort` | Quick testing; exposes a port on every node |
| `LoadBalancer` | Cloud LB per Service; simpler but one LB per Service |
| `ClusterIP` + `port-forward` | Local debugging only |

---

## Troubleshooting

```bash
# Check controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller

# Verify backend endpoints exist
kubectl get endpoints -n <namespace>

# Test from inside the cluster
kubectl run curl --rm -it --image=curlimages/curl -- \
  curl -H "Host: app.example.com" http://<ingress-controller-ip>/
```

Common issues:

- **404 / no route** — `host` or `path` does not match the request; check `pathType` (`Prefix`, `Exact`, `ImplementationSpecific`).
- **502 / no endpoints** — Service selector does not match Pod labels, or Pods are not ready.
- **TLS errors** — Secret missing, wrong namespace, or certificate does not cover the hostname.
