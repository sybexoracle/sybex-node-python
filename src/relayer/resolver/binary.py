from typing import cast
from web3.types import TxParams
from src.relayer.impl import RelayerClientImplementation
from src.relayer.abis import RESOLVER_MINIMAL_ABI
from src.relayer.roles import BINARY_OPERATOR_ROLE


class BinaryResolver:
    def __init__(self, client: RelayerClientImplementation) -> None:
        self.client = client

    def build_initialize_params(self) -> TxParams:
        nonce = self.client.get_nonce()
        gasPrice = self.client.get_gas_price()
        chainId = self.client.get_chain_id()

        return {
            "from": self.client.account.address,
            "chainId": chainId,
            "nonce": nonce,
            "gas": 500000,
            "gasPrice": gasPrice,
        }

    def has_role(self):
        resolver_contract = self.client.contract(
            address=self.client.addresses["SYBEX_BINARY_RESOLVER"],
            abi=RESOLVER_MINIMAL_ABI,
        )
        hasRole = resolver_contract.functions.hasRole(
            BINARY_OPERATOR_ROLE,
            self.client.account.address
        ).call()
        return hasRole

    def estimate_resolve_gas(self, questionId: int, outcome: int, proof: str) -> int:
        resolver_contract = self.client.contract(
            address=self.client.addresses["SYBEX_BINARY_RESOLVER"],
            abi=RESOLVER_MINIMAL_ABI,
        )
        transaction_params = self.build_initialize_params()

        gas_estimate = resolver_contract.functions.resolve(
            questionId, outcome, proof
        ).estimate_gas(transaction_params)

        return cast(int, gas_estimate)

    def resolve(self, questionId: int, outcome: int, proof: str) -> str:
        resolver_contract = self.client.contract(
            address=self.client.addresses["SYBEX_BINARY_RESOLVER"],
            abi=RESOLVER_MINIMAL_ABI,
        )
        transaction_params = self.build_initialize_params()

        transactions = resolver_contract.functions.resolve(
            questionId, outcome, proof
        ).build_transaction(transaction_params)

        signed_tx = self.client.sign_transaction(transaction_dict=transactions)

        tx_hash = self.client.send_transaction(transaction=signed_tx)

        return tx_hash
