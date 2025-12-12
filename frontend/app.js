// Main Application JavaScript
let provider = null;
let signer = null;
let userAddress = null;
let contract = null;

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    initializeTabs();
    await checkMetaMask();
    await loadContract();
});

// Xử lý Form Nạp tiền (Deposit)
document.getElementById('deposit-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Kiểm tra kết nối ví và contract
    if (!userAddress) {
        showNotification('Vui lòng kết nối ví trước!', 'error');
        return;
    }
    if (!contract) {
        showNotification('Hệ thống chưa sẵn sàng (Contract chưa load).', 'error');
        return;
    }

    showLoading(true);

    try {
        const amount = document.getElementById('deposit-amount').value;
        const amountWei = ethers.utils.parseEther(amount); // Chuyển đổi sang Wei

        console.log(`Đang nạp ${amount} ETH...`);

        // 1. Gọi Smart Contract để nạp tiền
        // Hàm deposit() trong Solidity là payable, nên ta gửi kèm { value: amountWei }
        const tx = await contract.deposit({ value: amountWei });
        
        showNotification('Giao dịch đã được gửi. Vui lòng đợi xác nhận...', 'info');
        
        // Đợi transaction được đào (xác nhận)
        const receipt = await tx.wait();
        console.log('Deposit thành công:', receipt);

        // 2. Lưu lịch sử giao dịch vào Database
        // Trước tiên cần lấy ID tài khoản của user hiện tại
        const accountsResponse = await fetch(`${CONFIG.API_URL}/accounts/user/${userAddress}`);
        const accounts = await accountsResponse.json();
        
        if (accounts.length > 0) {
            const accountId = accounts[0].AccountID; // Lấy tài khoản đầu tiên

            await fetch(`${CONFIG.API_URL}/transactions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    from_account_id: accountId, // Nạp tiền: từ chính mình
                    to_account_id: accountId,   // vào chính mình (hoặc có thể để null tùy logic backend)
                    amount: parseFloat(amount),
                    transaction_type: 'DEPOSIT',
                    description: 'Nạp tiền vào tài khoản',
                    blockchain_tx_hash: receipt.transactionHash
                })
            });
        }

        showNotification('Nạp tiền thành công!', 'success');
        document.getElementById('deposit-form').reset();
        
        // Cập nhật lại giao diện
        loadDashboard();
        loadAccounts(); // Số dư trong DB sẽ tăng lên
        loadTransactions();

    } catch (error) {
        console.error('Lỗi nạp tiền:', error);
        // Hiển thị lỗi chi tiết nếu có
        let errorMessage = error.message;
        if (error.data && error.data.message) errorMessage = error.data.message;
        showNotification('Nạp tiền thất bại: ' + errorMessage, 'error');
    } finally {
        showLoading(false);
    }
});

// Tab Navigation
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(targetTab).classList.add('active');

            // Load data when switching tabs
            if (targetTab === 'accounts') {
                loadAccounts();
            } else if (targetTab === 'transactions') {
                loadTransactions();
            } else if (targetTab === 'dashboard') {
                loadDashboard();
            }
        });
    });
}

// Check MetaMask
async function checkMetaMask() {
    if (typeof window.ethereum !== 'undefined') {
        try {
            const accounts = await window.ethereum.request({ method: 'eth_accounts' });
            if (accounts.length > 0) await connectWallet();
        } catch (error) {
            console.error('Error checking MetaMask:', error);
        }
    } else {
        showNotification('Vui lòng cài đặt MetaMask!', 'error');
    }

    document.getElementById('connect-wallet-btn').addEventListener('click', connectWallet);
}

// Connect Wallet
async function connectWallet() {
    if (!window.ethereum) {
        showNotification('MetaMask chưa được cài đặt!', 'error');
        return;
    }

    try {
        try {
            await window.ethereum.request({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId: '0x539' }], // 0x539 là mã Hex của 1337
            });
        } catch (switchError) {
            // Nếu mạng chưa được thêm vào MetaMask, tự động thêm nó
            if (switchError.code === 4902) {
                await window.ethereum.request({
                    method: 'wallet_addEthereumChain',
                    params: [{
                        chainId: '0x539',
                        chainName: 'ganache local',
                        rpcUrls: ['http://127.0.0.1:7545'],
                        nativeCurrency: {
                            name: 'ETH',
                            symbol: 'ETH',
                            decimals: 18
                        }
                    }],
                });
            }
        }
        provider = new ethers.providers.Web3Provider(window.ethereum);
        await provider.send("eth_requestAccounts", []);
        signer = provider.getSigner();
        userAddress = await signer.getAddress();

        document.getElementById('wallet-address').textContent =
            `${userAddress.substring(0, 6)}...${userAddress.slice(-4)}`;
        document.getElementById('connect-wallet-btn').textContent = 'Đã kết nối';

        // Lấy số dư từ blockchain
        const balanceWei = await provider.getBalance(userAddress);
        const balanceEth = parseFloat(ethers.utils.formatEther(balanceWei));
        console.log(`Số dư ETH: ${balanceEth} ETH`);
        // **Lưu wallet vào database**
        const createUserResponse = await fetch(`${CONFIG.API_URL}/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                wallet_address: userAddress,
                username: userAddress.substring(0, 8),
                email: `${userAddress.substring(0, 8)}@wallet.com`,
                full_name: 'Blockchain User',
                balance: balanceEth
            })
        });

        if (!createUserResponse.ok) {
            const errorData = await createUserResponse.json();
            throw new Error(`Lỗi tạo User: ${errorData.error || createUserResponse.statusText}`);
        }
        // Load dashboard/accounts/transactions
        await loadDashboard();
        await loadAccounts();
        await loadTransactions();

        // Listen for account changes
        window.ethereum.on('accountsChanged', async (accounts) => {
            if (accounts.length === 0) {
                userAddress = null;
                document.getElementById('wallet-address').textContent = 'Chưa kết nối ví';
                document.getElementById('connect-wallet-btn').textContent = 'Kết nối MetaMask';
            } else {
                await connectWallet();
            }
        });

    } catch (error) {
        console.error('Error connecting wallet:', error);
        showNotification('Lỗi kết nối ví: ' + error.message, 'error');
    }
}

