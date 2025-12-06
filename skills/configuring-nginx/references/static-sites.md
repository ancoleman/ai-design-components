# Static Site Configuration

nginx configuration patterns for static websites.


## Table of Contents

- [Basic Static Website](#basic-static-website)
- [Single Page Application (SPA)](#single-page-application-spa)
- [PHP Application (WordPress, Laravel)](#php-application-wordpress-laravel)

## Basic Static Website

Serve HTML/CSS/JS from a directory:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;

    root /var/www/example.com/html;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
    }
}
```

## Single Page Application (SPA)

React, Vue, Angular apps with client-side routing:

```nginx
server {
    listen 80;
    server_name app.example.com;

    root /var/www/app/dist;
    index index.html;

    # Try file, directory, then fallback to index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets aggressively
    location ~* \.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Don't cache index.html
    location = /index.html {
        add_header Cache-Control "no-cache, must-revalidate";
        expires 0;
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
}
```

## PHP Application (WordPress, Laravel)

```nginx
server {
    listen 80;
    server_name blog.example.com;

    root /var/www/blog;
    index index.php index.html;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    # PHP processing
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    # Deny access to sensitive files
    location ~ /\.(ht|git|env) {
        deny all;
    }

    # Cache static files
    location ~* \.(jpg|jpeg|gif|png|css|js|ico|xml|woff2)$ {
        expires 30d;
        access_log off;
    }
}
```
