#!/usr/bin/env python3
import sqlite3
import os

# Path to the database
db_path = 'db.sqlite3'

if os.path.exists(db_path):
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Fixing gender column to allow NULL values...")
        
        # SQLite doesn't support ALTER COLUMN directly, so we need to:
        # 1. Create a new table with the correct schema
        # 2. Copy data from old table
        # 3. Drop old table
        # 4. Rename new table
        
        # First, get the current table schema
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='employees_employee';")
        current_schema = cursor.fetchone()[0]
        print(f"Current schema: {current_schema}")
        
        # Create new table with gender allowing NULL
        cursor.execute("""
            CREATE TABLE employees_employee_new AS 
            SELECT * FROM employees_employee;
        """)
        
        # Drop the old table
        cursor.execute("DROP TABLE employees_employee;")
        
        # Create the new table with correct schema
        cursor.execute("""
            CREATE TABLE "employees_employee" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "payroll_number" varchar(20) NOT NULL UNIQUE,
                "first_name" varchar(50) NOT NULL,
                "middle_name" varchar(50) NOT NULL,
                "last_name" varchar(50) NOT NULL,
                "date_of_birth" date,
                "gender" varchar(1),
                "marital_status" varchar(10) NOT NULL,
                "email" varchar(254) UNIQUE,
                "phone_number" varchar(15),
                "address" text NOT NULL,
                "national_id" varchar(8) UNIQUE,
                "department_id" bigint NOT NULL REFERENCES "employees_department" ("id") DEFERRABLE INITIALLY DEFERRED,
                "job_title_id" bigint NOT NULL REFERENCES "employees_jobtitle" ("id") DEFERRABLE INITIALLY DEFERRED,
                "employment_type" varchar(10) NOT NULL,
                "date_hired" date,
                "basic_salary" decimal NOT NULL,
                "kra_pin" varchar(11) UNIQUE,
                "nssf_number" varchar(20) UNIQUE,
                "shif_number" varchar(20) UNIQUE,
                "bank_name" varchar(100) NOT NULL,
                "bank_branch" varchar(100),
                "account_number" varchar(20) NOT NULL,
                "user_id" integer UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
                "bank_code" varchar(10)
            );
        """)
        
        # Copy data back from the temporary table
        cursor.execute("""
            INSERT INTO employees_employee 
            SELECT * FROM employees_employee_new;
        """)
        
        # Drop the temporary table
        cursor.execute("DROP TABLE employees_employee_new;")
        
        # Commit the changes
        conn.commit()
        print("✅ Successfully updated gender column to allow NULL values")
        
        # Close the connection
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.rollback()
            conn.close()
else:
    print(f"❌ Database file {db_path} not found")
