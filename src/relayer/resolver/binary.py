from typing import cast
from web3.types import TxParams
from src.relayer.impl import RelayerClientImplementation
from src.relayer.abis import RESOLVER_MINIMAL_ABI


class BinaryResolver:
    def __init__(self, client: RelayerClientImplementation) -> None:
        self.client = client

    async def build_initialize_params(self) -> TxParams:
        nonce = await self.client.get_nonce()
        gasPrice = await self.client.get_gas_price()
        chainId = await self.client.get_chain_id()

        return {
            "from": self.client.account.address,
            "chainId": chainId,
            "nonce": nonce,
            "gas": 500000,
            "gasPrice": gasPrice,
        }

    async def resolve(self, questionId: int, outcome: int, proof: str) -> str:
        resolver_contract = await self.client.contract(
            address=self.client.addresses["SYBEX_BINARY_RESOLVER"],
            abi=RESOLVER_MINIMAL_ABI,
        )
        transaction_params = await self.build_initialize_params()

        transactions = resolver_contract.functions.resolve(
            questionId, outcome, proof
        ).build_transaction(transaction_params)

        signed_tx = await self.client.sign_transaction(transaction_dict=transactions)

        tx_hash = await self.client.send_transaction(transaction=signed_tx)

        return tx_hash
