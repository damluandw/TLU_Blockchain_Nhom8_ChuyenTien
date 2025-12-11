# 🚀 Hướng Dẫn Chạy Chương Trình Ngân Hàng Blockchain (Truffle)

## 📋 Yêu Cầu Hệ Thống

- **Python 3.8+** (để chạy backend)
- **Node.js và npm** (để chạy Ganache và Truffle)
- **SQL Server 2017+** (database)
- **SQL Server Management Studio (SSMS)** (quản lý database)
- **Trình duyệt có MetaMask** (Chrome, Edge, Firefox)

---

## 🔧 BƯỚC 1: Cài Đặt Python Dependencies

1. Mở Command Prompt hoặc PowerShell
2. Di chuyển đến thư mục dự án:
   ```bash
   cd D:\00.Code\Blockchain\TLU_Blockchain_Nhom8_ChuyenTien
   ```

3. Cài đặt các thư viện Python:
   ```bash
   pip install -r requirements.txt
   ```

   **Lưu ý:** Nếu gặp lỗi với `pyodbc`, cần cài đặt:
   - Trên Windows: Tải **ODBC Driver 17 for SQL Server** từ Microsoft
   - Hoặc: `pip install pyodbc`

---

## 🗄️ BƯỚC 2: Setup SQL Server Database

### 2.1. Tạo Database

1. Mở **SQL Server Management Studio (SSMS)**
2. Kết nối đến SQL Server của bạn
3. Click chuột phải vào **Databases** → **New Database**
4. Đặt tên: `BankingBlockchain`
5. Click **OK**

### 2.2. Tạo Các Bảng

1. Trong SSMS, chọn database `BankingBlockchain`
2. Mở file `database/schema.sql`
3. Copy toàn bộ nội dung
4. Paste vào cửa sổ Query trong SSMS
5. Click **Execute** (F5) để chạy script
6. Kiểm tra các bảng đã được tạo trong Object Explorer

---

## ⚙️ BƯỚC 3: Cấu Hình File .env

1. Tạo file `.env` trong thư mục `backend/`
2. Copy nội dung mẫu sau và điền thông tin của bạn:

```env
# SQL Server Configuration
SQL_SERVER=localhost
SQL_DATABASE=BankingBlockchain
SQL_USERNAME=sa
SQL_PASSWORD=MatKhauCuaBan

# Blockchain Configuration
BLOCKCHAIN_NETWORK=http://127.0.0.1:8545
CONTRACT_ADDRESS=
PRIVATE_KEY=

# Flask Configuration
SECRET_KEY=my-secret-key-change-in-production-12345
DEBUG=True
```

**Lưu ý:**
- `SQL_PASSWORD`: Điền mật khẩu SQL Server của bạn
- `CONTRACT_ADDRESS`: Sẽ điền sau khi deploy contract (Bước 6)
- `PRIVATE_KEY`: Private key từ Ganache (sẽ có sau Bước 4)

---

## 🚀 BƯỚC 4: Khởi Động Blockchain Node (Ganache)

### Cách 1: Sử dụng Ganache GUI (Phần mềm Desktop) - **KHUYẾN NGHỊ**

#### 4.1. Tải và Cài Đặt Ganache GUI

1. Truy cập trang web: https://trufflesuite.com/ganache/
2. Tải **Ganache** (phiên bản GUI - Desktop App)
3. Cài đặt phần mềm:
   - Windows: Chạy file `.exe` đã tải
   - Mac: Mở file `.dmg` và kéo vào Applications
   - Linux: Giải nén và chạy file thực thi

#### 4.2. Khởi Động Ganache GUI

