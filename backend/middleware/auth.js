import jwt from 'jsonwebtoken';
import { query } from '../config/database.js';

// Authenticate JWT token
export const authenticateToken = async (req, res, next) => {
  try {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

    if (!token) {
      return res.status(401).json({
        success: false,
        message: 'Access token required',
      });
    }

    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'your-secret-key');
    
    // Check if user still exists and is active
    const userResult = await query(
      'SELECT id, username, email, is_staff, is_superuser, is_active FROM users WHERE id = $1',
      [decoded.id]
    );

    if (userResult.rows.length === 0 || !userResult.rows[0].is_active) {
      return res.status(401).json({
        success: false,
        message: 'Invalid or expired token',
      });
    }

    // Add user to request object
    req.user = {
      id: decoded.id,
      username: decoded.username,
      email: decoded.email,
      isStaff: decoded.isStaff,
      isSuperuser: decoded.isSuperuser,
    };

    next();
  } catch (error) {
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({
        success: false,
        message: 'Invalid token',
      });
    }
    
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({
        success: false,
        message: 'Token expired',
      });
    }

    console.error('Authentication error:', error);
    return res.status(500).json({
      success: false,
      message: 'Internal server error',
    });
  }
};

// Require admin privileges
export const requireAdmin = (req, res, next) => {
  if (!req.user.isSuperuser) {
    return res.status(403).json({
      success: false,
      message: 'Admin privileges required',
    });
  }
  next();
};

// Require staff privileges
export const requireStaff = (req, res, next) => {
  if (!req.user.isStaff && !req.user.isSuperuser) {
    return res.status(403).json({
      success: false,
      message: 'Staff privileges required',
    });
  }
  next();
};

// Optional authentication (for public endpoints that can benefit from user context)
export const optionalAuth = async (req, res, next) => {
  try {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (token) {
      const decoded = jwt.verify(token, process.env.JWT_SECRET || 'your-secret-key');
      
      const userResult = await query(
        'SELECT id, username, email, is_staff, is_superuser, is_active FROM users WHERE id = $1',
        [decoded.id]
      );

      if (userResult.rows.length > 0 && userResult.rows[0].is_active) {
        req.user = {
          id: decoded.id,
          username: decoded.username,
          email: decoded.email,
          isStaff: decoded.isStaff,
          isSuperuser: decoded.isSuperuser,
        };
      }
    }

    next();
  } catch (error) {
    // For optional auth, we don't return errors, just continue without user
    next();
  }
};
