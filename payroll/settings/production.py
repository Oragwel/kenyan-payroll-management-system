"""
Production settings for Kenyan Payroll Management System
Optimized for Render deployment with PostgreSQL
"""

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Allowed hosts for production
ALLOWED_HOSTS = [
    '.onrender.com',
    '.render.com',
    'localhost',
    '127.0.0.1',
    'kenyan-payroll-management-system.onrender.com',
]

# CSRF Settings for production
CSRF_TRUSTED_ORIGINS = [
    'https://kenyan-payroll-management-system.onrender.com',
    'https://*.onrender.com',
    'http://kenyan-payroll-management-system.onrender.com',  # In case of HTTP redirects
]

# Additional CSRF settings for deployment - temporarily relaxed
CSRF_COOKIE_SECURE = False  # Allow HTTP for debugging
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript access if needed
CSRF_COOKIE_SAMESITE = 'Lax'  # More permissive for cross-origin requests

# Session settings for deployment - temporarily relaxed
SESSION_COOKIE_SECURE = False  # Allow HTTP for debugging
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_SAMESITE = 'Lax'  # More permissive for cross-origin requests

# Additional security settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Render handles SSL termination

# Application definition - FULL PAYROLL SYSTEM
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Payroll system apps
    'employees',
    'payroll_processing',
    'statutory_deductions',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # Temporarily disabled for debugging
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
                'employees.context_processors.organization_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'payroll.wsgi.application'

# Database - PostgreSQL via DATABASE_URL
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Use WhiteNoise for static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin configuration
LOGIN_URL = '/login/'  # Default login URL for @login_required
LOGIN_REDIRECT_URL = '/dashboard/'  # Where to go after login (frontend)
LOGOUT_REDIRECT_URL = '/'  # Where to go after logout

# Authentication settings
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'  # For frontend login
LOGOUT_REDIRECT_URL = '/'

# Admin settings - prevent redirect to frontend dashboard
ADMIN_URL = 'admin/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}