1. Mở ứng dụng **Ganache** từ menu Start (Windows) hoặc Applications (Mac)
2. Click vào **"New Workspace"** (hoặc **"Quickstart"** nếu lần đầu)
3. Cấu hình workspace:
   - **Workspace Name:** Đặt tên (ví dụ: "Banking Blockchain")
   - **Server** tab:
     - **Hostname:** `127.0.0.1`
     - **Port:** `8545` (mặc định)
     - **Network ID:** `1337` (hoặc để mặc định)
   - **Accounts & Keys** tab:
     - **Number of accounts:** 10 (mặc định)
     - **Default balance:** 100 ETH (mặc định)
4. Click **"Save Workspace"** hoặc **"Start"**

#### 4.3. Lấy Thông Tin Từ Ganache GUI

1. Sau khi khởi động, bạn sẽ thấy giao diện với:
   - **ACCOUNTS** tab: Danh sách các accounts với địa chỉ và số dư
   - **BLOCKS** tab: Các blocks đã được tạo
   - **TRANSACTIONS** tab: Các giao dịch

2. **Lấy Private Key:**
   - Click vào một account trong danh sách **ACCOUNTS**
   - Click vào icon **"Key"** (🔑) hoặc click vào account để xem chi tiết
   - Copy **PRIVATE KEY** (bắt đầu bằng `0x...`)
   - Lưu lại để dùng cho `PRIVATE_KEY` trong `backend/.env`

3. **Lấy Account Address:**
   - Copy **ADDRESS** của account (bắt đầu bằng `0x...`)
   - Dùng để import vào MetaMask

#### 4.4. Kiểm Tra Ganache Đang Chạy

- ✅ Ứng dụng Ganache GUI đang mở và hiển thị workspace
- ✅ Có 10 accounts với số dư 100 ETH mỗi account
- ✅ Server đang chạy tại `127.0.0.1:8545` (hiển thị ở góc trên)
- ✅ **GIỮ ỨNG DỤNG GANACHE MỞ** trong suốt quá trình chạy ứng dụng

---

### Cách 2: Sử dụng Ganache CLI (Command Line)

Nếu bạn muốn dùng command line thay vì GUI:

1. Mở Command Prompt mới
2. Cài đặt Ganache CLI (nếu chưa có):
   ```bash
   npm install -g ganache-cli
   ```

3. Khởi động Ganache:
   ```bash
   ganache-cli --port 8545
   ```

4. **QUAN TRỌNG:** Ghi lại các thông tin hiển thị:
   - Private keys của các accounts
   - Copy một private key để dùng cho `PRIVATE_KEY` trong `.env`

5. **GIỮ CỬA SỔ NÀY MỞ** trong suốt quá trình chạy ứng dụng

---

## 📝 BƯỚC 5: Cài Đặt Dependencies cho Truffle

1. Mở Command Prompt mới
2. Di chuyển đến thư mục dự án:
   ```bash
   cd D:\00.Code\Blockchain\TLU_Blockchain_Nhom8_ChuyenTien
   ```

3. Cài đặt Node.js packages (Truffle):
   ```bash
   npm install
   ```

   Lần đầu có thể mất vài phút để tải dependencies.

---

## 📦 BƯỚC 6: Compile và Deploy Smart Contract với Truffle

1. Vẫn ở trong thư mục dự án

2. **Compile contract:**
   ```bash
   truffle compile
   ```
   
   Hoặc dùng npm script:
   ```bash
   npm run compile
   ```

   Sau khi compile, bạn sẽ thấy thư mục `build/contracts/` được tạo với file `BankContract.json`

3. **Deploy contract lên mạng local:**
   ```bash
   truffle migrate --network localhost
   ```
   
   Hoặc dùng npm script:
   ```bash
   npm run migrate:local
   ```

4. **QUAN TRỌNG:** Sau khi deploy, bạn sẽ thấy:
   ```
   Deploying 'BankContract'
   -------------------------
   > transaction hash:    0x...
   > contract address:    0x1234567890abcdef...
   > block number:        1
   > block timestamp:     ...
   > account:             0x...
   > balance:             ...
   > gas used:            ...
   > gas price:           ...
   > deployment status:   succeeded
   ```

