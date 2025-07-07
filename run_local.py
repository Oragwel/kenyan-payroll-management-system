#!/usr/bin/env python
"""
Local development server runner for Kenyan Payroll Management System
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run the local development server"""
    
    # Set Django settings for local development
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings.local')
    
    print("🚀 Starting Kenyan Payroll Management System - Local Development")
    print("=" * 60)
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  WARNING: Virtual environment not detected!")
        print("   Consider activating your virtual environment first:")
        print("   source .venv/bin/activate  # Linux/Mac")
        print("   .venv\\Scripts\\activate     # Windows")
        print()
    
    # Check if database exists
    db_path = Path('db.sqlite3')
    if not db_path.exists():
        print("📊 Database not found. Setting up local database...")
        
        # Run migrations
        print("🔧 Running database migrations...")
        try:
            subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                         env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'payroll.settings.local'}, 
                         check=True)
            print("✅ Database migrations completed!")
        except subprocess.CalledProcessError:
            print("❌ Migration failed. Please check for errors.")
            return
        
        # Create superuser and setup data
        print("👤 Setting up admin user and tax data...")
        try:
            subprocess.run([sys.executable, 'create_superuser.py'], 
                         env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'payroll.settings.local'}, 
                         check=True)
            print("✅ Admin user and tax data setup completed!")
        except subprocess.CalledProcessError:
            print("⚠️  Admin user setup failed, but you can create one manually.")
    
    print()
    print("🌐 Starting development server...")
    print("📍 Local URLs:")
    print("   Frontend: http://127.0.0.1:8000/")
    print("   Admin:    http://127.0.0.1:8000/admin/")
    print()
    print("👤 Default Login Credentials:")
    print("   Username: admin")
    print("   Password: PayrollAdmin2024!")
    print()
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start the development server
    try:
        subprocess.run([
            sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'
        ], env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'payroll.settings.local'})
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == '__main__':
    main()
