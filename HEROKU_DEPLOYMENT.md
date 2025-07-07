# Heroku Deployment Guide
## Kenyan Payroll Management System

This guide will help you deploy the Kenyan Payroll Management System to Heroku.

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure your code is in a Git repository

## Quick Deploy (One-Click)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Oragwel/kenyan-payroll-management-system)

## Manual Deployment Steps

### 1. Login to Heroku
```bash
heroku login
```

### 2. Create Heroku App
```bash
# Create app with a custom name
heroku create your-payroll-app-name

# Or let Heroku generate a name
heroku create
```

### 3. Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:mini
```

### 4. Set Environment Variables
```bash
# Required environment variables
heroku config:set DJANGO_SETTINGS_MODULE=payroll.settings.heroku
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set DEBUG=False
heroku config:set SECURE_SSL_REDIRECT=True

# Admin user credentials
heroku config:set ADMIN_USERNAME=admin
heroku config:set ADMIN_EMAIL=admin@yourcompany.com
heroku config:set ADMIN_PASSWORD=YourSecurePassword123!
```

### 5. Deploy to Heroku
```bash
# Add Heroku remote (if not already added)
heroku git:remote -a your-app-name

# Deploy
git push heroku main
```

### 6. Run Database Migrations
```bash
heroku run python manage.py migrate
```

### 7. Create Superuser (if not created automatically)
```bash
heroku run python create_superuser.py
```

### 8. Open Your App
```bash
heroku open
```

## Configuration Files

The following files are configured for Heroku deployment:

- **Procfile**: Defines web and release processes
- **runtime.txt**: Specifies Python version (3.11.7)
- **requirements-heroku.txt**: Heroku-specific dependencies
- **payroll/settings/heroku.py**: Heroku-specific Django settings
- **app.json**: Heroku app configuration for one-click deploy

## Environment Variables

Set these in your Heroku dashboard or via CLI:

| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SETTINGS_MODULE` | Django settings module | `payroll.settings.heroku` |
| `SECRET_KEY` | Django secret key | Auto-generated |
| `DEBUG` | Debug mode | `False` |
| `SECURE_SSL_REDIRECT` | Force HTTPS | `True` |
| `ADMIN_USERNAME` | Default admin username | `admin` |
| `ADMIN_EMAIL` | Default admin email | `admin@company.com` |
| `ADMIN_PASSWORD` | Default admin password | `SecurePassword123!` |

## Post-Deployment

### 1. Access Your Application
- **Frontend**: `https://your-app-name.herokuapp.com/`
- **Admin**: `https://your-app-name.herokuapp.com/admin/`

### 2. Login Credentials
- **Username**: Value of `ADMIN_USERNAME` (default: `admin`)
- **Password**: Value of `ADMIN_PASSWORD`

### 3. Set Up Organization
1. Login to admin panel
2. Go to Organizations
3. Create your organization details
4. Set up departments and job titles

### 4. Add Employees
1. Use the bulk import feature
2. Download the Excel template
3. Fill in employee data
4. Upload the completed template

## Troubleshooting

### View Logs
```bash
heroku logs --tail
```

### Run Django Commands
```bash
heroku run python manage.py shell
heroku run python manage.py collectstatic
heroku run python manage.py migrate
```

### Database Access
```bash
heroku pg:psql
```

### Restart App
```bash
heroku restart
```

## Scaling

### Scale Web Dynos
```bash
# Scale to 2 web dynos
heroku ps:scale web=2

# Scale back to 1 (free tier)
heroku ps:scale web=1
```

### Upgrade Database
```bash
# Upgrade to Basic plan ($9/month)
heroku addons:upgrade heroku-postgresql:basic
```

## Security Notes

1. **Change Default Password**: Change the admin password after first login
2. **Environment Variables**: Never commit sensitive data to Git
3. **HTTPS**: SSL is enforced in production
4. **Database**: PostgreSQL is encrypted at rest

## Support

For deployment issues:
1. Check Heroku logs: `heroku logs --tail`
2. Verify environment variables: `heroku config`
3. Check app status: `heroku ps`

## Cost Estimation

### Free Tier
- **Web Dyno**: Free (550-1000 hours/month)
- **PostgreSQL**: Free (10,000 rows, 1GB storage)
- **Total**: $0/month

### Basic Tier
- **Web Dyno**: $7/month
- **PostgreSQL**: $9/month (10 million rows, 64GB storage)
- **Total**: $16/month

## Features Included

✅ Employee Management
✅ Payroll Calculator (SHIF, NSSF, PAYE)
✅ Bulk Employee Import
✅ Excel Reports
✅ Mobile Responsive
✅ Data Preservation
✅ Security Features
✅ Kenyan Tax Compliance
