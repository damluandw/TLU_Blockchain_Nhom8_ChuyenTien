# Database Setup

## Cài đặt SQL Server

1. Tải và cài đặt SQL Server từ Microsoft
2. Cài đặt SQL Server Management Studio (SSMS)

## Tạo Database

1. Mở SSMS và kết nối với SQL Server
2. Tạo database mới:
   ```sql
   CREATE DATABASE BankingBlockchain;
   ```
3. Chạy script `schema.sql` để tạo các bảng

## Cấu hình ODBC Driver

Trên Windows:
1. Mở "ODBC Data Sources (64-bit)"
2. Đảm bảo có "ODBC Driver 17 for SQL Server" hoặc version mới hơn
3. Nếu chưa có, tải từ Microsoft

Trên Linux/Mac:
- Cài đặt `unixODBC` và `ODBC Driver for SQL Server`

## Kết nối từ Python

Cập nhật thông tin kết nối trong file `.env`:
- SQL_SERVER: địa chỉ server (localhost hoặc IP)
- SQL_DATABASE: tên database (BankingBlockchain)
- SQL_USERNAME: tên user SQL Server
- SQL_PASSWORD: mật khẩu

## Kiểm tra kết nối

Chạy script test:
```python
from backend.config import Config
from backend.database import db
from backend.app import app

with app.app_context():
    db.create_all()
    print("Database connection successful!")
```

