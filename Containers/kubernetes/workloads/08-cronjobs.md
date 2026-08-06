# CronJobs

A **CronJob** creates Jobs on a schedule (same idea as Unix cron). Use for periodic backups, reports, and cleanup tasks.

[← Jobs](./07-jobs.md) · [Kubernetes index](../README.md) · [Services →](./09-services.md)

---

![CronJob creates Jobs on a schedule](../images/cronjob.png)

## Schedule

```
┌────────── minute (0–59)
│ ┌──────── hour (0–23)
│ │ ┌────── day of month (1–31)
│ │ │ ┌──── month (1–12)
│ │ │ │ ┌── day of week (0–6, Sun=0)
* * * * *
```

Examples: `0 * * * *` (hourly), `0 2 * * *` (02:00 daily), `*/5 * * * *` (every 5 minutes).

`* * * * *` runs **every minute** — fine for labs, noisy in production.

---

## Important fields

| Field | Meaning |
| --- | --- |
| `schedule` | Cron expression (required) |
| `concurrencyPolicy` | `Allow` / `Forbid` / `Replace` overlapping runs |
| `startingDeadlineSeconds` | Skip run if missed by this many seconds |
| `successfulJobsHistoryLimit` | How many completed Jobs to keep (default 3) |
| `failedJobsHistoryLimit` | How many failed Jobs to keep (default 1) |
| `suspend` | `true` pauses new Job creation |

Timezone follows the kube-controller-manager (often UTC). Use explicit UTC schedules to avoid surprises.

---

## Commands

```bash
kubectl get cronjobs -n <namespace>
kubectl describe cronjob <name> -n <namespace>
kubectl get jobs -n <namespace>
kubectl delete cronjob <name> -n <namespace>
```

---

## Example manifest

Example: [manifests/cronjob.yaml](./manifests/cronjob.yaml)

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: date-tick
  namespace: ns
spec:
  schedule: "*/5 * * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: Never
          containers:
            - name: tick
              image: busybox:1.36
              command: ["/bin/sh", "-c", "date; echo tick"]
```

---

## Related

- [Jobs](./07-jobs.md) — completions, parallelism, backoff
