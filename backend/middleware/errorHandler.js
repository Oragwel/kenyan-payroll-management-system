// Global error handler middleware
export const errorHandler = (err, req, res, next) => {
  let error = { ...err };
  error.message = err.message;

  // Log error
  console.error('Error:', err);

  // Mongoose bad ObjectId
  if (err.name === 'CastError') {
    const message = 'Resource not found';
    error = { message, statusCode: 404 };
  }

  // Mongoose duplicate key
  if (err.code === 11000) {
    const message = 'Duplicate field value entered';
    error = { message, statusCode: 400 };
  }

  // Mongoose validation error
  if (err.name === 'ValidationError') {
    const message = Object.values(err.errors).map(val => val.message).join(', ');
    error = { message, statusCode: 400 };
  }

  // PostgreSQL errors
  if (err.code) {
    switch (err.code) {
      case '23505': // Unique violation
        error = {
          message: 'Duplicate entry. This record already exists.',
          statusCode: 400
        };
        break;
      case '23503': // Foreign key violation
        error = {
          message: 'Referenced record does not exist.',
          statusCode: 400
        };
        break;
      case '23502': // Not null violation
        error = {
          message: 'Required field is missing.',
          statusCode: 400
        };
        break;
      case '42P01': // Undefined table
        error = {
          message: 'Database table not found. Please run migrations.',
          statusCode: 500
        };
        break;
      default:
        error = {
          message: 'Database error occurred.',
          statusCode: 500
        };
    }
  }

  // JWT errors
  if (err.name === 'JsonWebTokenError') {
    error = {
      message: 'Invalid token.',
      statusCode: 401
    };
  }

  if (err.name === 'TokenExpiredError') {
    error = {
      message: 'Token expired.',
      statusCode: 401
    };
  }

  // Default error response
  const statusCode = error.statusCode || 500;
  const message = error.message || 'Internal Server Error';

  res.status(statusCode).json({
    success: false,
    message,
    ...(process.env.NODE_ENV === 'development' && {
      stack: err.stack,
      error: err
    })
  });
};

// Async error handler wrapper
export const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};
