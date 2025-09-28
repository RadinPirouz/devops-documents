# Setting Up a Web Server on Nginx

This guide covers the steps to configure Nginx as a basic web server to serve static HTML files and handle HTTP requests. We'll set up a sample web server on a Debian-based system, but the steps are similar for other Linux distributions.

---

## Prerequisites

- A server with **Nginx installed**. If you haven’t installed Nginx yet, follow the installation instructions in the [Nginx Installation Guide](2-Installtion.md) (or use the provided installation commands).
- **Root or sudo privileges** to edit configuration files and restart Nginx services.

---

## Step 1: Set Up the Web Directory

1. **Create a Directory for Your Website**
   Nginx typically serves content from `/var/www/`. Create a new directory for your website content.
   ```bash
   sudo mkdir -p /var/www/example.com/html
   ```

2. **Set Permissions**
   Ensure that the Nginx user (usually `www-data`) has permission to read files in this directory.
   ```bash
   sudo chown -R $USER:$USER /var/www/example.com/html
   sudo chmod -R 755 /var/www/example.com
   ```

3. **Add a Sample HTML File**
   Create a simple HTML file to confirm the setup.
   ```bash
   echo "<html>
   <head>
      <title>Welcome to Example.com!</title>
   </head>
   <body>
      <h1>Success! Nginx is serving your website.</h1>
   </body>
   </html>" | sudo tee /var/www/example.com/html/index.html
   ```

---

## Step 2: Configure Nginx to Serve the Website

1. **Create a Server Block Configuration File**
   Nginx server blocks (similar to Apache virtual hosts) allow you to host multiple sites on the same server. Create a new configuration file for your site.
   ```bash
   sudo vim /etc/nginx/sites-available/example.com
   ```

2. **Add Server Block Configuration**
   Paste the following configuration into the file, replacing `example.com` with your domain or IP address:

   ```nginx
   server {
       listen 80;
       server_name example.com www.example.com;

       root /var/www/example.com/html;
       index index.html;

       location / {
           try_files $uri $uri/ =404;
       }
   }
   ```

3. **Enable the Server Block**
   Link the configuration file to `sites-enabled` to enable it in Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
   ```

4. **Test the Nginx Configuration**
   Run the following command to check for any syntax errors in the configuration:
   ```bash
   sudo nginx -t
   ```

5. **Reload Nginx to Apply Changes**
   If the syntax test passes, reload Nginx to apply the new configuration.
   ```bash
   sudo systemctl reload nginx
   ```

---

## Step 3: Configure DNS (Optional)

If you have a domain name, point it to your server’s IP address in your DNS provider’s settings. Create an A record for `example.com` and, if desired, `www.example.com` to direct traffic to your server’s IP address.

---

## Step 4: Access Your Website

In a web browser, navigate to `http://example.com` (replace `example.com` with your domain or IP address). You should see the sample HTML page you created, confirming that Nginx is serving your web content.

---

## Optional: Enabling HTTPS with SSL/TLS

For added security, you can configure HTTPS on your Nginx web server. One free and easy way to do this is by using **Let’s Encrypt**.

1. **Install Certbot and the Nginx Plugin**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Obtain and Install a Certificate**
   Run the following Certbot command to automatically obtain and configure an SSL certificate for your website:
   ```bash
   sudo certbot --nginx -d example.com -d www.example.com
   ```

3. **Verify Renewal Process**
   Certificates from Let’s Encrypt expire every 90 days. To automatically renew the certificates, add a cron job or use Certbot’s built-in renewal service:
   ```bash
   sudo certbot renew --dry-run
   ```

Now your website will be accessible securely at `https://example.com`.

---

## Nginx Configuration Summary

Here's a quick reference for the key commands and file paths:

- **Site root directory**: `/var/www/example.com/html`
- **Nginx configuration files**:
  - Site-specific: `/etc/nginx/sites-available/example.com`
  - Enabled sites: `/etc/nginx/sites-enabled/`
- **Commands**:
  - Check configuration syntax: `sudo nginx -t`
  - Reload Nginx: `sudo systemctl reload nginx`

---

## Troubleshooting Common Issues

1. **Error: 403 Forbidden**  
   - Check that Nginx has the necessary permissions to access files in the root directory (`/var/www/example.com/html`). Use `chmod 755` and `chown` commands as shown above.

2. **Error: 404 Not Found**  
   - Ensure the `index.html` file exists in the specified directory and that `try_files` directive is correctly pointing to it.

3. **Configuration Errors**  
   - Always run `sudo nginx -t` to check configuration changes before reloading Nginx.

4. **SSL Issues**  
   - If HTTPS fails, make sure Certbot successfully installed the certificate and that the DNS settings correctly point to your server’s IP address.

---

