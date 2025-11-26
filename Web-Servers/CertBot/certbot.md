# 🔐 Certbot 

## 📦 Install Certbot

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
```

*Installs Certbot and the Nginx plugin to automatically manage certificates.*

---

## 🖥️ Method 1 – Standalone Mode

```bash
sudo certbot certonly --standalone -d www.example.com
```

💡 **Standalone mode** runs its own temporary server for domain verification.

* Use if **Nginx is not running** on port 80/443.
* Certificates saved in:

  * `/etc/letsencrypt/live/<domain>/` → latest version (symlink)
  * `/etc/letsencrypt/archive/<domain>/` → all versions

---

## 🌐 Method 2 – Webroot Mode

```bash
sudo certbot certonly --webroot -w /var/www/html -d www.example.com
```

💡 **Webroot mode** places verification files in your website’s public folder.

* `<path>` = Nginx document root
* Use if Nginx is running and serving your site.

---

## 🛠️ Method 3 – Nginx Plugin (Auto Configuration)

```bash
sudo certbot --nginx -d www.example.com -d example.com
```

💡 **Nginx plugin** automatically:

* Obtains SSL certificate
* Configures HTTPS in Nginx
* Adds HTTP → HTTPS redirect
* Reloads Nginx

---

## 🌱 Method 4 – Manual DNS Challenge (Wildcard)

```bash
sudo certbot certonly --manual --preferred-challenges dns -d "*.example.com" -d example.com
```

💡 **DNS challenge** is required for wildcard certificates or if HTTP verification isn’t possible.

* Add TXT record as instructed by Certbot
* Works even if Nginx is down or port 80 is blocked

---

## ♻️ Renew Certificates

### Automatic Renewal

```bash
sudo certbot renew
```

* Renews all certificates nearing expiration

### Force Renewal

```bash
sudo certbot renew --force-renewal
```

* Immediately renews certificates, even if not near expiry

### Test Renewal

```bash
sudo certbot renew --dry-run
```

* Tests renewal without making changes

---

## 🔄 Reload Nginx After Renewal

```bash
sudo systemctl reload nginx
```

* Apply new certificates without downtime

*Tip:* You can add a **deploy-hook** for automatic reload:

```bash
sudo certbot renew --deploy-hook "systemctl reload nginx"
```

---

## 📅 Tips & Best Practices

* Certificates expire every **90 days** — enable **auto-renewal**.
* Keep `/etc/letsencrypt/` **backed up** (contains keys and configs).
* Use **staging** for testing to avoid hitting rate limits:

```bash
sudo certbot --staging --nginx -d www.example.com
```

* Monitor renewal logs: `/var/log/letsencrypt/letsencrypt.log`

---

✨ **Result:** Fully automated HTTPS for Nginx with Let’s Encrypt certificates. Fast, free, and secure! 🔒🚀

