#!/usr/bin/env python3
"""
Test database connection script
Run this to verify your DATABASE_URL is working correctly
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

def test_database_connection():
    """Test database connection"""
    
    # Get DATABASE_URL from environment
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL environment variable not set")
        print("Please set DATABASE_URL in your environment or .env file")
        return False
    
    print(f"🔍 Testing connection to: {database_url}")
    
    try:
        # Create engine
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            connect_args={
                "connect_timeout": 10,
                "application_name": "test_connection"
            }
        )
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            
            if row and row[0] == 1:
                print("✅ Database connection successful!")
                return True
            else:
                print("❌ Database connection failed: Unexpected result")
                return False
                
    except OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check if your PostgreSQL server is running")
        print("2. Verify the DATABASE_URL format:")
        print("   postgresql://username:password@hostname:port/database_name")
        print("3. For Render: Use the External Database URL, not Internal")
        print("4. Check if the database exists and user has permissions")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing database connection...")
    success = test_database_connection()
    
    if success:
        print("\n🎉 Database connection test passed!")
        sys.exit(0)
    else:
        print("\n💥 Database connection test failed!")
        sys.exit(1)
