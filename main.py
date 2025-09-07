"""
CA Compliance Management System - Backend API
Main FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine, Base
from app.api.api_v1.api import api_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables (with error handling)
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")
    # Don't fail the entire application if database is not available
    # This allows the app to start and handle database connection later

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Comprehensive accounting and compliance management platform for CAs and SMBs",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        # Test database connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Database connection successful")
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully")
        
        # Create default users if they don't exist
        from app.core.database import SessionLocal
        from app.models.user import User, UserRole, UserStatus
        from app.core.security import get_password_hash
        
        db = SessionLocal()
        try:
            # Check if admin user exists
            admin_user = db.query(User).filter(User.username == "admin").first()
            if not admin_user:
                admin_user = User(
                    email="admin@compliance.com",
                    username="admin",
                    full_name="System Administrator",
                    hashed_password=get_password_hash("admin123"),
                    role=UserRole.ADMIN,
                    status=UserStatus.ACTIVE,
                    phone="+91 98765 43210",
                    department="IT"
                )
                db.add(admin_user)
                logger.info("Created default admin user: admin / admin123")
            
            # Check if demo user exists
            demo_user = db.query(User).filter(User.username == "demo").first()
            if not demo_user:
                demo_user = User(
                    email="demo@compliance.com",
                    username="demo",
                    full_name="Demo User",
                    hashed_password=get_password_hash("demo123"),
                    role=UserRole.CLIENT,
                    status=UserStatus.ACTIVE,
                    phone="+91 98765 43211",
                    department="Demo"
                )
                db.add(demo_user)
                logger.info("Created default demo user: demo / demo123")
            
            db.commit()
            logger.info("Default users created successfully")
        except Exception as e:
            logger.error(f"Error creating default users: {e}")
            db.rollback()
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        logger.error("Please check your DATABASE_URL environment variable")
        # Don't fail the startup, but log the error

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files (if directory exists)
import os
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CA Compliance Management System API",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
    
    return {
        "status": "healthy", 
        "version": settings.VERSION,
        "database": db_status,
        "environment": settings.ENVIRONMENT,
        "database_url_set": bool(settings.DATABASE_URL and settings.DATABASE_URL != "postgresql://user:password@localhost/compliance_db")
    }

@app.get("/ping")
async def ping():
    """Simple ping endpoint that doesn't require database"""
    return {"message": "pong", "status": "ok"}

@app.get("/test-auth")
async def test_auth():
    """Test authentication endpoint with demo credentials"""
    return {
        "message": "Authentication test endpoint",
        "demo_credentials": {
            "admin": {"username": "admin", "password": "admin123"},
            "demo": {"username": "demo", "password": "demo123"}
        },
        "endpoints": {
            "login": "/api/v1/auth/login-json",
            "health": "/health",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