5. **Copy Contract Address** (0x...)

6. **Lấy ABI từ file compiled:**
   - Mở file `build/contracts/BankContract.json`
   - Tìm phần `"abi"` (là một mảng JSON bắt đầu bằng `[`)
   - Copy toàn bộ mảng ABI

7. **Cập nhật file `backend/.env`:**
   ```env
   CONTRACT_ADDRESS=0x1234567890abcdef...  # Dán địa chỉ contract ở đây
   PRIVATE_KEY=0x...                       # Dán một private key từ Ganache
   ```

8. **Cập nhật file `frontend/config.js`:**
   ```javascript
   const CONFIG = {
       API_URL: 'http://localhost:5000/api',
       CONTRACT_ADDRESS: '0x1234567890abcdef...', // Dán địa chỉ contract
       CONTRACT_ABI: [                          // Dán ABI từ build/contracts/BankContract.json
           {
               "inputs": [],
               "stateMutability": "nonpayable",
               "type": "constructor"
           },
           // ... phần còn lại của ABI
       ]
   };
   ```

---

## 🔌 BƯỚC 7: Cấu Hình MetaMask

### 7.1. Cài Đặt MetaMask
- Cài extension MetaMask trên trình duyệt (Chrome, Edge, Firefox)
- Tạo wallet hoặc import wallet mới

### 7.2. Thêm Mạng Local

1. Mở MetaMask
2. Click vào network dropdown (phía trên)
3. Click **"Add Network"** → **"Add a network manually"**
4. Điền thông tin:
   - **Network Name:** Localhost 8545
   - **New RPC URL:** http://127.0.0.1:8545
   - **Chain ID:** 1337
   - **Currency Symbol:** ETH
   - **Block Explorer URL:** (để trống)

5. Click **Save**

### 7.3. Import Account từ Ganache

**Nếu dùng Ganache GUI:**
1. Trong Ganache GUI, click vào một account trong danh sách **ACCOUNTS**
2. Click icon **Key** (🔑) để xem private key
3. Copy private key
4. Trong MetaMask, click icon account (góc trên bên phải)
5. Chọn **"Import Account"**
6. Dán private key và click **Import**
7. Bây giờ bạn có ETH test trong account này!

**Nếu dùng Ganache CLI:**
1. Copy một private key từ cửa sổ Command Prompt (Bước 4)
2. Trong MetaMask, click icon account (góc trên bên phải)
3. Chọn **"Import Account"**
4. Dán private key và click **Import**
5. Bây giờ bạn có ETH test trong account này!

---

## 🖥️ BƯỚC 8: Khởi Động Backend Server

1. Mở Command Prompt mới
2. Di chuyển đến thư mục dự án:
   ```bash
   cd D:\00.Code\Blockchain\TLU_Blockchain_Nhom8_ChuyenTien
   ```

3. Chạy backend:
   ```bash
   python backend/app.py
   ```
   
   Hoặc dùng script:
   ```bash
   start_backend.bat
   ```

4. Bạn sẽ thấy:
   ```
   * Running on http://0.0.0.0:5000
   ```

5. **GIỮ CỬA SỔ NÀY MỞ**

6. Kiểm tra backend hoạt động:
   - Mở trình duyệt
   - Truy cập: `http://localhost:5000/api/health`
   - Bạn sẽ thấy JSON response:
     ```json
     {
       "status": "healthy",
       "blockchain_connected": true
     }
     ```

---

## 🌐 BƯỚC 9: Mở Frontend

### Cách 1: Mở Trực Tiếp

1. Mở file `frontend/index.html` bằng trình duyệt
2. Hoặc double-click vào file `index.html`

### Cách 2: Dùng HTTP Server (Khuyến nghị)

1. Mở Command Prompt mới
2. Di chuyển đến thư mục frontend:
   ```bash
   cd D:\00.Code\Blockchain\TLU_Blockchain_Nhom8_ChuyenTien\frontend
   ```

