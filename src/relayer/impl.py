from typing import Dict
from abc import ABC
from web3 import Web3
from web3.contract import Contract
from web3.types import Nonce, Wei, TxParams
from eth_account.datastructures import SignedTransaction
from eth_account.signers.local import LocalAccount
from src.relayer.addresses import AddressesType
from eth_typing import ChecksumAddress


class RelayerClientImplementation(ABC):
    client: Web3
    account: LocalAccount
    addresses: Dict[AddressesType, ChecksumAddress]

    def initialize(self) -> None: ...
    def get_chain_id(self) -> int: ...
    def get_nonce(self) -> Nonce: ...
    def get_gas_price(self) -> Wei: ...
    def sign_transaction(
        self, transaction_dict: TxParams
    ) -> SignedTransaction: ...
    def send_transaction(self, transaction: SignedTransaction) -> str: ...
    
    def contract(self, address: str, abi: list) -> Contract: ...
