"""
Test database connection
"""
import sys
import os
sys.path.insert(0, 'backend')

from app import app
from database import db

with app.app_context():
    try:
        print("Testing database connection...")
        connection = db.engine.connect()
        print("✓ Database connection successful!")
        
        print("\nCreating tables...")
        db.create_all()
        print("✓ Database tables created/verified successfully!")
        
        connection.close()
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nPlease check:")
        print("1. SQL Server is running")
        print("2. Database 'BankingBlockchain' exists")
        print("3. Connection settings in backend/.env are correct")
        print("4. ODBC Driver 17 for SQL Server is installed")
        import traceback
        traceback.print_exc()

