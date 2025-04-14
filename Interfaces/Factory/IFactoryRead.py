from dataclasses import dataclass

@dataclass
class Bot:
    prefix: str
    name: str
    owner: str
    manager_address: str
    strategy_address: str
    sub_account_address: str
    payments_address: str
    token_pass_address: str

class IFactoryRead:
    def __init__(self, contract):
        self.contract = contract

    def get_bot_info(self, contract_address: str) -> Bot:
        bot = self.contract.getBotInfo(contract_address)
        return Bot(*bot)