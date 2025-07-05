# 🚀 Deployment Guide

## Overview

This guide covers deploying the Kenyan Payroll Management System to production environments, including server setup, security configuration, and maintenance procedures.

## 🏗️ Production Architecture

### Recommended Infrastructure
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Web Server    │    │    Database     │
│    (Nginx)      │────│   (Gunicorn)    │────│  (PostgreSQL)   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │   Static Files  │              │
         └──────────────│   (Nginx/CDN)   │──────────────┘
                        │                 │
                        └─────────────────┘
```

### System Requirements

#### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 50GB SSD
- **OS**: Ubuntu 20.04 LTS or CentOS 8
- **Python**: 3.8+
- **Database**: PostgreSQL 12+

#### Recommended Requirements
- **CPU**: 4 cores
- **RAM**: 8GB
- **Storage**: 100GB SSD
- **OS**: Ubuntu 22.04 LTS
- **Python**: 3.10+
- **Database**: PostgreSQL 14+

## 🐧 Server Setup (Ubuntu)

### 1. System Updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib redis-server supervisor git curl
```

### 2. Database Setup
```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE kenyan_payroll;
CREATE USER payroll_user WITH PASSWORD 'secure_password_here';
ALTER ROLE payroll_user SET client_encoding TO 'utf8';
ALTER ROLE payroll_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE payroll_user SET timezone TO 'Africa/Nairobi';
GRANT ALL PRIVILEGES ON DATABASE kenyan_payroll TO payroll_user;
\q
```

### 3. Application Deployment
```bash
# Create application user
sudo adduser payroll
sudo usermod -aG sudo payroll

# Switch to application user
sudo su - payroll

# Clone repository
git clone <repository-url> /home/payroll/kenyan-payroll-system
cd /home/payroll/kenyan-payroll-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 4. Environment Configuration
```bash
# Create environment file
cat > .env << EOF
DEBUG=False
SECRET_KEY=your_very_secure_secret_key_here
DATABASE_URL=postgresql://payroll_user:secure_password_here@localhost/kenyan_payroll
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
STATIC_ROOT=/home/payroll/kenyan-payroll-system/staticfiles
MEDIA_ROOT=/home/payroll/kenyan-payroll-system/media
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
ENCRYPTION_KEY=your_encryption_key_here
BACKUP_ENCRYPTION_KEY=your_backup_encryption_key_here
EOF

# Set secure permissions
chmod 600 .env
```

### 5. Django Configuration
```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Load initial data
python manage.py loaddata initial_data.json
```

## 🌐 Web Server Configuration

### Nginx Configuration
```nginx
# /etc/nginx/sites-available/kenyan-payroll
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Configuration
    ssl_certificate /path/to/ssl/certificate.crt;
    ssl_certificate_key /path/to/ssl/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Static files
    location /static/ {
        alias /home/payroll/kenyan-payroll-system/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /home/payroll/kenyan-payroll-system/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    # Application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
    }

    # File upload size limit
    client_max_body_size 10M;
}
```

### Enable Nginx Site
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/kenyan-payroll /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

## 🔧 Process Management

### Gunicorn Configuration
```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 300
keepalive = 5
user = "payroll"
group = "payroll"
tmp_upload_dir = None
errorlog = "/home/payroll/logs/gunicorn_error.log"
accesslog = "/home/payroll/logs/gunicorn_access.log"
loglevel = "info"
```

### Supervisor Configuration
```ini
# /etc/supervisor/conf.d/kenyan-payroll.conf
[program:kenyan-payroll]
command=/home/payroll/kenyan-payroll-system/venv/bin/gunicorn payroll.wsgi:application -c gunicorn.conf.py
directory=/home/payroll/kenyan-payroll-system
user=payroll
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/payroll/logs/supervisor.log
environment=PATH="/home/payroll/kenyan-payroll-system/venv/bin"
```

### Start Services
```bash
# Create log directory
sudo mkdir -p /home/payroll/logs
sudo chown payroll:payroll /home/payroll/logs

# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start kenyan-payroll

