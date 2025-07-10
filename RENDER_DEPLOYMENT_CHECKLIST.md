# ✅ Render Deployment Checklist

## 📋 Pre-Deployment Checklist

### **Repository Preparation**
- [ ] All code committed and pushed to GitHub
- [ ] Optimized Dockerfile in place
- [ ] .dockerignore configured
- [ ] render.yaml file present
- [ ] Docker builds successfully locally

### **Environment Variables Ready**
- [ ] SECRET_KEY generated (new one for production)
- [ ] DATABASE_URL from your existing Render PostgreSQL
- [ ] ALLOWED_HOSTS with your Render domain
- [ ] CSRF_TRUSTED_ORIGINS with HTTPS domain
- [ ] Admin user credentials (optional)

## 🚀 Deployment Steps

### **Step 1: Create Render Service**
- [ ] Go to https://dashboard.render.com
- [ ] Click "New +" → "Blueprint" (for render.yaml)
- [ ] OR "New +" → "Web Service" (manual setup)
- [ ] Connect your GitHub repository

### **Step 2: Configure Service**
- [ ] Service name: `kenyan-payroll-system`
- [ ] Runtime: Docker
- [ ] Plan: Starter (free)
- [ ] Dockerfile path: `./Dockerfile`
- [ ] Docker context: `.`

### **Step 3: Add Persistent Storage**
- [ ] Disk name: `kenyan-payroll-data`
- [ ] Mount path: `/data`
- [ ] Size: 2GB

### **Step 4: Set Environment Variables**
```bash
SECRET_KEY=your-new-secret-key
DEBUG=False
DJANGO_SETTINGS_MODULE=payroll.settings.production
DATABASE_URL=postgresql://user:pass@host:port/db
ALLOWED_HOSTS=your-app.onrender.com,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com
```

### **Step 5: Deploy**
- [ ] Click "Apply" or "Create Web Service"
- [ ] Monitor build logs
- [ ] Wait for "Starting Gunicorn server" message

## ✅ Post-Deployment Verification

### **Health Checks**
- [ ] Visit: `https://your-app.onrender.com/health/`
- [ ] Should return: `{"status": "healthy"}`

### **Application Access**
- [ ] Main app loads: `https://your-app.onrender.com/`
- [ ] Admin panel works: `https://your-app.onrender.com/admin/`
- [ ] Login functionality working
- [ ] Static files loading correctly

### **Database Verification**
- [ ] Can create/view employees
- [ ] Database migrations applied
- [ ] Admin user can log in (if created)

### **Persistent Storage**
- [ ] File uploads working
- [ ] Static files served from /data/static
- [ ] Media files accessible

## 🔧 Troubleshooting Checklist

### **If Build Fails**
- [ ] Check Dockerfile syntax locally
- [ ] Verify .dockerignore excludes unnecessary files
- [ ] Test Docker build: `docker build -t test .`

### **If App Won't Start**
- [ ] Check environment variables spelling
- [ ] Verify DATABASE_URL format
- [ ] Review deployment logs in Render

### **If Database Issues**
- [ ] Confirm PostgreSQL service is running
- [ ] Test DATABASE_URL connection
- [ ] Check allowed connections in PostgreSQL

### **If Static Files Missing**
- [ ] Verify ALLOWED_HOSTS includes domain
- [ ] Check persistent disk mounted at /data
- [ ] Confirm collectstatic ran successfully

## 📞 Quick Commands

### **Generate Secret Key**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **Test Health Endpoint**
```bash
curl https://your-app.onrender.com/health/
```

### **Check Your Current Setup**
```bash
# Test Docker build locally
docker build -t kenyan-payroll .

# Test Docker run locally
docker run -p 8000:8000 kenyan-payroll
```

## 🎯 Success Criteria

Your deployment is successful when:
- ✅ Application loads without errors
- ✅ Admin panel accessible
- ✅ Database operations work
- ✅ File uploads function
- ✅ Health check returns 200 OK
- ✅ No critical errors in logs

## 📝 Notes

- **Free Tier**: Service sleeps after 15 minutes of inactivity
- **Auto-Deploy**: Enable for automatic deployments on git push
- **Monitoring**: Check logs regularly for any issues
- **Scaling**: Upgrade plan if you need always-on service

Ready to deploy? Follow the checklist step by step! 🚀
