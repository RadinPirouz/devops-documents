# ConfigMaps

Store non-confidential configuration as key/value data and inject it into Pods as env vars or files. Keep images free of environment-specific config.

[← Deployment + Service](./10-deployment-with-service.md) · [Kubernetes index](../README.md) · [ResourceQuota →](./12-resource-quota.md)

---

![ConfigMap injects configuration into Pods](../images/configmap.png)

## What is a ConfigMap?

A **ConfigMap** holds **non-secret** configuration. You can:

* Mount it as files inside a Pod
* Expose it as environment variables
* Decouple container images from environment-specific settings

---

## Creating a ConfigMap

You can create a ConfigMap from files or directories:

```bash
kubectl -n <namespace> create configmap <configmap-name> --from-file=<file-or-directory>
```

### Examples

```bash
# From a single file
kubectl -n <ns> create configmap nginx-conf --from-file=./nginx.conf

# From multiple files
kubectl -n <ns> create configmap nginx-conf \
  --from-file=./nginx.conf \
  --from-file=./site.conf
```

---

## Viewing & Editing ConfigMaps

```bash
# List all ConfigMaps in a namespace
kubectl get cm -n <namespace>

# View detailed ConfigMap info
kubectl describe configmap <name> -n <namespace>

# Edit in-place
kubectl -n <namespace> edit configmap <configmap-name>
```

---

## YAML: ConfigMap Example

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: game-demo
data:
  player_initial_lives: "3"
  ui_properties_file_name: "user-interface.properties"

  game.properties: |
    enemy.types=aliens,monsters
    player.maximum-lives=5    

  user-interface.properties: |
    color.good=purple
    color.bad=yellow
    allow.textmode=true    
```

---

## Usage Examples

### ConfigMap as Environment Variables

**ConfigMap:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: default
data:
  APP_MODE: "production"
  LOG_LEVEL: "info"
  FEATURE_FLAG_X: "enabled"
```

**Pod:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
    - name: my-container
      image: busybox
      command: ["/bin/sh", "-c", "env && sleep 3600"]
      envFrom:
        - configMapRef:
            name: app-config
```

---

### Mounting ConfigMap as a File (nginx.conf example)

**ConfigMap:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: default
data:
  nginx.conf: |
    worker_processes  1;

    events {
        worker_connections  1024;
    }

    http {
        include       mime.types;
        default_type  application/octet-stream;

        sendfile        on;
        keepalive_timeout  65;

        server {
            listen       80;
            server_name  localhost;

            location / {
                root   /usr/share/nginx/html;
                index  index.html index.htm;
            }

            error_page   500 502 503 504  /50x.html;
            location = /50x.html {
                root   /usr/share/nginx/html;
            }
        }
    }
```

**Pod:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
    - name: nginx
      image: nginx:latest
      volumeMounts:
        - name: nginx-config-volume
          mountPath: /etc/nginx/nginx.conf
          subPath: nginx.conf
  volumes:
    - name: nginx-config-volume
      configMap:
        name: nginx-config
```

---

## Notes

* Sensitive data → use [Secrets](./13-secrets.md), not ConfigMaps.
* Updating a ConfigMap does **not** restart Pods automatically. Remounted files may update (depending on kubelet sync); env vars usually need a rollout: `kubectl rollout restart deploy/<name>`.
* Optional: `immutable: true` on the ConfigMap to block updates (safer for hashed/referenced configs).
* Load many keys from a `.env`-style file:

  ```bash
  kubectl create configmap my-config --from-env-file=env.list -n <namespace>
  ```

