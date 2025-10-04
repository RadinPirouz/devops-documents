# 🐳 Containerd and Kubernetes Installation Guide

A comprehensive step-by-step guide for setting up a Kubernetes cluster using **Containerd** as the container runtime. This guide is intended for Ubuntu-based systems.

---

## ⚙️ 1. Disable Swap

Kubernetes requires swap to be disabled for proper scheduling and memory management.

```bash
sudo swapoff -a
sudo sed -i '/swap/d' /etc/fstab
```

---

## 🧩 2. Enable Required Kernel Modules

Load the necessary kernel modules for networking and overlay file systems.

```bash
cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter
```

---

## 🌐 3. Enable IPv4 Forwarding

Enable packet forwarding to allow pods to communicate across the network.

```bash
sudo tee /etc/sysctl.d/99-kubernetes-cri.conf <<EOF
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

sudo sysctl --system
```

---

## 📦 4. Install and Configure Containerd

Install and configure **Containerd** with `systemd` as the cgroup driver.

```bash
sudo apt-get update && sudo apt-get install -y containerd

sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

sudo systemctl restart containerd
sudo systemctl enable containerd
```

---

## ⎈ 5. Install Kubernetes Components

Add the Kubernetes repository and install the core components: `kubelet`, `kubeadm`, and `kubectl`.

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

---

## 🔁 6. Enable Kubelet Service

Start and enable the kubelet to run on system boot.

```bash
sudo systemctl enable --now kubelet
```

---

## 🚀 7. Initialize the Kubernetes Control Plane

Initialize the cluster. Replace the IP with your master node's IP address.

```bash
sudo kubeadm init \
  --control-plane-endpoint 192.168.2.100 \
  --apiserver-advertise-address 192.168.2.100 \
  --pod-network-cidr 10.244.0.0/16 | tee kuber-install.log
```

---

## 🛠 8. Configure kubectl Access

Set up `kubectl` for the current (non-root) user.

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

---

## 🧾 9. Create Control Plane Join Command

Generate a command for other control plane nodes to join the cluster.

```bash
sudo kubeadm init phase upload-certs --upload-certs
```

Copy the **certificate key** from the output above and run:

```bash
sudo kubeadm token create --certificate-key <CERTIFICATE_KEY> --print-join-command | tee cp-command.txt
```

Replace `<CERTIFICATE_KEY>` with the actual key.

---

## 🧑‍🤝‍🧑 10. Join Control Plane and Worker Nodes

* **Control Plane Nodes**: Use the command from `cp-command.txt` on each node.
* **Worker Nodes**: Use the `kubeadm join` command printed at the end of the `kubeadm init` output or found in `kuber-install.log`.

---

## ✅ Final Step: Install a Pod Network Add-on

Choose and apply a pod network add-on (e.g., Flannel, Calico, Cilium). Here's an example with Flannel:

```bash
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
```

---

🎉 **Your Kubernetes cluster is now up and running!**
Ensure all nodes are ready by running:

```bash
kubectl get nodes
```

