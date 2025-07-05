# 🚀 Vercel Deployment Guide

## Complete guide to deploy the Kenyan Payroll Management System on Vercel with PostgreSQL

## 🎯 **Why This Setup?**

### **✅ Vercel + PostgreSQL Benefits:**
- **🌐 Global CDN**: Fast loading worldwide
- **🔒 Automatic HTTPS**: Built-in SSL certificates
- **📈 Auto-scaling**: Handles traffic spikes automatically
- **💰 Cost-effective**: Free tier for small projects
- **🛡️ Security**: Enterprise-grade security features
- **📊 Analytics**: Built-in performance monitoring

## 📋 **Prerequisites Checklist**

### **Required Accounts:**
- ✅ **GitHub Account**: For code repository
- ✅ **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
- ✅ **Vercel Postgres**: Database service (included with Vercel)

### **Required Tools:**
```bash
# Install Node.js (for Vercel CLI)
# Download from: https://nodejs.org/

# Install Vercel CLI
npm install -g vercel

# Install Git (if not already installed)
# Windows: https://git-scm.com/download/win
# macOS: brew install git
# Linux: sudo apt install git
```

## 🗄️ **Database Setup: Vercel Postgres**

### **Step 1: Create Vercel Postgres Database**
```bash
# Login to Vercel
vercel login

# Create a new Postgres database
vercel postgres create payroll-db

# Note: Save the connection details provided
```

### **Alternative: Using Vercel Dashboard**
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **Storage** → **Create Database**
3. Select **Postgres**
4. Name: `payroll-db`
5. Region: Choose closest to your users
6. Click **Create**

### **Step 2: Get Database Connection String**
```bash
# Get database URL
vercel postgres connect payroll-db

# Copy the DATABASE_URL provided
# Format: postgresql://username:password@host:port/database
```

## 📁 **Project Preparation**

### **Step 1: Update Project Structure**
```bash
# Your project should have these files:
kenyan-payroll-system/
├── vercel.json                 # ✅ Created
├── build_files.sh             # ✅ Created
├── requirements.txt           # ✅ Updated
├── payroll/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py           # ✅ Created
│   │   └── production.py     # ✅ Created
│   └── wsgi.py
└── manage.py
```

### **Step 2: Create Settings Init File**
```python
# payroll/settings/__init__.py
import os

if os.environ.get('VERCEL'):
    from .production import *
else:
    from .base import *
    
    # Development database (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

### **Step 3: Make Build Script Executable**
```bash
# Make build script executable
chmod +x build_files.sh
```

## 🚀 **Deployment Steps**

### **Step 1: Push Code to GitHub**
```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Prepare for Vercel deployment"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/kenyan-payroll-system.git
git branch -M main
git push -u origin main
```

### **Step 2: Deploy to Vercel**

#### **Option A: Using Vercel CLI**
```bash
# Deploy from project directory
vercel

# Follow the prompts:
# ? Set up and deploy "~/kenyan-payroll-system"? [Y/n] y
# ? Which scope do you want to deploy to? [Your Account]
# ? Link to existing project? [y/N] n
# ? What's your project's name? kenyan-payroll-system
# ? In which directory is your code located? ./
```

#### **Option B: Using Vercel Dashboard**
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **New Project**
3. Import from GitHub repository
4. Select `kenyan-payroll-system`
5. Configure project settings (see below)

### **Step 3: Configure Environment Variables**

#### **Required Environment Variables:**
```bash
# In Vercel Dashboard → Project → Settings → Environment Variables

# Database
DATABASE_URL=postgresql://username:password@host:port/database

# Django Settings
SECRET_KEY=your-super-secret-key-here
DJANGO_SETTINGS_MODULE=payroll.settings.production
VERCEL=1

# Superuser (optional - for initial setup)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourcompany.com
DJANGO_SUPERUSER_PASSWORD=secure-password-here

# Email Configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourcompany.com

# Security (optional)
SENTRY_DSN=your-sentry-dsn-here
```

#### **Setting Environment Variables via CLI:**
```bash
# Set environment variables
vercel env add SECRET_KEY
vercel env add DATABASE_URL
vercel env add DJANGO_SETTINGS_MODULE
vercel env add VERCEL

# Deploy with new environment variables
vercel --prod
```

## 🔧 **Post-Deployment Configuration**

### **Step 1: Run Initial Setup**
```bash
# Access your deployed app
# https://your-project-name.vercel.app

