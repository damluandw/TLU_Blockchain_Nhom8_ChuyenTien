# Hướng Dẫn Tạo File .env

## Tạo File .env

1. Tạo file `.env` trong thư mục `backend/`
2. Copy nội dung sau và điền thông tin của bạn:

```env
# SQL Server Configuration
SQL_SERVER=localhost
SQL_DATABASE=BankingBlockchain
SQL_USERNAME=sa
SQL_PASSWORD=mật_khẩu_của_bạn

# Blockchain Configuration
BLOCKCHAIN_NETWORK=http://127.0.0.1:8545
CONTRACT_ADDRESS=
PRIVATE_KEY=

# Flask Configuration
SECRET_KEY=my-secret-key-change-in-production-12345
DEBUG=True
```

## Lưu Ý

- Thay `mật_khẩu_của_bạn` bằng mật khẩu SQL Server thực tế
- Nếu dùng Windows Authentication, có thể cần đổi connection string trong `config.py`
- File `.env` không được commit vào git (đã có trong .gitignore)

## Kiểm Tra

Sau khi tạo file `.env`, chạy lại backend:
```bash
python backend/app.py
```

Kiểm tra health endpoint:
```bash
curl http://localhost:5000/api/health
```

Bạn sẽ thấy `"database_connected": true` nếu kết nối thành công.

