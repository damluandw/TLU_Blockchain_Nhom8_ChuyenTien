"""
Configuration file for the Banking Blockchain Application
"""
import os
from urllib.parse import quote_plus

class Config:
    # Database Configuration
    # NOTE: Use environment variables or a .env file to set sensitive values in production.
    SQL_SERVER = os.getenv('SQL_SERVER', 'localhost')
    SQL_DATABASE = os.getenv('SQL_DATABASE', 'BankingBlockchain')
    SQL_USERNAME = os.getenv('SQL_USERNAME', 'sa')
    # Do NOT hardcode production passwords here. Default to empty to force explicit set.
    SQL_PASSWORD = os.getenv('SQL_PASSWORD', '')

    # Encode password
    ENCODED_PASSWORD = quote_plus(SQL_PASSWORD) if SQL_PASSWORD else ''

    # SQLAlchemy connection string
    # Encode server name if it contains backslash (for named instances)
    encoded_server = quote_plus(SQL_SERVER) if '\\' in SQL_SERVER else SQL_SERVER
    
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{SQL_USERNAME}:{ENCODED_PASSWORD}@{encoded_server}/{SQL_DATABASE}"
        "?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Blockchain config
    BLOCKCHAIN_NETWORK = os.getenv('BLOCKCHAIN_NETWORK', 'HTTP://127.0.0.1:7545')
    CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512')
    PRIVATE_KEY = os.getenv('PRIVATE_KEY', '0xc8063286f77fedfc2d9e3468e59f98a903f80dcaec3cd188192fd31ccac96ed6')

    # Flask config
    SECRET_KEY = os.getenv('SECRET_KEY', '0x5f88514565012345650123456501234565012345650123456501234565012345')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

    # Gas config
    GAS_LIMIT = 300_000
    GAS_PRICE = 20_000_000_000  # 20 Gwei
