# Certbot Examples

Examples for obtaining and renewing Let's Encrypt certificates with Certbot.

## Standalone Mode

```bash
# Obtain certificate (port 80 must be free)
sudo certbot certonly --standalone \
  -d example.com \
  -d www.example.com \
  --email admin@example.com \
  --agree-tos
```

## Webroot Mode

```bash
# Obtain certificate (web server keeps running)
sudo certbot certonly --webroot \
  -w /var/www/html \
  -d example.com \
  -d www.example.com
```

## DNS Challenge (Wildcard)

```bash
# Manual DNS challenge
sudo certbot certonly --manual \
  --preferred-challenges dns \
  -d example.com \
  -d "*.example.com"
```

## Automatic Renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Renewal runs automatically via cron or systemd timer
systemctl status certbot.timer
```

See `../automation-patterns.md` for detailed Certbot configuration.
