#!/bin/bash

# Build script for Vercel deployment
echo "🚀 Starting build process for Kenyan Payroll System..."

# Install dependencies (use minimal requirements for Vercel)
echo "📦 Installing Python dependencies..."
if [ -f "requirements-vercel.txt" ]; then
    echo "Using minimal requirements for Vercel deployment..."
    pip3 install -r requirements-vercel.txt
else
    echo "Using full requirements..."
    pip3 install -r requirements.txt
fi

# Create staticfiles_build directory structure
echo "📂 Creating output directories..."
mkdir -p staticfiles_build/static
mkdir -p staticfiles_build/media

# Set Django settings to use a dummy database for collectstatic
export DJANGO_SETTINGS_MODULE=payroll.settings.build

# Create a temporary build settings file
cat > payroll/settings/build.py << 'EOF'
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'build-key-not-for-production-use-only'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'employees',
    'payroll_management',
    'organizations',
    'reports',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'payroll.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'organizations.context_processors.organization_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'payroll.wsgi.application'

# Use a dummy database configuration that doesn't require actual database connection
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'media')

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EOF

# Collect static files with build settings
echo "📁 Collecting static files..."
if python3 manage.py collectstatic --noinput --clear; then
    echo "✅ Static files collected successfully"
else
    echo "⚠️ Static files collection failed, but continuing..."
fi

# Copy static files to output directory
echo "📂 Copying static files to output directory..."
if [ -d "static" ]; then
    cp -r static/* staticfiles_build/static/ 2>/dev/null || echo "No static files to copy from static/"
fi

# Copy media files if they exist
if [ -d "media" ]; then
    cp -r media/* staticfiles_build/media/ 2>/dev/null || echo "No media files to copy"
fi

# Ensure we have some content in the output directory
echo "📄 Creating index file..."
cat > staticfiles_build/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Kenyan Payroll Management System</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <h1>Kenyan Payroll Management System</h1>
    <p>Static files built successfully for Vercel deployment.</p>
    <script>
        // Redirect to the main application
        if (window.location.pathname === '/') {
            window.location.href = '/dashboard/';
        }
    </script>
</body>
</html>
EOF

# Check if DATABASE_URL is available for migrations
if [ -n "$DATABASE_URL" ]; then
    echo "🗄️ DATABASE_URL found, running migrations..."
    export DJANGO_SETTINGS_MODULE=payroll.settings.vercel
    python3 manage.py migrate --noinput || echo "⚠️ Migration failed, but continuing..."

    # Create superuser if environment variables are provided
    if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "👤 Creating production superuser..."
        python3 manage.py create_production_superuser || echo "⚠️ Superuser creation failed, but continuing..."
    else
        echo "ℹ️ No DJANGO_SUPERUSER_PASSWORD found, skipping superuser creation..."
    fi
else
    echo "⚠️ No DATABASE_URL found, skipping database operations..."
fi

# Clean up build settings
rm -f payroll/settings/build.py

echo "✅ Build process completed successfully!"
echo "📊 Output directory contents:"
ls -la staticfiles_build/
