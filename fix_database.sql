-- Fix database schema to allow NULL values for optional fields

-- Create new table with correct schema
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

-- Copy data from old table, converting empty strings to NULL
INSERT INTO employees_employee_new 
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

-- Drop old table
DROP TABLE employees_employee;

-- Rename new table
ALTER TABLE employees_employee_new RENAME TO employees_employee;

-- Recreate indexes with proper NULL handling
CREATE UNIQUE INDEX employees_employee_payroll_number_unique ON employees_employee(payroll_number);
CREATE UNIQUE INDEX employees_employee_email_unique ON employees_employee(email) WHERE email IS NOT NULL;
CREATE UNIQUE INDEX employees_employee_national_id_unique ON employees_employee(national_id) WHERE national_id IS NOT NULL;
CREATE UNIQUE INDEX employees_employee_kra_pin_unique ON employees_employee(kra_pin) WHERE kra_pin IS NOT NULL;
CREATE UNIQUE INDEX employees_employee_nssf_number_unique ON employees_employee(nssf_number) WHERE nssf_number IS NOT NULL;
CREATE UNIQUE INDEX employees_employee_shif_number_unique ON employees_employee(shif_number) WHERE shif_number IS NOT NULL;
CREATE UNIQUE INDEX employees_employee_user_id_unique ON employees_employee(user_id) WHERE user_id IS NOT NULL;
