# kubectl Basic Setup

Shell completion, useful aliases, and context management for day-to-day cluster work.

---

![kubectl talks to the API server](../images/kubectl.png)


## Shell completion

Enable tab completion for `kubectl`:

```bash
kubectl completion <shell>
```

**Zsh** (add to `~/.zshrc`):

```bash
kubectl completion zsh > "${fpath[1]}/_kubectl"
```

**Bash** (add to `~/.bashrc`):

```bash
kubectl completion bash > ~/.kube/completion.bash.inc
source ~/.kube/completion.bash.inc
```

---

## Useful aliases

Add to your shell profile:

```bash
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get svc'
alias kgn='kubectl get nodes'
alias kaf='kubectl apply -f'
alias kdel='kubectl delete'
alias klog='kubectl logs -f'
```

---

## Context and namespace

```bash
# List contexts
kubectl config get-contexts

# Switch context (cluster)
kubectl config use-context <context-name>

# Set default namespace for current context
kubectl config set-context --current --namespace=<namespace>

# Run a single command in another namespace
kubectl get pods -n <namespace>
```

---

## Verify access

After [cluster installation](./02-installation.md), confirm `kubectl` can reach the API server:

```bash
kubectl cluster-info
kubectl get nodes
kubectl get pods -A
```
