from src.relayer.impl import RelayerClientImplementation
from src.relayer.abis import AUTOMATED_MARKET_MAKER_MINIMAL_ABI


class RelayerAMM:
    def __init__(self, client: RelayerClientImplementation) -> None:
        self.client = client

    def get_outcome_label(self, market_id: int, outcome_id: int) -> str:
        amm_contract = self.client.contract(
            address=self.client.addresses["SYBEX_AMM"],
            abi=AUTOMATED_MARKET_MAKER_MINIMAL_ABI,
        )

        outcome_label = amm_contract.functions.getOutcomeLabel(
            market_id, outcome_id
        ).call()

        return outcome_label
