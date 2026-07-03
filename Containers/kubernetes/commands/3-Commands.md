# Kubernetes Command Reference

This guide provides a concise reference for common `kubectl` commands used to manage Kubernetes clusters. Whether you’re managing nodes, namespaces, pods, deployments, or autoscaling, the examples below will help you perform everyday tasks with confidence.

## General Commands

- **List API Resources**  
  Display all available API resources along with their short names:

  ```bash
  kubectl api-resources
  ```

---
## API Resources & Documentation

- **Get Detailed Documentation for an API Resource**

  ```bash
  kubectl explain <api-resource-name>
  ```

  *Example:*

  ```bash
  kubectl explain pod
  ```

  ```bash
  kubectl explain pod.metadata
  ```


---

## Applying YAML Files

- **Apply a Configuration from a YAML File**

  Apply a YAML configuration to a specific namespace:

  ```bash
  kubectl apply -f <yaml-file> -n <namespace-name>
  ```

---

## Viewing Cluster Resources

- **Display All Resources in a Namespace**

  ```bash
  kubectl get all -n <namespace-name>
  ```

- **Display ReplicaSets, Pods, and Deployments in a Specific Namespace**

  ```bash
  kubectl get rs,pods,deployments -n <namespace-name>
  ```

---

## ReplicaSet & Deployment Management

### Scaling and Rollouts

- **Scale a ReplicaSet**

  ```bash
  kubectl scale rs <replicaset-name> --replicas=<count> -n <namespace-name>
  ```

- **View Rollout History of a Deployment**

  ```bash
  kubectl rollout history deployment <deployment-name> -n <namespace-name>
  ```

- **View Details of a Specific Revision**

  ```bash
  kubectl rollout history deployment <deployment-name> -n <namespace-name> --revision=<number>
  ```

- **Roll Back a Deployment to a Specific Revision**

  ```bash
  kubectl rollout undo deployment <deployment-name> -n <namespace-name> --to-revision=<number>
  ```

### Autoscaling

- **Autoscale a Deployment**  
  Automatically scale a deployment based on CPU utilization:

  ```bash
  kubectl autoscale deployment <deployment-name> -n <namespace-name> --cpu-percent=<target-cpu-percentage> --min=<min-pods> --max=<max-pods>
  ```

- **View Horizontal Pod Autoscalers (HPA)**

  ```bash
  kubectl get hpa -n <namespace-name>
  ```

---


---

## Additional Information

- **Static Manifest Files**  
  Any YAML files placed in `/etc/kubernetes/manifests/` are automatically loaded when the kubelet starts (for example, after a server reboot).



```bash
kubectl cp -n <ns> <pod-name>:dir/ ./
```
