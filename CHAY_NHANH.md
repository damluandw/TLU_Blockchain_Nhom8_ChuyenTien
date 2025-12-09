# 🚀 Hướng Dẫn Chạy Nhanh

## Tóm Tắt 10 Bước

### ✅ Bước 1: Cài Python packages
```bash
pip install -r requirements.txt
```

### ✅ Bước 2: Setup SQL Server
- Mở SSMS → Tạo database `BankingBlockchain`
- Chạy file `database/schema.sql`

### ✅ Bước 3: Tạo file .env
Tạo `backend/.env`:
```env
SQL_SERVER=localhost
SQL_DATABASE=BankingBlockchain
SQL_USERNAME=sa
SQL_PASSWORD=mật_khẩu_của_bạn
BLOCKCHAIN_NETWORK=http://127.0.0.1:8545
CONTRACT_ADDRESS=
PRIVATE_KEY=
SECRET_KEY=secret-key-123
DEBUG=True
```

### ✅ Bước 4: Chạy Ganache
```bash
ganache-cli --port 8545
```
**Copy 1 private key** để dùng sau!

### ✅ Bước 5: Cài npm packages
```bash
cd contracts
npm install
```

### ✅ Bước 6: Deploy Contract
```bash
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```
**Copy Contract Address và ABI** từ output!

### ✅ Bước 7: Cập nhật Config
- `backend/.env`: Thêm `CONTRACT_ADDRESS` và `PRIVATE_KEY`
- `frontend/config.js`: Thêm `CONTRACT_ADDRESS` và `CONTRACT_ABI`

### ✅ Bước 8: Setup MetaMask
- Thêm mạng: Localhost 8545 (RPC: http://127.0.0.1:8545, ChainID: 1337)
- Import account từ Ganache

### ✅ Bước 9: Chạy Backend
```bash
python backend/app.py
```

### ✅ Bước 10: Mở Frontend
```bash
cd frontend
python -m http.server 8000
```
Truy cập: http://localhost:8000

---

## ⚠️ Lưu Ý Quan Trọng

1. **GIỮ MỞ** 3 cửa sổ:
   - Ganache (port 8545)
   - Backend server (port 5000)
   - Frontend server (port 8000)

2. **Thứ tự chạy:**
   - Ganache → Deploy Contract → Backend → Frontend

3. **Kiểm tra:**
   ```bash
   python test_connection.py
   ```

---

Xem chi tiết đầy đủ trong file **HUONG_DAN_CHAY.md**

