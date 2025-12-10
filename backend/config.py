"""
Configuration file for the Banking Blockchain Application
"""
import os
from urllib.parse import quote_plus

class Config:
    # Database Configuration
    SQL_SERVER = os.getenv('SQL_SERVER', 'localhost')
    SQL_DATABASE = os.getenv('SQL_DATABASE', 'BankingBlockchain')
    SQL_USERNAME = os.getenv('SQL_USERNAME', 'miad')
    SQL_PASSWORD = os.getenv('SQL_PASSWORD', 'Dapp@2026')

    # Encode password
    ENCODED_PASSWORD = quote_plus(SQL_PASSWORD)

    # SQLAlchemy connection string
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{SQL_USERNAME}:{ENCODED_PASSWORD}@{SQL_SERVER}/{SQL_DATABASE}"
        "?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Blockchain config
    BLOCKCHAIN_NETWORK = os.getenv('BLOCKCHAIN_NETWORK', 'http://127.0.0.1:8545')
    CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '')
    PRIVATE_KEY = os.getenv('PRIVATE_KEY', '')

    # Flask config
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

    # Gas config
    GAS_LIMIT = 300_000
    GAS_PRICE = 20_000_000_000  # 20 Gwei
