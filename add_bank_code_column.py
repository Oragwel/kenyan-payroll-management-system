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
        
        # Check if the column already exists
        cursor.execute("PRAGMA table_info(employees_employee);")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'bank_code' not in columns:
            # Add the bank_code column
            cursor.execute("ALTER TABLE employees_employee ADD COLUMN bank_code VARCHAR(10);")
            conn.commit()
            print("✅ Successfully added bank_code column to employees_employee table")
        else:
            print("ℹ️  bank_code column already exists in employees_employee table")
        
        # Close the connection
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print(f"❌ Database file {db_path} not found")