// Load Contract
async function loadContract() {
    if (CONFIG.CONTRACT_ADDRESS && CONFIG.CONTRACT_ABI.length > 0) {
        try {
            if (provider) {
                contract = new ethers.Contract(
                    CONFIG.CONTRACT_ADDRESS,
                    CONFIG.CONTRACT_ABI,
                    signer || provider
                );
                console.log('Contract loaded:', CONFIG.CONTRACT_ADDRESS);
            }
        } catch (error) {
            console.error('Error loading contract:', error);
            showNotification('Lỗi load contract. Vui lòng kiểm tra CONTRACT_ADDRESS và CONTRACT_ABI trong config.js', 'error');
        }
    } else {
        console.warn('Contract address or ABI not configured');
    }
}

// Load User Data
async function loadUserData() {
    if (!userAddress) return;

    try {
        const response = await fetch(`${CONFIG.API_URL}/users/${userAddress}`);
        if (!response.ok) {
            // User doesn't exist, might need to create
            console.log('User not found in database');
        } else {
            const user = await response.json();
            console.log('User loaded:', user);
        }
    } catch (error) {
        console.error('Error loading user:', error);
    }
}

// Load Dashboard
async function loadDashboard() {
    if (!userAddress) return;

    try {
        const accountsResponse = await fetch(`${CONFIG.API_URL}/accounts/user/${userAddress}`);
        if (accountsResponse.ok) {
            const accounts = await accountsResponse.json();
            document.getElementById('account-count').textContent = accounts.length;

            let totalBalance = 0;
            console.log('accounts', accounts);
            accounts.forEach(acc => {
                console.log('acc.Balance', acc.Balance);
                if (acc.Balance) {
                    totalBalance += acc.Balance;
                }
            });
            console.log('totalBalance', totalBalance);
            document.getElementById('total-balance').textContent = totalBalance.toFixed(4) + ' ETH';
        }

        // Load transaction count
        const accounts = await accountsResponse.json();
        if (accounts.length > 0) {
            const txResponse = await fetch(`${CONFIG.API_URL}/transactions/account/${accounts[0].AccountID}`);
            if (txResponse.ok) {
                const transactions = await txResponse.json();
                document.getElementById('transaction-count').textContent = transactions.length;
            }
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Load Accounts
async function loadAccounts() {
    if (!userAddress) {
        document.getElementById('accounts-list').innerHTML = '<p>Vui lòng kết nối ví để xem tài khoản</p>';
        return;
    }

    try {
        const response = await fetch(`${CONFIG.API_URL}/accounts/user/${userAddress}`);
        if (!response.ok) throw new Error('Failed to load accounts');

        const accounts = await response.json();
        const accountsList = document.getElementById('accounts-list');

        if (accounts.length === 0) {
            accountsList.innerHTML = '<p>Chưa có tài khoản nào. Hãy tạo tài khoản mới!</p>';
        } else {
            accountsList.innerHTML = accounts.map(acc => `
                <div class="account-item">
                    <div class="account-info">
                        <h4>${acc.AccountNumber}</h4>
                        <p>Loại: ${acc.AccountType}</p>
                        <p>Số dư: ${acc.Balance ? acc.Balance.toFixed(4) : '0'} ETH</p>
                    </div>
                </div>
            `).join('');
        }

        // Populate transfer form
        const fromAccountSelect = document.getElementById('from-account');
        fromAccountSelect.innerHTML = accounts.map(acc =>
            `<option value="${acc.AccountID}">${acc.AccountNumber} (${acc.Balance ? acc.Balance.toFixed(4) : '0'} ETH)</option>`
        ).join('');
    } catch (error) {
        console.error('Error loading accounts:', error);
        showNotification('Lỗi tải tài khoản: ' + error.message, 'error');
    }
}

// Create Account Form
document.getElementById('create-account-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!userAddress) {
        showNotification('Vui lòng kết nối ví trước!', 'error');
        return;
    }

    showLoading(true);

    try {
        const accountType = document.getElementById('account-type').value;

        // First, get or create user
        let userResponse = await fetch(`${CONFIG.API_URL}/users/${userAddress}`);
        let user;

        if (!userResponse.ok) {
            // Create user
            const createUserResponse = await fetch(`${CONFIG.API_URL}/users`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: userAddress.substring(0, 10),
                    email: `${userAddress.substring(0, 10)}@wallet.com`,
                    full_name: 'Blockchain User',
                    wallet_address: userAddress
                })
            });

            if (!createUserResponse.ok) throw new Error('Failed to create user');
            user = await createUserResponse.json();
            user = user.user;
        } else {
            user = await userResponse.json();
        }

        // Create account in database
        const accountResponse = await fetch(`${CONFIG.API_URL}/accounts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: user.UserID,
                account_type: accountType,
                wallet_address: userAddress,
                balance:  user.Balance
            })
        });

        if (!accountResponse.ok) throw new Error('Failed to create account');
        const accountData = await accountResponse.json();

        // Create account on blockchain if contract is available
        if (contract) {
            try {
                const tx = await contract.createAccount(accountData.account.AccountNumber);
                await tx.wait();
                showNotification('Tài khoản đã được tạo trên blockchain!', 'success');
            } catch (blockchainError) {
                console.error('Blockchain error:', blockchainError);
                showNotification('Tài khoản đã được tạo nhưng có lỗi trên blockchain', 'error');
            }
        }

        showNotification('Tạo tài khoản thành công!', 'success');
        document.getElementById('create-account-form').reset();
        loadAccounts();
        loadDashboard();
    } catch (error) {
        console.error('Error creating account:', error);
        showNotification('Lỗi tạo tài khoản: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
});

// Transfer Form
document.getElementById('transfer-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!userAddress) {
        showNotification('Vui lòng kết nối ví trước!', 'error');
        return;
    }

    if (!contract) {
        showNotification('Contract chưa được cấu hình!', 'error');
        return;
    }

    showLoading(true);

    try {
        const fromAccountId = document.getElementById('from-account').value;
        const toAddress = document.getElementById('to-address').value;
        const amount = document.getElementById('transfer-amount').value;
        const description = document.getElementById('transfer-description').value;

        // Validate input
        if (!fromAccountId || !toAddress || !amount) {
            throw new Error('Vui lòng điền đầy đủ thông tin');
        }

        // Validate Ethereum address
        if (!ethers.utils.isAddress(toAddress)) {
            throw new Error('Địa chỉ ví không hợp lệ');
        }

        console.log('=== BẮT ĐẦU CHUYỂN TIỀN ===');
        console.log('From Account ID:', fromAccountId);
        console.log('To Address:', toAddress);
        console.log('Amount:', amount);

        // Get account info
        const accountResponse = await fetch(`${CONFIG.API_URL}/accounts/${fromAccountId}`);
        if (!accountResponse.ok) throw new Error('Không tìm thấy tài khoản nguồn');
        const fromAccount = await accountResponse.json();
        
        console.log('From Account:', fromAccount);

        // Check balance
        if (parseFloat(fromAccount.Balance) < parseFloat(amount)) {
            throw new Error('Số dư không đủ');
        }

        // Get to account
        let toAccountResponse = await fetch(`${CONFIG.API_URL}/accounts/user/${toAddress}`);
        let toAccountId;

        if (toAccountResponse.ok) {
            const toAccounts = await toAccountResponse.json();
            if (toAccounts.length > 0) {
                toAccountId = toAccounts[0].AccountID;
                console.log('To Account ID:', toAccountId);
            } else {
                console.log('Người nhận chưa có tài khoản trong hệ thống');
            }
        }

        // Check if recipient account exists on blockchain
        const recipientExists = await contract.accountExist(toAddress);
        console.log('Recipient exists on blockchain:', recipientExists);
        
        if (!recipientExists) {
            throw new Error('Địa chỉ nhận chưa có tài khoản trên blockchain. Người nhận cần tạo tài khoản trước.');
        }

        // Execute transfer on blockchain
        const amountWei = ethers.utils.parseEther(amount);
        const transactionHash = `TXN${Date.now()}`;
        
        console.log('Calling contract.transfer()...');
        console.log('Amount in Wei:', amountWei.toString());
        console.log('Transaction Hash:', transactionHash);

        const tx = await contract.transfer(toAddress, amountWei, transactionHash);
        console.log('Transaction sent:', tx.hash);
        
        showNotification('Giao dịch đã được gửi. Vui lòng đợi xác nhận...', 'info');
        
        const receipt = await tx.wait();
        console.log('Transaction confirmed:', receipt);

        // Create transaction in database
        const txResponse = await fetch(`${CONFIG.API_URL}/transactions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                from_account_id: parseInt(fromAccountId),
                to_account_id: toAccountId || parseInt(fromAccountId), // Fallback
                amount: parseFloat(amount),
                transaction_type: 'TRANSFER',
                description: description,
                blockchain_tx_hash: receipt.transactionHash
            })
        });

        if (!txResponse.ok) {
            const errorData = await txResponse.json();
            console.error('Database error:', errorData);
            throw new Error('Lỗi lưu giao dịch vào database: ' + (errorData.error || 'Unknown'));
        }

        showNotification('Chuyển tiền thành công!', 'success');
        document.getElementById('transfer-form').reset();
        
        // Reload data
        await loadAccounts();
        await loadTransactions();
        await loadDashboard();
        
    } catch (error) {
        console.error('=== LỖI CHUYỂN TIỀN ===');
        console.error('Error:', error);
        
        let errorMessage = 'Lỗi chuyển tiền: ';
        
        if (error.code === 'CALL_EXCEPTION') {
            errorMessage += 'Lỗi gọi contract. Kiểm tra số dư hoặc địa chỉ nhận.';
        } else if (error.code === 'INSUFFICIENT_FUNDS') {
            errorMessage += 'Không đủ ETH để trả phí gas.';
        } else if (error.code === 4001) {
            errorMessage += 'Bạn đã từ chối giao dịch.';
        } else if (error.reason) {
            errorMessage += error.reason;
        } else if (error.data && error.data.message) {
            errorMessage += error.data.message;
        } else {
            errorMessage += error.message;
        }
        
        showNotification(errorMessage, 'error');
    } finally {
        showLoading(false);
    }
});

