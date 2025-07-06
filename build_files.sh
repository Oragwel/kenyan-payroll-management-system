#!/bin/bash

# Build script for Vercel deployment
echo "🚀 Starting build process for Kenyan Payroll System..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput --clear

# Create staticfiles_build directory if it doesn't exist
mkdir -p staticfiles_build

# Copy static files to the expected output directory
echo "📂 Copying static files to output directory..."
cp -r staticfiles/* staticfiles_build/ 2>/dev/null || echo "No static files to copy"

# Run database migrations (only if DATABASE_URL is set)
if [ ! -z "$DATABASE_URL" ]; then
    echo "🗄️ Running database migrations..."
    python3 manage.py migrate --noinput

    # Create superuser if it doesn't exist
    echo "👤 Setting up initial data..."
    python3 manage.py shell << EOF
from django.contrib.auth.models import User
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@payroll.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' already exists.")
EOF
else
    echo "⚠️ No DATABASE_URL found, skipping database operations..."
fi

echo "✅ Build process completed successfully!"
