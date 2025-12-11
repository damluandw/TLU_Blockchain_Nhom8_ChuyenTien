"""
Blockchain interaction module using Web3.py
"""
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import os
from config import Config

class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(Config.BLOCKCHAIN_NETWORK))
        
        # Add middleware for PoA networks (like Ganache)
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        self.contract_address = Config.CONTRACT_ADDRESS
        self.contract_abi = self._load_contract_abi()
        
        if self.contract_address and self.contract_abi:
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.contract_address),
                abi=self.contract_abi
            )
        else:
            self.contract = None
    
    def _load_contract_abi(self):
        """Load ABI from compiled contract (Truffle build output)"""
        # Truffle stores compiled contracts in build/contracts/
        abi_path = os.path.join(os.path.dirname(__file__), '..', 'build', 'contracts', 'BankContract.json')
        abi_path = os.path.abspath(abi_path)  # Convert to absolute path
        
        try:
            if not os.path.exists(abi_path):
                print(f"Warning: ABI file not found at {abi_path}")
                # Fallback to old location (if exists)
                old_path = os.path.join(os.path.dirname(__file__), '..', 'contracts', 'BankContract.json')
                old_path = os.path.abspath(old_path)
                if os.path.exists(old_path):
                    print(f"Trying fallback location: {old_path}")
                    abi_path = old_path
                else:
                    print(f"Fallback location also not found: {old_path}")
                    return []
            
            with open(abi_path, 'r', encoding='utf-8') as f:
                contract_data = json.load(f)
                abi = contract_data.get('abi', [])
                if abi:
                    print(f"Successfully loaded ABI from {abi_path}")
                    return abi
                else:
                    print(f"Warning: ABI is empty in {abi_path}")
                    return []
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {abi_path} - {e}")
            return []
        except Exception as e:
            print(f"Error loading ABI: {e}")
            return []
    
    def is_connected(self):
        """Check if connected to blockchain"""
        return self.w3.is_connected()
    
    def get_account_balance(self, account_address):
        """Get account balance from blockchain"""
        if not self.contract:
            return None
        try:
            balance = self.contract.functions.getBalance(
                Web3.to_checksum_address(account_address)
            ).call()
            return self.w3.from_wei(balance, 'ether')
        except Exception as e:
            print(f"Error getting balance: {e}")
            return None
    
    def check_account_exists(self, account_address):
        """Check if account exists on blockchain"""
        if not self.contract:
            return False
        try:
            return self.contract.functions.accountExist(
                Web3.to_checksum_address(account_address)
            ).call()
        except Exception as e:
            print(f"Error checking account: {e}")
            return False
    
    def create_account_on_blockchain(self, account_number, wallet_address, private_key):
        """Create account on blockchain"""
        if not self.contract:
            return None
        
        try:
            account = self.w3.eth.account.from_key(private_key)
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            transaction = self.contract.functions.createAccount(account_number).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': Config.GAS_LIMIT,
                'gasPrice': self.w3.to_wei(20, 'gwei')
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'transaction_hash': tx_hash.hex(),
                'block_number': receipt.blockNumber,
                'status': receipt.status
            }
        except Exception as e:
            print(f"Error creating account: {e}")
            return None
    
    def transfer_on_blockchain(self, from_address, to_address, amount, transaction_hash, private_key):
        """Execute transfer on blockchain"""
        if not self.contract:
            return None
        
        try:
            account = self.w3.eth.account.from_key(private_key)
            amount_wei = self.w3.to_wei(amount, 'ether')
            
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            transaction = self.contract.functions.transfer(
                Web3.to_checksum_address(to_address),
                amount_wei,
                transaction_hash
            ).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': Config.GAS_LIMIT,
                'gasPrice': self.w3.to_wei(20, 'gwei')
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'transaction_hash': tx_hash.hex(),
                'block_number': receipt.blockNumber,
                'status': receipt.status,
                'gas_used': receipt.gasUsed
            }
        except Exception as e:
            print(f"Error transferring: {e}")
            return None
    
    def get_transaction_receipt(self, tx_hash):
        """Get transaction receipt"""
        try:
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            return {
                'status': receipt.status,
                'block_number': receipt.blockNumber,
                'gas_used': receipt.gasUsed
            }
        except Exception as e:
            print(f"Error getting receipt: {e}")
            return None
    
    def get_latest_block(self):
        """Get latest block number"""
        try:
            return self.w3.eth.block_number
        except Exception as e:
            print(f"Error getting block: {e}")
            return None
    
    def get_transaction(self, transaction_id):
        """Get transaction details by ID from blockchain"""
        if not self.contract:
            return None
        try:
            result = self.contract.functions.getTransaction(transaction_id).call()
            return {
                'transaction_id': transaction_id,
                'from': result[0],
                'to': result[1],
                'amount': self.w3.from_wei(result[2], 'ether'),
                'amount_wei': result[2],
                'timestamp': result[3],
                'transaction_hash': result[4]
            }
        except Exception as e:
            print(f"Error getting transaction: {e}")
            return None
    
    def get_transaction_count(self, account_address):
        """Get total number of transactions for an account"""
        if not self.contract:
            return None
        try:
            count = self.contract.functions.getTransactionCount(
                Web3.to_checksum_address(account_address)
            ).call()
            return count
        except Exception as e:
            print(f"Error getting transaction count: {e}")
            return None
    
    def get_transaction_ids(self, account_address, offset=0, limit=50):
        """Get transaction IDs for an account"""
        if not self.contract:
            return []
        try:
            ids = self.contract.functions.getTransactionIds(
                Web3.to_checksum_address(account_address),
                offset,
                limit
            ).call()
            return ids
        except Exception as e:
            print(f"Error getting transaction IDs: {e}")
            return []
    
    def get_account_transactions(self, account_address, offset=0, limit=50):
        """Get all transactions for an account"""
        if not self.contract:
            return []
        try:
            transaction_ids = self.get_transaction_ids(account_address, offset, limit)
            transactions = []
            
            for tx_id in transaction_ids:
                tx = self.get_transaction(tx_id)
                if tx:
                    transactions.append(tx)
            
            return transactions
        except Exception as e:
            print(f"Error getting account transactions: {e}")
            return []
    
    def get_total_transactions(self):
        """Get total number of transactions in the system"""
        if not self.contract:
            return None
        try:
            total = self.contract.functions.getTotalTransactions().call()
            return total
        except Exception as e:
            print(f"Error getting total transactions: {e}")
            return None

# Global instance
blockchain_service = BlockchainService()

