# Node Labels

Labels on nodes are used for scheduling (node selectors, affinity), organization, and tooling.

---

## Set a label

```bash
kubectl label node <node-name> <key>=<value>
```

Example:

```bash
kubectl label node worker-1 disktype=ssd
kubectl label node worker-1 zone=us-east-1a
```

---

## View labels

```bash
kubectl get nodes --show-labels
kubectl describe node <node-name>
```

---

## Update or remove a label

```bash
# Overwrite an existing label
kubectl label node <node-name> <key>=<new-value> --overwrite

# Remove a label
kubectl label node <node-name> <key>-
```

---

## Use labels in Pod specs

```yaml
spec:
  nodeSelector:
    disktype: ssd
```

For more expressive rules, use `nodeAffinity` in the Pod spec.
