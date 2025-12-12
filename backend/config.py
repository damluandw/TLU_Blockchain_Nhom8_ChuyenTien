"""
Configuration file for the Banking Blockchain Application
"""
import os

class Config:
    # Database Configuration
    SQL_SERVER = os.getenv('SQL_SERVER', 'DESKTOP-CRFJV4A\\SQL2022')
    SQL_DATABASE = os.getenv('SQL_DATABASE', 'DB_BLOCKCHAIN')
    SQL_USERNAME = os.getenv('SQL_USERNAME', 'sa')
    SQL_PASSWORD = os.getenv('SQL_PASSWORD', '12345')

    # SQLAlchemy connection string - Dùng pyodbc connection string trực tiếp
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc:///?odbc_connect="
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        f"UID={SQL_USERNAME};"
        f"PWD={SQL_PASSWORD};"
        f"TrustServerCertificate=yes"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Blockchain config
    BLOCKCHAIN_NETWORK = os.getenv('BLOCKCHAIN_NETWORK', 'HTTP://127.0.0.1:7545')
    CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '0x0CCEB2124A8f152707230258FfBeB047de9912a2')
    PRIVATE_KEY = os.getenv('PRIVATE_KEY', '0x6d711f0d3073c58fcfe710595166a5fa08b5bf66bb4a545c0834cb39e4be187b')

    # Flask config
    SECRET_KEY = os.getenv('SECRET_KEY', '0x5f88514565012345650123456501234565012345650123456501234565012345')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

    # Gas config
    GAS_LIMIT = 300_000
    GAS_PRICE = 20_000_000_000  # 20 Gwei