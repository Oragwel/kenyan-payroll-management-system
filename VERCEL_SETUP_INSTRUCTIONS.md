# 🚀 Vercel Deployment Setup - Kenyan Payroll System

## ✅ Database Already Configured
Your Supabase PostgreSQL database is ready to use!

## 🔧 Step 1: Configure Environment Variables in Vercel

Go to your Vercel project dashboard → Settings → Environment Variables

Add these **EXACT** environment variables:

### Required Variables:

```
DATABASE_URL
postgres://postgres.tjfnxsozfmxhcanlhgcc:rdNGSmdBk6oXS7RS@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require
```

```
SECRET_KEY
zbk3HW6l2TLXtzZRslzrgW5M282yIDVA14ps44mPp6Aq8rCgAJFjre4hPPPC6mpbAJo
```

```
DEBUG
False
```

```
DJANGO_SETTINGS_MODULE
payroll.settings.production
```

```
ALLOWED_HOSTS
.vercel.app,.now.sh,localhost,127.0.0.1
```

### Optional Email Variables (for notifications):

```
EMAIL_HOST
smtp.gmail.com
```

```
EMAIL_PORT
587
```

```
EMAIL_HOST_USER
your-email@gmail.com
```

```
EMAIL_HOST_PASSWORD
your-gmail-app-password
```

```
DEFAULT_FROM_EMAIL
noreply@yourcompany.com
```

## 🚀 Step 2: Deploy to Vercel

### Option A: Auto-deploy (if already connected)
- Your GitHub repository should automatically trigger a new deployment
- Check the Vercel dashboard for deployment status

### Option B: Manual deploy via Vercel Dashboard
1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository: `kenyan-payroll-management-system`
3. Configure project settings:
   - **Framework Preset**: Other
   - **Root Directory**: (leave empty)
   - **Build Command**: (leave empty - uses vercel.json)
   - **Output Directory**: (leave empty)
   - **Install Command**: (leave empty)
4. Click "Deploy"

### Option C: Deploy via Vercel CLI
```bash
# Install Vercel CLI (if not installed)
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from your project directory
vercel --prod
```

## 📋 Step 3: Monitor Deployment

1. **Check Build Logs**: Go to Vercel dashboard → Deployments → Click on latest deployment
2. **Watch for Errors**: Look for any build or runtime errors
3. **Test Database Connection**: The deployment should automatically run migrations

## 🎯 Step 4: Post-Deployment Setup

### Create Superuser Account

After successful deployment, you'll need to create an admin account. Add this to your environment variables:

```
DJANGO_SUPERUSER_USERNAME
admin
```

```
DJANGO_SUPERUSER_EMAIL
admin@yourcompany.com
```

```
DJANGO_SUPERUSER_PASSWORD
YourSecurePassword123!
```

Then redeploy to automatically create the superuser.

## 🔍 Step 5: Test Your Deployment

1. **Visit your app**: `https://your-app-name.vercel.app`
2. **Test login**: Use your superuser credentials
3. **Check admin panel**: `/admin/`
4. **Test functionality**: Create organizations, employees, payroll

## 🛠️ Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check environment variables are set correctly
   - Verify DATABASE_URL format
   - Check build logs in Vercel dashboard

2. **Database Connection Error**:
   - Verify DATABASE_URL is exactly as provided
   - Check if Supabase database is active
   - Ensure SSL mode is enabled

3. **Static Files Not Loading**:
   - Check if build completed successfully
   - Verify static files were collected during build

4. **500 Internal Server Error**:
   - Check function logs in Vercel dashboard
   - Verify all required environment variables are set
   - Check SECRET_KEY is properly set

### Debug Steps:

1. **View Logs**: Vercel Dashboard → Functions → Click on your function
2. **Check Environment**: Settings → Environment Variables
3. **Redeploy**: Deployments → Redeploy latest

## 🔒 Security Checklist

- ✅ SECRET_KEY is secure and not in code
- ✅ DEBUG=False in production
- ✅ Database uses SSL connection
- ✅ ALLOWED_HOSTS is properly configured
- ✅ Environment variables are secure

## 📞 Support

If you encounter issues:
1. Check the deployment logs first
2. Verify all environment variables are correctly set
3. Ensure your GitHub repository has the latest changes
4. Try redeploying after fixing any issues

## 🎉 Success Indicators

Your deployment is successful when:
- ✅ Build completes without errors
- ✅ Database migrations run successfully
- ✅ Static files are collected
- ✅ App loads at your Vercel URL
- ✅ Admin login works
- ✅ You can create organizations and employees

---

**Next Steps After Successful Deployment:**
1. Set up your organization details
2. Import employee data
3. Configure payroll periods
4. Test payroll generation
5. Set up email notifications (optional)
