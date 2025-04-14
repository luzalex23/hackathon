class Origin:
    def __init__(self, name, symbol, decimals, token):
        self.name = name
        self.symbol = symbol
        self.decimals = decimals
        self.token = token

class LPToken:
    def __init__(self, contract, origin: Origin):
        self.contract = contract
        self.origin = origin

    def mint(self, to, amount, sender):
        self.contract.mint(to, amount, {"from": sender})

    def burn_from(self, account, amount, sender):
        self.contract.burnFrom(account, amount, {"from": sender})

    def get_contract_origin(self) -> Origin:
        return self.origin