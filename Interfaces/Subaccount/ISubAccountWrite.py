class ISubAccountWrite:
    def __init__(self, contract):
        self.contract = contract

    def create(self, user: str, name: str):
        return self.contract.create(user, name)

    def add_liquidity(self, user: str, account_id: str, strategy_token: str, amount: int, coin: str):
        return self.contract.addLiquidy(user, account_id, strategy_token, amount, coin)

    def remove_liquidity(self, user: str, account_id: str, strategy_token: str, amount: int, coin: str):
        return self.contract.removeLiquidy(user, account_id, strategy_token, amount, coin)

    def toggle_pause(self, user: str, account_id: str, strategy_token: str, coin: str, paused: bool):
        return self.contract.togglePause(user, account_id, strategy_token, coin, paused)

    def position(self, contract_address: str, user: str, account_id: str, strategy_token: str, coin: str, amount: int) -> int:
        return self.contract.position(contract_address, user, account_id, strategy_token, coin, amount)