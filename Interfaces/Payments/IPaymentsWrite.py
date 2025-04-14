from typing import List
from dataclasses import dataclass


@dataclass
class FeeTier:
    limit: int
    fee: int

class IPaymentsWrite:
    def __init__(self, contract):
        self.contract = contract

    def revoke_or_allow_currency(self, contract_address: str, coin: str, status: bool):
        return self.contract.revokeOrAllowCurrency(contract_address, coin, status)

    def add_fee_tiers(self, contract_address: str, tiers: List[FeeTier]):
        return self.contract.addFeeTiers(
            contract_address,
            [(tier.limit, tier.fee) for tier in tiers]
        )