#!/bin/bash

echo "🚀 Deploying SQLite version to eliminate psycopg2 errors..."

# Backup current requirements
cp requirements.txt requirements-postgres-backup.txt

# Use SQLite-only requirements (no psycopg2!)
cp requirements-sqlite.txt requirements.txt

echo "✅ Using SQLite-only requirements:"
echo "  - Django==4.2.7"
echo "  - gunicorn==21.2.0"
echo "  - whitenoise==6.6.0"
echo ""
echo "🎯 This eliminates ALL PostgreSQL compilation issues!"

# Commit changes
git add .
git commit -m "Use SQLite to eliminate psycopg2 compilation errors

- Removed psycopg2-binary and dj-database-url dependencies
- Created SQLite-only configuration
- Uses /tmp/db.sqlite3 for Render compatibility
- Should eliminate 'Error loading psycopg2 module' issues
- Basic Django functionality preserved"

git push origin main

echo ""
echo "🎯 Now update your Render deployment:"
echo ""
echo "1. Update DJANGO_SETTINGS_MODULE to:"
echo "   payroll.settings.sqlite"
echo ""
echo "2. Update Build Command to:"
echo "   pip install -r requirements.txt && python manage.py collectstatic --noinput"
echo ""
echo "3. Update Start Command to:"
echo "   python manage.py migrate && gunicorn payroll.wsgi:application"
echo ""
echo "4. Remove DATABASE_URL environment variable (not needed for SQLite)"
echo ""
echo "5. Redeploy"
echo ""
echo "✅ This should work without any database compilation errors!"
echo "📝 Note: Using SQLite for now - we'll add PostgreSQL back later"
