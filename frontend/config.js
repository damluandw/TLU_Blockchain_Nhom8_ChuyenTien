// Configuration
const CONFIG = {
    API_URL: 'http://localhost:5000/api',
    CONTRACT_ADDRESS: "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512",
    CONTRACT_ABI: [
                    {
                      "inputs": [],
                      "stateMutability": "nonpayable",
                      "type": "constructor"
                    },
                    {
                      "anonymous": false,
                      "inputs": [
                        {
                          "indexed": true,
                          "internalType": "address",
                          "name": "account",
                          "type": "address"
                        },
                        {
                          "indexed": false,
                          "internalType": "string",
                          "name": "accountNumber",
                          "type": "string"
                        },
                        {
                          "indexed": false,
                          "internalType": "uint256",
                          "name": "timestamp",
                          "type": "uint256"
                        }
                      ],
                      "name": "AccountCreated",
                      "type": "event"
                    },
                    {
                      "anonymous": false,
                      "inputs": [
                        {
                          "indexed": true,
                          "internalType": "address",
                          "name": "account",
                          "type": "address"
                        },
                        {
                          "indexed": false,
                          "internalType": "uint256",
                          "name": "amount",
                          "type": "uint256"
                        },
                        {
                          "indexed": false,
                          "internalType": "uint256",
                          "name": "timestamp",
                          "type": "uint256"
                        }
                      ],
                      "name": "Deposit",
                      "type": "event"
                    },
                    {
                      "anonymous": false,
                      "inputs": [
                        {
                          "indexed": true,
                          "internalType": "address",
                          "name": "from",
                          "type": "address"
                        },
                        {
                          "indexed": true,
                          "internalType": "address",
                          "name": "to",
                          "type": "address"
                        },
                        {
                          "indexed": false,
                          "internalType": "uint256",
                          "name": "amount",
                          "type": "uint256"
                        },
                        {
                          "indexed": false,
                          "internalType": "string",
                          "name": "transactionHash",
                          "type": "string"
                        },
                        {
                          "indexed": false,
                          "internalType": "uint256",
                          "name": "timestamp",
                          "type": "uint256"
                        }
                      ],
                      "name": "Transfer",
                      "type": "event"
                    },
                    {
                      "anonymous": false,
                      "inputs": [
                        {
                          "indexed": true,
                          "internalType": "address",
                          "name": "account",
                          "type": "address"
                        },
                        {
                          "indexed": false,
                          "internalType": "uint256",
                          "name": "amount",
                          "type": "uint256"
                        },
                        {
                          "indexed": false,
                          "internalType": "uint256",
                          "name": "timestamp",
                          "type": "uint256"
                        }
                      ],
                      "name": "Withdraw",
                      "type": "event"
                    },
                    {
                      "inputs": [
                        {
                          "internalType": "address",
                          "name": "_account",
                          "type": "address"
                        }
                      ],
                      "name": "accountExist",
                      "outputs": [
                        {
                          "internalType": "bool",
                          "name": "exists",
                          "type": "bool"
                        }
                      ],
                      "stateMutability": "view",
                      "type": "function"
                    },
                    {
                      "inputs": [
                        {
                          "internalType": "string",
                          "name": "",
                          "type": "string"
                        }
                      ],
                      "name": "accountNumberToAddress",
                      "outputs": [
                        {
                          "internalType": "address",
                          "name": "",
                          "type": "address"
                        }
                      ],
                      "stateMutability": "view",
                      "type": "function"
                    },
                    {
                      "inputs": [
                        {
                          "internalType": "address",
                          "name": "",
                          "type": "address"
                        }
                      ],
                      "name": "accounts",
                      "outputs": [
                        {
                          "internalType": "address",
                          "name": "accountOwner",
                          "type": "address"
                        },
                        {
                          "internalType": "uint256",
                          "name": "balance",
                          "type": "uint256"
                        },
                        {
                          "internalType": "bool",
                          "name": "exists",
                          "type": "bool"
                        },
                        {
                          "internalType": "uint256",
                          "name": "createdAt",
                          "type": "uint256"
                        }
                      ],
                      "stateMutability": "view",
                      "type": "function"
                    },
                    {
                      "inputs": [
                        {
                          "internalType": "uint256",
                          "name": "",
                          "type": "uint256"
                        }
                      ],
                      "name": "allAccounts",
                      "outputs": [
                        {
                          "internalType": "address",
                          "name": "",
                          "type": "address"
                        }
                      ],
                      "stateMutability": "view",
                      "type": "function"
                    },
                    {
                      "inputs": [
                        {
                          "internalType": "string",
                          "name": "_accountNumber",
                          "type": "string"
                        }
                      ],
                      "name": "createAccount",
                      "outputs": [],
                      "stateMutability": "nonpayable",
                      "type": "function"
                    },
                    {
                      "inputs": [],
                      "name": "deposit",
                      "outputs": [],
                      "stateMutability": "payable",
                      "type": "function"
                    },
                    {
                      "inputs": [
                        {
                          "internalType": "address",
                          "name": "_account",
                          "type": "address"
                        }
                      ],
                      "name": "getAccountInfo",
                      "outputs": [
                        {
                          "internalType": "address",
                          "name": "accountOwner",
                          "type": "address"
                        },
                        {
                          "internalType": "uint256",
                          "name": "balance",
                          "type": "uint256"
                        },
                        {
                          "internalType": "bool",
                          "name": "exists",
                          "type": "bool"
                        },
                        {
                          "internalType": "uint256",
                          "name": "createdAt",
                          "type": "uint256"
                        }
                      ],
                      "stateMutability": "view",
                      "type": "function"
                    },
                    {
                      "inputs": [
                        {
                          "internalType": "string",
                          "name": "_accountNumber",
                          "type": "string"
                        }
                      ],
                      "name": "getAddressByAccountNumber",
                      "outputs": [
                        {
                          "internalType": "address",
                          "name": "accountAddress",
                          "type": "address"
                        }
                      ],
                      "stateMutability": "view",
                      "type": "function"
                    },
                    {
                      "inputs": [
                        {
                          "internalType": "address",
                          "name": "_account",
                          "type": "address"
                        }
                      ],
                      "name": "getBalance",
                      "outputs": [
                        {
                          "internalType": "uint256",
                          "name": "balance",
                          "type": "uint256"
                        }
                      ],
                      "stateMutability": "view",
                      "type": "function"
                    },
                    {
                      "inputs": [],
                      "name": "getTotalAccounts",
                      "outputs": [
                        {
                          "internalType": "uint256",
                          "name": "totalAccounts",
                          "type": "uint256"
                        }
                      ],
                      "stateMutability": "view",
                      "type": "function"
                    },
                    {
                      "inputs": [],
                      "name": "owner",
                      "outputs": [
                        {
                          "internalType": "address",
                          "name": "",
                          "type": "address"
                        }
                      ],
                      "stateMutability": "view",
                      "type": "function"
                    },
                    {
                      "inputs": [
                        {
                          "internalType": "address",
                          "name": "_to",
                          "type": "address"
                        },
                        {
                          "internalType": "uint256",
                          "name": "_amount",
                          "type": "uint256"
                        },
                        {
                          "internalType": "string",
                          "name": "_transactionHash",
                          "type": "string"
                        }
                      ],
                      "name": "transfer",
                      "outputs": [],
                      "stateMutability": "nonpayable",
                      "type": "function"
                    },
                    {
                      "inputs": [
                        {
                          "internalType": "uint256",
                          "name": "_amount",
                          "type": "uint256"
                        }
                      ],
                      "name": "withdraw",
                      "outputs": [],
                      "stateMutability": "nonpayable",
                      "type": "function"
                    }
                  ]
};