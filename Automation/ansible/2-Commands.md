
# **Ansible Commands**

Below are some frequently used Ansible commands for managing your servers.

### **Listing Hosts**

List all hosts defined in the inventory file:

```bash
ansible --list-hosts all -i servers.ini
# or for YAML format
ansible --list-hosts all -i servers.yaml
```

### **Ping All Servers**

Check the connectivity of all servers:

```bash
ansible -m ping all -i server.ini
```

### **Execute Commands**

Run a command (e.g., `uptime`) on all servers:

```bash
ansible -m command -a "uptime" all -i server.ini
```

### **Copy Files to Servers**

Copy a file from the Ansible server to all target servers:

```bash
ansible -m copy -a "src=<file-location-on-ansible-server> dest=<destination-location-on-server>" all -i server.ini
```

### **Run Commands with Sudo**

Execute a command with elevated privileges (sudo) as the root user:

```bash
ansible -m command -a "uptime" all -i server.ini --become --become-user root --become-method sudo 
```

### **Install a Package**

Install the `nginx` package on all servers:

```bash
ansible -m apt -a "name=nginx state=present" --become --become-user root --become-method sudo
```

### **Uninstall a Package**

Remove the `nginx` package from all servers:

```bash
ansible -m apt -a "name=nginx state=absent" --become --become-user root --become-method sudo
```

### **Update and Upgrade Packages**

Update the package list and upgrade all packages:

```bash
ansible -m apt -a "upgrade=yes update_cache=yes" --become --become-user root --become-method sudo
```

---

## **Advanced Usage and Notes**

### **Special Considerations**

- **Module Limitations**: The `command` module does not support special characters or shell features. For commands requiring shell features (like pipes or redirection), use the `shell` module.
  
  Example:
  ```bash
  ansible -m shell -a "cat /etc/passwd | grep -l" all -i server.ini --become
  ```

- **Raw Module**: Use the `raw` module for devices that do not have Python installed. It allows you to execute raw SSH commands directly.

  Example:
  ```bash
  ansible -m raw -a "hostnamectl" all -i server.ini --become
  ```

### **Gathering System Facts**

Use the `setup` module to gather system facts from all servers:

```bash
ansible -m setup --become all -i server.ini
```

You can filter specific facts:

```bash
ansible -m setup -a "filter=ansible_memory" --become all -i server.ini
ansible -m setup -a "filter=ansible_distribution" --become all -i server.ini
```

