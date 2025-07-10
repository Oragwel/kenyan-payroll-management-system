# 🚀 Render Deployment Guide - Kenyan Payroll Management System

## 📋 Prerequisites

✅ **What You Need:**
- Render account (free tier works)
- GitHub repository with your code
- PostgreSQL database on Render (you already have this)
- 10 minutes of your time

## 🔧 **Step 1: Prepare Your Repository**

### Push Your Optimized Code
```bash
# Make sure all changes are committed
git add .
git commit -m "feat: optimize Docker for Render deployment"
git push origin main
```

## 🌐 **Step 2: Deploy on Render**

### **Option A: Using render.yaml (Recommended)**

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Click "New +" → "Blueprint"

2. **Connect Repository**
   - Select your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Review Configuration**
   - Service name: `kenyan-payroll-system`
   - Runtime: Docker
   - Plan: Starter (free)
   - Disk: 2GB persistent storage

4. **Deploy**
   - Click "Apply"
   - Wait for deployment (5-10 minutes)

### **Option B: Manual Web Service Creation**

1. **Create Web Service**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"

2. **Connect Repository**
   - Select your GitHub repository
   - Branch: `main`

3. **Configure Service**
   ```
   Name: kenyan-payroll-system
   Runtime: Docker
   Plan: Starter
   Dockerfile Path: ./Dockerfile
   Docker Context: .
   ```

4. **Add Persistent Disk**
   ```
   Name: kenyan-payroll-data
   Mount Path: /data
   Size: 2GB
   ```

## 🔐 **Step 3: Environment Variables**

Add these environment variables in Render:

### **Required Variables:**
```bash
SECRET_KEY=your-secret-key-here  # Generate new one
DEBUG=False
DJANGO_SETTINGS_MODULE=payroll.settings.production
DATABASE_URL=your-postgresql-url-from-render
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
```

### **Optional Admin User:**
```bash
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your-email@example.com
DJANGO_SUPERUSER_PASSWORD=your-secure-password
```

## 🔑 **Step 4: Generate Secret Key**

Run this locally to generate a new SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🗄️ **Step 5: Database Configuration**

Your existing PostgreSQL database should work. Update the `DATABASE_URL` if needed:
```
postgresql://username:password@host:port/database
```

## 🚀 **Step 6: Deploy and Verify**

1. **Monitor Deployment**
   - Watch the build logs in Render dashboard
   - Look for "Starting Gunicorn server" message

2. **Check Health**
   - Visit: `https://your-app.onrender.com/health/`
   - Should return: `{"status": "healthy", "timestamp": "..."}`

3. **Access Application**
   - Main app: `https://your-app.onrender.com/`
   - Admin: `https://your-app.onrender.com/admin/`

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **Build Fails**
   ```bash
   # Check Dockerfile syntax
   docker build -t test .
   ```

2. **Database Connection Error**
   - Verify DATABASE_URL format
   - Check PostgreSQL service is running

3. **Static Files Not Loading**
   - Ensure ALLOWED_HOSTS includes your domain
   - Check persistent disk is mounted at /data

4. **Application Won't Start**
   - Check environment variables
   - Review deployment logs

### **Useful Commands:**
```bash
# View logs (in Render dashboard)
# Go to your service → Logs tab

# Check health endpoint
curl https://your-app.onrender.com/health/

# Test database connection
# Use Render shell (if available)
python manage.py dbshell
```

## 📊 **Expected Results**

After successful deployment:
- ✅ Application accessible via HTTPS
- ✅ Admin panel working
- ✅ Database connected
- ✅ Static files served
- ✅ Media uploads working
- ✅ Persistent storage active

## 🔄 **Auto-Deploy Setup**

Enable automatic deployments:
1. Go to your service settings
2. Enable "Auto-Deploy"
3. Select branch: `main`
4. Now every git push triggers deployment

## 💡 **Pro Tips**

1. **Free Tier Limitations:**
   - Service sleeps after 15 minutes of inactivity
   - 750 hours/month free usage

2. **Performance:**
   - Upgrade to paid plan for always-on service
   - Consider using CDN for static files

3. **Monitoring:**
   - Set up health check alerts
   - Monitor application logs regularly

## 🆘 **Need Help?**

If you encounter issues:
1. Check Render deployment logs
2. Verify environment variables
3. Test locally with Docker first
4. Check database connectivity

Your optimized Docker setup should deploy smoothly on Render! 🎉
