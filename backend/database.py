"""
Database models and connection for SQL Server
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    FullName = db.Column(db.String(100), nullable=False)
    WalletAddress = db.Column(db.String(100), unique=True, nullable=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    IsActive = db.Column(db.Boolean, default=True)
    
    accounts = db.relationship('Account', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'UserID': self.UserID,
            'Username': self.Username,
            'Email': self.Email,
            'FullName': self.FullName,
            'WalletAddress': self.WalletAddress,
            'CreatedAt': self.CreatedAt.isoformat() if self.CreatedAt else None,
            'IsActive': self.IsActive
        }

class Account(db.Model):
    __tablename__ = 'Accounts'
    
    AccountID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=False)
    AccountNumber = db.Column(db.String(20), unique=True, nullable=False)
    AccountType = db.Column(db.String(20), nullable=False)
    Balance = db.Column(db.Numeric(18, 2), default=0.00)
    BlockchainAddress = db.Column(db.String(100))
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    IsActive = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'AccountID': self.AccountID,
            'UserID': self.UserID,
            'AccountNumber': self.AccountNumber,
            'AccountType': self.AccountType,
            'Balance': float(self.Balance) if self.Balance else 0.00,
            'BlockchainAddress': self.BlockchainAddress,
            'CreatedAt': self.CreatedAt.isoformat() if self.CreatedAt else None,
            'IsActive': self.IsActive
        }

class Transaction(db.Model):
    __tablename__ = 'Transactions'
    
    TransactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TransactionHash = db.Column(db.String(100), unique=True)
    FromAccountID = db.Column(db.Integer, db.ForeignKey('Accounts.AccountID'), nullable=False)
    ToAccountID = db.Column(db.Integer, db.ForeignKey('Accounts.AccountID'), nullable=False)
    Amount = db.Column(db.Numeric(18, 2), nullable=False)
    TransactionType = db.Column(db.String(20), nullable=False)
    Status = db.Column(db.String(20), nullable=False)
    GasFee = db.Column(db.Numeric(18, 8))
    BlockNumber = db.Column(db.BigInteger)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    ConfirmedAt = db.Column(db.DateTime)
    Description = db.Column(db.String(500))
    
    from_account = db.relationship('Account', foreign_keys=[FromAccountID], backref='sent_transactions')
    to_account = db.relationship('Account', foreign_keys=[ToAccountID], backref='received_transactions')
    
    def to_dict(self):
        return {
            'TransactionID': self.TransactionID,
            'TransactionHash': self.TransactionHash,
            'FromAccountID': self.FromAccountID,
            'ToAccountID': self.ToAccountID,
            'Amount': float(self.Amount) if self.Amount else 0.00,
            'TransactionType': self.TransactionType,
            'Status': self.Status,
            'GasFee': float(self.GasFee) if self.GasFee else None,
            'BlockNumber': self.BlockNumber,
            'CreatedAt': self.CreatedAt.isoformat() if self.CreatedAt else None,
            'ConfirmedAt': self.ConfirmedAt.isoformat() if self.ConfirmedAt else None,
            'Description': self.Description
        }

class SmartContract(db.Model):
    __tablename__ = 'SmartContracts'
    
    ContractID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ContractAddress = db.Column(db.String(100), unique=True, nullable=False)
    ContractName = db.Column(db.String(100), nullable=False)
    ContractVersion = db.Column(db.String(20), nullable=False)
    DeployedAt = db.Column(db.DateTime, default=datetime.utcnow)
    DeployedBy = db.Column(db.String(100))
    IsActive = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'ContractID': self.ContractID,
            'ContractAddress': self.ContractAddress,
            'ContractName': self.ContractName,
            'ContractVersion': self.ContractVersion,
            'DeployedAt': self.DeployedAt.isoformat() if self.DeployedAt else None,
            'DeployedBy': self.DeployedBy,
            'IsActive': self.IsActive
        }

