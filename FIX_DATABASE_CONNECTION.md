# 🔧 Hướng Dẫn Sửa Lỗi Kết Nối Database

## Lỗi: "Named Pipes Provider: Could not open a connection to SQL Server [53]"

Lỗi này có nghĩa là không thể kết nối đến SQL Server.

## ✅ Giải Pháp

### Bước 1: Kiểm Tra SQL Server Đang Chạy

1. Mở **SQL Server Configuration Manager**
2. Kiểm tra **SQL Server Services**:
   - **SQL Server (SQL2022)** phải có status là **Running**
   - Nếu không chạy, click chuột phải → **Start**

Hoặc kiểm tra trong **Services** (services.msc):
- Tìm service: **SQL Server (SQL2022)**
- Đảm bảo status là **Running**

### Bước 2: Kiểm Tra SQL Server Cho Phép Remote Connections

1. Mở **SQL Server Management Studio (SSMS)**
2. Kết nối đến server: `DESKTOP-CRFJV4A\SQL2022`
3. Click chuột phải vào server → **Properties**
4. Chọn **Connections**
5. Đảm bảo **Allow remote connections to this server** được **checked**
6. Click **OK**

### Bước 3: Kiểm Tra SQL Server Authentication

1. Trong SSMS, vào **Security** → **Logins**
2. Click chuột phải vào **sa** → **Properties**
3. Chọn **Status**
4. Đảm bảo:
   - **Login:** Enabled
   - **SQL Server Authentication:** Enabled
5. Nếu chưa enable, chọn **General** tab → **SQL Server authentication** → Set password

### Bước 4: Kiểm Tra SQL Server Browser Service

1. Mở **SQL Server Configuration Manager**
2. Kiểm tra **SQL Server Browser** service:
   - Status phải là **Running**
   - Start Mode phải là **Automatic**

### Bước 5: Kiểm Tra Firewall

1. Mở **Windows Firewall**
2. Cho phép SQL Server qua firewall:
   - Port **1433** (TCP) - SQL Server default port
   - Port **1434** (UDP) - SQL Server Browser

Hoặc tạm thời tắt firewall để test (chỉ cho development).

### Bước 6: Kiểm Tra Connection String

Trong file `backend/.env`, đảm bảo:

```env
SQL_SERVER=DESKTOP-CRFJV4A\SQL2022
SQL_DATABASE=BLOCKCHAIN_CHUYENTIEN
SQL_USERNAME=sa
SQL_PASSWORD=your_password
```

**Lưu ý:** 
- SQL_SERVER có thể cần dùng format khác:
  - `localhost\SQL2022` (nếu kết nối local)
  - `DESKTOP-CRFJV4A\SQL2022` (tên máy\instance)
  - Hoặc IP address: `127.0.0.1\SQL2022`

### Bước 7: Kiểm Tra Database Tồn Tại

1. Mở SSMS
2. Kết nối đến server
3. Kiểm tra database **BLOCKCHAIN_CHUYENTIEN** có trong danh sách không
4. Nếu chưa có, tạo mới:
   ```sql
   CREATE DATABASE BLOCKCHAIN_CHUYENTIEN;
   ```

### Bước 8: Test Connection Bằng SSMS

1. Mở SSMS
2. Thử kết nối với:
   - Server name: `DESKTOP-CRFJV4A\SQL2022`
   - Authentication: **SQL Server Authentication**
   - Login: `sa`
   - Password: (mật khẩu của bạn)
3. Nếu kết nối thành công trong SSMS nhưng không kết nối được từ Python, có thể là vấn đề với ODBC Driver

### Bước 9: Kiểm Tra ODBC Driver

1. Mở **ODBC Data Source Administrator (64-bit)**
2. Vào tab **Drivers**
3. Tìm **ODBC Driver 17 for SQL Server**
4. Nếu không có, tải và cài đặt từ Microsoft

## 🔍 Test Connection

Sau khi sửa, chạy lại:

```bash
python test_db_connection_simple.py
```

Hoặc test trực tiếp trong Python:

```python
import pyodbc
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-CRFJV4A\\SQL2022;"
    "DATABASE=BLOCKCHAIN_CHUYENTIEN;"
    "UID=sa;"
    "PWD=12345;"
    "TrustServerCertificate=yes;"
)
conn = pyodbc.connect(conn_str)
print("✓ Connected!")
```

## ⚠️ Lưu Ý

- Backend vẫn có thể chạy được ngay cả khi không kết nối được database
- Các tính năng blockchain vẫn hoạt động bình thường
- Chỉ các tính năng liên quan đến database sẽ không hoạt động

## 🎯 Tóm Tắt Checklist

- [ ] SQL Server service đang chạy
- [ ] SQL Server Browser service đang chạy
- [ ] SQL Server cho phép remote connections
- [ ] SQL Server Authentication được enable
- [ ] Login 'sa' được enable
- [ ] Firewall cho phép port 1433, 1434
- [ ] Database 'BLOCKCHAIN_CHUYENTIEN' đã được tạo
- [ ] ODBC Driver 17 for SQL Server đã cài đặt
- [ ] Connection string trong .env đúng

