# ⏳ Kubernetes Jobs

A **Job** in Kubernetes runs a pod to completion. It ensures that a specified number of pods successfully terminate.

Use Jobs for **batch processing**, **one-off tasks**, or **short-lived workloads**.

---

## 🔍 Job Commands

### 📄 List Jobs in a Namespace
```bash
kubectl get jobs.batch -n <namespace>
```

### ❌ Delete a Job

```bash
kubectl delete jobs.batch -n <namespace> <job-name>
```

---

## 🧾 Example Job Manifest

Here’s a minimal example of a Job that runs a simple `echo` command:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: myjob
  namespace: ns
spec:
  template:
    spec:
      containers:
        - name: job1
          image: alpine
          command: ["/bin/sh", "-c", "echo hello world"]
      restartPolicy: Never
```

> 💡 **Note:** Always set `restartPolicy` to `Never` or `OnFailure` for jobs.
> 📌 Jobs are useful for tasks like backups, report generation, or database migrations.

