
- **Stream Logs for a Running Pod**

  ```bash
  kubectl logs -f -n <namespace-name> <pod-name>
  ```



  ```bash
  kubectl logs -f -n <namespace-name> <pod-name> -c <container-name>
  ```



- **Get Detailed Information About a Pod**

  ```bash
  kubectl describe pod <pod-name> -n <namespace-name>
  ```


in log swith the pod need to be up 

but in describe dont need to pod be up

describe work on all components