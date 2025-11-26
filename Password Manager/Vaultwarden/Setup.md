# 🚀 Vaultwarden Setup Guide (with Docker & Nginx SSL)

This guide walks you through deploying Vaultwarden (a lightweight Bitwarden server alternative) using Docker Compose, Nginx as a reverse proxy, and a self-signed SSL certificate for secure HTTPS access.

---

## 📦 Step 1: Docker Compose Configuration

Create a file named docker-compose.yml with the following content:

services:
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    restart: unless-stopped
    environment:
      DOMAIN: "https://<your-domain>"
      ADMIN_TOKEN: "<ADMIN_TOKEN>"
    volumes:
      - ./vw-data/:/data/
    ports:
      - 8000:80

  nginx:
    image: nginx:alpine
    container_name: nginx
    restart: unless-stopped
    volumes:
      - ./nginx-config:/etc/nginx/conf.d
      - ./nginx-certs/vault.local.key:/etc/ssl/private/vault.local.key
      - ./nginx-certs/vault.local.crt:/etc/ssl/certs/vault.local.crt
    ports:
      - 80:80
      - 443:443


🔹 Notes:
- Vaultwarden runs on port 8000 internally (proxied by Nginx).  
- Persistent data is stored in ./vw-data/.  
- Replace DOMAIN and ADMIN_TOKEN with your values.  

---

## 🌐 Step 2: Nginx Reverse Proxy Configuration

Inside your nginx-config directory, create a file named vaultwarden.conf with:

server {
    listen 443 ssl;
    server_name domain_name;

    ssl_certificate     /etc/ssl/certs/vault.local.crt;
    ssl_certificate_key /etc/ssl/private/vault.local.key;

    location / {
        proxy_pass http://vaultwarden:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


🔹 This configuration:  
- Forces HTTPS on your domain.  
- Proxies requests to the Vaultwarden container.  

---

## 🔐 Step 3: Generate a Self-Signed SSL Certificate

If you don’t already have an SSL certificate, generate one for local testing:

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout ./nginx-certs/vault.local.key \
-out ./nginx-certs/vault.local.crt


🔹 Fill in the required details (CN should match domain_name).  
🔹 Place the generated files inside ./nginx-certs/.  

---

## ▶️ Step 4: Start the Services

Run:

docker compose up -d


Check containers:

docker ps


- Vaultwarden should be running on port 8000 internally.  
- Nginx should be serving HTTPS on https://domain_name.  

---

## ✅ Step 5: Access Vaultwarden

- Open: https://domain_name  
- Admin portal: https://domain_name/admin (use your ADMIN_TOKEN)  

---

## 🎯 Summary

You now have:
- Vaultwarden running in Docker.  
- Nginx reverse proxy with HTTPS enabled.  
- Secure, self-hosted password manager ready for use.
