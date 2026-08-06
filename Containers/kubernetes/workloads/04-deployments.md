# Deployments

A **Deployment** manages ReplicaSets and provides declarative updates for Pods — scaling, rolling updates, pause/resume, and rollbacks.

Prefer Deployments over bare Pods or ReplicaSets for almost all long-running stateless apps.

[← ReplicaSets](./03-replicasets.md) · [Kubernetes index](../README.md) · [HPA →](./05-hpa.md)

---

![Deployment rolling update of Pods](../images/module-deployment.png)

![Rolling update replaces Pods gradually](../images/rolling-update.png)

## Commands

```bash
kubectl get deploy -n <namespace>
kubectl describe deploy <name> -n <namespace>
kubectl edit deploy <name> -n <namespace>

# Scale
kubectl scale deploy <name> --replicas=5 -n <namespace>

# Change image (creates a new revision)
kubectl set image deploy/<name> <container>=<image>:<tag> -n <namespace>

# Rollout
kubectl rollout status deploy/<name> -n <namespace>
kubectl rollout history deploy/<name> -n <namespace>
kubectl rollout history deploy/<name> --revision=2 -n <namespace>
kubectl rollout undo deploy/<name> -n <namespace>
kubectl rollout undo deploy/<name> --to-revision=2 -n <namespace>
kubectl rollout pause deploy/<name> -n <namespace>
kubectl rollout resume deploy/<name> -n <namespace>
```

Unlike editing a ReplicaSet, changing a Deployment’s Pod template triggers a controlled rollout.

---

## Rolling update strategy

Default strategy is `RollingUpdate`:

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 25%
      maxSurge: 25%
```

| Field | Meaning |
| --- | --- |
| `maxUnavailable` | How many Pods may be down during the update |
| `maxSurge` | How many extra Pods may exist above `replicas` |

`Recreate` kills all old Pods before creating new ones (downtime). See also overview notes on blue/green and canary patterns.

---

## Example manifest

Example: [manifests/deployment.yaml](./manifests/deployment.yaml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: dev
  labels:
    app: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 250m
              memory: 256Mi
```

---

## Comparison

| Feature | Pod | ReplicaSet | Deployment |
| --- | --- | --- | --- |
| Manual one-off | Yes | No | No |
| Scales Pods | No | Yes | Yes |
| Self-healing | No | Yes | Yes |
| Rolling updates | No | No | Yes |
| Revision history | No | No | Yes |

---

## Related

- [HPA](./05-hpa.md) — autoscale replica count
- [Deployment + Service walkthrough](./10-deployment-with-service.md)
- [Services](./09-services.md)
