"""
Configuration file for the Banking Blockchain Application
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database Configuration
    SQL_SERVER = os.getenv('SQL_SERVER', 'localhost')
    SQL_DATABASE = os.getenv('SQL_DATABASE', 'BankingBlockchain')
    SQL_USERNAME = os.getenv('SQL_USERNAME', 'sa')
    SQL_PASSWORD = os.getenv('SQL_PASSWORD', 'your_password')
    
    # SQL Server Connection String
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{SQL_USERNAME}:{SQL_PASSWORD}@{SQL_SERVER}/{SQL_DATABASE}"
        f"?driver=ODBC+Driver+17+for+SQL+Server"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Blockchain Configuration
    BLOCKCHAIN_NETWORK = os.getenv('BLOCKCHAIN_NETWORK', 'http://127.0.0.1:8545')  # Ganache/Anvil
    CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '')
    PRIVATE_KEY = os.getenv('PRIVATE_KEY', '')  # Private key for backend operations
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Gas Configuration
    GAS_LIMIT = 300000
    GAS_PRICE = 20000000000  # 20 Gwei

