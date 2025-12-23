RESOLVER_MINIMAL_ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "questionId", "type": "uint256"},
            {"internalType": "uint8", "name": "outcome", "type": "uint8"},
            {"internalType": "string", "name": "proof", "type": "string"},
        ],
        "name": "resolve",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "role", "type": "bytes32"},
            {"internalType": "address", "name": "account", "type": "address"},
        ],
        "name": "hasRole",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
]

AUTOMATED_MARKET_MAKER_MINIMAL_ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "_marketId", "type": "uint256"},
            {"internalType": "uint256", "name": "_outcomeId", "type": "uint256"},
        ],
        "name": "getOutcomeLabel",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    }
]
