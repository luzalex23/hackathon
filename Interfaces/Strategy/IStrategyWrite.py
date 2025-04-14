class IStrategyWrite:
    def __init__(self, contract):
        self.contract = contract

    def add_strategy(self, name: str, symbol: str, contract_address: str):
        return self.contract.addStrategy(name, symbol, contract_address)

    def update_strategy_status(self, contract_address: str, token_address: str, is_active: bool):
        return self.contract.updateStrategyStatus(contract_address, token_address, is_active)