class NFT:
    def __init__(self, contract):
        self.contract = contract

    def total_supply(self):
        return self.contract.totalSupply()

    def safe_mint(self, to, sender):
        return self.contract.safeMint(to, {"from": sender})