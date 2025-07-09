# Docker Deployment Guide - Kenyan Payroll Management System

This guide explains how to deploy the Kenyan Payroll Management System using Docker in a production environment with PostgreSQL on Render.

## 🐳 Prerequisites

- Docker and Docker Compose installed
- PostgreSQL database already set up on Render
- Domain name (optional but recommended)

## 📁 Files Overview

- `Dockerfile` - Multi-stage build for production
- `docker-compose.yml` - Local development and testing
- `.dockerignore` - Optimizes build process
- `.env.production.template` - Environment variables template

## 🚀 Production Deployment

### Step 1: Prepare Environment Variables

1. Copy the environment template:
```bash
cp .env.production.template .env.production
```

2. Edit `.env.production` with your actual values:
```bash
# Required - Generate a new secret key
SECRET_KEY=your-super-secret-django-key

# Required - Your Render PostgreSQL URL
DATABASE_URL=postgresql://username:password@hostname:port/database_name

# Required - Your domain/app URL
ALLOWED_HOSTS=your-app.onrender.com,your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com,https://your-domain.com
```

### Step 2: Build the Docker Image

```bash
# Build the production image
docker build -t kenyan-payroll:latest .

# Or build with specific tag
docker build -t kenyan-payroll:v1.0.0 .
```

### Step 3: Run Database Migrations

```bash
# Run migrations (one-time setup)
docker run --rm \
  --env-file .env.production \
  kenyan-payroll:latest \
  python manage.py migrate
```

### Step 4: Create Superuser

```bash
# Create admin user (interactive)
docker run -it --rm \
  --env-file .env.production \
  kenyan-payroll:latest \
  python manage.py createsuperuser
```

### Step 5: Deploy the Container

```bash
# Run the application
docker run -d \
  --name kenyan-payroll-app \
  --env-file .env.production \
  -p 8000:8000 \
  --restart unless-stopped \
  kenyan-payroll:latest
```

## 🔧 Local Development with Docker

### Using Docker Compose

```bash
# Start all services (Django + PostgreSQL)
docker-compose up -d

# View logs
docker-compose logs -f web

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Stop services
docker-compose down
```

### Access the Application

- Application: http://localhost:8000
- Admin Panel: http://localhost:8000/admin/
- Health Check: http://localhost:8000/health/

## 🔍 Health Checks

The Docker image includes health checks:

```bash
# Check application health
curl http://localhost:8000/health/

# Expected response:
{
  "status": "OK",
  "message": "Kenyan Payroll Management System is running",
  "timestamp": "2024-01-01T12:00:00Z",
  "database": "connected"
}
```

## 📊 Monitoring and Logs

### View Application Logs

```bash
# View real-time logs
docker logs -f kenyan-payroll-app

# View last 100 lines
docker logs --tail 100 kenyan-payroll-app
```

### Container Stats

```bash
# View resource usage
docker stats kenyan-payroll-app
```

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Pull latest code
git pull origin main

# Rebuild image
docker build -t kenyan-payroll:latest .

# Stop current container
docker stop kenyan-payroll-app
docker rm kenyan-payroll-app

# Run migrations if needed
docker run --rm \
  --env-file .env.production \
  kenyan-payroll:latest \
  python manage.py migrate

# Start new container
docker run -d \
  --name kenyan-payroll-app \
  --env-file .env.production \
  -p 8000:8000 \
  --restart unless-stopped \
  kenyan-payroll:latest
```

### Database Backup

```bash
# Backup database (if using local PostgreSQL)
docker-compose exec db pg_dump -U payroll_user kenyan_payroll > backup.sql

# Restore database
docker-compose exec -T db psql -U payroll_user kenyan_payroll < backup.sql
```

## 🛡️ Security Considerations

1. **Environment Variables**: Never commit `.env.production` to version control
2. **Secret Key**: Generate a new secret key for production
3. **Database**: Use strong passwords and restrict access
4. **HTTPS**: Always use HTTPS in production
5. **Updates**: Regularly update base images and dependencies

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check DATABASE_URL format
   # Ensure PostgreSQL is accessible
   docker run --rm --env-file .env.production kenyan-payroll:latest python manage.py dbshell
   ```

2. **Static Files Not Loading**
   ```bash
   # Collect static files
   docker run --rm --env-file .env.production kenyan-payroll:latest python manage.py collectstatic --noinput
   ```

3. **Permission Denied**
   ```bash
   # Check file permissions
   ls -la media/ staticfiles/
   ```

### Debug Mode

For debugging, temporarily set `DEBUG=True` in your environment file, but **never** use this in production.

## 📞 Support

For issues specific to the Kenyan Payroll Management System, check:
- Application logs: `docker logs kenyan-payroll-app`
- Health endpoint: `http://your-domain/health/`
- Django admin: `http://your-domain/admin/`
