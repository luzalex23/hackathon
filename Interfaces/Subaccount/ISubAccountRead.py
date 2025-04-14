from dataclasses import dataclass
from typing import List


@dataclass
class BalanceStrategy:
    amount: int
    token: str
    decimals: int
    ico: str
    name: str
    status: bool
    paused: bool

@dataclass
class StrategyDisplay:
    strategy_token: str
    balance: List[BalanceStrategy]

@dataclass
class SubAccountsDisplay:
    id: str
    name: str
    strategies: List[StrategyDisplay]

@dataclass
class SubAccount:
    id: str
    name: str

class ISubAccountRead:
    def __init__(self, contract):
        self.contract = contract

    def get_subaccounts(self, contract_address: str, user: str) -> List[SubAccount]:
        return [SubAccount(*sa) for sa in self.contract.getSubAccounts(contract_address, user)]

    def get_strategies(self, contract_address: str, user: str, account_id: str) -> List[str]:
        return self.contract.getStrategies(contract_address, user, account_id)

    def get_balances(self, contract_address: str, user: str, account_id: str, strategy_token: str) -> List[BalanceStrategy]:
        return [BalanceStrategy(*b) for b in self.contract.getBalances(contract_address, user, account_id, strategy_token)]