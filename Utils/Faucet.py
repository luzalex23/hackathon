class Faucet:
    def __init__(self, erc20_contract, decimals):
        self.contract = erc20_contract
        self.decimals = decimals
        self.mints = {}

    def mint(self, to, sender):
        if self.mints.get(to, 0) > 0:
            raise Exception("You have already exceeded the mint limit")
        self.contract._mint(to, 10000 * (10 ** self.decimals), {"from": sender})
        self.mints[to] = self.mints.get(to, 0) + 1