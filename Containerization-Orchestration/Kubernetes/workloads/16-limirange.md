## LimitRange in Kubernetes

### Overview

A **LimitRange** in Kubernetes is a namespace-level policy object that defines constraints on the compute resources that individual **Pods** and **Containers** can request and use. It helps ensure that workloads run efficiently and fairly within a shared cluster.

A LimitRange can set:

* Minimum and maximum resource requests and limits
* Default requests and limits if none are specified by the user

While a **ResourceQuota** enforces limits at the **namespace** level (total resource usage), a **LimitRange** enforces rules at the **Pod or Container** level.

---

### Why Use a LimitRange

In a shared cluster, users might:

* Deploy Pods without specifying any resource requests or limits.
* Request excessive resources, leading to inefficient utilization.

A LimitRange prevents these issues by:

* Automatically applying default resource values when unspecified.
* Enforcing minimum and maximum resource thresholds.
* Ensuring fair distribution of resources among applications.

---

### How It Works

When a Pod or Container is created in a namespace with a LimitRange:

1. The Kubernetes API server checks if resource requests and limits are defined.
2. If they are not provided, the LimitRange applies the configured default values.
3. If provided values fall outside the configured minimum or maximum bounds, the API server rejects the creation request.

---

### Example: LimitRange YAML

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-cpu-limits
  namespace: dev-team
spec:
  limits:
  - type: Container
    max:
      cpu: "2"          # Maximum 2 cores per container
      memory: "2Gi"     # Maximum 2Gi memory per container
    min:
      cpu: "200m"       # Minimum 0.2 cores per container
      memory: "256Mi"   # Minimum 256Mi memory per container
    default:
      cpu: "500m"       # Default limit if not specified
      memory: "512Mi"
    defaultRequest:
      cpu: "250m"       # Default request if not specified
      memory: "256Mi"
```

---

### Example Behavior

| Scenario | Request/Limit Defined? | Result                                        |
| -------- | ---------------------- | --------------------------------------------- |
| None     | No                     | Defaults applied (`250m` CPU, `256Mi` Memory) |
| Too High | Yes (e.g., 3 CPU)      | Rejected — exceeds max of 2                   |
| Too Low  | Yes (e.g., 100m CPU)   | Rejected — below min of 200m                  |

---

### Viewing a LimitRange

You can inspect LimitRanges in a namespace using:

```bash
kubectl get limitrange -n dev-team
kubectl describe limitrange mem-cpu-limits -n dev-team
```

---

### LimitRange vs ResourceQuota

| Feature         | LimitRange                       | ResourceQuota                  |
| --------------- | -------------------------------- | ------------------------------ |
| Scope           | Per Container/Pod                | Per Namespace                  |
| Controls        | Min/Max/Default resource values  | Total resource usage           |
| Purpose         | Enforce sane defaults and bounds | Prevent namespace-wide overuse |
| Works best with | ResourceQuota                    | LimitRange                     |

---

### Summary

A **LimitRange** ensures that every Pod or Container in a namespace has appropriate resource requests and limits, preventing resource misuse and ensuring cluster stability. It complements **ResourceQuota** to provide complete resource management across both individual workloads and namespaces.


