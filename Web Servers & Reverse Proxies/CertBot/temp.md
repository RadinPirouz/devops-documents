# 🔐 Certbot – SSL Certificate Management Guide

## 📦 Install Certbot

```bash
apt install certbot
```

Installs **Certbot**, the free tool to automatically obtain and manage SSL/TLS certificates from **Let's Encrypt**.

---

## 🖥️ Method 1 – Standalone Mode

```bash
certbot certonly --standalone -d www.example.com
```

💡 **Standalone mode** runs its own temporary web server to complete the verification.

* Use when no web server (Apache/Nginx) is running on the same port.
* Certificates will be saved in:

  * All versions: `/etc/letsencrypt/archive/`
  * Latest version (symlink): `/etc/letsencrypt/live/`

---

## 🌐 Method 2 – Webroot Mode

```bash
certbot certonly --webroot --webroot-path <path> -d <domain>
```

📌 **Webroot mode** places a verification file in your website's public directory.

* `<path>` = your website's document root (e.g., `/var/www/html`)
* Use when your site is already running and accessible.

---

## 🛠️ Method 3 – Manual DNS Challenge

```bash
certbot certonly --manual --preferred-challenges dns -d <domain>
```

🔹 **DNS mode** requires you to manually add a TXT record to your domain’s DNS.

* Best for **wildcard** certificates (`*.example.com`)
* Works even without a running web server.

---

## ♻️ Renew Certificates

### Automatic Renewal

```bash
certbot renew
```

* Renews all certificates close to expiration.

### Force Renewal

```bash
certbot renew --force-renewal
```

* Renews certificates **immediately**, even if not expiring soon.

---

## 📅 Tips

* Certificates expire every **90 days** — always set up **auto-renew**.
* Test renewal without changes:

```bash
certbot renew --dry-run
```

* Restart your web server after renewal to apply new certificates:

```bash
systemctl restart nginx
# or
systemctl restart apache2
```

---

✨ **With Certbot, your HTTPS setup can be fast, free, and automatic!** 🔒🚀
