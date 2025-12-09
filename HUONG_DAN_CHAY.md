# Hướng Dẫn Chạy Chương Trình Ngân Hàng Blockchain

## 📋 Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- Node.js và npm (để chạy Ganache và Hardhat)
- SQL Server (2017 trở lên)
- SQL Server Management Studio (SSMS)
- Trình duyệt có MetaMask extension (Chrome, Edge, Firefox)

---

## 🔧 BƯỚC 1: Cài Đặt Python Dependencies

1. Mở Command Prompt hoặc PowerShell
2. Di chuyển đến thư mục dự án:
   ```bash
   cd D:\00.Code\Blockchain\NganHang
   ```

3. Cài đặt các thư viện Python:
   ```bash
   pip install -r requirements.txt
   ```

   **Lưu ý:** Nếu gặp lỗi với `pyodbc`, có thể cần cài đặt:
   - Trên Windows: Tải ODBC Driver 17 for SQL Server từ Microsoft
   - Hoặc cài qua: `pip install pyodbc`

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

### Cách 1: Cài đặt Ganache CLI

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

### Cách 2: Sử dụng Anvil (Foundry)

Nếu đã cài Foundry:
```bash
anvil --port 8545
```

### Kiểm tra Ganache đang chạy:
- Bạn sẽ thấy danh sách 10 accounts với private keys
- Server đang listen tại `127.0.0.1:8545`
- **GIỮ CỬA SỔ NÀY MỞ** trong suốt quá trình chạy ứng dụng

---

## 📝 BƯỚC 5: Cài Đặt Dependencies cho Smart Contract

1. Mở Command Prompt mới
2. Di chuyển đến thư mục contracts:
   ```bash
   cd D:\00.Code\Blockchain\NganHang\contracts
   ```

3. Cài đặt Node.js packages:
   ```bash
   npm install
   ```

   Lần đầu có thể mất vài phút để tải dependencies.

---

## 📦 BƯỚC 6: Compile và Deploy Smart Contract

1. Vẫn ở trong thư mục `contracts/`

2. Compile contract:
   ```bash
   npx hardhat compile
   ```

3. Deploy contract lên mạng local:
   ```bash
   npx hardhat run scripts/deploy.js --network localhost
   ```

4. **QUAN TRỌNG:** Sau khi deploy, bạn sẽ thấy:
   ```
   BankContract deployed to: 0x...
   Contract ABI: [...]
   ```

5. Copy **Contract Address** (0x...) và **ABI**

6. Cập nhật file `backend/.env`:
   - Dán địa chỉ vào `CONTRACT_ADDRESS=0x...`
   - Dán một private key từ Ganache vào `PRIVATE_KEY=...`

7. Cập nhật file `frontend/config.js`:
   ```javascript
   const CONFIG = {
       API_URL: 'http://localhost:5000/api',
       CONTRACT_ADDRESS: '0x...', // Dán địa chỉ contract ở đây
       CONTRACT_ABI: [...] // Dán ABI ở đây (mảng JSON)
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

1. Trong MetaMask, click icon account (góc trên bên phải)
2. Chọn **"Import Account"**
3. Copy một private key từ Ganache (Bước 4)
4. Dán vào và click **Import**
5. Bây giờ bạn có ETH test trong account này!

---

## 🖥️ BƯỚC 8: Khởi Động Backend Server

1. Mở Command Prompt mới
2. Di chuyển đến thư mục dự án:
   ```bash
   cd D:\00.Code\Blockchain\NganHang
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
   - Bạn sẽ thấy JSON response

---

## 🌐 BƯỚC 9: Mở Frontend

### Cách 1: Mở Trực Tiếp

1. Mở file `frontend/index.html` bằng trình duyệt
2. Hoặc double-click vào file `index.html`

### Cách 2: Dùng HTTP Server (Khuyến nghị)

