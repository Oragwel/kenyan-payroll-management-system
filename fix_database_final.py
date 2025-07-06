#!/usr/bin/env python3
import sqlite3
import os
import shutil

# Path to the database
db_path = 'db.sqlite3'
backup_path = 'db_backup_final.sqlite3'

if os.path.exists(db_path):
    try:
        # Create a backup first
        shutil.copy2(db_path, backup_path)
        print(f"✅ Created backup: {backup_path}")
        
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Rebuilding employees_employee table with correct schema...")
        
        # Step 1: Create new table with correct schema (all optional fields allow NULL)
        cursor.execute("""
            CREATE TABLE employees_employee_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payroll_number VARCHAR(20) NOT NULL UNIQUE,
                first_name VARCHAR(50) NOT NULL,
                middle_name VARCHAR(50),
                last_name VARCHAR(50) NOT NULL,
                date_of_birth DATE,
                gender VARCHAR(1),
                marital_status VARCHAR(10),
                email VARCHAR(254) UNIQUE,
                phone_number VARCHAR(15),
                address TEXT,
                national_id VARCHAR(8) UNIQUE,
                department_id INTEGER NOT NULL,
                job_title_id INTEGER NOT NULL,
                employment_type VARCHAR(10) NOT NULL,
                date_hired DATE,
                basic_salary DECIMAL NOT NULL,
                kra_pin VARCHAR(11) UNIQUE,
                nssf_number VARCHAR(20) UNIQUE,
                shif_number VARCHAR(20) UNIQUE,
                bank_name VARCHAR(100) NOT NULL,
                bank_branch VARCHAR(100),
                account_number VARCHAR(20) NOT NULL,
                user_id INTEGER UNIQUE,
                bank_code VARCHAR(10),
                is_active BOOLEAN DEFAULT 1
            );
        """)
        print("✅ Created new table with correct schema")
        
        # Step 2: Copy data from old table to new table, handling NULL values
        cursor.execute("""
            INSERT INTO employees_employee_new 
            (id, payroll_number, first_name, middle_name, last_name, date_of_birth, 
             gender, marital_status, email, phone_number, address, national_id, 
             department_id, job_title_id, employment_type, date_hired, basic_salary, 
             kra_pin, nssf_number, shif_number, bank_name, bank_branch, account_number, 
             user_id, bank_code, is_active)
            SELECT 
                id, payroll_number, first_name, 
                CASE WHEN middle_name = '' THEN NULL ELSE middle_name END,
                last_name, date_of_birth,
                CASE WHEN gender = '' THEN NULL ELSE gender END,
                CASE WHEN marital_status = '' THEN NULL ELSE marital_status END,
                CASE WHEN email = '' THEN NULL ELSE email END,
                phone_number, 
                CASE WHEN address = '' THEN NULL ELSE address END,
                national_id, department_id, job_title_id, employment_type, date_hired, 
                basic_salary,
                CASE WHEN kra_pin = '' THEN NULL ELSE kra_pin END,
                CASE WHEN nssf_number = '' THEN NULL ELSE nssf_number END,
                CASE WHEN shif_number = '' THEN NULL ELSE shif_number END,
                bank_name,
                CASE WHEN bank_branch = '' THEN NULL ELSE bank_branch END,
                account_number, user_id,
                CASE WHEN bank_code = '' THEN NULL ELSE bank_code END,
                COALESCE(is_active, 1)
            FROM employees_employee;
        """)
        print("✅ Copied data to new table with proper NULL handling")
        
        # Step 3: Drop the old table
        cursor.execute("DROP TABLE employees_employee;")
        print("✅ Dropped old table")
        
        # Step 4: Rename the new table
        cursor.execute("ALTER TABLE employees_employee_new RENAME TO employees_employee;")
        print("✅ Renamed new table")
        
        # Step 5: Recreate indexes
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_payroll_number_unique ON employees_employee(payroll_number);")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_email_unique ON employees_employee(email) WHERE email IS NOT NULL;")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_national_id_unique ON employees_employee(national_id) WHERE national_id IS NOT NULL;")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_kra_pin_unique ON employees_employee(kra_pin) WHERE kra_pin IS NOT NULL;")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_nssf_number_unique ON employees_employee(nssf_number) WHERE nssf_number IS NOT NULL;")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_shif_number_unique ON employees_employee(shif_number) WHERE shif_number IS NOT NULL;")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_user_id_unique ON employees_employee(user_id) WHERE user_id IS NOT NULL;")
        print("✅ Recreated indexes with proper NULL handling")
        
        # Commit the changes
        conn.commit()
        print("✅ Successfully rebuilt database schema - all optional fields now allow NULL")
        
        # Verify the change
        cursor.execute("PRAGMA table_info(employees_employee);")
        columns = cursor.fetchall()
        print("\n📋 Updated table structure:")
        for col in columns:
            null_allowed = "allows NULL" if col[3] == 0 else "NOT NULL"
            print(f"   {col[1]}: {null_allowed}")
        
        # Close the connection
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        # Restore backup if something went wrong
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, db_path)
            print(f"🔄 Restored backup due to error")
else:
    print(f"❌ Database file {db_path} not found")
