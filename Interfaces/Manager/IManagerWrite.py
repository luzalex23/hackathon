class IManagerWrite:
    def __init__(self, contract):
        self.contract = contract

    def rebalance_position(self, user: str, amount: int, gas: int, coin: str, fee: int):
        tx = self.contract.rebalancePosition(user, amount, gas, coin, fee)
        return tx