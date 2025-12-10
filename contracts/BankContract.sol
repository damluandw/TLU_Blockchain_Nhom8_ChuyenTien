// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title BankContract
 * @dev Smart Contract cho hệ thống giao dịch ngân hàng
 */
contract BankContract {
    
    // Cấu trúc tài khoản
    struct Account {
        address accountOwner;
        uint256 balance;
        bool exists;
        uint256 createdAt;
    }
    
    // Mapping từ địa chỉ ví đến tài khoản
    mapping(address => Account) public accounts;
    
    // Mapping từ số tài khoản đến địa chỉ ví
    mapping(string => address) public accountNumberToAddress;
    
    // Danh sách tất cả địa chỉ ví
    address[] public allAccounts;
    
    // Cấu trúc giao dịch để lưu vào blockchain
    struct TransactionRecord {
        address from;
        address to;
        uint256 amount;
        uint256 timestamp;
        string transactionHash;
        bool exists;
    }
    
    // Mapping từ transaction ID đến TransactionRecord
    mapping(uint256 => TransactionRecord) public transactions;
    
    // Mapping từ địa chỉ ví đến danh sách transaction IDs
    mapping(address => uint256[]) public userTransactions;
    
    // Tổng số giao dịch
    uint256 public totalTransactions;
    
    // Event cho các giao dịch
    event Deposit(address indexed account, uint256 amount, uint256 timestamp);
    event Withdraw(address indexed account, uint256 amount, uint256 timestamp);
    event Transfer(
        address indexed from,
        address indexed to,
        uint256 amount,
        string transactionHash,
        uint256 timestamp
    );
    event AccountCreated(address indexed account, string accountNumber, uint256 timestamp);
    
    // Owner của contract
    address public owner;
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier accountExists(address _account) {
        require(accounts[_account].exists, "Account does not exist");
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    /**
     * @dev Tạo tài khoản mới
     * @param _accountNumber Số tài khoản ngân hàng
     */
    function createAccount(string memory _accountNumber) public {
        require(!accounts[msg.sender].exists, "Account already exists");
        require(accountNumberToAddress[_accountNumber] == address(0), "Account number already in use");
        
        accounts[msg.sender] = Account({
            accountOwner: msg.sender,
            balance: 0,
            exists: true,
            createdAt: block.timestamp
        });
        
        accountNumberToAddress[_accountNumber] = msg.sender;
        allAccounts.push(msg.sender);
        
        emit AccountCreated(msg.sender, _accountNumber, block.timestamp);
    }
    
    /**
     * @dev Nạp tiền vào tài khoản
     */
    function deposit() public payable accountExists(msg.sender) {
        require(msg.value > 0, "Amount must be greater than 0");
        
        accounts[msg.sender].balance += msg.value;
        
        emit Deposit(msg.sender, msg.value, block.timestamp);
    }
    
    /**
     * @dev Rút tiền từ tài khoản
     * @param _amount Số tiền cần rút
     */
    function withdraw(uint256 _amount) public accountExists(msg.sender) {
        require(_amount > 0, "Amount must be greater than 0");
        require(accounts[msg.sender].balance >= _amount, "Insufficient balance");
        
        accounts[msg.sender].balance -= _amount;
        payable(msg.sender).transfer(_amount);
        
        emit Withdraw(msg.sender, _amount, block.timestamp);
    }
    
    /**
     * @dev Chuyển tiền giữa các tài khoản
     * @param _to Địa chỉ ví người nhận
     * @param _amount Số tiền chuyển
     * @param _transactionHash Hash giao dịch từ database
     */
    function transfer(
        address _to,
        uint256 _amount,
        string memory _transactionHash
    ) public accountExists(msg.sender) {
        require(_to != address(0), "Invalid recipient address");
        require(_amount > 0, "Amount must be greater than 0");
        require(accounts[msg.sender].balance >= _amount, "Insufficient balance");
        require(accounts[_to].exists, "Recipient account does not exist");
        
        accounts[msg.sender].balance -= _amount;
        accounts[_to].balance += _amount;
        
        // Lưu thông tin giao dịch vào blockchain
        uint256 transactionId = totalTransactions;
        transactions[transactionId] = TransactionRecord({
            from: msg.sender,
            to: _to,
            amount: _amount,
            timestamp: block.timestamp,
            transactionHash: _transactionHash,
            exists: true
        });
        
        // Thêm transaction ID vào danh sách của người chuyển và người nhận
        userTransactions[msg.sender].push(transactionId);
        userTransactions[_to].push(transactionId);
        
        totalTransactions++;
        
        emit Transfer(msg.sender, _to, _amount, _transactionHash, block.timestamp);
    }
    
    /**
     * @dev Lấy số dư tài khoản
     * @param _account Địa chỉ ví
     * @return balance Số dư tài khoản
     */
    function getBalance(address _account) public view returns (uint256 balance) {
        require(accounts[_account].exists, "Account does not exist");
        return accounts[_account].balance;
    }

    /**
     * @dev Kiểm tra tài khoản có tồn tại không
     * @param _account Địa chỉ ví
     * @return exists true nếu tài khoản tồn tại
     */
    function accountExist(address _account) public view returns (bool exists) {
        return accounts[_account].exists;
    }

    /**
     * @dev Lấy thông tin tài khoản
     * @param _account Địa chỉ ví
     * @return accountOwner Chủ tài khoản
     * @return balance Số dư tài khoản
     * @return exists Tài khoản có tồn tại hay không
     * @return createdAt Thời gian tạo tài khoản
     */
    function getAccountInfo(address _account) public view returns (
        address accountOwner,
        uint256 balance,
        bool exists,
        uint256 createdAt
    ) {
        require(accounts[_account].exists, "Account does not exist");
        Account memory acc = accounts[_account];
        return (acc.accountOwner, acc.balance, acc.exists, acc.createdAt);
    }

    /**
     * @dev Lấy tổng số tài khoản
     * @return totalAccounts Số lượng tài khoản
     */
    function getTotalAccounts() public view returns (uint256 totalAccounts) {
        return allAccounts.length;
    }

    /**
     * @dev Lấy địa chỉ từ số tài khoản
     * @param _accountNumber Số tài khoản
     * @return accountAddress Địa chỉ ví
     */
    function getAddressByAccountNumber(string memory _accountNumber) public view returns (address accountAddress) {
        return accountNumberToAddress[_accountNumber];
    }

    /**
     * @dev Lấy thông tin giao dịch theo ID
     * @param _transactionId ID của giao dịch
     * @return from Địa chỉ người chuyển
     * @return to Địa chỉ người nhận
     * @return amount Số tiền
     * @return timestamp Thời gian giao dịch
     * @return transactionHash Hash giao dịch
     */
    function getTransaction(uint256 _transactionId) public view returns (
        address from,
        address to,
        uint256 amount,
        uint256 timestamp,
        string memory transactionHash
    ) {
        require(transactions[_transactionId].exists, "Transaction does not exist");
        TransactionRecord memory tx = transactions[_transactionId];
        return (tx.from, tx.to, tx.amount, tx.timestamp, tx.transactionHash);
    }

    /**
     * @dev Lấy tổng số giao dịch của một địa chỉ ví
     * @param _account Địa chỉ ví
     * @return count Số lượng giao dịch
     */
    function getTransactionCount(address _account) public view returns (uint256 count) {
        return userTransactions[_account].length;
    }

    /**
     * @dev Lấy danh sách transaction IDs của một địa chỉ ví
     * @param _account Địa chỉ ví
     * @param _offset Vị trí bắt đầu
     * @param _limit Số lượng giao dịch cần lấy
     * @return transactionIds Mảng các transaction IDs
     */
    function getTransactionIds(address _account, uint256 _offset, uint256 _limit) public view returns (uint256[] memory transactionIds) {
        uint256[] memory allIds = userTransactions[_account];
        uint256 length = allIds.length;
        
        if (_offset >= length) {
            return new uint256[](0);
        }
        
        uint256 end = _offset + _limit;
        if (end > length) {
            end = length;
        }
        
        uint256 resultLength = end - _offset;
        uint256[] memory result = new uint256[](resultLength);
        
        for (uint256 i = 0; i < resultLength; i++) {
            result[i] = allIds[_offset + i];
        }
        
        return result;
    }

    /**
     * @dev Lấy tổng số giao dịch trong hệ thống
     * @return total Số lượng giao dịch tổng cộng
     */
    function getTotalTransactions() public view returns (uint256 total) {
        return totalTransactions;
    }
}