
# **Vagrant Configuration Reference for DevOps Engineers**

This document provides a practical collection of Vagrant configurations commonly used in DevOps workflows. Each example includes explanations and recommended usage patterns.

---

# **1. Basic Ubuntu VM**

### **Vagrantfile**

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  config.vm.network "private_network", ip: "192.168.56.10"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 1
  end
end
```

### **Summary**

* Defines a simple Ubuntu VM.
* Adds private network access.
* Sets CPU and memory limits for VirtualBox.

---

# **2. VM with Shell Provisioning**

### **Vagrantfile**

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  config.vm.provision "shell", inline: <<-SHELL
    apt update
    apt install -y nginx
    systemctl enable nginx
  SHELL
end
```

### **Summary**

* Runs a shell script automatically on VM boot.
* Installs and enables Nginx.

---

# **3. Multi-Machine Environment (Web + Database)**

### **Vagrantfile**

```ruby
Vagrant.configure("2") do |config|

  config.vm.define "web" do |web|
    web.vm.box = "ubuntu/focal64"
    web.vm.hostname = "web"
    web.vm.network "private_network", ip: "192.168.56.11"

    web.vm.provision "shell", inline: <<-SHELL
      apt update
      apt install -y apache2
    SHELL
  end

  config.vm.define "db" do |db|
    db.vm.box = "ubuntu/focal64"
    db.vm.hostname = "db"
    db.vm.network "private_network", ip: "192.168.56.12"

    db.vm.provision "shell", inline: <<-SHELL
      apt update
      apt install -y mysql-server
    SHELL
  end

end
```

### **Summary**

* Creates two VMs.
* Web VM runs Apache.
* DB VM runs MySQL.
* Local network enables app-to-database communication.

---

# **4. Using Ansible for Provisioning**

### **Vagrantfile**

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yml"
    ansible.inventory_path = "hosts"
  end
end
```

### **Summary**

* Leverages Ansible for idempotent provisioning.
* Requires a playbook and inventory file.

---

# **5. Docker Provider Example**

### **Vagrantfile**

```ruby
Vagrant.configure("2") do |config|
  config.vm.provider "docker" do |d|
    d.image = "nginx:latest"
    d.remains_running = true
    d.ports = ["8080:80"]
  end
end
```

### **Summary**

* Uses Docker engine instead of a VM.
* Runs Nginx container accessible on host port 8080.

---

# **6. Synced Folder Example**

### **Vagrantfile**

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  config.vm.synced_folder "./app", "/var/www/app", type: "virtualbox"

  config.vm.provision "shell", inline: <<-SHELL
    apt update
    apt install -y nodejs npm
  SHELL
end
```

### **Summary**

* Syncs host source code into VM.
* Suitable for development environments where code updates must sync immediately.

---

# **7. Kubernetes Single-Node Cluster (kubeadm)**

### **Vagrantfile**

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "k8s-master"

  config.vm.provider "virtualbox" do |vb|
    vb.cpus = 2
    vb.memory = 4096
  end

  config.vm.provision "shell", path: "install-k8s.sh"
end
```

### **Summary**

* Boots a VM with enough resources for Kubernetes.
* Runs external script containing Kubernetes installation steps.

---

# **8. Port Forwarding with Multiple Shell Provisioners and VirtualBox Limits**

### **Vagrantfile**

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "webserver"

  # Port forwarding (host 8080 → guest 80)
  config.vm.network "forwarded_port", guest: 80, host: 8080

  # VirtualBox hardware limits
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
  end

  # Provisioner 1: package install
  config.vm.provision "shell", inline: <<-SHELL
    apt update
    apt install -y nginx curl
  SHELL

  # Provisioner 2: configuration and service restart
  config.vm.provision "shell", inline: <<-SHELL
    echo "Hello from Vagrant" > /var/www/html/index.html
    systemctl restart nginx
  SHELL
end
```

### **Summary**

* Demonstrates forwarded ports for local development.
* Runs two shell provisioners in sequence.
* Applies VirtualBox memory and CPU constraints.

---

# **Additional Recommendations**

### **General Best Practices**

* Use `config.ssh.insert_key = false` for shared team environments.
* Install recommended plugins:

  * vagrant-vbguest
  * vagrant-hostmanager
* Pin specific box versions for reproducibility.
* Store provisioning scripts in separate files for maintainability.

### **Resource Allocation Guidelines**

* Web servers: 1–2 GB RAM, 1–2 CPUs
* Kubernetes nodes: 4 GB+ RAM, 2 CPUs+
* Database nodes: 2–4 GB RAM minimum