3. Chạy HTTP server:
   ```bash
   python -m http.server 8000
   ```

4. Mở trình duyệt và truy cập:
   ```
   http://localhost:8000
   ```

---

## ✅ BƯỚC 10: Sử Dụng Ứng Dụng

### 10.1. Kết Nối Ví
1. Trên trang web, click nút **"Kết nối MetaMask"**
2. MetaMask sẽ hiện popup yêu cầu kết nối
3. Chọn account và click **"Connect"**
4. Địa chỉ ví sẽ hiển thị trên trang web

### 10.2. Tạo Tài Khoản Ngân Hàng
1. Click tab **"Tài khoản"**
2. Chọn loại tài khoản
3. Nhập số tài khoản (hoặc để hệ thống tự tạo)
4. Click **"Tạo tài khoản"**
5. MetaMask sẽ yêu cầu xác nhận giao dịch
6. Click **"Confirm"** trong MetaMask
7. Đợi transaction được confirm

### 10.3. Nạp Tiền (Deposit)
1. Click tab **"Nạp tiền"** hoặc **"Tài khoản"**
2. Chọn tài khoản
3. Nhập số tiền (ETH)
4. Click **"Nạp tiền"**
5. Xác nhận trong MetaMask
6. Đợi transaction được confirm

### 10.4. Chuyển Tiền
1. Click tab **"Chuyển tiền"**
2. Chọn tài khoản nguồn
3. Nhập địa chỉ ví người nhận
4. Nhập số tiền (ETH)
5. Nhập mô tả (tùy chọn)
6. Click **"Chuyển tiền"**
7. Xác nhận trong MetaMask
8. Đợi transaction được confirm

   **Lưu ý:** Giao dịch sẽ được lưu vào blockchain với đầy đủ thông tin:
   - Người chuyển
   - Người nhận
   - Số tiền
   - Thời gian

### 10.5. Xem Lịch Sử
1. Click tab **"Lịch sử"**
2. Xem tất cả các giao dịch đã thực hiện
3. Có thể xem lịch sử từ database hoặc từ blockchain

---

## 🔍 Kiểm Tra Kết Nối

Chạy script test:
```bash
python test_connection.py
```

Script này sẽ kiểm tra:
- ✅ Kết nối database
- ✅ Kết nối blockchain
- ✅ Contract đã được load chưa

---

## 📊 API Endpoints Mới

### Blockchain Transactions API:

1. **Lấy lịch sử giao dịch từ blockchain:**
   ```bash
   GET /api/blockchain/transactions/<wallet_address>?offset=0&limit=50
   ```

2. **Lấy thông tin một giao dịch cụ thể:**
   ```bash
   GET /api/blockchain/transaction/<transaction_id>
   ```

3. **Lấy tổng số giao dịch:**
   ```bash
   GET /api/blockchain/transactions/total
   ```

---

## ❗ Xử Lý Lỗi Thường Gặp

### Lỗi: "Cannot connect to database"
- ✅ Kiểm tra SQL Server đang chạy
- ✅ Kiểm tra thông tin trong `backend/.env`
- ✅ Kiểm tra firewall không chặn port SQL Server

### Lỗi: "Connection refused" khi kết nối blockchain
- ✅ Kiểm tra Ganache GUI đang mở và workspace đã được start (Bước 4)
- ✅ Hoặc kiểm tra Ganache CLI đang chạy trong Command Prompt
- ✅ Kiểm tra port 8545 không bị chiếm bởi ứng dụng khác
- ✅ Kiểm tra `BLOCKCHAIN_NETWORK` trong `.env` là `http://127.0.0.1:8545`
- ✅ Trong Ganache GUI, kiểm tra server đang chạy tại đúng port (hiển thị ở góc trên)

