#!/bin/bash

echo "🚀 Setting up Kenyan Payroll Management System (Node.js + Vite)"
echo "================================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    print_error "Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi

print_status "Node.js version: $(node -v)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi

print_status "npm version: $(npm -v)"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    print_warning "PostgreSQL is not installed or not in PATH."
    print_info "For local development, please install PostgreSQL:"
    print_info "Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    print_info "macOS: brew install postgresql"
    print_info "Windows: Download from https://www.postgresql.org/download/"
    echo ""
fi

# Install root dependencies
print_info "Installing root dependencies..."
npm install

# Install backend dependencies
print_info "Installing backend dependencies..."
cd backend
npm install
cd ..

# Install frontend dependencies
print_info "Installing frontend dependencies..."
cd frontend
npm install
cd ..

print_status "All dependencies installed successfully!"

# Create environment files
print_info "Creating environment configuration files..."

# Backend .env
if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    print_status "Created backend/.env file"
    print_warning "Please update backend/.env with your database credentials"
else
    print_info "backend/.env already exists"
fi

# Frontend .env
if [ ! -f "frontend/.env" ]; then
    cat > frontend/.env << EOF
# Frontend Environment Variables
VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=Kenyan Payroll Management System
VITE_APP_VERSION=1.0.0
EOF
    print_status "Created frontend/.env file"
else
    print_info "frontend/.env already exists"
fi

# Create necessary directories
print_info "Creating necessary directories..."
mkdir -p backend/uploads
mkdir -p backend/logs
mkdir -p frontend/public/assets

print_status "Directory structure created"

# Database setup instructions
echo ""
echo "🗄️  DATABASE SETUP INSTRUCTIONS"
echo "================================"
print_info "1. Make sure PostgreSQL is running"
print_info "2. Create a database for the application:"
echo "   sudo -u postgres psql"
echo "   CREATE DATABASE kenyan_payroll_dev;"
echo "   CREATE USER payroll_user WITH PASSWORD 'your_password';"
echo "   GRANT ALL PRIVILEGES ON DATABASE kenyan_payroll_dev TO payroll_user;"
echo "   \\q"
echo ""
print_info "3. Update backend/.env with your database credentials"
print_info "4. Run database migrations: npm run migrate"
print_info "5. Seed initial data: npm run seed"

echo ""
echo "🚀 NEXT STEPS"
echo "============="
print_info "1. Update backend/.env with your database credentials"
print_info "2. Run: npm run migrate (to create database tables)"
print_info "3. Run: npm run seed (to add initial data)"
print_info "4. Run: npm run dev (to start both backend and frontend)"
echo ""
print_info "Frontend will be available at: http://localhost:5173"
print_info "Backend API will be available at: http://localhost:5000"
echo ""

print_status "Setup completed successfully! 🎉"
print_info "Read the README.md file for detailed usage instructions."
