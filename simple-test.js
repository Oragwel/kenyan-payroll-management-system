// Simple Node.js test without external dependencies
const http = require('http');
const url = require('url');

const PORT = 5000;

// Sample employee data
const employees = [
  {
    id: 1,
    firstName: 'John',
    lastName: 'Mwangi',
    nationalId: '12345678',
    department: 'Administration',
    jobTitle: 'Officer',
    employmentType: 'PERMANENT',
    basicSalary: 50000,
    shif: 1375, // 2.75% of 50000
    nssf: 3000, // 6% of 50000
    paye: 5000,
    netSalary: 40625
  },
  {
    id: 2,
    firstName: 'Jane',
    lastName: 'Wanjiku',
    nationalId: '87654321',
    department: 'Finance',
    jobTitle: 'Manager',
    employmentType: 'PERMANENT',
    basicSalary: 75000,
    shif: 2062.5, // 2.75% of 75000
    nssf: 4500, // 6% of 75000
    paye: 12500,
    netSalary: 55937.5
  },
  {
    id: 3,
    firstName: 'Peter',
    lastName: 'Kiprotich',
    nationalId: '11223344',
    department: 'Ugatuzi',
    jobTitle: 'Casual Worker',
    employmentType: 'CASUAL',
    basicSalary: 30000,
    shif: 825, // 2.75% of 30000
    nssf: 0, // No NSSF for casual workers
    paye: 2500,
    netSalary: 26675
  }
];

// Calculate SHIF (2.75%)
function calculateSHIF(salary) {
  return salary * 0.0275;
}

// Calculate NSSF (6% for permanent, 0% for casual)
function calculateNSSF(salary, employmentType) {
  if (employmentType === 'CASUAL') return 0;
  return salary * 0.06;
}

// Simple PAYE calculation (simplified)
function calculatePAYE(salary) {
  if (salary <= 24000) return 0;
  if (salary <= 32333) return (salary - 24000) * 0.1;
  if (salary <= 40385) return 833.3 + (salary - 32333) * 0.15;
  if (salary <= 48462) return 2041.1 + (salary - 40385) * 0.2;
  if (salary <= 56538) return 3656.5 + (salary - 48462) * 0.25;
  return 4675.5 + (salary - 56538) * 0.3;
}

// Create HTTP server
const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const path = parsedUrl.pathname;
  
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Content-Type', 'application/json');

  if (path === '/health') {
    res.writeHead(200);
    res.end(JSON.stringify({
      status: 'OK',
      message: 'Kenyan Payroll Management System API is running',
      timestamp: new Date().toISOString(),
      nodeVersion: process.version,
      features: ['SHIF', 'NSSF', 'PAYE', 'Housing Levy']
    }));
  }
  else if (path === '/api/employees') {
    res.writeHead(200);
    res.end(JSON.stringify({
      success: true,
      message: 'Employees retrieved successfully',
      data: employees,
      count: employees.length
    }));
  }
  else if (path === '/api/payroll/calculate') {
    if (req.method === 'POST') {
      let body = '';
      req.on('data', chunk => {
        body += chunk.toString();
      });
      req.on('end', () => {
        try {
          const { employeeId, basicSalary, employmentType } = JSON.parse(body);
          
          const shif = calculateSHIF(basicSalary);
          const nssf = calculateNSSF(basicSalary, employmentType);
          const paye = calculatePAYE(basicSalary);
          const housingLevy = basicSalary * 0.015; // 1.5% employer contribution
          const totalDeductions = shif + nssf + paye;
          const netSalary = basicSalary - totalDeductions;
          
          res.writeHead(200);
          res.end(JSON.stringify({
            success: true,
            message: 'Payroll calculated successfully',
            data: {
              employeeId,
              basicSalary,
              employmentType,
              deductions: {
                shif: Math.round(shif * 100) / 100,
                nssf: Math.round(nssf * 100) / 100,
                paye: Math.round(paye * 100) / 100,
                total: Math.round(totalDeductions * 100) / 100
              },
              employerContributions: {
                nssf: employmentType !== 'CASUAL' ? Math.round(nssf * 100) / 100 : 0,
                housingLevy: Math.round(housingLevy * 100) / 100
              },
              netSalary: Math.round(netSalary * 100) / 100
            }
          }));
        } catch (error) {
          res.writeHead(400);
          res.end(JSON.stringify({
            success: false,
            message: 'Invalid request data',
            error: error.message
          }));
        }
      });
    } else {
      res.writeHead(405);
      res.end(JSON.stringify({
        success: false,
        message: 'Method not allowed'
      }));
    }
  }
  else if (path === '/api/departments') {
    res.writeHead(200);
    res.end(JSON.stringify({
      success: true,
      data: [
        'Administration',
        'Finance',
        'Human Resources',
        'IT',
        'Operations',
        'Ugatuzi',
        'Municipality'
      ]
    }));
  }
  else if (path === '/api/job-titles') {
    res.writeHead(200);
    res.end(JSON.stringify({
      success: true,
      data: [
        'Manager',
        'Officer',
        'Assistant',
        'Clerk',
        'Driver',
        'Security Guard',
        'Casual Worker'
      ]
    }));
  }
  else {
    res.writeHead(404);
    res.end(JSON.stringify({
      success: false,
      message: 'Route not found',
      path: path,
      availableRoutes: [
        '/health',
        '/api/employees',
        '/api/payroll/calculate',
        '/api/departments',
        '/api/job-titles'
      ]
    }));
  }
});

server.listen(PORT, () => {
  console.log(`🚀 Kenyan Payroll API Server running on port ${PORT}`);
  console.log(`📍 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/health`);
  console.log(`👥 Employees: http://localhost:${PORT}/api/employees`);
  console.log(`💰 Payroll calc: http://localhost:${PORT}/api/payroll/calculate`);
  console.log(`🏢 Departments: http://localhost:${PORT}/api/departments`);
  console.log(`💼 Job titles: http://localhost:${PORT}/api/job-titles`);
  console.log('');
  console.log('✅ Server is ready for testing!');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received. Shutting down gracefully...');
  server.close(() => {
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('SIGINT received. Shutting down gracefully...');
  server.close(() => {
    process.exit(0);
  });
});