### Lỗi: "Contract not found"
- ✅ Đảm bảo đã deploy contract (Bước 6)
- ✅ Kiểm tra `CONTRACT_ADDRESS` trong `.env` và `frontend/config.js` đúng
- ✅ Đảm bảo `CONTRACT_ABI` trong `frontend/config.js` đầy đủ
- ✅ Kiểm tra file `build/contracts/BankContract.json` tồn tại

### Lỗi: "Truffle command not found"
- ✅ Đảm bảo đã chạy `npm install`
- ✅ Thử: `npx truffle compile` thay vì `truffle compile`

### Lỗi: "MetaMask not found"
- ✅ Đảm bảo MetaMask extension đã được cài đặt
- ✅ Refresh trang web
- ✅ Thử trình duyệt khác

### Lỗi: "Insufficient funds"
- ✅ Đảm bảo account trong MetaMask có ETH
- ✅ Import account từ Ganache (account có nhiều ETH)

### Lỗi khi migrate: "Network localhost not found"
- ✅ Kiểm tra `truffle-config.js` có cấu hình network `localhost`
- ✅ Đảm bảo Ganache đang chạy trên port 8545

---

## 📊 Tóm Tắt Các Cửa Sổ Cần Mở

Khi chạy ứng dụng, bạn cần **GIỮ MỞ** các cửa sổ sau:

1. ✅ **Ganache GUI** (Ứng dụng desktop) hoặc **Ganache CLI** (Command Prompt) - Port 8545
2. ✅ **Backend Server** (Command Prompt) - Port 5000
3. ✅ **HTTP Server** (Command Prompt, nếu dùng) - Port 8000
4. ✅ **Trình duyệt** với MetaMask

---

## 🎯 Checklist Trước Khi Chạy

- [ ] Python dependencies đã cài (`pip install -r requirements.txt`)
- [ ] SQL Server database đã tạo và chạy script schema.sql
- [ ] File `backend/.env` đã tạo và cấu hình đúng
- [ ] Ganache GUI đang mở và workspace đã được start (hoặc Ganache CLI đang chạy) trên port 8545
- [ ] Truffle dependencies đã cài (`npm install`)
- [ ] Smart contract đã được compile (`truffle compile`)
- [ ] Smart contract đã được deploy (`truffle migrate --network localhost`)
- [ ] `CONTRACT_ADDRESS` đã cập nhật trong `backend/.env`
- [ ] `CONTRACT_ADDRESS` và `CONTRACT_ABI` đã cập nhật trong `frontend/config.js`
- [ ] MetaMask đã được cài đặt và cấu hình mạng local
- [ ] Backend server đang chạy
- [ ] Frontend đang mở trong trình duyệt

---

## 🎉 Hoàn Thành!

Nếu tất cả các bước trên đã hoàn thành, bạn có thể:
- ✅ Tạo tài khoản ngân hàng
- ✅ Thực hiện giao dịch chuyển tiền
- ✅ Xem lịch sử giao dịch
- ✅ **Tất cả giao dịch được lưu vào blockchain với đầy đủ thông tin:**
  - Người chuyển
  - Người nhận
  - Số tiền
  - Thời gian
  - Transaction hash

**Chúc bạn thành công!** 🚀

---

## 📝 Lưu Ý Quan Trọng

1. **Sau khi sửa smart contract**, cần:
   - Compile lại: `truffle compile`
   - Migrate lại: `truffle migrate --network localhost` (hoặc `--reset` để reset)
   - Cập nhật ABI trong `frontend/config.js` từ `build/contracts/BankContract.json`

2. **Khi deploy lại contract**, địa chỉ contract sẽ thay đổi, cần cập nhật:
   - `backend/.env`: `CONTRACT_ADDRESS`
   - `frontend/config.js`: `CONTRACT_ADDRESS` và `CONTRACT_ABI`

3. **Giao dịch được lưu vào blockchain** khi gọi hàm `transfer()`, không cần thao tác thêm.

