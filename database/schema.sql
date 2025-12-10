-- Database Schema cho Hệ thống Ngân hàng Blockchain
-- SQL Server

-- Bảng Người dùng
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) UNIQUE NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    FullName NVARCHAR(100) NOT NULL,
    WalletAddress NVARCHAR(100) UNIQUE NOT NULL,
    Balance DECIMAL(18,2) DEFAULT 0.00,
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE(),
    IsActive BIT DEFAULT 1
);

-- Bảng Tài khoản Ngân hàng
CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    AccountNumber NVARCHAR(20) UNIQUE NOT NULL,
    AccountType NVARCHAR(20) NOT NULL, -- 'CHECKING', 'SAVINGS', 'BUSINESS'
    Balance DECIMAL(18,2) DEFAULT 0.00,
    BlockchainAddress NVARCHAR(100),
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE(),
    IsActive BIT DEFAULT 1,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Bảng Giao dịch
CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY IDENTITY(1,1),
    TransactionHash NVARCHAR(100) UNIQUE,
    FromAccountID INT NOT NULL,
    ToAccountID INT NOT NULL,
    Amount DECIMAL(18,2) NOT NULL,
    TransactionType NVARCHAR(20) NOT NULL, -- 'TRANSFER', 'DEPOSIT', 'WITHDRAW'
    Status NVARCHAR(20) NOT NULL, -- 'PENDING', 'CONFIRMED', 'FAILED'
    GasFee DECIMAL(18,8),
    BlockNumber BIGINT,
    CreatedAt DATETIME DEFAULT GETDATE(),
    ConfirmedAt DATETIME,
    Description NVARCHAR(500),
    FOREIGN KEY (FromAccountID) REFERENCES Accounts(AccountID),
    FOREIGN KEY (ToAccountID) REFERENCES Accounts(AccountID)
);

-- Bảng Smart Contracts
CREATE TABLE SmartContracts (
    ContractID INT PRIMARY KEY IDENTITY(1,1),
    ContractAddress NVARCHAR(100) UNIQUE NOT NULL,
    ContractName NVARCHAR(100) NOT NULL,
    ContractVersion NVARCHAR(20) NOT NULL,
    DeployedAt DATETIME DEFAULT GETDATE(),
    DeployedBy NVARCHAR(100),
    IsActive BIT DEFAULT 1
);

-- Bảng Lịch sử Giao dịch Blockchain
CREATE TABLE BlockchainLogs (
    LogID INT PRIMARY KEY IDENTITY(1,1),
    TransactionID INT,
    EventName NVARCHAR(50) NOT NULL,
    BlockNumber BIGINT,
    LogData NVARCHAR(MAX),
    CreatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID)
);

-- Indexes
CREATE INDEX IX_Users_WalletAddress ON Users(WalletAddress);
CREATE INDEX IX_Accounts_AccountNumber ON Accounts(AccountNumber);
CREATE INDEX IX_Transactions_TransactionHash ON Transactions(TransactionHash);
CREATE INDEX IX_Transactions_FromAccountID ON Transactions(FromAccountID);
CREATE INDEX IX_Transactions_ToAccountID ON Transactions(ToAccountID);
CREATE INDEX IX_Transactions_Status ON Transactions(Status);
CREATE INDEX IX_Transactions_CreatedAt ON Transactions(CreatedAt);

