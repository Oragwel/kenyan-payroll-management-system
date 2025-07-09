import { query, closePool } from '../config/database.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const migrations = [
  {
    name: '001_create_users_table',
    sql: `
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(150) UNIQUE NOT NULL,
        email VARCHAR(254) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        first_name VARCHAR(150),
        last_name VARCHAR(150),
        is_active BOOLEAN DEFAULT true,
        is_staff BOOLEAN DEFAULT false,
        is_superuser BOOLEAN DEFAULT false,
        date_joined TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP WITH TIME ZONE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
      
      CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
      CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
    `
  },
  
  {
    name: '002_create_organizations_table',
    sql: `
      CREATE TABLE IF NOT EXISTS organizations (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        organization_type VARCHAR(50) DEFAULT 'GOVERNMENT',
        address TEXT,
        phone VARCHAR(20),
        email VARCHAR(254),
        website VARCHAR(200),
        logo_path VARCHAR(500),
        tax_pin VARCHAR(50),
        registration_number VARCHAR(100),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `
  },
  
  {
    name: '003_create_departments_table',
    sql: `
      CREATE TABLE IF NOT EXISTS departments (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL,
        description TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `
  },
  
  {
    name: '004_create_job_titles_table',
    sql: `
      CREATE TABLE IF NOT EXISTS job_titles (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) UNIQUE NOT NULL,
        description TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `
  },
  
  {
    name: '005_create_employees_table',
    sql: `
      CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        employee_number VARCHAR(50) UNIQUE,
        first_name VARCHAR(100) NOT NULL,
        middle_name VARCHAR(100),
        last_name VARCHAR(100) NOT NULL,
        national_id VARCHAR(20) UNIQUE,
        phone_number VARCHAR(20),
        email VARCHAR(254),
        gender VARCHAR(10),
        date_of_birth DATE,
        address TEXT,
        department_id INTEGER REFERENCES departments(id),
        job_title_id INTEGER REFERENCES job_titles(id),
        employment_type VARCHAR(20) DEFAULT 'PERMANENT',
        date_hired DATE,
        basic_salary DECIMAL(12, 2),
        bank_name VARCHAR(100),
        bank_code VARCHAR(10),
        bank_branch VARCHAR(100),
        account_number VARCHAR(50) UNIQUE,
        kra_pin VARCHAR(20) UNIQUE,
        nssf_number VARCHAR(20) UNIQUE,
        shif_number VARCHAR(20) UNIQUE,
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
      
      CREATE INDEX IF NOT EXISTS idx_employees_national_id ON employees(national_id);
      CREATE INDEX IF NOT EXISTS idx_employees_employee_number ON employees(employee_number);
      CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department_id);
      CREATE INDEX IF NOT EXISTS idx_employees_job_title ON employees(job_title_id);
    `
  },
  
  {
    name: '006_create_tax_tables',
    sql: `
      -- PAYE Tax Bands
      CREATE TABLE IF NOT EXISTS paye_tax_bands (
        id SERIAL PRIMARY KEY,
        min_amount DECIMAL(12, 2) NOT NULL,
        max_amount DECIMAL(12, 2),
        rate DECIMAL(5, 2) NOT NULL,
        is_active BOOLEAN DEFAULT true,
        effective_date DATE DEFAULT CURRENT_DATE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
      
      -- NSSF Rates
      CREATE TABLE IF NOT EXISTS nssf_rates (
        id SERIAL PRIMARY KEY,
        employee_rate DECIMAL(5, 2) NOT NULL,
        employer_rate DECIMAL(5, 2) NOT NULL,
        minimum_contribution DECIMAL(12, 2),
        maximum_contribution DECIMAL(12, 2),
        is_active BOOLEAN DEFAULT true,
        effective_date DATE DEFAULT CURRENT_DATE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
      
      -- SHIF Rates
      CREATE TABLE IF NOT EXISTS shif_rates (
        id SERIAL PRIMARY KEY,
        contribution_rate DECIMAL(5, 2) NOT NULL,
        minimum_contribution DECIMAL(12, 2),
        maximum_contribution DECIMAL(12, 2),
        is_active BOOLEAN DEFAULT true,
        effective_date DATE DEFAULT CURRENT_DATE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
      
      -- Housing Levy Rates
      CREATE TABLE IF NOT EXISTS housing_levy_rates (
        id SERIAL PRIMARY KEY,
        employer_rate DECIMAL(5, 2) NOT NULL,
        minimum_contribution DECIMAL(12, 2),
        maximum_contribution DECIMAL(12, 2),
        is_active BOOLEAN DEFAULT true,
        effective_date DATE DEFAULT CURRENT_DATE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `
  },
  
  {
    name: '007_create_payroll_tables',
    sql: `
      -- Payroll Periods
      CREATE TABLE IF NOT EXISTS payroll_periods (
        id SERIAL PRIMARY KEY,
        period_name VARCHAR(100) NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        pay_date DATE NOT NULL,
        is_processed BOOLEAN DEFAULT false,
        created_by INTEGER REFERENCES users(id),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
      
      -- Payroll Records
      CREATE TABLE IF NOT EXISTS payroll_records (
        id SERIAL PRIMARY KEY,
        employee_id INTEGER REFERENCES employees(id) NOT NULL,
        payroll_period_id INTEGER REFERENCES payroll_periods(id) NOT NULL,
        basic_salary DECIMAL(12, 2) NOT NULL,
        gross_salary DECIMAL(12, 2) NOT NULL,
        paye_tax DECIMAL(12, 2) DEFAULT 0,
        nssf_employee DECIMAL(12, 2) DEFAULT 0,
        nssf_employer DECIMAL(12, 2) DEFAULT 0,
        shif_contribution DECIMAL(12, 2) DEFAULT 0,
        housing_levy DECIMAL(12, 2) DEFAULT 0,
        total_deductions DECIMAL(12, 2) DEFAULT 0,
        net_salary DECIMAL(12, 2) NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(employee_id, payroll_period_id)
      );
      
      CREATE INDEX IF NOT EXISTS idx_payroll_records_employee ON payroll_records(employee_id);
      CREATE INDEX IF NOT EXISTS idx_payroll_records_period ON payroll_records(payroll_period_id);
    `
  },
  
  {
    name: '008_create_migrations_table',
    sql: `
      CREATE TABLE IF NOT EXISTS migrations (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `
  }
];

async function runMigrations() {
  console.log('🔧 Starting database migrations...');
  
  try {
    // Create migrations table first
    await query(migrations[migrations.length - 1].sql);
    
    for (const migration of migrations) {
      // Check if migration already executed
      const result = await query(
        'SELECT id FROM migrations WHERE name = $1',
        [migration.name]
      );
      
      if (result.rows.length === 0) {
        console.log(`📊 Running migration: ${migration.name}`);
        await query(migration.sql);
        
        // Record migration
        await query(
          'INSERT INTO migrations (name) VALUES ($1)',
          [migration.name]
        );
        
        console.log(`✅ Migration completed: ${migration.name}`);
      } else {
        console.log(`⏭️  Migration already executed: ${migration.name}`);
      }
    }
    
    console.log('🎉 All migrations completed successfully!');
    
  } catch (error) {
    console.error('❌ Migration failed:', error);
    process.exit(1);
  } finally {
    await closePool();
  }
}

// Run migrations if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runMigrations();
}

export { runMigrations };
