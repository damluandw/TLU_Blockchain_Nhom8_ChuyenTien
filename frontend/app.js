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
            // Request account access
            const accounts = await window.ethereum.request({ method: 'eth_accounts' });
            if (accounts.length > 0) {
                await connectWallet();
            }
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
    if (typeof window.ethereum === 'undefined') {
        showNotification('MetaMask chưa được cài đặt!', 'error');
        return;
    }

    try {
        provider = new ethers.providers.Web3Provider(window.ethereum);
        await provider.send("eth_requestAccounts", []);
        signer = provider.getSigner();
        userAddress = await signer.getAddress();

        document.getElementById('wallet-address').textContent = 
            `${userAddress.substring(0, 6)}...${userAddress.substring(38)}`;
        document.getElementById('connect-wallet-btn').textContent = 'Đã kết nối';

        // Load user data
        await loadUserData();
        loadDashboard();
        loadAccounts();
        loadTransactions();

        // Listen for account changes
        window.ethereum.on('accountsChanged', (accounts) => {
            if (accounts.length === 0) {
                userAddress = null;
                document.getElementById('wallet-address').textContent = 'Chưa kết nối ví';
                document.getElementById('connect-wallet-btn').textContent = 'Kết nối MetaMask';
            } else {
                connectWallet();
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
            accounts.forEach(acc => {
                if (acc.blockchain_balance) {
                    totalBalance += acc.blockchain_balance;
                }
            });
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
                        <p>Số dư: ${acc.blockchain_balance ? acc.blockchain_balance.toFixed(4) : '0'} ETH</p>
                    </div>
                </div>
            `).join('');
        }

        // Populate transfer form
        const fromAccountSelect = document.getElementById('from-account');
        fromAccountSelect.innerHTML = accounts.map(acc => 
            `<option value="${acc.AccountID}">${acc.AccountNumber} (${acc.blockchain_balance ? acc.blockchain_balance.toFixed(4) : '0'} ETH)</option>`
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
                wallet_address: userAddress
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
        showNotification('Contract chưa được cấu hình. Vui lòng kiểm tra CONTRACT_ADDRESS và CONTRACT_ABI trong config.js', 'error');
        return;
    }

    showLoading(true);

    try {
        const fromAccountId = document.getElementById('from-account').value;
        const toAddress = document.getElementById('to-address').value;
        const amount = document.getElementById('transfer-amount').value;
        const description = document.getElementById('transfer-description').value;

        // Get account info
        const accountResponse = await fetch(`${CONFIG.API_URL}/accounts/${fromAccountId}`);
        if (!accountResponse.ok) throw new Error('Account not found');
        const fromAccount = await accountResponse.json();

        // Get to account
        let toAccountResponse = await fetch(`${CONFIG.API_URL}/accounts/user/${toAddress}`);
        let toAccountId;

        if (toAccountResponse.ok) {
            const toAccounts = await toAccountResponse.json();
            if (toAccounts.length > 0) {
                toAccountId = toAccounts[0].AccountID;
            }
        }

        // Execute transfer on blockchain
        const amountWei = ethers.utils.parseEther(amount);
        const transactionHash = `TXN${Date.now()}`;

        const tx = await contract.transfer(toAddress, amountWei, transactionHash);
        const receipt = await tx.wait();

        // Create transaction in database
        const txResponse = await fetch(`${CONFIG.API_URL}/transactions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                from_account_id: parseInt(fromAccountId),
                to_account_id: toAccountId || fromAccountId, // Fallback if not found
                amount: parseFloat(amount),
                transaction_type: 'TRANSFER',
                description: description,
                blockchain_tx_hash: receipt.transactionHash
            })
        });

        if (!txResponse.ok) throw new Error('Failed to save transaction');

        showNotification('Chuyển tiền thành công!', 'success');
        document.getElementById('transfer-form').reset();
        loadAccounts();
        loadTransactions();
        loadDashboard();
    } catch (error) {
        console.error('Error transferring:', error);
        showNotification('Lỗi chuyển tiền: ' + error.message, 'error');
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

