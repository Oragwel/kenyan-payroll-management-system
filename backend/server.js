const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const dotenv = require('dotenv');
const path = require('path');

// Import routes (will be created as CommonJS modules)
// const authRoutes = require('./routes/auth');
// const employeeRoutes = require('./routes/employees');
// const payrollRoutes = require('./routes/payroll');
// const organizationRoutes = require('./routes/organizations');
// const reportsRoutes = require('./routes/reports');
// const taxRoutes = require('./routes/tax');

// Import middleware (will be created as CommonJS modules)
// const { errorHandler } = require('./middleware/errorHandler');
// const { authenticateToken } = require('./middleware/auth');

// Load environment variables
dotenv.config();

// __dirname is available in CommonJS

const app = express();
const PORT = process.env.PORT || 5000;

// Security middleware
app.use(helmet({
  crossOriginEmbedderPolicy: false,
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.',
});
app.use('/api/', limiter);

// CORS configuration
app.use(cors({
  origin: process.env.NODE_ENV === 'production' 
    ? process.env.FRONTEND_URL 
    : ['http://localhost:3000', 'http://localhost:5173'],
  credentials: true,
}));

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Compression middleware
app.use(compression());

// Logging middleware
app.use(morgan(process.env.NODE_ENV === 'production' ? 'combined' : 'dev'));

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'OK',
    message: 'Kenyan Payroll Management System API is running',
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development',
  });
});

// API routes (commented out for initial setup)
// app.use('/api/auth', authRoutes);
// app.use('/api/employees', authenticateToken, employeeRoutes);
// app.use('/api/payroll', authenticateToken, payrollRoutes);
// app.use('/api/organizations', authenticateToken, organizationRoutes);
// app.use('/api/reports', authenticateToken, reportsRoutes);
// app.use('/api/tax', authenticateToken, taxRoutes);

// Simple test route
app.get('/api/test', (req, res) => {
  res.json({
    success: true,
    message: 'Kenyan Payroll API is working!',
    timestamp: new Date().toISOString(),
  });
});

// Serve static files in production
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, '../frontend/dist')));

  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/dist/index.html'));
  });
}

// Simple error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({
    success: false,
    message: 'Internal server error',
    ...(process.env.NODE_ENV === 'development' && { error: err.message })
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    message: 'Route not found',
    path: req.originalUrl,
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Kenyan Payroll API Server running on port ${PORT}`);
  console.log(`📍 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/health`);
  
  if (process.env.NODE_ENV !== 'production') {
    console.log(`📊 API Base URL: http://localhost:${PORT}/api`);
  }
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received. Shutting down gracefully...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received. Shutting down gracefully...');
  process.exit(0);
});

module.exports = app;
