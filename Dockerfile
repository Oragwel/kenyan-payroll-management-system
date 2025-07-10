# Multi-stage Dockerfile for Kenyan Payroll Management System
# Stage 1: Build React frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install frontend dependencies (including dev dependencies for build)
RUN npm install

# Copy frontend source code
COPY frontend/ ./

# Build the frontend
RUN npm run build

# Stage 2: Python backend with built frontend
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=payroll.settings.production \
    PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN addgroup --system --gid 1001 django \
    && adduser --system --uid 1001 --gid 1001 --no-create-home django

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy only necessary Django application files
COPY manage.py .
COPY core/ ./core/
COPY employees/ ./employees/
COPY payroll/ ./payroll/
COPY payroll_processing/ ./payroll_processing/
COPY statutory_deductions/ ./statutory_deductions/
COPY templates/ ./templates/
COPY static/ ./static/

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/dist ./static/frontend/

# Create necessary directories and set permissions
RUN mkdir -p /app/staticfiles /app/media /app/media/company_logos /data/static /data/media \
    && chmod -R 755 /app/staticfiles /app/media /data \
    && chown -R django:django /app /data

# Note: collectstatic will be run at runtime when DATABASE_URL is available

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Copy startup script (already executable)
COPY docker-entrypoint.sh /app/

# Start command
CMD ["/app/docker-entrypoint.sh"]
