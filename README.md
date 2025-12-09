# Hệ thống Ngân hàng Blockchain

Hệ thống giao dịch ngân hàng trên nền tảng Web sử dụng blockchain và hợp đồng thông minh (Smart Contracts).

## Công nghệ sử dụng

- **Backend**: Python (Flask)
- **Database**: SQL Server
- **Blockchain**: Ethereum (Solidity)
- **Frontend**: HTML, CSS, JavaScript
- **Wallet**: MetaMask

## Cấu trúc dự án

```
NganHang/
├── database/
│   └── schema.sql              # Schema database SQL Server
├── contracts/
│   └── BankContract.sol        # Smart Contract
├── backend/
│   ├── app.py                  # Flask API server
│   ├── database.py             # Database models
│   ├── blockchain.py           # Blockchain interaction
│   └── config.py               # Configuration
├── frontend/
│   ├── index.html              # Giao diện web
│   ├── styles.css              # CSS styling
│   ├── app.js                  # JavaScript logic
│   └── config.js               # Frontend config
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

## Cài đặt

Xem file [SETUP.md](SETUP.md) để có hướng dẫn chi tiết từng bước.

### Tóm tắt nhanh:

1. **Cài đặt Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup SQL Server:**
   - Cài đặt SQL Server
   - Tạo database `BankingBlockchain`
   - Chạy script `database/schema.sql`

3. **Cấu hình môi trường:**
   - Tạo file `backend/.env` (xem `backend/.env.example`)

4. **Khởi động blockchain node:**
   ```bash
   ganache-cli --port 8545
   ```

5. **Deploy Smart Contract:**
   ```bash
   cd contracts
   npm install
   npx hardhat compile
   npx hardhat run scripts/deploy.js --network localhost
   ```

6. **Cập nhật contract address:**
   - Trong `backend/.env`: `CONTRACT_ADDRESS`
   - Trong `frontend/config.js`: `CONTRACT_ADDRESS` và `CONTRACT_ABI`

7. **Cài đặt MetaMask và kết nối với mạng local**

## Chạy ứng dụng

### 1. Khởi động blockchain node

```bash
ganache-cli
# hoặc
anvil
```

### 2. Khởi động backend server

```bash
cd backend
python app.py
```

Backend sẽ chạy tại: `http://localhost:5000`

### 3. Mở frontend

Mở file `frontend/index.html` trong trình duyệt hoặc dùng local server:

```bash
cd frontend
python -m http.server 8000
```

Truy cập: `http://localhost:8000`

## Sử dụng

1. **Kết nối MetaMask**: Click nút "Kết nối MetaMask" và chấp nhận kết nối
2. **Tạo tài khoản**: Vào tab "Tài khoản" và tạo tài khoản mới
3. **Nạp tiền**: Sử dụng MetaMask để gửi ETH đến địa chỉ ví của bạn
4. **Chuyển tiền**: Vào tab "Chuyển tiền" và điền thông tin
5. **Xem lịch sử**: Tab "Lịch sử" hiển thị tất cả giao dịch

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/users` - Tạo user mới
- `GET /api/users/<wallet_address>` - Lấy thông tin user
- `POST /api/accounts` - Tạo tài khoản mới
- `GET /api/accounts/<account_id>` - Lấy thông tin tài khoản
- `GET /api/accounts/user/<wallet_address>` - Lấy tài khoản theo ví
- `POST /api/transactions` - Tạo giao dịch
- `GET /api/transactions/<transaction_id>` - Lấy thông tin giao dịch
- `GET /api/transactions/account/<account_id>` - Lấy giao dịch theo tài khoản
- `GET /api/blockchain/balance/<wallet_address>` - Lấy số dư từ blockchain

## Lưu ý

- Đảm bảo blockchain node đang chạy trước khi start backend
- Private key trong `.env` chỉ dùng cho development, không commit vào git
- Cần compile và deploy smart contract trước khi sử dụng
- MetaMask cần được cấu hình để kết nối với mạng local

## License

MIT

