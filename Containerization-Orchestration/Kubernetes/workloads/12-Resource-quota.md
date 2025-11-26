resource Quota:

```bash
kubectl get resourcequota -n <ns>
```


```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
    name: my-ns-quota
    namcespace: dev
spec:
    hard:
        pod: 10
        requests.cpu: "1"
        requests.memory: "1024Mb"
        service: "5"
        configmap: "2"
```