# Enable services
sudo systemctl enable nginx postgresql redis-server supervisor
```

## 🔒 Security Configuration

### Firewall Setup
```bash
# Configure UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Database Security
```bash
# PostgreSQL security
sudo -u postgres psql

# Disable remote connections (if not needed)
ALTER SYSTEM SET listen_addresses = 'localhost';

# Set strong password policy
ALTER SYSTEM SET password_encryption = 'scram-sha-256';

# Restart PostgreSQL
sudo systemctl restart postgresql
```

## 📊 Monitoring & Logging

### Log Configuration
```python
# settings/production.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/home/payroll/logs/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'security': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/home/payroll/logs/security.log',
            'maxBytes': 1024*1024*15,
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'security': {
            'handlers': ['security'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
```

### Health Check Script
```bash
#!/bin/bash
# health_check.sh

# Check application status
curl -f http://localhost:8000/health/ || echo "Application down"

# Check database connection
sudo -u postgres psql -d kenyan_payroll -c "SELECT 1;" || echo "Database connection failed"

# Check disk space
df -h | awk '$5 > 80 {print "Disk space warning: " $0}'

# Check memory usage
free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }'

# Check log file sizes
find /home/payroll/logs -name "*.log" -size +100M -exec echo "Large log file: {}" \;
```

## 🔄 Backup & Recovery

### Automated Backup Script
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/home/payroll/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
sudo -u postgres pg_dump kenyan_payroll | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Media files backup
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/payroll/kenyan-payroll-system/media/

# Application backup
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /home/payroll/kenyan-payroll-system/ --exclude=venv --exclude=media --exclude=staticfiles

# Encrypt backups
gpg --cipher-algo AES256 --compress-algo 1 --s2k-mode 3 --s2k-digest-algo SHA512 --s2k-count 65536 --symmetric --output $BACKUP_DIR/backup_$DATE.gpg $BACKUP_DIR/*_$DATE.*

# Clean up unencrypted files
rm $BACKUP_DIR/*_$DATE.sql.gz $BACKUP_DIR/*_$DATE.tar.gz

# Remove old backups (keep 30 days)
find $BACKUP_DIR -name "backup_*.gpg" -mtime +30 -delete

# Upload to remote storage (optional)
# aws s3 cp $BACKUP_DIR/backup_$DATE.gpg s3://your-backup-bucket/
```

### Cron Job for Backups
```bash
# Add to crontab
sudo crontab -e

# Daily backup at 2 AM
0 2 * * * /home/payroll/scripts/backup.sh

# Weekly full backup on Sunday at 3 AM
0 3 * * 0 /home/payroll/scripts/full_backup.sh
```

## 🔧 Maintenance

### Update Procedure
```bash
# 1. Backup current system
/home/payroll/scripts/backup.sh

# 2. Update code
cd /home/payroll/kenyan-payroll-system
git pull origin main

# 3. Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Collect static files
python manage.py collectstatic --noinput

# 6. Restart application
sudo supervisorctl restart kenyan-payroll

# 7. Test application
curl -f http://localhost:8000/health/
```

### Performance Monitoring
```bash
# Monitor application performance
htop
iotop
netstat -tulpn

# Check application logs
tail -f /home/payroll/logs/django.log
tail -f /home/payroll/logs/gunicorn_error.log

# Monitor database performance
sudo -u postgres psql -d kenyan_payroll -c "SELECT * FROM pg_stat_activity;"
```

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Server provisioned and secured
- [ ] Domain name configured
- [ ] SSL certificate obtained
- [ ] Database created and secured
- [ ] Environment variables configured
- [ ] Backup strategy implemented

### Deployment
- [ ] Code deployed and tested
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] Services configured and started
- [ ] Health checks passing
- [ ] Monitoring configured

### Post-Deployment
- [ ] Application accessible via HTTPS
- [ ] All features tested
- [ ] Performance benchmarks met
- [ ] Security scan completed
- [ ] Backup tested and verified
- [ ] Documentation updated

This deployment guide ensures a secure, scalable, and maintainable production environment for the Kenyan Payroll Management System.