1. Mở Command Prompt mới
2. Di chuyển đến thư mục frontend:
   ```bash
   cd D:\00.Code\Blockchain\NganHang\frontend
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
3. Click **"Tạo tài khoản"**
4. MetaMask sẽ yêu cầu xác nhận giao dịch
5. Click **"Confirm"** trong MetaMask
6. Đợi transaction được confirm

### 10.3. Nạp Tiền (Deposit)
1. Copy địa chỉ ví của bạn từ MetaMask
2. Trong Ganache, sử dụng account có nhiều ETH
3. Gửi ETH đến địa chỉ ví của bạn (có thể dùng Remix hoặc script khác)
4. Hoặc đơn giản: chuyển ETH giữa các accounts trong Ganache

### 10.4. Chuyển Tiền
1. Click tab **"Chuyển tiền"**
2. Chọn tài khoản nguồn
3. Nhập địa chỉ ví người nhận
4. Nhập số tiền (ETH)
5. Nhập mô tả (tùy chọn)
6. Click **"Chuyển tiền"**
7. Xác nhận trong MetaMask
8. Đợi transaction được confirm

### 10.5. Xem Lịch Sử
1. Click tab **"Lịch sử"**
2. Xem tất cả các giao dịch đã thực hiện

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

## ❗ Xử Lý Lỗi Thường Gặp

### Lỗi: "Cannot connect to database"
- ✅ Kiểm tra SQL Server đang chạy
- ✅ Kiểm tra thông tin trong `backend/.env`
- ✅ Kiểm tra firewall không chặn port SQL Server

### Lỗi: "Connection refused" khi kết nối blockchain
- ✅ Kiểm tra Ganache đang chạy (Bước 4)
- ✅ Kiểm tra port 8545 không bị chiếm bởi ứng dụng khác
- ✅ Kiểm tra `BLOCKCHAIN_NETWORK` trong `.env`

### Lỗi: "Contract not found"
- ✅ Đảm bảo đã deploy contract (Bước 6)
- ✅ Kiểm tra `CONTRACT_ADDRESS` trong `.env` và `frontend/config.js` đúng
- ✅ Đảm bảo `CONTRACT_ABI` trong `frontend/config.js` đầy đủ

### Lỗi: "MetaMask not found"
- ✅ Đảm bảo MetaMask extension đã được cài đặt
- ✅ Refresh trang web
- ✅ Thử trình duyệt khác

### Lỗi: "Insufficient funds"
- ✅ Đảm bảo account trong MetaMask có ETH
- ✅ Import account từ Ganache (account có nhiều ETH)

---

## 📊 Tóm Tắt Các Cửa Sổ Cần Mở

Khi chạy ứng dụng, bạn cần **GIỮ MỞ** các cửa sổ sau:

1. ✅ **Ganache** (Blockchain node) - Port 8545
2. ✅ **Backend Server** - Port 5000
3. ✅ **HTTP Server** (nếu dùng) - Port 8000
4. ✅ **Trình duyệt** với MetaMask

---

## 🎯 Checklist Trước Khi Chạy

- [ ] Python dependencies đã cài (`pip install -r requirements.txt`)
- [ ] SQL Server database đã tạo và chạy script schema.sql
- [ ] File `backend/.env` đã tạo và cấu hình đúng
- [ ] Ganache đang chạy trên port 8545
- [ ] Smart contract đã được compile và deploy
- [ ] `CONTRACT_ADDRESS` và `CONTRACT_ABI` đã cập nhật trong `frontend/config.js`
- [ ] MetaMask đã được cài đặt và cấu hình mạng local
- [ ] Backend server đang chạy
- [ ] Frontend đang mở trong trình duyệt

---

## 🎉 Hoàn Thành!

Nếu tất cả các bước trên đã hoàn thành, bạn có thể:
- Tạo tài khoản ngân hàng
- Thực hiện giao dịch chuyển tiền
- Xem lịch sử giao dịch
- Tất cả đều được lưu trên blockchain và database!

**Chúc bạn thành công!** 🚀

