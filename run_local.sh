#!/bin/bash

echo "🚀 Starting Kenyan Payroll Management System - Local Development"
echo "============================================================"

# Set Django settings for local development
export DJANGO_SETTINGS_MODULE=payroll.settings.local

# Check if virtual environment exists and activate it
if [ -f ".venv/bin/activate" ]; then
    echo "🔧 Activating virtual environment..."
    source .venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found"
    echo "   Consider creating one with: python -m venv .venv"
    echo "   Then activate with: source .venv/bin/activate"
    echo ""
fi

# Check if database exists
if [ ! -f "db.sqlite3" ]; then
    echo "📊 Database not found. Setting up local database..."
    echo "🔧 Running database migrations..."
    python manage.py migrate
    if [ $? -ne 0 ]; then
        echo "❌ Migration failed. Please check for errors."
        exit 1
    fi
    echo "✅ Database migrations completed!"
    
    echo "👤 Setting up admin user and tax data..."
    python create_superuser.py
    if [ $? -ne 0 ]; then
        echo "⚠️  Admin user setup failed, but you can create one manually."
    else
        echo "✅ Admin user and tax data setup completed!"
    fi
fi

echo ""
echo "🌐 Starting development server..."
echo "📍 Local URLs:"
echo "   Frontend: http://127.0.0.1:8000/"
echo "   Admin:    http://127.0.0.1:8000/admin/"
echo ""
echo "👤 Default Login Credentials:"
echo "   Username: admin"
echo "   Password: PayrollAdmin2024!"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo "============================================================"

# Start the development server
python manage.py runserver 127.0.0.1:8000
