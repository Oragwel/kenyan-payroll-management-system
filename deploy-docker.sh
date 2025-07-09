#!/bin/bash

# Docker Deployment Script for Kenyan Payroll Management System
# This script helps deploy the application using Docker

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="kenyan-payroll"
CONTAINER_NAME="kenyan-payroll-management-system-web-1"
PORT="8000"

# Functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Kenyan Payroll Docker Deploy  ${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    print_step "Checking requirements..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if .env.production exists
    if [ ! -f ".env.production" ]; then
        print_warning ".env.production not found. Creating from template..."
        if [ -f ".env.production.template" ]; then
            cp .env.production.template .env.production
            print_warning "Please edit .env.production with your actual values before continuing."
            exit 1
        else
            print_error ".env.production.template not found."
            exit 1
        fi
    fi
    
    echo -e "${GREEN}✓${NC} Requirements check passed"
}

build_image() {
    print_step "Building Docker image..."
    docker build -t $IMAGE_NAME:latest .
    echo -e "${GREEN}✓${NC} Image built successfully"
}

stop_existing_container() {
    print_step "Stopping existing container (if any)..."
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        docker stop $CONTAINER_NAME
        docker rm $CONTAINER_NAME
        echo -e "${GREEN}✓${NC} Existing container stopped and removed"
    else
        echo -e "${GREEN}✓${NC} No existing container found"
    fi
}

run_migrations() {
    print_step "Running database migrations..."
    docker run --rm \
        --env-file .env.production \
        $IMAGE_NAME:latest \
        python manage.py migrate
    echo -e "${GREEN}✓${NC} Migrations completed"
}

collect_static() {
    print_step "Collecting static files..."
    docker run --rm \
        --env-file .env.production \
        $IMAGE_NAME:latest \
        python manage.py collectstatic --noinput
    echo -e "${GREEN}✓${NC} Static files collected"
}

start_container() {
    print_step "Starting new container..."
    docker run -d \
        --name $CONTAINER_NAME \
        --env-file .env.production \
        -p $PORT:8000 \
        --restart unless-stopped \
        $IMAGE_NAME:latest
    echo -e "${GREEN}✓${NC} Container started successfully"
}

health_check() {
    print_step "Performing health check..."
    sleep 10  # Wait for container to start
    
    for i in {1..30}; do
        if curl -f http://localhost:$PORT/health/ &> /dev/null; then
            echo -e "${GREEN}✓${NC} Health check passed"
            return 0
        fi
        echo "Waiting for application to start... ($i/30)"
        sleep 2
    done
    
    print_error "Health check failed. Check container logs:"
    docker logs $CONTAINER_NAME
    exit 1
}

show_status() {
    print_step "Deployment status:"
    echo "Container: $(docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep $CONTAINER_NAME || echo 'Not running')"
    echo "Application URL: http://localhost:$PORT"
    echo "Admin URL: http://localhost:$PORT/admin/"
    echo "Health Check: http://localhost:$PORT/health/"
    echo ""
    echo "To view logs: docker logs -f $CONTAINER_NAME"
    echo "To stop: docker stop $CONTAINER_NAME"
}

# Main deployment function
deploy() {
    print_header
    check_requirements
    build_image
    stop_existing_container
    run_migrations
    collect_static
    start_container
    health_check
    show_status
    
    echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
}

# Handle command line arguments
case "${1:-deploy}" in
    "deploy")
        deploy
        ;;
    "build")
        build_image
        ;;
    "start")
        start_container
        ;;
    "stop")
        docker stop $CONTAINER_NAME 2>/dev/null || true
        docker rm $CONTAINER_NAME 2>/dev/null || true
        echo -e "${GREEN}✓${NC} Container stopped"
        ;;
    "logs")
        docker logs -f $CONTAINER_NAME
        ;;
    "shell")
        docker exec -it $CONTAINER_NAME /bin/bash
        ;;
    "health")
        curl -f http://localhost:$PORT/health/
        ;;
    *)
        echo "Usage: $0 {deploy|build|start|stop|logs|shell|health}"
        echo ""
        echo "Commands:"
        echo "  deploy  - Full deployment (default)"
        echo "  build   - Build Docker image only"
        echo "  start   - Start container only"
        echo "  stop    - Stop and remove container"
        echo "  logs    - View container logs"
        echo "  shell   - Access container shell"
        echo "  health  - Check application health"
        exit 1
        ;;
esac
