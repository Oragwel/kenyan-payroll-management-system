import pg from 'pg';
import dotenv from 'dotenv';

dotenv.config();

const { Pool } = pg;

// Database configuration
const dbConfig = {
  // Production (PostgreSQL)
  production: {
    connectionString: process.env.DATABASE_URL,
    ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
  },
  
  // Development (PostgreSQL)
  development: {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'kenyan_payroll_dev',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'password',
    max: 10,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
  },
  
  // Test (PostgreSQL)
  test: {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_TEST_NAME || 'kenyan_payroll_test',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'password',
    max: 5,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
  }
};

const environment = process.env.NODE_ENV || 'development';
const config = dbConfig[environment];

// Create connection pool
const pool = new Pool(config);

// Test database connection
pool.on('connect', () => {
  console.log('✅ Connected to PostgreSQL database');
});

pool.on('error', (err) => {
  console.error('❌ PostgreSQL connection error:', err);
  process.exit(-1);
});

// Database query helper
export const query = async (text, params) => {
  const start = Date.now();
  try {
    const res = await pool.query(text, params);
    const duration = Date.now() - start;
    
    if (process.env.NODE_ENV === 'development') {
      console.log('📊 Query executed:', { text, duration, rows: res.rowCount });
    }
    
    return res;
  } catch (error) {
    console.error('❌ Database query error:', error);
    throw error;
  }
};

// Get a client from the pool
export const getClient = async () => {
  return await pool.connect();
};

// Close all connections
export const closePool = async () => {
  await pool.end();
  console.log('🔌 Database connection pool closed');
};

// Transaction helper
export const transaction = async (callback) => {
  const client = await getClient();
  
  try {
    await client.query('BEGIN');
    const result = await callback(client);
    await client.query('COMMIT');
    return result;
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
};

// Health check
export const healthCheck = async () => {
  try {
    const result = await query('SELECT NOW() as current_time');
    return {
      status: 'healthy',
      timestamp: result.rows[0].current_time,
      environment,
    };
  } catch (error) {
    return {
      status: 'unhealthy',
      error: error.message,
      environment,
    };
  }
};

export default pool;
