#!/usr/bin/env python3
import sqlite3
import os
import shutil

# Path to the database
db_path = 'db.sqlite3'
backup_path = 'db_backup.sqlite3'

if os.path.exists(db_path):
    try:
        # Create a backup first
        shutil.copy2(db_path, backup_path)
        print(f"✅ Created backup: {backup_path}")
        
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Modifying employees_employee table schema...")
        
        # Step 1: Create new table with correct schema
        cursor.execute("""
            CREATE TABLE employees_employee_temp (
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
                bank_code VARCHAR(10)
            );
        """)
        print("✅ Created temporary table with correct schema")
        
        # Step 2: Copy data from old table to new table
        cursor.execute("""
            INSERT INTO employees_employee_temp 
            SELECT * FROM employees_employee;
        """)
        print("✅ Copied data to temporary table")
        
        # Step 3: Drop the old table
        cursor.execute("DROP TABLE employees_employee;")
        print("✅ Dropped old table")
        
        # Step 4: Rename the new table
        cursor.execute("ALTER TABLE employees_employee_temp RENAME TO employees_employee;")
        print("✅ Renamed temporary table")
        
        # Step 5: Recreate indexes if needed
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_payroll_number_unique ON employees_employee(payroll_number);")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_email_unique ON employees_employee(email);")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_national_id_unique ON employees_employee(national_id);")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_kra_pin_unique ON employees_employee(kra_pin);")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_nssf_number_unique ON employees_employee(nssf_number);")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_shif_number_unique ON employees_employee(shif_number);")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS employees_employee_user_id_unique ON employees_employee(user_id);")
        print("✅ Recreated indexes")
        
        # Commit the changes
        conn.commit()
        print("✅ Successfully updated database schema - gender and other fields now allow NULL")
        
        # Verify the change
        cursor.execute("PRAGMA table_info(employees_employee);")
        columns = cursor.fetchall()
        for col in columns:
            if col[1] == 'gender':
                print(f"✅ Gender column: {col[1]} - NOT NULL: {col[3]} (0 = allows NULL)")
        
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
