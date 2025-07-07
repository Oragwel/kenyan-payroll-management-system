@echo off
echo 🚀 Starting Kenyan Payroll Management System - Local Development
echo ============================================================

REM Set Django settings for local development
set DJANGO_SETTINGS_MODULE=payroll.settings.local

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️  Virtual environment not found at .venv\Scripts\
    echo    You may need to create one or activate manually
    echo.
)

REM Check if database exists
if not exist "db.sqlite3" (
    echo 📊 Database not found. Setting up local database...
    echo 🔧 Running database migrations...
    python manage.py migrate
    if errorlevel 1 (
        echo ❌ Migration failed. Please check for errors.
        pause
        exit /b 1
    )
    echo ✅ Database migrations completed!
    
    echo 👤 Setting up admin user and tax data...
    python create_superuser.py
    if errorlevel 1 (
        echo ⚠️  Admin user setup failed, but you can create one manually.
    ) else (
        echo ✅ Admin user and tax data setup completed!
    )
)

echo.
echo 🌐 Starting development server...
echo 📍 Local URLs:
echo    Frontend: http://127.0.0.1:8000/
echo    Admin:    http://127.0.0.1:8000/admin/
echo.
echo 👤 Default Login Credentials:
echo    Username: admin
echo    Password: PayrollAdmin2024!
echo.
echo 🛑 Press Ctrl+C to stop the server
echo ============================================================

REM Start the development server
python manage.py runserver 127.0.0.1:8000

pause
