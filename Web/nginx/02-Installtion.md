# Installing Nginx

## Prerequisites
Before installing Nginx, ensure that you have root or sudo privileges on your system to carry out installation and configuration commands.

## Step-by-Step Installation

### For Debian-Based Systems (e.g., Ubuntu)

1. **Update Package Repositories**  
   It’s a good practice to update your package repositories before installing new software to ensure you’re downloading the latest version available.
   ```bash
   sudo apt update
   ```

2. **Install Nginx**
   Install Nginx from the package repository.
   ```bash
   sudo apt install nginx
   ```

3. **Start Nginx Service**
   Once installed, start the Nginx service.
   ```bash
   sudo systemctl start nginx
   ```

4. **Enable Nginx to Start on Boot**
   This command configures Nginx to start automatically whenever the server reboots.
   ```bash
   sudo systemctl enable nginx
   ```

5. **Check Status (Optional)**
   Verify that Nginx is running correctly.
   ```bash
   sudo systemctl status nginx
   ```

### For Red Hat-Based Systems (e.g., CentOS, Fedora)

1. **Update Package Repositories**
   As with Debian-based systems, it’s recommended to update repositories first.
   ```bash
   sudo yum update
   ```

2. **Install Nginx**
   On Red Hat-based systems, install Nginx with `yum`.
   ```bash
   sudo yum install nginx
   ```

3. **Start Nginx Service**
   Start Nginx after installation.
   ```bash
   sudo systemctl start nginx
   ```

4. **Enable Nginx to Start on Boot**
   Configure Nginx to launch automatically on system startup.
   ```bash
   sudo systemctl enable nginx
   ```

5. **Check Status (Optional)**
   Confirm that Nginx is running and functioning properly.
   ```bash
   sudo systemctl status nginx
   ```

---

## Post-Installation Steps

1. **Allow Nginx Through the Firewall**
   If your server has a firewall enabled, you may need to allow HTTP (port 80) and HTTPS (port 443) traffic.

   ### Debian-Based Systems:
   ```bash
   sudo ufw allow 'Nginx Full'
   ```

   ### Red Hat-Based Systems:
   ```bash
   sudo firewall-cmd --permanent --add-service=http
   sudo firewall-cmd --permanent --add-service=https
   sudo firewall-cmd --reload
   ```

2. **Verify Installation**
   Open a web browser and navigate to your server’s IP address or domain name:
   ```
   http://<your-server-ip>
   ```
   You should see the default Nginx welcome page, which confirms that the installation is successful.

---

## Troubleshooting Common Installation Issues

- **Error: Package Not Found**  
  If you encounter an error stating that the Nginx package was not found, you may need to install the **EPEL repository** (Extra Packages for Enterprise Linux) on Red Hat-based systems:
  ```bash
  sudo yum install epel-release
  sudo yum install nginx
  ```

- **Permission Denied Errors**  
  Ensure you’re using `sudo` to run commands that require root privileges.

- **Firewall Blocking Access**  
  If you can’t access Nginx via a browser, ensure that firewall rules are configured to allow HTTP/HTTPS traffic.

