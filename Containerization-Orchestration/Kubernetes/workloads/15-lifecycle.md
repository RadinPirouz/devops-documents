# Kubernetes Lifecycle Hooks: `postStart` and `preStop`

## Overview

In Kubernetes, **lifecycle hooks** allow you to run specific code when a container starts or stops. These hooks are part of a container’s lifecycle and are useful for performing setup and cleanup tasks.

The two main lifecycle hooks are:

* **`postStart`** – Executed immediately after the container starts.
* **`preStop`** – Executed just before the container stops.

These hooks can be defined inside the container specification in a Pod manifest.

---

## 1. `postStart` Hook

### Description

The `postStart` hook runs **immediately after a container is created**, but before it is marked as *Running*. It can be used to perform initialization tasks that need to occur right after startup.

The `postStart` hook supports two types of actions:

* `exec` – Run a command inside the container.
* `httpGet` – Send an HTTP request to a specified endpoint inside the container.

### Notes

* The `postStart` hook and the container’s main process run **concurrently**.
* If the hook fails, the container is considered to have failed and will be restarted according to its restart policy.

### Example

```yaml
lifecycle:
  postStart:
    exec:
      command: ["/bin/sh", "-c", "echo Container started at $(date) >> /var/log/startup.log"]
```

Using an HTTP GET action:

```yaml
lifecycle:
  postStart:
    httpGet:
      path: /startup
      port: 8080
```

### Common Use Cases

* Initializing configuration files or environment data.
* Sending startup notifications to monitoring systems.
* Preparing application dependencies.

---

## 2. `preStop` Hook

### Description

The `preStop` hook runs **just before a container is terminated**. Kubernetes will execute the hook and wait for it to complete before sending the `SIGTERM` signal to the container’s main process.

This hook is typically used to ensure a **graceful shutdown** of the application.

Like `postStart`, it supports:

* `exec`
* `httpGet`

### Notes

* The hook must complete within the time defined by `terminationGracePeriodSeconds`.
* If the hook does not finish within that time, the container will be forcibly terminated.

### Example

```yaml
lifecycle:
  preStop:
    exec:
      command: ["/bin/sh", "-c", "echo Shutting down... >> /var/log/shutdown.log && sleep 5"]
```

### Common Use Cases

* Closing active connections.
* Flushing logs or metrics.
* Deregistering the service from a load balancer or discovery system.
* Notifying external systems about the shutdown event.

---

## 3. Full Example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: lifecycle-demo
spec:
  containers:
  - name: demo-container
    image: nginx
    lifecycle:
      postStart:
        exec:
          command: ["/bin/sh", "-c", "echo 'Container started!' > /usr/share/nginx/html/index.html"]
      preStop:
        exec:
          command: ["/bin/sh", "-c", "echo 'Container stopping...' >> /usr/share/nginx/html/index.html && sleep 10"]
    terminationGracePeriodSeconds: 15
```

---

## 4. Best Practices for DevOps Engineers

1. **Handle Signals in Your Application**
   Ensure your application properly handles `SIGTERM` and `SIGKILL` for clean shutdowns.

2. **Combine Hooks with Grace Periods**
   Use `preStop` together with `terminationGracePeriodSeconds` to allow sufficient cleanup time.

3. **Monitor Hook Execution**
   Log hook outputs for debugging and verification.

4. **Avoid Long-Running or Blocking Hooks**
   Hooks should be lightweight to avoid delaying container lifecycle events.

---

## 5. Summary

| Hook Type   | Trigger Time                       | Purpose           | Common Actions                                    |
| ----------- | ---------------------------------- | ----------------- | ------------------------------------------------- |
| `postStart` | Immediately after container starts | Initialization    | Load configs, warm cache, notify service          |
| `preStop`   | Before container termination       | Graceful shutdown | Flush data, close connections, deregister service |

