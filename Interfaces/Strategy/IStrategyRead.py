from dataclasses import dataclass

@dataclass
class Strategy:
    name: str
    token_address: str
    is_active: bool

class IStrategyRead:
    def __init__(self, contract):
        self.contract = contract

    def find_strategy(self, contract_address: str, token_address: str) -> Strategy:
        result = self.contract.findStrategy(contract_address, token_address)
        return Strategy(*result)

    def get_strategies(self, contract_address: str) -> List[Strategy]:
        return [Strategy(*s) for s in self.contract.getStrategies(contract_address)]