# 🚀 Vercel Environment Variables Import Guide

## 📁 Files Created for You:

1. **`.env.production`** - Contains all your production environment variables
2. **`.env.example`** - Template file for reference
3. **This guide** - Step-by-step import instructions

## 🔧 Method 1: Import via Vercel Dashboard (Recommended)

### Step 1: Access Your Vercel Project
1. Go to [vercel.com](https://vercel.com) and login
2. Navigate to your project dashboard
3. Click on **Settings** tab
4. Click on **Environment Variables** in the sidebar

### Step 2: Import Environment Variables
1. Click the **"Import from .env"** button (or similar import option)
2. Copy the contents of `.env.production` file
3. Paste into the import dialog
4. Click **"Import"** or **"Add"**

### Step 3: Verify Variables
Ensure these variables are imported correctly:
- ✅ `DATABASE_URL`
- ✅ `SECRET_KEY`
- ✅ `DEBUG`
- ✅ `DJANGO_SETTINGS_MODULE`
- ✅ `ALLOWED_HOSTS`
- ✅ `DJANGO_SUPERUSER_USERNAME`
- ✅ `DJANGO_SUPERUSER_EMAIL`
- ✅ `DJANGO_SUPERUSER_PASSWORD`

## 🔧 Method 2: Manual Entry (Alternative)

If import doesn't work, add each variable manually:

### Required Variables:

**DATABASE_URL**
```
postgres://postgres.tjfnxsozfmxhcanlhgcc:rdNGSmdBk6oXS7RS@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require
```

**SECRET_KEY**
```
zbk3HW6l2TLXtzZRslzrgW5M282yIDVA14ps44mPp6Aq8rCgAJFjre4hPPPC6mpbAJo
```

**DEBUG**
```
False
```

**DJANGO_SETTINGS_MODULE**
```
payroll.settings.production
```

**ALLOWED_HOSTS**
```
.vercel.app,.now.sh,localhost,127.0.0.1
```

**DJANGO_SUPERUSER_USERNAME**
```
admin
```

**DJANGO_SUPERUSER_EMAIL**
```
admin@yourcompany.com
```

**DJANGO_SUPERUSER_PASSWORD**
```
PayrollAdmin2024!
```

## 🔧 Method 3: Vercel CLI (Advanced)

If you have Vercel CLI installed:

```bash
# Navigate to your project directory
cd /path/to/your/payroll/project

# Pull current environment variables (optional)
vercel env pull

# Add environment variables from file
vercel env add DATABASE_URL production
# Then paste the database URL when prompted

# Repeat for each variable or use:
vercel env add < .env.production
```

## 🎯 Environment Scopes

Make sure to set the environment variables for the correct scopes:

- **Production**: ✅ (Required for live deployment)
- **Preview**: ✅ (Recommended for testing)
- **Development**: ❌ (Not needed for Vercel deployment)

## 🔒 Security Notes

1. **Never commit `.env.production`** to version control (it's in `.gitignore`)
2. **Keep your database credentials secure**
3. **Change the superuser password** after first login
4. **Regenerate SECRET_KEY** if compromised

## 🚀 After Setting Environment Variables

1. **Redeploy your application**:
   - Go to **Deployments** tab
   - Click **"Redeploy"** on the latest deployment
   - Or push a new commit to trigger auto-deployment

2. **Monitor the deployment**:
   - Watch build logs for any errors
   - Check that migrations run successfully
   - Verify superuser creation

## ✅ Verification Checklist

After deployment, verify:

- [ ] App loads at your Vercel URL
- [ ] Database connection works
- [ ] Admin login works with superuser credentials
- [ ] Static files load correctly
- [ ] No 500 errors in function logs

## 🛠️ Troubleshooting

### Common Issues:

1. **Environment variables not taking effect**:
   - Redeploy after adding variables
   - Check variable names are exact (case-sensitive)

2. **Database connection errors**:
   - Verify DATABASE_URL is complete and correct
   - Check Supabase database is active

3. **Build failures**:
   - Check build logs in Vercel dashboard
   - Ensure all required variables are set

### Debug Steps:

1. **Check Environment Variables**: Settings → Environment Variables
2. **View Build Logs**: Deployments → Click on deployment → View logs
3. **Check Function Logs**: Functions → Click on function → View logs

## 📞 Support

If you encounter issues:
1. Check that all environment variables match exactly
2. Verify your Supabase database is accessible
3. Try redeploying after setting variables
4. Check Vercel documentation for environment variable import

## 🎉 Success!

Once environment variables are imported and deployment succeeds:
1. Visit your Vercel app URL
2. Login with: `admin` / `PayrollAdmin2024!`
3. Set up your organization
4. Start using your payroll system!

---

**Remember**: You can always update environment variables later in the Vercel dashboard and redeploy to apply changes.
