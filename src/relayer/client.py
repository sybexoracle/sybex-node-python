from abc import ABC
from web3 import Web3, HTTPProvider
from web3.contract import Contract
from eth_account import Account
from web3.types import Nonce, TxParams, Wei
from eth_account.datastructures import SignedTransaction
from eth_account.types import TransactionDictType
from src.relayer.impl import RelayerClientImplementation
from src.constants import RELAYER_RPC_URL, RELAYER_PRIVATE_KEY
from src.relayer.addresses import Addresses


class RelayerClient(RelayerClientImplementation):
    def __init__(self) -> None:
        self.addresses = Addresses

    def initialize(self) -> None:
        self.client = Web3(HTTPProvider(RELAYER_RPC_URL))
        self.account = Account.from_key(RELAYER_PRIVATE_KEY)

    def get_chain_id(self) -> int:
        return self.client.eth.chain_id

    def get_nonce(self) -> Nonce:
        return self.client.eth.get_transaction_count(
            self.account.address, "latest"
        )

    def get_gas_price(self) -> Wei:
        return self.client.eth.gas_price

    def sign_transaction(self, transaction_dict: TxParams) -> SignedTransaction:
        return self.client.eth.account.sign_transaction(
            transaction_dict=transaction_dict, private_key=self.account.key
        )

    def send_transaction(self, transaction: SignedTransaction) -> str:
        raw_transaction = transaction.raw_transaction

        tx_hash = self.client.eth.send_raw_transaction(raw_transaction)
        return tx_hash.hex()

    def contract(self, address: str, abi: list) -> Contract:
        return self.client.eth.contract(address=address, abi=abi)  # type: ignore
