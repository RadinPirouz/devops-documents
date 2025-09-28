# Setting Up a Reverse Proxy with Nginx

A reverse proxy can forward client requests to multiple backend servers, helping manage traffic, load balance, and secure the backend infrastructure. This guide provides a step-by-step approach to setting up a basic reverse proxy configuration in Nginx.

---

## Prerequisites

- **Nginx Installed**: Ensure that Nginx is installed and running on your server.
- **Root or sudo privileges** to edit configuration files and restart Nginx.
- **Backend Servers**: At least two backend services or applications you want to proxy, such as `http://web1.com` and `http://web2.com`.

---

## Step 1: Create the Reverse Proxy Configuration File

1. **Open a new configuration file** for your reverse proxy in Nginx's `sites-available` directory:
   ```bash
   sudo vim /etc/nginx/sites-available/reverse-proxy.conf
   ```

2. **Define the Reverse Proxy Configuration**
   Copy the following configuration into the file. Adjust the backend server names (`web1.com` and `web2.com`) to match your actual server addresses.

   ```nginx
   server {
       listen 80;
       server_name _;  # Use "_" to accept any hostname, or specify a domain name

       # Proxy for the first backend application
       location /web1 {
           proxy_pass http://web1.com;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       # Proxy for the second backend application
       location /web2 {
           proxy_pass http://web2.com;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       # Log settings
       access_log /var/log/nginx/reverse-proxy-access.log;
       error_log /var/log/nginx/reverse-proxy-error.log;
   }
   ```

   ### Explanation of Key Directives
   - **listen**: Specifies the port Nginx will listen on (80 for HTTP).
   - **server_name**: The domain name or IP address for this reverse proxy. Using `_` allows it to accept any hostname.
   - **location**: Defines the URL path (`/web1`, `/web2`) to route to different backend servers.
   - **proxy_pass**: Specifies the backend server URL to which traffic should be forwarded.
   - **proxy_set_header**: Sets headers that pass client information to the backend, preserving the original IP and protocol.
   - **access_log**: Logs access requests.
   - **error_log**: Logs error messages for easier troubleshooting.

---

## Step 2: Enable the Reverse Proxy Configuration

1. **Create a symbolic link** from `sites-available` to `sites-enabled` to enable the reverse proxy configuration in Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/reverse-proxy.conf
   ```

2. **Verify Nginx Configuration**
   Run a configuration test to ensure there are no syntax errors:
   ```bash
   sudo nginx -t
   ```

3. **Reload Nginx** to apply the changes:
   ```bash
   nginx -s reload
   ```

---

## Step 3: Access Your Reverse Proxy

With the reverse proxy set up, you can now access your backend services using the following URLs:

- **http://your-server-ip/web1**: For requests proxied to `http://web1.com`
- **http://your-server-ip/web2**: For requests proxied to `http://web2.com`

Replace `your-server-ip` with the actual IP address or domain name of your Nginx server.

---

## Troubleshooting Common Issues

- **Error: 502 Bad Gateway**
  - This error usually occurs if the backend server is down or unreachable. Verify that the backend server addresses (`http://web1.com`, `http://web2.com`) are correct and accessible.

- **Permission Denied for Log Files**
  - Make sure the log file paths are writable by Nginx. Use `sudo chown www-data:www-data /var/log/nginx/reverse-proxy-access.log` if necessary.

- **Configuration Errors**
  - Always test configuration changes using `sudo nginx -t` before reloading or restarting Nginx.

---

