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

**Cách 1: Ganache GUI (Phần mềm) - Khuyến nghị**
1. Tải Ganache từ: https://trufflesuite.com/ganache/
2. Mở ứng dụng → Click **"New Workspace"**
3. Cấu hình:
   - Port: `8545`
   - Network ID: `1337`
   - Click **"Save Workspace"**
4. Copy **PRIVATE KEY** của một account (click vào account → icon Key 🔑)

**Cách 2: Ganache CLI**
```bash
npm install -g ganache-cli
ganache-cli --port 8545
```
**Copy 1 private key** để dùng sau!

### ✅ Bước 5: Cài npm packages
```bash
npm install
```

### ✅ Bước 6: Compile và Deploy Contract với Truffle
```bash
truffle compile
truffle migrate --network localhost
```
**Copy Contract Address** từ output!

Sau khi compile, ABI sẽ có trong: `build/contracts/BankContract.json`

### ✅ Bước 7: Cập nhật Config
- `backend/.env`: Thêm `CONTRACT_ADDRESS` và `PRIVATE_KEY`
- `frontend/config.js`: 
  - Thêm `CONTRACT_ADDRESS` (copy từ output deploy)
  - Copy `CONTRACT_ABI` từ file `build/contracts/BankContract.json` (mở file, copy phần "abi")

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

## 📚 Xem Thêm

- **Hướng dẫn chi tiết:** Xem file **HUONG_DAN_CHAY_MOI.md** (hướng dẫn đầy đủ với Truffle)
- **Hướng dẫn cũ:** File **HUONG_DAN_CHAY.md** (đã cập nhật một phần)