// Load Transactions
async function loadTransactions() {
    if (!userAddress) {
        document.getElementById('transactions-list').innerHTML = '<p>Vui lòng kết nối ví để xem giao dịch</p>';
        return;
    }

    try {
        const accountsResponse = await fetch(`${CONFIG.API_URL}/accounts/user/${userAddress}`);
        if (!accountsResponse.ok) return;

        const accounts = await accountsResponse.json();
        if (accounts.length === 0) {
            document.getElementById('transactions-list').innerHTML = '<p>Chưa có giao dịch nào</p>';
            return;
        }

        const transactionsList = document.getElementById('transactions-list');
        let allTransactions = [];

        for (const acc of accounts) {
            const txResponse = await fetch(`${CONFIG.API_URL}/transactions/account/${acc.AccountID}`);
            if (txResponse.ok) {
                const transactions = await txResponse.json();
                allTransactions = allTransactions.concat(transactions);
            }
        }

        // Sort by date
        allTransactions.sort((a, b) => new Date(b.CreatedAt) - new Date(a.CreatedAt));

        if (allTransactions.length === 0) {
            transactionsList.innerHTML = '<p>Chưa có giao dịch nào</p>';
        } else {
            transactionsList.innerHTML = allTransactions.map(tx => {
                const isSent = accounts.some(acc => acc.AccountID === tx.FromAccountID);
                const amount = parseFloat(tx.Amount);
                return `
                    <div class="transaction-item ${isSent ? 'sent' : 'received'}">
                        <div class="transaction-header">
                            <span>${tx.TransactionType}</span>
                            <span class="transaction-amount ${isSent ? 'negative' : 'positive'}">
                                ${isSent ? '-' : '+'}${amount.toFixed(4)} ETH
                            </span>
                        </div>
                        <p>Hash: ${tx.TransactionHash || 'N/A'}</p>
                        <p>Thời gian: ${new Date(tx.CreatedAt).toLocaleString('vi-VN')}</p>
                        ${tx.Description ? `<p>Mô tả: ${tx.Description}</p>` : ''}
                    </div>
                `;
            }).join('');
        }
    } catch (error) {
        console.error('Error loading transactions:', error);
        showNotification('Lỗi tải giao dịch: ' + error.message, 'error');
    }
}

// Utility Functions
function showLoading(show) {
    document.getElementById('loading').classList.toggle('hidden', !show);
}

function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.classList.remove('hidden');

    setTimeout(() => {
        notification.classList.add('hidden');
    }, 5000);
}