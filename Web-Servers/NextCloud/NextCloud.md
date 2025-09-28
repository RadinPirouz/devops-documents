# Setting up Nextcloud with Nginx

## Step 1: Update Repositories and Packages

```bash
apt update && apt upgrade -y
```

## Step 2: Install Nginx and MariaDB Server

```bash
apt install nginx mariadb-server
```

## Step 3: Install and Enable Dependencies and Certbot

```bash
apt install imagemagick php-imagick php-common php-mysql php-fpm php-gd php-json php-curl php-zip php-xml php-mbstring php-bz2 php-intl php-bcmath php-gmp php-zip libmagickcore-6.q16-6-extra
apt install certbot python3-certbot-nginx
systemctl start php8.1-fpm && systemctl enable php8.1-fpm
```

## Step 4: Get and Install Nextcloud

```bash
wget https://download.nextcloud.com/server/releases/nextcloud-28.0.4.zip && mkdir -p /sites/nextcloud && unzip nextcloud-*.zip -d /sites/nextcloud
```

## Step 5: Configure SQL

```bash
mysql -u root -p
```

```sql
CREATE DATABASE nextcloud_db;
CREATE USER 'admin2'@'localhost' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON nextcloud_db.* TO 'admin2'@'localhost' IDENTIFIED BY '123';
FLUSH PRIVILEGES;
EXIT;
```

## Step 6: Configure Nginx

```bash
vim /etc/nginx/sites-enabled/default
```

**Nginx Configuration**

```conf
upstream php-handler {
    server unix:/var/run/php/php8.1-fpm.sock;
}

server {
    listen 80;
    server_name _;
    add_header Referrer-Policy "no-referrer" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Download-Options "noopen" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Permitted-Cross-Domain-Policies "none" always;
    add_header X-Robots-Tag "none" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security 'max-age=31536000; includeSubDomains; preload';

    # Remove X-Powered-By, which is an information leak
    fastcgi_hide_header X-Powered-By;

    # Path to the root of your installation
    root /sites/nextcloud/;

    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }

    location = /.well-known/carddav {
        return 301 $scheme://$host:$server_port/remote.php/dav;
    }
    location = /.well-known/caldav {
        return 301 $scheme://$host:$server_port/remote.php/dav;
    }

    # set max upload size
    client_max_body_size 512M;
    fastcgi_buffers 64 4K;

    # Enable gzip but do not remove ETag headers
    gzip on;
    gzip_vary on;
    gzip_comp_level 4;
    gzip_min_length 256;
    gzip_proxied expired no-cache no-store private no_last_modified no_etag auth;
    gzip_types application/atom+xml application/javascript application/json application/ld+json application/manifest+json application/rss+xml application/vnd.geo+json application/vnd.ms-fontobject application/x-font-ttf application/x-web-app-manifest+json application/xhtml+xml application/xml font/opentype image/bmp image/svg+xml image/x-icon text/cache-manifest text/css text/plain text/vcard text/vnd.rim.location.xloc text/vtt text/x-component text/x-cross-domain-policy;

    # Uncomment if your server is built with the ngx_pagespeed module
    # This module is currently not supported.
    # pagespeed off;

    location / {
        rewrite ^ /index.php;
    }

    location ~ ^\/(?:build|tests|config|lib|3rdparty|templates|data)\/ {
        deny all;
    }
    location ~ ^\/(?:\.|autotest|occ|issue|indie|db_|console) {
        deny all;
    }

    location ~ ^\/(?:index|remote|public|cron|core\/ajax\/update|status|ocs\/v[12]|updater\/.+|oc[ms]-provider\/.+)\.php(?:$|\/) {
        fastcgi_split_path_info ^(.+?\.php)(\/.*|)$;
        set $path_info $fastcgi_path_info;
        try_files $fastcgi_script_name =404;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $path_info;
        fastcgi_param HTTP on;
        # Avoid sending the security headers twice
        fastcgi_param modHeadersAvailable true;
        # Enable pretty urls
        fastcgi_param front_controller_active true;
        fastcgi_pass php-handler;
        fastcgi_intercept_errors on;
        fastcgi_request_buffering off;
    }

    location ~ ^\/(?:updater|oc[ms]-provider)(?:$|\/) {
        try_files $uri/ =404;
        index index.php;
    }

    # Adding the cache control header for js, css and map files
    # Make sure it is BELOW the PHP block
    location ~ \.(?:css|js|woff2?|svg|gif|map)$ {
        try_files $uri /index.php$request_uri;
        add_header Cache-Control "public, max-age=15778463";
        add_header Referrer-Policy "no-referrer" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-Download-Options "noopen" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add

_header X-Permitted-Cross-Domain-Policies "none" always;
        add_header X-Robots-Tag "none" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Optional: Don't log access to assets
        access_log off;
    }

    location ~ \.(?:png|html|ttf|ico|jpg|jpeg|bcmap)$ {
        try_files $uri /index.php$request_uri;
        # Optional: Don't log access to other assets
        access_log off;
    }
}
```

## Step 7: Nginx Check

```bash
nginx -t # Check if configuration has errors
nginx -s reload
```

