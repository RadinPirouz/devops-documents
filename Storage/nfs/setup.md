# 📡 NFS Server & Client Setup Guide (Ubuntu)

Easily set up a Network File System (NFS) for sharing files between Linux systems on the same network.

---

## 🖥️ Server Configuration (Ubuntu)

### 1. Install NFS Kernel Server

Install the required package:

```bash
sudo apt update
sudo apt install nfs-kernel-server
```

### 2. Create a Shared Directory

Replace `<shared-directory>` with your preferred path:

```bash
sudo mkdir -p <shared-directory>
sudo chown nobody:nogroup <shared-directory>
sudo chmod 777 <shared-directory>
```

> ✅ *Best practice:* Use a dedicated directory for NFS shares, e.g., `/srv/nfs/shared`.

### 3. Configure NFS Exports

Create an exports configuration file:

```bash
sudo vim /etc/exports.d/shared.exports
```

Add the following line (update paths and IPs accordingly):

```
<shared-directory> <client-ip>(rw,sync,no_root_squash,no_subtree_check)
```

> 💡 **Notes:**  
> - `<shared-directory>`: Full path to the directory you want to share  
> - `<client-ip>`: IP address of the client allowed to access the share  

### 4. Apply Export Changes

```bash
sudo exportfs -ra
```

### 5. Enable and Restart NFS Service

```bash
sudo systemctl enable nfs-server
sudo systemctl restart nfs-server
```

---

## 💻 Client Configuration (Ubuntu)

### 1. Install NFS Client Packages

```bash
sudo apt update
sudo apt install nfs-common rpcbind
```

### 2. Create a Mount Point

Choose a local directory to mount the share (e.g., `/mnt/nfs`):

```bash
sudo mkdir -p <mount-point>
sudo chmod 777 <mount-point>
```

### 3. Mount the NFS Share (Temporary)

```bash
sudo mount -t nfs <server-ip>:<shared-directory> <mount-point>
```

> Example:  
> `sudo mount -t nfs 192.168.0.10:/srv/nfs/shared /mnt/nfs`

### 4. Enable Auto-Mount at Boot

Edit the fstab file:

```bash
sudo vim /etc/fstab
```

Add this line:

```
<server-ip>:<shared-directory> <mount-point> nfs defaults 0 0
```

> Example:  
> `192.168.0.10:/srv/nfs/shared /mnt/nfs nfs defaults 0 0`

### 5. Verify and Reload Mounts

```bash
sudo mount -a
```

---

## ✅ Final Checklist

- 🔄 NFS server and client packages installed  
- 📁 Shared and mount directories properly set  
- 🔐 Permissions and access IPs correctly configured  
- ⚙️ Auto-mount enabled with `/etc/fstab`  

