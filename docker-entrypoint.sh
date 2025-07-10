#!/bin/bash

# Docker entrypoint script for Kenyan Payroll Management System
# This script handles database migrations, static files, and superuser creation

set -e

echo "🚀 Starting Kenyan Payroll Management System..."

# Set up persistent storage directories
echo "📁 Setting up persistent storage..."
if [ -d "/data" ]; then
    # Create persistent directories if they don't exist
    mkdir -p /data/static /data/media /data/media/company_logos

    # Set proper permissions
    chown -R django:django /data
    chmod -R 755 /data

    # Create symlinks to persistent storage
    if [ ! -L "/app/staticfiles" ]; then
        rm -rf /app/staticfiles
        ln -sf /data/static /app/staticfiles
    fi

    if [ ! -L "/app/media" ]; then
        rm -rf /app/media
        ln -sf /data/media /app/media
    fi

    echo "✅ Persistent storage configured"
else
    echo "ℹ️  No persistent disk found, using container storage"
fi

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
python << END
import sys
import time
import psycopg2
from urllib.parse import urlparse
import os

# Parse DATABASE_URL
database_url = os.environ.get('DATABASE_URL')
if database_url:
    url = urlparse(database_url)
    
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                host=url.hostname,
                port=url.port,
                user=url.username,
                password=url.password,
                database=url.path[1:]
            )
            conn.close()
            print("✅ Database is ready!")
            break
        except psycopg2.OperationalError:
            retry_count += 1
            print(f"⏳ Database not ready yet... ({retry_count}/{max_retries})")
            time.sleep(2)
    
    if retry_count >= max_retries:
        print("❌ Database connection failed after maximum retries")
        sys.exit(1)
else:
    print("⚠️  No DATABASE_URL found, skipping database check")
END

# Run database migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Note: Superuser creation can be done manually after deployment
echo "ℹ️  Superuser creation skipped - can be created manually with 'python manage.py createsuperuser'"

# Get port from environment or default to 8000
PORT=${PORT:-8000}

echo "🌟 Starting Gunicorn server on port $PORT..."

# Start Gunicorn
exec gunicorn \
    --bind "0.0.0.0:$PORT" \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    payroll.wsgi:application
