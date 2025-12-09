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
        """Load ABI from compiled contract"""
        abi_path = os.path.join(os.path.dirname(__file__), '..', 'contracts', 'BankContract.json')
        try:
            with open(abi_path, 'r') as f:
                contract_data = json.load(f)
                return contract_data.get('abi', [])
        except FileNotFoundError:
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

# Global instance
blockchain_service = BlockchainService()

