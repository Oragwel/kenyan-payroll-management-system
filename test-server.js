// Simple test server for Node.js 12 compatibility
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    message: 'Kenyan Payroll Management System API is running',
    timestamp: new Date().toISOString(),
    nodeVersion: process.version,
  });
});

// Test API endpoint
app.get('/api/test', (req, res) => {
  res.json({
    success: true,
    message: 'Kenyan Payroll API is working!',
    timestamp: new Date().toISOString(),
    features: [
      'Employee Management',
      'Payroll Processing', 
      'SHIF Calculations',
      'NSSF Contributions',
      'PAYE Tax Bands',
      'Housing Levy'
    ]
  });
});

// Simple employee endpoint (mock data)
app.get('/api/employees', (req, res) => {
  res.json({
    success: true,
    data: [
      {
        id: 1,
        firstName: 'John',
        lastName: 'Mwangi',
        nationalId: '12345678',
        department: 'Administration',
        jobTitle: 'Officer',
        employmentType: 'PERMANENT',
        basicSalary: 50000
      },
      {
        id: 2,
        firstName: 'Jane',
        lastName: 'Wanjiku',
        nationalId: '87654321',
        department: 'Finance',
        jobTitle: 'Manager',
        employmentType: 'PERMANENT',
        basicSalary: 75000
      }
    ]
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
  console.log(`📊 API Test: http://localhost:${PORT}/api/test`);
  console.log(`👥 Employees: http://localhost:${PORT}/api/employees`);
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
