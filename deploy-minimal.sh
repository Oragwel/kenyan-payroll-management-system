#!/bin/bash

echo "🚀 Deploying minimal version for reliable deployment..."

# Backup current requirements
cp requirements.txt requirements-backup.txt

# Use minimal requirements
cp requirements-minimal.txt requirements.txt

echo "✅ Switched to minimal requirements"
echo "📋 What's included:"
echo "  ✅ Core Django functionality"
echo "  ✅ Employee management"
echo "  ✅ Basic payroll processing"
echo "  ✅ PDF generation (reportlab)"
echo "  ✅ Excel exports (openpyxl)"
echo "  ✅ Admin interface"
echo ""
echo "⏳ Temporarily removed (will add back later):"
echo "  - weasyprint (advanced PDF styling)"
echo "  - pandas (advanced analytics)"
echo "  - django-axes (advanced security)"
echo "  - crispy-bootstrap5 (advanced forms)"

# Commit changes
git add .
git commit -m "Switch to minimal requirements for reliable deployment

- Use ultra-minimal requirements to avoid compilation errors
- Core payroll functionality preserved
- Basic PDF and Excel generation included
- Will incrementally add advanced features after successful deployment"

git push origin main

echo ""
echo "🎯 Now deploy to Render:"
echo "1. Go to render.com"
echo "2. New Web Service → Connect your repo"
echo "3. Use these settings:"
echo "   Build Command: pip install -r requirements-minimal.txt && python manage.py collectstatic --noinput"
echo "   Start Command: python manage.py migrate && python manage.py create_production_superuser && gunicorn payroll.wsgi:application"
echo "4. Add environment variables from render.yaml"
echo ""
echo "✅ This should deploy successfully!"
