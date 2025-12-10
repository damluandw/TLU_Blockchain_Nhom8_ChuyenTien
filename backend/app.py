"""
Flask API Application for Banking Blockchain System
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db, User, Account, Transaction, SmartContract
from blockchain import blockchain_service
from config import Config
from datetime import datetime
import secrets
import uuid

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    blockchain_connected = blockchain_service.is_connected()
    return jsonify({
        'status': 'healthy',
        'blockchain_connected': blockchain_connected
    }), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        full_name = data.get('full_name')
        wallet_address = data.get('wallet_address')
        balance = data.get('balance', 0)  # mặc định 0 nếu không có
        
        if not all([username, email, full_name, wallet_address, balance]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(WalletAddress=wallet_address).first()
        if existing_user:
            return jsonify({'message': 'User already exists', 'user': existing_user.to_dict()}), 200
        
        user = User(
            Username=username,
            Email=email,
            FullName=full_name,
            WalletAddress=wallet_address,
            Balance=balance
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User created successfully', 'user': user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<wallet_address>', methods=['GET'])
def get_user(wallet_address):
    """Get user by wallet address"""
    try:
        user = User.query.filter_by(WalletAddress=wallet_address).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts', methods=['POST'])
def create_account():
    """Create a new bank account"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        account_type = data.get('account_type', 'CHECKING')
        wallet_address = data.get('wallet_address')
        balance = data.get('balance', 0)  # mặc định 0 nếu không có
        
        if not user_id or not wallet_address:
            return jsonify({'error': 'Missing required fields'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Generate unique account number
        account_number = f"ACC{secrets.token_hex(8).upper()}"
        
        account = Account(
            UserID=user_id,
            AccountNumber=account_number,
            AccountType=account_type,
            BlockchainAddress=wallet_address,
            Balance=balance
        )
        
        db.session.add(account)
        db.session.commit()
        
        # Create account on blockchain
        # Note: This requires private key - should be handled by frontend with MetaMask
        # blockchain_result = blockchain_service.create_account_on_blockchain(
        #     account_number, wallet_address, private_key
        # )
        
        return jsonify({
            'message': 'Account created successfully',
            'account': account.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    """Get account by ID"""
    try:
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        account_data = account.to_dict()
        
        # Get blockchain balance if address exists
        if account.BlockchainAddress:
            blockchain_balance = blockchain_service.get_account_balance(account.BlockchainAddress)
            account_data['blockchain_balance'] = float(blockchain_balance) if blockchain_balance else 0
        
        return jsonify(account_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/user/<wallet_address>', methods=['GET'])
def get_accounts_by_wallet(wallet_address):
    """Get all accounts for a wallet address"""
    try:
        user = User.query.filter_by(WalletAddress=wallet_address).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        accounts = Account.query.filter_by(UserID=user.UserID, IsActive=True).all()
        accounts_data = []
        
        for acc in accounts:
            acc_dict = acc.to_dict()
            if acc.BlockchainAddress:
                blockchain_balance = blockchain_service.get_account_balance(acc.BlockchainAddress)
                acc_dict['blockchain_balance'] = float(blockchain_balance) if blockchain_balance else 0
            accounts_data.append(acc_dict)
        
        return jsonify(accounts_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction"""
    try:
        data = request.get_json()
        from_account_id = data.get('from_account_id')
        to_account_id = data.get('to_account_id')
        amount = data.get('amount')
        transaction_type = data.get('transaction_type', 'TRANSFER')
        description = data.get('description', '')
        blockchain_tx_hash = data.get('blockchain_tx_hash')  # From MetaMask
        
        if not all([from_account_id, to_account_id, amount]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        from_account = Account.query.get(from_account_id)
        to_account = Account.query.get(to_account_id)
        
        if not from_account or not to_account:
            return jsonify({'error': 'Account not found'}), 404
        
        # Generate unique transaction hash if not provided
        if not blockchain_tx_hash:
            blockchain_tx_hash = f"TXN{uuid.uuid4().hex.upper()}"
        
        transaction = Transaction(
            TransactionHash=blockchain_tx_hash,
            FromAccountID=from_account_id,
            ToAccountID=to_account_id,
            Amount=amount,
            TransactionType=transaction_type,
            Status='CONFIRMED' if blockchain_tx_hash else 'PENDING',
            ConfirmedAt=datetime.utcnow() if blockchain_tx_hash else None,
            Description=description
        )
        
        db.session.add(transaction)
        
        # Update balances
        from_account.Balance -= amount
        to_account.Balance += amount
        
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction created successfully',
            'transaction': transaction.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    """Get transaction by ID"""
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        return jsonify(transaction.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions/account/<int:account_id>', methods=['GET'])
def get_transactions_by_account(account_id):
    """Get all transactions for an account"""
    try:
        transactions = Transaction.query.filter(
            (Transaction.FromAccountID == account_id) | 
            (Transaction.ToAccountID == account_id)
        ).order_by(Transaction.CreatedAt.desc()).limit(50).all()
        
        return jsonify([t.to_dict() for t in transactions]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain/balance/<wallet_address>', methods=['GET'])
def get_blockchain_balance(wallet_address):
    """Get balance from blockchain"""
    try:
        balance = blockchain_service.get_account_balance(wallet_address)
        exists = blockchain_service.check_account_exists(wallet_address)
        
        return jsonify({
            'wallet_address': wallet_address,
            'balance': float(balance) if balance else 0,
            'exists': exists
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

