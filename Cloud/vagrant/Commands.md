# Vagrant Installation and Operations Guide (Debian/Ubuntu)

## 1. Install Vagrant on Debian/Ubuntu

Add the HashiCorp GPG key and repository, then install Vagrant:

```bash
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vagrant
```

---

## 2. Project Setup

### Initialize a Vagrant Environment

```bash
vagrant init
```

### Initialize with a Specific Base Box

```bash
vagrant init ubuntu/focal64
```

---

## 3. Lifecycle Management

### Start and Provision the VM

```bash
vagrant up
```

### Stop the VM (Graceful Shutdown)

```bash
vagrant halt
```

### Force Stop (Power Off)

```bash
vagrant halt -f
```

### Reboot the VM

```bash
vagrant reload
```

### Reload and Re-Provision

```bash
vagrant reload --provision
```

---

## 4. Provisioning

### Run Provisioners Without Restarting

```bash
vagrant provision
```

---

## 5. Box Operations

### List Installed Boxes

```bash
vagrant box list
```

### Add a Box

```bash
vagrant box add ubuntu/focal64
```

### Remove a Box

```bash
vagrant box remove ubuntu/focal64
```

---

## 6. VM Management and Access

### SSH into the Machine

```bash
vagrant ssh
```

### Get SSH Configuration

```bash
vagrant ssh-config
```

### Check VM Status

```bash
vagrant status
```

### Show Machine Information

```bash
vagrant info
```

---

## 7. Cleanup

### Destroy a VM

```bash
vagrant destroy
```

### Destroy Without Confirmation

```bash
vagrant destroy -f
```

---

## 8. Synced Folder and Debugging

### View Global VM List

```bash
vagrant global-status
```

### Prune Stale Global Entries

```bash
vagrant global-status --prune
```

### Enable Debug Output

```bash
vagrant up --debug
```
