@echo off
REM Kenyan Payroll Management System - Windows Installation Script
REM This script automates the setup process for the payroll system on Windows

echo 🇰🇪 Kenyan Payroll Management System - Windows Installation Script
echo =================================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

echo ✅ pip found
pip --version

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Check if Django is installed correctly
echo 🔍 Verifying Django installation...
python -c "import django; print(f'✅ Django {django.get_version()} installed successfully')"

REM Run migrations
echo 🗄️ Setting up database...
python manage.py makemigrations
python manage.py migrate

REM Create media directories
echo 📁 Creating media directories...
if not exist "media" mkdir media
if not exist "media\company_logos" mkdir media\company_logos
if not exist "media\payslips" mkdir media\payslips
if not exist "media\reports" mkdir media\reports

REM Collect static files
echo 📋 Collecting static files...
python manage.py collectstatic --noinput

REM Create superuser prompt
echo.
echo 👤 Create a superuser account for system administration:
echo    This account will have full access to the payroll system.
echo.
set /p create_superuser="Do you want to create a superuser now? (y/n): "

if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
) else (
    echo ⚠️ You can create a superuser later by running: python manage.py createsuperuser
)

REM Installation complete
echo.
echo 🎉 Installation completed successfully!
echo.
echo 📋 Next Steps:
echo 1. Start the development server:
echo    .venv\Scripts\activate.bat
echo    python manage.py runserver
echo.
echo 2. Open your browser and go to: http://127.0.0.1:8000
echo.
echo 3. Login with your superuser credentials
echo.
echo 4. Complete the organization setup:
echo    - Add your organization details
echo    - Upload organization logo
echo    - Create departments and job titles
echo    - Add employees
echo.
echo 📚 Documentation:
echo    - README.md - Complete system documentation
echo    - KENYAN_STATUTORY_COMPLIANCE.md - Compliance guide
echo    - SECURITY_IMPLEMENTATION.md - Security features
echo    - PAYSLIP_PRINTING_GUIDE.md - Printing setup
echo.
echo 🔧 Troubleshooting:
echo    If you encounter any issues, check the documentation files
echo    or ensure all dependencies are properly installed.
echo.
echo 🇰🇪 Built for Kenya - Compliant with KRA, NSSF, SHIF ^& Housing Levy
echo =================================================================
pause
