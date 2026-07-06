# Logs and Debugging

Commands for inspecting Pod state, streaming logs, and troubleshooting failed workloads.

---

## Stream logs

```bash
# Follow logs from a Pod
kubectl logs -f -n <namespace> <pod-name>

# Multi-container Pod — specify the container
kubectl logs -f -n <namespace> <pod-name> -c <container-name>

# Previous container instance (after a crash/restart)
kubectl logs -n <namespace> <pod-name> --previous
```

> `kubectl logs` requires the Pod to be running (or to have a previous instance). For terminated Pods, use `--previous` or `kubectl describe`.

---

## Describe resources

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl describe deployment <name> -n <namespace>
kubectl describe node <node-name>
```

`describe` works even when a Pod is not running. Check **Events** at the bottom for scheduling failures, image pull errors, probe failures, and OOM kills.

---

## Quick diagnostics

```bash
# All resources in a namespace
kubectl get all -n <namespace>

# Pod details (IP, node, restarts)
kubectl get pods -o wide -n <namespace>

# Events cluster-wide (recent issues)
kubectl get events -A --sort-by='.lastTimestamp'

# Execute into a running Pod
kubectl exec -it -n <namespace> <pod-name> -- /bin/sh

# Copy files from a Pod
kubectl cp -n <namespace> <pod-name>:/path/to/dir ./local-dir
```

---

## Common failure patterns

| Symptom | What to check |
| --- | --- |
| `ImagePullBackOff` | Image name/tag, registry credentials, network |
| `CrashLoopBackOff` | `kubectl logs --previous`, entrypoint/command, probes |
| `Pending` | Node resources, taints, PVC binding, `kubectl describe pod` events |
| `OOMKilled` | Memory limits too low; check `kubectl describe pod` |
| Service unreachable | Endpoints (`kubectl get ep`), selector labels, `targetPort` |
