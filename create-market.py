import random
from web3 import Web3
from src.relayer.client import RelayerClient
from src.relayer.addresses import Addresses

# Current date, 22 December 2025, please create a question for prediction market with current date
questions = [
    "Will the price of Bitcoin be above $1M on December 31, 2025?",
    "Will the price of Ethereum be above $100K on December 31, 2025?",
    "Will the price of Dogecoin be above $1 on December 31, 2025?",
]

AMM_MINIMAL_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "_question", "type": "string"},
            {"internalType": "string[]", "name": "_outcomeLabels", "type": "string[]"},
            {
                "internalType": "enum ISybexOracle.QuestionType",
                "name": "_questionType",
                "type": "uint8",
            },
            {"internalType": "uint256", "name": "_timeout", "type": "uint256"},
        ],
        "name": "createMarket",
        "outputs": [{"internalType": "uint256", "name": "marketId", "type": "uint256"}],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "marketCounter",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_market", "type": "uint256"}],
        "name": "getMarket",
        "outputs": [
            {"internalType": "string", "name": "question", "type": "string"},
            {
                "internalType": "enum ISybexOracle.QuestionType",
                "name": "questionType",
                "type": "uint8",
            },
            {
                "internalType": "enum SybexAutomatedMarket.MarketStatus",
                "name": "status",
                "type": "uint8",
            },
            {"internalType": "uint256", "name": "totalPool", "type": "uint256"},
            {"internalType": "uint256", "name": "totalFees", "type": "uint256"},
            {"internalType": "uint256", "name": "winningOutcome", "type": "uint256"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_marketId", "type": "uint256"},
            {"internalType": "uint256", "name": "_outcome", "type": "uint256"},
        ],
        "name": "placePosition",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
]

client = RelayerClient()
client.initialize()
amm_contract = client.contract(Addresses["SYBEX_AMM"], abi=AMM_MINIMAL_ABI)
question = random.choice(questions)


def create_market():
    gas_price = client.get_gas_price()
    nonce = client.get_nonce()

    print(f"Current gas price: {gas_price} wei")

    transaction = amm_contract.functions.createMarket(
        question,
        ["Yes", "No"],
        0,  # QuestionType.BINARY
        60,  # Timeout 1 minutes
    ).build_transaction(
        {
            "from": client.account.address,
            "value": Web3.to_wei(0.001, "ether"),  # Example market creation fee
            "gas": 500000,
            "gasPrice": gas_price,
            "nonce": nonce,
        }
    )
    signed_txn = client.sign_transaction(transaction)
    print(signed_txn)

    tx_hash = client.send_transaction(signed_txn)
    print(f"Market creation transaction sent with hash: {tx_hash}")


def get_latest_market():
    market_count = amm_contract.functions.marketCounter().call()
    if market_count == 0:
        print("No markets have been created yet.")
        return

    latest_market_id = market_count - 1
    market_details = amm_contract.functions.getMarket(latest_market_id).call()

    print(f"Latest Market ID: {latest_market_id}")
    print(f"Question: {market_details[0]}")
    print(f"Question Type: {market_details[1]}")
    print(f"Status: {market_details[2]}")
    print(f"Total Pool: {Web3.from_wei(market_details[3], 'ether')} ETH")
    print(f"Total Fees: {Web3.from_wei(market_details[4], 'ether')} ETH")
    print(f"Winning Outcome: {market_details[5]}")
    print(f"Deadline (timestamp): {market_details[6]}")

    market_details_question = market_details[0]
    if market_details_question == question:
        print("The latest market matches the created market question.")


def place_position():
    for i in range(10):
        outcome = random.randint(0, 1)
        gas_price = client.get_gas_price()
        nonce = client.get_nonce()

        print(f"Current gas price: {gas_price} wei")

        current_market_id = amm_contract.functions.marketCounter().call() - 1

        transaction = amm_contract.functions.placePosition(
            current_market_id, outcome
        ).build_transaction(
            {
                "from": client.account.address,
                "value": Web3.to_wei(0.001, "ether"),  # Example position fee
                "gas": 500000,
                "gasPrice": gas_price,
                "nonce": nonce,
            }
        )
        signed_txn = client.sign_transaction(transaction)
        tx_hash = client.send_transaction(signed_txn)
        print(f"Position placement transaction sent with hash: {tx_hash}")


if __name__ == "__main__":
    get_latest_market()
    place_position()
    get_latest_market()
