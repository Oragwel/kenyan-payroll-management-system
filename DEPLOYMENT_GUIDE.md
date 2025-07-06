# Kenyan Payroll Management System - Vercel Deployment Guide

## Prerequisites

1. **GitHub Repository**: Your code should be pushed to GitHub
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
3. **PostgreSQL Database**: We'll use Vercel Postgres

## Step 1: Set Up Vercel Postgres Database

1. Go to your Vercel dashboard
2. Click "Storage" in the sidebar
3. Click "Create Database"
4. Select "Postgres"
5. Choose a name for your database (e.g., `payroll-db`)
6. Select a region close to your users
7. Click "Create"

## Step 2: Get Database Connection String

1. After creating the database, go to the database dashboard
2. Click on the "Settings" tab
3. Copy the `DATABASE_URL` connection string
4. It should look like: `postgres://username:password@host:port/database`

## Step 3: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: Leave empty (use root)
   - **Build Command**: Leave empty (we use vercel.json)
   - **Output Directory**: Leave empty
   - **Install Command**: Leave empty

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from your project directory
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (select your account)
# - Link to existing project? N
# - What's your project's name? kenyan-payroll-system
# - In which directory is your code located? ./
```

## Step 4: Configure Environment Variables

In your Vercel project dashboard:

1. Go to "Settings" → "Environment Variables"
2. Add the following variables:

### Required Variables:
```
DATABASE_URL = postgres://username:password@host:port/database
SECRET_KEY = your-super-secret-key-here
DEBUG = False
DJANGO_SETTINGS_MODULE = payroll.settings.production
```

### Optional Variables:
```
ALLOWED_HOSTS = your-app-name.vercel.app,your-custom-domain.com
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_HOST_USER = your-email@gmail.com
EMAIL_HOST_PASSWORD = your-app-password
DEFAULT_FROM_EMAIL = noreply@yourcompany.com
```

## Step 5: Generate Secret Key

Generate a secure Django secret key:

```python
# Run this in Python
import secrets
print(secrets.token_urlsafe(50))
```

Or use an online generator: https://djecrety.ir/

## Step 6: Redeploy

After setting environment variables:

1. Go to "Deployments" tab in Vercel dashboard
2. Click "Redeploy" on the latest deployment
3. Or push a new commit to trigger automatic deployment

## Step 7: Run Database Migrations

After successful deployment:

1. Go to your Vercel project dashboard
2. Click on "Functions" tab
3. Find your Django function and click on it
4. In the function logs, you should see migration output
5. If migrations didn't run automatically, you can trigger them by:
   - Making a small change and redeploying
   - Or using Vercel CLI: `vercel env pull` then run migrations locally

## Step 8: Create Superuser

You'll need to create a superuser account. Since Vercel functions are stateless, you have a few options:

### Option A: Create via Django Admin Command (Recommended)

Create a management command to create superuser:

```python
# In your Django app, create: management/commands/create_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'your-secure-password')
            self.stdout.write('Superuser created successfully')
        else:
            self.stdout.write('Superuser already exists')
```

### Option B: Use Environment Variables

Add to your environment variables:
```
DJANGO_SUPERUSER_USERNAME = admin
DJANGO_SUPERUSER_EMAIL = admin@yourcompany.com
DJANGO_SUPERUSER_PASSWORD = your-secure-password
```

Then add to your build script:
```bash
python3 manage.py createsuperuser --noinput
```

## Step 9: Test Your Deployment

1. Visit your Vercel app URL (e.g., `https://your-app.vercel.app`)
2. Try logging in with your superuser credentials
3. Test creating organizations, employees, and payroll
4. Check that static files are loading correctly

## Troubleshooting

### Common Issues:

1. **Build Fails**: Check the build logs in Vercel dashboard
2. **Database Connection Error**: Verify DATABASE_URL is correct
3. **Static Files Not Loading**: Check STATIC_URL and STATIC_ROOT settings
4. **500 Internal Server Error**: Check function logs in Vercel dashboard

### Debugging:

1. **View Logs**: Go to Vercel dashboard → Functions → Click on your function
2. **Check Environment Variables**: Settings → Environment Variables
3. **Redeploy**: Sometimes a fresh deployment fixes issues

## Custom Domain (Optional)

1. Go to "Settings" → "Domains"
2. Add your custom domain
3. Configure DNS records as instructed
4. Update ALLOWED_HOSTS environment variable

## Security Considerations

1. **Never commit sensitive data** to your repository
2. **Use environment variables** for all secrets
3. **Enable HTTPS** (Vercel does this automatically)
4. **Regularly update dependencies**
5. **Monitor your application** for security issues

## Performance Optimization

1. **Enable caching** by adding Redis (Vercel KV)
2. **Optimize database queries** 
3. **Use CDN** for static files (Vercel handles this)
4. **Monitor function execution time**

## Backup Strategy

1. **Database Backups**: Vercel Postgres includes automatic backups
2. **Code Backups**: Your GitHub repository serves as code backup
3. **Media Files**: Consider using external storage like AWS S3

## Support

If you encounter issues:
1. Check Vercel documentation: https://vercel.com/docs
2. Django deployment guides
3. Check the deployment logs for specific error messages
