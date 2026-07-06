# Kubernetes

Cluster setup, workloads, storage, and day-to-day operations with `kubectl`.

[← Back to Containers](../README.md) · [Main index](../../README.md)

---

## Directory layout

```
kubernetes/
├── setup/           Cluster bootstrap and kubectl configuration
├── workloads/       Pods, controllers, networking, config
│   └── manifests/   Example YAML files
├── storage/         Volumes, PV/PVC, Longhorn
└── operations/      kubectl reference, debugging, node management
```

---

## Learning path

| Step | Topic | Guide |
| --- | --- | --- |
| 1 | Architecture & concepts | [setup/01-overview.md](./setup/01-overview.md) |
| 2 | Install cluster (containerd + kubeadm) | [setup/02-installation.md](./setup/02-installation.md) |
| 3 | Shell setup & kubectl basics | [setup/03-kubectl-basics.md](./setup/03-kubectl-basics.md) |
| 4 | External HA etcd (optional) | [setup/04-external-etcd.md](./setup/04-external-etcd.md) |

---

## Workloads

Apply manifests from [workloads/manifests/](./workloads/manifests/) alongside each guide.

| # | Topic | Guide |
| --- | --- | --- |
| 01 | Namespaces | [workloads/01-namespaces.md](./workloads/01-namespaces.md) |
| 02 | Pods | [workloads/02-pods.md](./workloads/02-pods.md) |
| 03 | ReplicaSets | [workloads/03-replicasets.md](./workloads/03-replicasets.md) |
| 04 | Deployments | [workloads/04-deployments.md](./workloads/04-deployments.md) |
| 05 | Horizontal Pod Autoscaler (HPA) | [workloads/05-hpa.md](./workloads/05-hpa.md) |
| 06 | DaemonSets | [workloads/06-daemonsets.md](./workloads/06-daemonsets.md) |
| 07 | Jobs | [workloads/07-jobs.md](./workloads/07-jobs.md) |
| 08 | CronJobs | [workloads/08-cronjobs.md](./workloads/08-cronjobs.md) |
| 09 | Services | [workloads/09-services.md](./workloads/09-services.md) |
| 10 | Deployment + Service (walkthrough) | [workloads/10-deployment-with-service.md](./workloads/10-deployment-with-service.md) |
| 11 | ConfigMaps | [workloads/11-configmaps.md](./workloads/11-configmaps.md) |
| 12 | ResourceQuota | [workloads/12-resource-quota.md](./workloads/12-resource-quota.md) |
| 13 | Secrets | [workloads/13-secrets.md](./workloads/13-secrets.md) |
| 14 | Ingress | [workloads/14-ingress.md](./workloads/14-ingress.md) |
| 15 | Lifecycle hooks | [workloads/15-lifecycle-hooks.md](./workloads/15-lifecycle-hooks.md) |
| 16 | LimitRange | [workloads/16-limit-range.md](./workloads/16-limit-range.md) |

**Controller comparison**

| Feature | Pod | ReplicaSet | Deployment | StatefulSet | DaemonSet | Job / CronJob |
| --- | --- | --- | --- | --- | --- | --- |
| Self-healing | No | Yes | Yes | Yes | Yes | No |
| Stable network identity | No | No | No | Yes | No | No |
| Rolling updates | No | No | Yes | Yes | No | N/A |
| Runs on every node | No | No | No | No | Yes | No |
| Runs to completion | No | No | No | No | No | Yes |

Example manifests: [k8s-examples.container-solutions.com](https://k8s-examples.container-solutions.com/)

---

## Storage

| # | Topic | Guide |
| --- | --- | --- |
| 01 | Persistent Volumes & Claims | [storage/01-pv-pvc.md](./storage/01-pv-pvc.md) |
| 02 | emptyDir volumes | [storage/02-emptydir.md](./storage/02-emptydir.md) |
| 03 | Longhorn | [storage/03-longhorn.md](./storage/03-longhorn.md) |

---

## Operations

| # | Topic | Guide |
| --- | --- | --- |
| 01 | kubectl reference | [operations/01-kubectl-reference.md](./operations/01-kubectl-reference.md) |
| 02 | Logs & debugging | [operations/02-debugging.md](./operations/02-debugging.md) |
| 03 | Node management | [operations/03-node-management.md](./operations/03-node-management.md) |
| 04 | Labels & selectors | [operations/04-labels.md](./operations/04-labels.md) |
| 05 | crictl (CRI runtime CLI) | [operations/05-crictl.md](./operations/05-crictl.md) |

---

## Quick reference

```bash
# Cluster health
kubectl get nodes
kubectl get pods -A

# Apply a manifest
kubectl apply -f manifest.yaml -n <namespace>

# Inspect a resource
kubectl describe pod <name> -n <namespace>
kubectl logs -f <pod> -n <namespace>

# Port-forward a Service
kubectl port-forward -n <namespace> svc/<service> 8080:80
```
