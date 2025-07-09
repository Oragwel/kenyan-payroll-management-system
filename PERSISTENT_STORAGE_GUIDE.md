# 💾 Persistent Storage Configuration Guide

## 🎯 **Overview**

This guide explains how persistent storage is configured for the Kenyan Payroll Management System to ensure data persistence across deployments and container restarts.

## 📁 **What Gets Persisted**

### **1. Static Files (`/data/static`)**
- CSS, JavaScript, and image files
- Collected Django static files
- Frontend build artifacts
- Admin interface assets

### **2. Media Files (`/data/media`)**
- User-uploaded files
- Company logos
- Employee documents
- Generated reports

### **3. Database (PostgreSQL)**
- Employee records
- Payroll data
- User accounts
- System configurations

## 🏗️ **Architecture**

### **Render Production:**
```
┌─────────────────┐    ┌──────────────────┐
│   Docker        │    │  Persistent Disk │
│   Container     │◄──►│  (1GB)          │
│                 │    │  /data          │
│  /app/static ───┼────┼─► /data/static   │
│  /app/media  ───┼────┼─► /data/media    │
└─────────────────┘    └──────────────────┘
```

### **Local Development:**
```
┌─────────────────┐    ┌──────────────────┐
│   Docker        │    │  Docker Volume   │
│   Container     │◄──►│  payroll_data   │
│                 │    │                 │
│  /data ─────────┼────┼─► Volume Storage │
└─────────────────┘    └──────────────────┘
```

## ⚙️ **Configuration Details**

### **1. Render Configuration (`render.yaml`)**
```yaml
services:
  - type: web
    name: kenyan-payroll-system
    runtime: docker
    disk:
      name: kenyan-payroll-data
      mountPath: /data
      sizeGB: 1
```

### **2. Docker Configuration (`Dockerfile`)**
```dockerfile
# Create persistent directories
RUN mkdir -p /data/static /data/media
RUN chown -R django:django /data
```

### **3. Startup Script (`docker-entrypoint.sh`)**
```bash
# Set up persistent storage
mkdir -p /data/static /data/media
ln -sf /data/static /app/staticfiles
ln -sf /data/media /app/media
```

### **4. Django Settings (`production.py`)**
```python
# Use persistent storage if available
if os.path.exists('/data'):
    STATIC_ROOT = '/data/static'
    MEDIA_ROOT = '/data/media'
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 🔄 **How It Works**

### **Deployment Process:**
1. **Container Starts** → Persistent disk mounted at `/data`
2. **Startup Script** → Creates directories and symlinks
3. **Django Settings** → Detects `/data` and uses persistent paths
4. **Static Collection** → Files saved to `/data/static`
5. **Media Uploads** → Files saved to `/data/media`

### **File Persistence:**
- ✅ **Static files persist** across deployments
- ✅ **Media files persist** across container restarts
- ✅ **Database data persists** (external PostgreSQL)
- ✅ **No data loss** during updates

## 🧪 **Testing Persistence**

### **Local Testing:**
```bash
# Start containers
docker-compose up -d

# Upload a test file or create static content
# Stop containers
docker-compose down

# Start again
docker-compose up -d

# Verify files are still there
docker-compose exec web ls -la /data/
```

### **Production Testing:**
```bash
# Check persistent disk
curl https://your-app.onrender.com/health/

# Upload test content via admin
# Trigger a new deployment
# Verify content persists
```

## 📊 **Storage Monitoring**

### **Check Disk Usage:**
```bash
# In container
df -h /data

# Expected output:
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/disk       1.0G   XX   XX   XX%  /data
```

### **Check File Permissions:**
```bash
# In container
ls -la /data/
# Should show django:django ownership
```

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **1. Permission Denied**
```bash
# Fix permissions
chown -R django:django /data
chmod -R 755 /data
```

#### **2. Symlinks Not Created**
```bash
# Recreate symlinks
rm -rf /app/staticfiles /app/media
ln -sf /data/static /app/staticfiles
ln -sf /data/media /app/media
```

#### **3. Static Files Not Loading**
```bash
# Recollect static files
python manage.py collectstatic --clear --noinput
```

#### **4. Disk Full**
```bash
# Check usage
du -sh /data/*
# Clean old files if needed
```

## 🔧 **Maintenance**

### **Backup Strategy:**
1. **Database**: Handled by Render PostgreSQL backups
2. **Static Files**: Can be regenerated from source
3. **Media Files**: Should be backed up regularly

### **Cleanup:**
```bash
# Remove old static files
find /data/static -type f -mtime +30 -delete

# Clean temporary files
find /data -name "*.tmp" -delete
```

## 📈 **Scaling Considerations**

### **Current Setup (1GB):**
- ✅ Suitable for small to medium applications
- ✅ Handles typical static and media files
- ✅ Cost-effective for starter plan

### **If You Need More Storage:**
```yaml
# In render.yaml
disk:
  name: kenyan-payroll-data
  mountPath: /data
  sizeGB: 5  # Increase as needed
```

## ✅ **Benefits**

1. **🔒 Data Persistence**: Files survive deployments
2. **⚡ Performance**: Local disk access is fast
3. **💰 Cost-Effective**: Only pay for storage used
4. **🔧 Automatic**: No manual intervention needed
5. **🛡️ Secure**: Proper permissions and isolation

Your Kenyan Payroll Management System now has robust persistent storage! 🎉
