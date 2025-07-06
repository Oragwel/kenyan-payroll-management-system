#!/bin/bash

# Quick Railway deployment script
echo "🚂 Preparing for Railway deployment..."

# Backup original requirements
cp requirements.txt requirements-full.txt

# Use simplified requirements for initial deployment
cp requirements-railway-simple.txt requirements.txt

echo "✅ Ready for Railway deployment!"
echo "📋 Next steps:"
echo "1. Commit and push these changes"
echo "2. Deploy to Railway"
echo "3. After successful deployment, we'll add back advanced features"

# Commit the changes
git add .
git commit -m "Simplify requirements for Railway deployment

- Use lightweight requirements for initial deployment
- Remove weasyprint and pandas temporarily to avoid build issues
- Will add back advanced features after basic deployment succeeds
- Core payroll functionality will work with reportlab and openpyxl"

echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ Ready to deploy to Railway!"
