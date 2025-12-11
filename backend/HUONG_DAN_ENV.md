# 📝 Hướng Dẫn Cấu Hình File .env

## Bước 1: Tạo File .env

1. Vào thư mục `backend/`
2. Tạo file mới tên `.env` (không có phần mở rộng)
3. Copy nội dung từ file `backend/.env.example` và điền thông tin của bạn

## Bước 2: Cấu Hình SQL Server

### 2.1. Kiểm Tra SQL Server

- Đảm bảo SQL Server đang chạy
- Mở SQL Server Management Studio (SSMS) để kiểm tra

### 2.2. Tạo Database

1. Mở SSMS
2. Kết nối đến SQL Server
3. Click chuột phải vào **Databases** → **New Database**
4. Đặt tên: `BankingBlockchain`
5. Click **OK**

### 2.3. Chạy Script Tạo Bảng

1. Trong SSMS, chọn database `BankingBlockchain`
2. Mở file `database/schema.sql`
3. Copy toàn bộ nội dung
4. Paste vào cửa sổ Query
5. Click **Execute** (F5)

### 2.4. Điền Thông Tin Đăng Nhập

Trong file `.env`, điền:

```env
SQL_SERVER=localhost
SQL_DATABASE=BankingBlockchain
SQL_USERNAME=sa
SQL_PASSWORD=mật_khẩu_của_bạn
```

**Lưu ý:**
- Nếu SQL Server dùng Windows Authentication, có thể cần sửa connection string trong `config.py`
- Nếu không biết mật khẩu `sa`, có thể:
  - Reset password trong SSMS: Security → Logins → sa → Properties → Set Password
  - Hoặc tạo user mới với quyền db_owner

## Bước 3: Cấu Hình Blockchain

### 3.1. Khởi Động Ganache

**Cách 1: Ganache GUI (Khuyến nghị)**
1. Mở ứng dụng Ganache
2. Click **"New Workspace"**
3. Cấu hình:
   - Port: `8545`
   - Network ID: `1337`
4. Click **"Save Workspace"**

**Cách 2: Ganache CLI**
```bash
ganache-cli --port 8545
```

### 3.2. Lấy Private Key

**Từ Ganache GUI:**
1. Click vào một account trong danh sách
2. Click icon **Key** (🔑)
3. Copy private key

**Từ Ganache CLI:**
- Copy một private key từ danh sách hiển thị

### 3.3. Deploy Contract và Lấy Contract Address

```bash
# Compile contract
truffle compile

# Deploy contract
truffle migrate --network localhost
```

Sau khi deploy, copy **Contract Address** từ output.

### 3.4. Điền Thông Tin Blockchain

Trong file `.env`:

```env
BLOCKCHAIN_NETWORK=http://127.0.0.1:8545
CONTRACT_ADDRESS=0x1234567890abcdef...  # Dán địa chỉ contract ở đây
PRIVATE_KEY=0xabcdef1234567890...       # Dán private key từ Ganache
```

## Bước 4: Cấu Hình Flask

### 4.1. Secret Key

Tạo một secret key ngẫu nhiên mạnh:

```python
import secrets
print(secrets.token_hex(32))
```

Hoặc dùng một chuỗi ngẫu nhiên bất kỳ (ít nhất 32 ký tự).

### 4.2. Debug Mode

- `DEBUG=True`: Bật debug (hiển thị lỗi chi tiết, tự reload khi code thay đổi)
- `DEBUG=False`: Tắt debug (dùng cho production)

## File .env Hoàn Chỉnh Mẫu

```env
# SQL Server
SQL_SERVER=localhost
SQL_DATABASE=BankingBlockchain
SQL_USERNAME=sa
SQL_PASSWORD=MyPassword123

# Blockchain
BLOCKCHAIN_NETWORK=http://127.0.0.1:8545
CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3
PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80

# Flask
SECRET_KEY=my-super-secret-key-change-in-production-1234567890abcdef
DEBUG=True
```

## Kiểm Tra Cấu Hình

Sau khi tạo file `.env`, chạy backend:

```bash
python backend/app.py
```

Kiểm tra health endpoint:

```bash
curl http://localhost:5000/api/health
```

Hoặc mở trình duyệt: `http://localhost:5000/api/health`

Bạn sẽ thấy:
```json
{
  "status": "healthy",
  "blockchain_connected": true
}
```

## ⚠️ Lưu Ý Bảo Mật

1. **KHÔNG commit file `.env` vào git** (đã có trong .gitignore)
2. **KHÔNG chia sẻ private key** với ai
3. **Đổi SECRET_KEY** trước khi deploy production
4. **Đổi SQL_PASSWORD** thành mật khẩu mạnh
5. File `.env.example` có thể commit (không chứa thông tin nhạy cảm)

## Xử Lý Lỗi

### Lỗi: "Login failed for user 'sa'"
- Kiểm tra SQL Server đang chạy
- Kiểm tra username/password trong `.env` đúng
- Thử reset password `sa` trong SSMS

### Lỗi: "Cannot connect to blockchain"
- Kiểm tra Ganache đang chạy
- Kiểm tra `BLOCKCHAIN_NETWORK` trong `.env` đúng
- Kiểm tra port 8545 không bị chiếm

### Lỗi: "Contract not found"
- Đảm bảo đã deploy contract
- Kiểm tra `CONTRACT_ADDRESS` trong `.env` đúng
- Kiểm tra contract address có trong Ganache (tab Contracts)

## Hỗ Trợ

Nếu gặp vấn đề, kiểm tra:
1. File `.env` có trong thư mục `backend/` không?
2. Tất cả các giá trị đã được điền chưa?
3. SQL Server và Ganache đang chạy chưa?
4. Database `BankingBlockchain` đã được tạo chưa?

