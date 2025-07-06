#!/bin/bash

echo "🚀 Deploying ULTRA-MINIMAL version to avoid subprocess errors..."

# Backup current requirements
cp requirements.txt requirements-full-backup.txt

# Use ultra-minimal requirements (only 5 packages!)
cp requirements-ultra-minimal.txt requirements.txt

echo "✅ Using ULTRA-MINIMAL requirements:"
echo "  - Django==4.2.7"
echo "  - psycopg2-binary==2.9.9"
echo "  - gunicorn==21.2.0"
echo "  - whitenoise==6.6.0"
echo "  - dj-database-url==2.1.0"
echo ""
echo "🎯 This should eliminate ALL compilation errors!"

# Commit changes
git add .
git commit -m "Ultra-minimal deployment to fix subprocess compilation errors

- Reduced to only 5 essential packages
- All packages are pure Python or pre-compiled binaries
- No C compilation required
- Should eliminate subprocess-exited-with-error issues
- Core Django functionality preserved"

git push origin main

echo ""
echo "🎯 Now update your Render deployment:"
echo ""
echo "1. Go to your Render web service"
echo "2. Update Build Command to:"
echo "   pip install -r requirements.txt && python manage.py collectstatic --noinput"
echo ""
echo "3. Update Start Command to:"
echo "   python manage.py migrate && python manage.py create_production_superuser && gunicorn payroll.wsgi:application"
echo ""
echo "4. Update DJANGO_SETTINGS_MODULE environment variable to:"
echo "   payroll.settings.ultra_minimal"
echo ""
echo "5. Redeploy"
echo ""
echo "✅ This should build successfully without any compilation errors!"
