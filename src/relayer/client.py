from abc import ABC
from web3 import Web3, HTTPProvider
from web3.contract import Contract
from eth_account import Account
from eth_utils.currency import from_wei
from web3.types import Nonce, TxParams, Wei
from eth_account.datastructures import SignedTransaction
from src.relayer.impl import RelayerClientImplementation
from src.logger import AppLogger
from src.constants import RELAYER_RPC_URL, RELAYER_PRIVATE_KEY, MIN_BALANCE_WEI
from src.relayer.addresses import Addresses
from src.relayer.resolver.binary import BinaryResolver


class RelayerClient(RelayerClientImplementation):
    def __init__(self) -> None:
        self.addresses = Addresses

        self.total_permissions = 0
        self.binary = BinaryResolver(self)

    def initialize(self) -> None:
        AppLogger.info("Initializing Relayer Client...")

        self.client = Web3(HTTPProvider(RELAYER_RPC_URL))
        if not self.client.is_connected():
            AppLogger.error(f"Failed to connect to Relayer RPC at {RELAYER_RPC_URL}")
            raise ConnectionError("Could not connect to Relayer RPC")

        AppLogger.info(f"Connected to Relayer RPC at {RELAYER_RPC_URL}")

        self.connect_account()
        self.check_balance()
        self.check_role_permissions()

    def connect_account(self) -> None:
        try:
            AppLogger.info("Connecting Relayer account...")
            self.account = Account.from_key(RELAYER_PRIVATE_KEY)
            AppLogger.info(f"Relayer account connected: {self.account.address}")
        except (ValueError, TypeError) as e:
            AppLogger.error("Failed to connect Relayer account.")
            raise e

    def check_balance(self) -> None:
        balance = self.get_balance()
        ether_balance = from_wei(balance, "ether")
        if balance < MIN_BALANCE_WEI:
            min_balance_ether = from_wei(MIN_BALANCE_WEI, "ether")
            AppLogger.error(
                f"Relayer account balance is too low: {ether_balance} BNB. Minimum required is {min_balance_ether} BNB."
            )
            raise ValueError("Insufficient balance in Relayer account")
        AppLogger.info(f"Relayer account balance: {ether_balance} BNB")

    def check_role_permissions(self) -> None:
        if self.binary.has_role():
            self.total_permissions += 1
            AppLogger.info("You have Binary Resolver role permission.")
        else:
            AppLogger.warning("You do NOT have Binary Resolver role permission.")

        if self.total_permissions == 0:
            AppLogger.error("No role permissions assigned to Relayer.")
            AppLogger.info(
                "Please contact the contract administrator on official X account."
            )
            raise PermissionError("No role permissions assigned to Relayer")

    def get_nonce(self) -> Nonce:
        return self.client.eth.get_transaction_count(self.account.address, "latest")

    def get_gas_price(self) -> Wei:
        return self.client.eth.gas_price

    def get_balance(self) -> Wei:
        return self.client.eth.get_balance(self.account.address)

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
