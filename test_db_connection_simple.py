"""
Test database connection với thông tin từ .env
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path('backend/.env')
if env_path.exists():
    load_dotenv(env_path)
    print("✓ Loaded .env file")
else:
    print("⚠ .env file not found")

# Import after loading .env
sys.path.insert(0, 'backend')
from config import Config
from database import db
from app import app

print("\n" + "="*60)
print("KIỂM TRA KẾT NỐI DATABASE")
print("="*60)
print(f"SQL_SERVER: {Config.SQL_SERVER}")
print(f"SQL_DATABASE: {Config.SQL_DATABASE}")
print(f"SQL_USERNAME: {Config.SQL_USERNAME}")
print(f"SQL_PASSWORD: {'*' * len(Config.SQL_PASSWORD) if Config.SQL_PASSWORD else '(empty)'}")
print(f"Connection String: {Config.SQLALCHEMY_DATABASE_URI[:80]}...")
print("="*60 + "\n")

with app.app_context():
    try:
        print("Đang thử kết nối...")
        connection = db.engine.connect()
        print("✓ Kết nối database thành công!")
        
        # Test query
        result = db.session.execute(db.text("SELECT @@VERSION"))
        version = result.fetchone()[0]
        print(f"✓ SQL Server Version: {version[:50]}...")
        
        connection.close()
        print("\n✅ Database hoạt động bình thường!")
        
    except Exception as e:
        print(f"❌ Lỗi kết nối database:")
        print(f"   {str(e)[:200]}")
        print("\nKiểm tra:")
        print("1. SQL Server đang chạy?")
        print("2. Database 'BLOCKCHAIN_CHUYENTIEN' đã được tạo?")
        print("3. Username/Password trong .env đúng?")
        print("4. SQL Server cho phép SQL Authentication?")
        sys.exit(1)

