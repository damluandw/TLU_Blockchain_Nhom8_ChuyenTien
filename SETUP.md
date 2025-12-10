# Hướng dẫn Setup Dự án Ngân hàng Blockchain

## Bước 1: Cài đặt Python và Dependencies

```bash
# Cài đặt Python packages
pip install -r requirements.txt
```

## Bước 2: Setup SQL Server

1. Cài đặt SQL Server và SQL Server Management Studio
2. Tạo database mới:
   ```sql
   CREATE DATABASE BankingBlockchain;
   ```
3. Chạy script tạo bảng:
   - Mở file `database/schema.sql`
   - Chạy toàn bộ script trong SSMS

4. Cài đặt ODBC Driver 17 for SQL Server (nếu chưa có)

## Bước 3: Tạo file .env

Tạo file `backend/.env` với nội dung:

```env
SQL_SERVER=localhost
SQL_DATABASE=BankingBlockchain
SQL_USERNAME=sa
SQL_PASSWORD=your_password
BLOCKCHAIN_NETWORK=http://127.0.0.1:8545
CONTRACT_ADDRESS=
PRIVATE_KEY=
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
```

## Bước 4: Setup Blockchain Node

### Option A: Ganache GUI (Phần mềm Desktop) - **KHUYẾN NGHỊ**

1. **Tải và cài đặt:**
   - Truy cập: https://trufflesuite.com/ganache/
   - Tải Ganache (Desktop App)
   - Cài đặt phần mềm

2. **Khởi động:**
   - Mở ứng dụng Ganache
   - Click **"New Workspace"** hoặc **"Quickstart"**
   - Cấu hình:
     - Port: `8545`
     - Network ID: `1337`
   - Click **"Save Workspace"** hoặc **"Start"**

3. **Lấy Private Key:**
   - Click vào một account trong danh sách
   - Click icon **Key** (🔑) để xem private key
   - Copy private key để dùng cho `PRIVATE_KEY` trong `.env`

### Option B: Ganache CLI

```bash
npm install -g ganache-cli
ganache-cli --port 8545
```

### Option C: Anvil (Foundry)

```bash
anvil --port 8545
```

### Option D: Truffle Develop (Built-in)

```bash
truffle develop
```

## Bước 5: Deploy Smart Contract với Truffle

### Cài đặt Truffle:

```bash
npm install
```

### Compile và Deploy:

```bash
# Compile contracts
truffle compile

# Deploy lên mạng localhost
truffle migrate --network localhost

# Hoặc dùng npm scripts
npm run compile
npm run migrate:local
```

Sau khi deploy:
- Copy địa chỉ contract từ output và dán vào `backend/.env` (CONTRACT_ADDRESS)
- Mở file `build/contracts/BankContract.json`, copy phần `"abi"` và dán vào `frontend/config.js` (CONTRACT_ABI)

### Với Remix IDE:

1. Truy cập https://remix.ethereum.org
2. Tạo file mới và copy nội dung từ `contracts/BankContract.sol`
3. Compile contract
4. Deploy lên mạng local (Ganache/Anvil)
5. Copy địa chỉ contract và ABI

## Bước 6: Cấu hình MetaMask

1. Cài đặt MetaMask extension trên trình duyệt
2. Tạo hoặc import account
3. Thêm mạng custom:
   - Network Name: Localhost 8545
   - RPC URL: http://127.0.0.1:8545
   - Chain ID: 1337 (hoặc chain ID từ Ganache)
   - Currency Symbol: ETH
4. Import account từ Ganache để có ETH test

## Bước 7: Khởi động Backend

```bash
# Windows
start_backend.bat

# Linux/Mac
chmod +x start_backend.sh
./start_backend.sh

# Hoặc
cd backend
python app.py
```

Backend sẽ chạy tại: `http://localhost:5000`

## Bước 8: Mở Frontend

### Option A: Mở trực tiếp
- Mở file `frontend/index.html` trong trình duyệt

### Option B: Dùng HTTP Server

```bash
cd frontend
python -m http.server 8000
```

Truy cập: `http://localhost:8000`

## Bước 9: Cập nhật Contract Address trong Frontend

Mở `frontend/config.js` và cập nhật:
```javascript
const CONFIG = {
    API_URL: 'http://localhost:5000/api',
    CONTRACT_ADDRESS: '0x...', // Địa chỉ contract đã deploy
    CONTRACT_ABI: [...] // ABI từ contract
};
```

## Kiểm tra hoạt động

1. Mở trình duyệt và truy cập frontend
2. Click "Kết nối MetaMask"
3. Chấp nhận kết nối trong MetaMask
4. Tạo tài khoản mới
5. Thử chuyển tiền

## Troubleshooting

### Lỗi kết nối database:
- Kiểm tra SQL Server đang chạy
- Kiểm tra thông tin trong `.env`
- Kiểm tra ODBC Driver đã cài đặt

### Lỗi kết nối blockchain:
- Đảm bảo Ganache/Anvil đang chạy
- Kiểm tra `BLOCKCHAIN_NETWORK` trong `.env`
- Kiểm tra contract đã được deploy

### MetaMask không kết nối:
- Kiểm tra MetaMask đã cài đặt
- Kiểm tra mạng local đã được thêm vào MetaMask
- Đảm bảo blockchain node đang chạy

### Lỗi CORS:
- Backend đã có CORS enabled
- Nếu vẫn lỗi, kiểm tra port của backend

## Lưu ý bảo mật

- ⚠️ Không commit file `.env` vào git
- ⚠️ Private key chỉ dùng cho development
- ⚠️ Đổi SECRET_KEY trước khi deploy production
- ⚠️ Sử dụng HTTPS trong production

