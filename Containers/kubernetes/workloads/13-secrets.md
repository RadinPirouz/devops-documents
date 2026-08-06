# Secrets

Store sensitive data (passwords, tokens, TLS keys) separately from Pod specs and images. Secrets are **base64-encoded in etcd by default — not encrypted**. Treat them as confidential config, not a vault.

[← ResourceQuota](./12-resource-quota.md) · [Kubernetes index](../README.md) · [Ingress →](./14-ingress.md)

---

![Secret mounts sensitive data into Pods](../images/secret.png)

## Common types

| Type | Use |
| --- | --- |
| `Opaque` | Arbitrary key/value (default) |
| `kubernetes.io/tls` | TLS cert + key |
| `kubernetes.io/dockerconfigjson` | Private registry pull credentials |
| `kubernetes.io/basic-auth` | Username / password |
| `kubernetes.io/ssh-auth` | SSH private key |

---

## Create

```bash
# Generic (Opaque)
kubectl create secret generic db-pass \
  --from-literal=username=admin \
  --from-literal=password='s3cret' \
  -n <namespace>

# From files
kubectl create secret generic app-config \
  --from-file=./username.txt \
  --from-file=./password.txt \
  -n <namespace>

# TLS
kubectl create secret tls my-tls \
  --cert=path/to/tls.crt \
  --key=path/to/tls.key \
  -n <namespace>

# Registry
kubectl create secret docker-registry regcred \
  --docker-server=<registry> \
  --docker-username=<user> \
  --docker-password=<pass> \
  -n <namespace>

kubectl get secrets -n <namespace>
kubectl describe secret db-pass -n <namespace>
```

Never commit real secret values to git. Prefer sealed-secrets, External Secrets, or a cloud KMS in production; enable encryption at rest for etcd when you can.

---

## Manifest (`stringData`)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-pass
  namespace: ns
type: Opaque
stringData:
  username: admin
  password: "s3cret"
```

`stringData` is plaintext in YAML; the API server stores `data` as base64. You can also put base64 values under `data:` yourself.

---

## Use in a Pod — environment

```yaml
env:
  - name: MARIADB_ROOT_PASSWORD
    valueFrom:
      secretKeyRef:
        name: db-pass
        key: password
```

---

## Use in a Pod — volume mount

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
  namespace: ns
spec:
  containers:
    - name: app
      image: busybox:1.36
      command: ["sleep", "3600"]
      volumeMounts:
        - name: creds
          mountPath: /etc/creds
          readOnly: true
  volumes:
    - name: creds
      secret:
        secretName: db-pass
```

Each key becomes a file under `/etc/creds` (for example `/etc/creds/password`).

For private images on the Pod:

```yaml
spec:
  imagePullSecrets:
    - name: regcred
```

---

## Related

- [ConfigMaps](./11-configmaps.md) — non-sensitive configuration
- [Ingress](./14-ingress.md) — TLS Secrets for HTTPS
