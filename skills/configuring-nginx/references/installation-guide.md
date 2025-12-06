# nginx Installation Guide

Detailed installation instructions for nginx across different platforms.

## Table of Contents

1. [Ubuntu/Debian Installation](#ubuntudebian-installation)
2. [RHEL/CentOS/Rocky Installation](#rhelcentosrocky-installation)
3. [macOS Installation](#macos-installation)
4. [Docker Installation](#docker-installation)
5. [Building from Source](#building-from-source)
6. [Post-Installation](#post-installation)

## Ubuntu/Debian Installation

### Standard Installation

```bash
# Update package list
sudo apt update

# Install nginx
sudo apt install nginx -y

# Enable nginx to start on boot
sudo systemctl enable nginx

# Start nginx
sudo systemctl start nginx

# Check status
sudo systemctl status nginx
```

### Latest Stable from Official Repository

```bash
# Install prerequisites
sudo apt install curl gnupg2 ca-certificates lsb-release ubuntu-keyring

# Import nginx signing key
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null

# Add nginx stable repository
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
http://nginx.org/packages/ubuntu `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list

# Update and install
sudo apt update
sudo apt install nginx
```

### Verify Installation

```bash
nginx -v
# nginx version: nginx/1.24.0

curl http://localhost
# Should return nginx welcome page
```

## RHEL/CentOS/Rocky Installation

### Standard Installation

```bash
# Install nginx
sudo dnf install nginx -y

# Enable and start
sudo systemctl enable nginx
sudo systemctl start nginx

# Configure firewall
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### From Official Repository

```bash
# Create repo file
sudo tee /etc/yum.repos.d/nginx.repo <<EOF
[nginx-stable]
name=nginx stable repo
baseurl=http://nginx.org/packages/centos/\$releasever/\$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
EOF

# Install
sudo dnf install nginx -y
```

## macOS Installation

### Using Homebrew

```bash
# Install nginx
brew install nginx

# Start nginx
brew services start nginx

# Configuration location
ls -la /usr/local/etc/nginx/

# Default document root
ls -la /usr/local/var/www/
```

### Manual Start/Stop

```bash
# Start
nginx

# Stop
nginx -s stop

# Reload
nginx -s reload
```

## Docker Installation

### Basic Container

```bash
# Run nginx container
docker run -d \
  --name nginx-server \
  -p 80:80 \
  nginx:alpine

# With custom config
docker run -d \
  --name nginx-server \
  -p 80:80 \
  -v /path/to/nginx.conf:/etc/nginx/nginx.conf:ro \
  -v /path/to/html:/usr/share/nginx/html:ro \
  nginx:alpine
```

### Docker Compose

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./conf.d:/etc/nginx/conf.d:ro
      - ./html:/usr/share/nginx/html:ro
      - ./ssl:/etc/nginx/ssl:ro
    restart: unless-stopped
```

## Building from Source

Build nginx with custom modules:

```bash
# Install dependencies (Ubuntu/Debian)
sudo apt install build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev \
  libssl-dev libgd-dev libgeoip-dev

# Download nginx
wget http://nginx.org/download/nginx-1.24.0.tar.gz
tar -xzf nginx-1.24.0.tar.gz
cd nginx-1.24.0

# Configure with modules
./configure \
  --prefix=/etc/nginx \
  --sbin-path=/usr/sbin/nginx \
  --modules-path=/usr/lib64/nginx/modules \
  --conf-path=/etc/nginx/nginx.conf \
  --error-log-path=/var/log/nginx/error.log \
  --http-log-path=/var/log/nginx/access.log \
  --pid-path=/var/run/nginx.pid \
  --lock-path=/var/run/nginx.lock \
  --http-client-body-temp-path=/var/cache/nginx/client_temp \
  --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
  --user=nginx \
  --group=nginx \
  --with-http_ssl_module \
  --with-http_realip_module \
  --with-http_addition_module \
  --with-http_sub_module \
  --with-http_dav_module \
  --with-http_flv_module \
  --with-http_mp4_module \
  --with-http_gunzip_module \
  --with-http_gzip_static_module \
  --with-http_random_index_module \
  --with-http_secure_link_module \
  --with-http_stub_status_module \
  --with-http_auth_request_module \
  --with-http_v2_module \
  --with-threads \
  --with-stream \
  --with-stream_ssl_module

# Compile and install
make
sudo make install

# Create nginx user
sudo useradd -r -M -s /sbin/nologin nginx

# Create cache directories
sudo mkdir -p /var/cache/nginx/{client_temp,proxy_temp}
sudo chown -R nginx:nginx /var/cache/nginx
```

## Post-Installation

### File Locations

**Configuration:**
- `/etc/nginx/nginx.conf` - Main configuration
- `/etc/nginx/conf.d/` - Additional configs
- `/etc/nginx/sites-available/` - Available sites (Debian/Ubuntu)
- `/etc/nginx/sites-enabled/` - Enabled sites (Debian/Ubuntu)

**Logs:**
- `/var/log/nginx/access.log` - Access logs
- `/var/log/nginx/error.log` - Error logs

**Web Root:**
- `/usr/share/nginx/html/` - Default (RHEL)
- `/var/www/html/` - Default (Debian/Ubuntu)

### Initial Configuration Test

```bash
# Test configuration
sudo nginx -t

# View configuration
sudo nginx -T

# Check version and modules
nginx -V
```

### Service Management

```bash
# Start nginx
sudo systemctl start nginx

# Stop nginx
sudo systemctl stop nginx

# Reload configuration (zero downtime)
sudo systemctl reload nginx

# Restart nginx
sudo systemctl restart nginx

# Check status
sudo systemctl status nginx

# View logs
sudo journalctl -u nginx -f
```

### Firewall Configuration

**UFW (Ubuntu/Debian):**
```bash
sudo ufw allow 'Nginx Full'
# Or individually:
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

**firewalld (RHEL/CentOS):**
```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### SELinux Configuration (RHEL/CentOS)

```bash
# Allow nginx to make network connections
sudo setsebool -P httpd_can_network_connect 1

# Allow nginx to serve files from custom directory
sudo chcon -R -t httpd_sys_content_t /path/to/webroot/
```

## Verification

Test nginx is working:

```bash
# Check nginx is running
ps aux | grep nginx

# Test HTTP locally
curl http://localhost

# Test from external machine
curl http://your-server-ip

# Check listening ports
sudo netstat -tlnp | grep nginx
# OR
sudo ss -tlnp | grep nginx
```

## Next Steps

After installation:
1. Configure firewall (see above)
2. Set up virtual hosts (see `static-sites.md`)
3. Configure SSL/TLS (see `ssl-tls-config.md`)
4. Optimize performance (see `performance-tuning.md`)
5. Implement security hardening (see `security-hardening.md`)