# The build script automatically:
# ✅ Installs dependencies
# ✅ Runs migrations
# ✅ Collects static files
# ✅ Creates superuser (if configured)
# ✅ Loads initial data
```

### **Step 2: Verify Deployment**
1. **Visit your app**: `https://your-project-name.vercel.app`
2. **Check login**: Go to `/login/`
3. **Test admin access**: Go to `/admin/`
4. **Verify database**: Check if data is persisting

### **Step 3: Configure Custom Domain (Optional)**
```bash
# Add custom domain via CLI
vercel domains add your-domain.com

# Or via dashboard:
# Project → Settings → Domains → Add Domain
```

## 🔒 **Security Configuration**

### **Step 1: Update Allowed Hosts**
```python
# In production.py, add your domain:
ALLOWED_HOSTS = [
    '.vercel.app',
    '.now.sh',
    'your-domain.com',
    'www.your-domain.com',
]
```

### **Step 2: Configure CORS (if using API)**
```python
# In production.py:
CORS_ALLOWED_ORIGINS = [
    "https://your-project-name.vercel.app",
    "https://your-domain.com",
]
```

### **Step 3: SSL and Security Headers**
```python
# Already configured in production.py:
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 📊 **Monitoring & Maintenance**

### **Step 1: Monitor Performance**
```bash
# View deployment logs
vercel logs

# Monitor function performance
# Dashboard → Project → Functions → View Logs
```

### **Step 2: Database Monitoring**
```bash
# Connect to database for maintenance
vercel postgres connect payroll-db

# Monitor database performance
# Dashboard → Storage → payroll-db → Insights
```

### **Step 3: Regular Updates**
```bash
# Update code and redeploy
git add .
git commit -m "Update payroll system"
git push origin main

# Vercel automatically redeploys on git push
```

## 💰 **Cost Estimation**

### **Vercel Pricing:**
- **Hobby Plan (Free)**:
  - 100GB bandwidth/month
  - 100 serverless function executions/day
  - 1 concurrent build
  - Perfect for small organizations

- **Pro Plan ($20/month)**:
  - 1TB bandwidth/month
  - Unlimited serverless functions
  - 12 concurrent builds
  - Analytics and monitoring
  - Suitable for medium organizations

### **Vercel Postgres Pricing:**
- **Hobby (Free)**: 256MB storage, 60 hours compute/month
- **Pro ($20/month)**: 8GB storage, 300 hours compute/month
- **Enterprise**: Custom pricing for large organizations

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **1. Build Failures**
```bash
# Check build logs
vercel logs --follow

# Common fixes:
# - Ensure all dependencies in requirements.txt
# - Check Python version compatibility
# - Verify file permissions on build_files.sh
```

#### **2. Database Connection Issues**
```bash
# Verify DATABASE_URL format
# Should be: postgresql://user:pass@host:port/db

# Test connection locally:
python manage.py dbshell
```

#### **3. Static Files Not Loading**
```bash
# Ensure STATIC_ROOT is correct in production.py
# Check vercel.json routes configuration
# Verify WhiteNoise is installed and configured
```

#### **4. Environment Variables Not Working**
```bash
# Redeploy after adding environment variables
vercel --prod

# Check environment variables are set:
# Dashboard → Project → Settings → Environment Variables
```

### **Debug Commands:**
```bash
# View deployment details
vercel inspect

# Check function logs
vercel logs --follow

# Test locally with production settings
DJANGO_SETTINGS_MODULE=payroll.settings.production python manage.py runserver
```

## ✅ **Deployment Checklist**

### **Pre-Deployment:**
- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] Postgres database created
- [ ] Environment variables configured
- [ ] Build script tested locally

### **Deployment:**
- [ ] Project deployed to Vercel
- [ ] Database migrations completed
- [ ] Static files collected
- [ ] Superuser created
- [ ] Initial data loaded

### **Post-Deployment:**
- [ ] Application accessible via HTTPS
- [ ] Login functionality working
- [ ] Database operations working
- [ ] Admin panel accessible
- [ ] Mobile responsiveness verified
- [ ] Security headers configured

### **Production Ready:**
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Error tracking configured
- [ ] Performance optimized

## 🎉 **Success!**

Your Kenyan Payroll Management System is now live on Vercel with PostgreSQL! 

**Access your application:**
- **Main App**: `https://your-project-name.vercel.app`
- **Admin Panel**: `https://your-project-name.vercel.app/admin/`
- **API**: `https://your-project-name.vercel.app/api/`

**Next Steps:**
1. Set up your organization profile
2. Add departments and job titles
3. Import or create employees
4. Generate your first payroll
5. Customize branding and settings

Your payroll system is now ready to serve Kenyan organizations with full statutory compliance! 🇰🇪✅
