# 📈 Horizontal Pod Autoscaler (HPA)

The Horizontal Pod Autoscaler automatically scales the number of pods in a deployment based on observed CPU utilization (or other select metrics).

---

## ⚙️ Basic Commands

### 🚀 Create an HPA
Create an HPA for a deployment, scaling based on CPU usage:

```bash
kubectl -n <namespace> autoscale deployment <deployment-name> --cpu-percent=20 --min=4 --max=10
````

### 📊 View Existing HPAs

List all HPAs in a specific namespace:

```bash
kubectl get hpa -n <namespace>
```

### ❌ Delete an HPA

Remove a Horizontal Pod Autoscaler:

```bash
kubectl delete hpa -n <namespace> <hpa-name>
```

### 🛠️ Edit an HPA

Manually edit an existing HPA configuration:

```bash
kubectl edit hpa -n <namespace> <hpa-name>
```

---

## 🧾 Example HPA Manifest

You can define an HPA using a YAML file for more control:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hpa-test
  namespace: dev
spec:
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

> ℹ️ **Note:** The above manifest uses API version `autoscaling/v2` for enhanced metric support.

---

