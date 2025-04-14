from Interfaces.Payments.IPaymentsWrite import IPaymentsWrite, FeeTier
from Interfaces.Strategy.IStrategyWrite import IStrategyWrite
from Interfaces.Factory.IFactoryRead import IFactoryRead, Bot

class WebDEXFactory:
    def __init__(self, owner: str):
        self.owner = owner
        self.bots: dict[str, Bot] = {}

    def _check_bot(self, contract_address: str):
        if contract_address not in self.bots or not self.bots[contract_address].manager_address:
            raise Exception("Bot not found")

    def add_bot(self, name: str, prefix: str, owner: str, contract_address: str,
                strategy_address: str, sub_account_address: str,
                payments_address: str, token_pass_address: str,
                fee_tiers: list[FeeTier], payments_contract):
        if contract_address in self.bots and self.bots[contract_address].manager_address:
            raise Exception("Bot already registered")

        self.bots[contract_address] = Bot(
            prefix, name, owner, contract_address, strategy_address,
            sub_account_address, payments_address, token_pass_address
        )

        payments = IPaymentsWrite(payments_contract)
        payments.add_fee_tiers(contract_address, fee_tiers)

    def update_bot(self, contract_address: str, strategy_address: str = None,
                   sub_account_address: str = None, payments_address: str = None):
        self._check_bot(contract_address)
        if strategy_address:
            self.bots[contract_address].strategy_address = strategy_address
        if sub_account_address:
            self.bots[contract_address].sub_account_address = sub_account_address
        if payments_address:
            self.bots[contract_address].payments_address = payments_address

    def remove_bot(self, contract_address: str):
        self._check_bot(contract_address)
        del self.bots[contract_address]

    def currency_allow(self, contract_address: str, coin: str, payments_contract):
        self._check_bot(contract_address)
        payments = IPaymentsWrite(payments_contract)
        payments.revoke_or_allow_currency(contract_address, coin, True)

    def currency_revoke(self, contract_address: str, coin: str, payments_contract):
        self._check_bot(contract_address)
        payments = IPaymentsWrite(payments_contract)
        payments.revoke_or_allow_currency(contract_address, coin, False)

    def add_strategy(self, name: str, symbol: str, contract_address: str, strategy_contract):
        self._check_bot(contract_address)
        strategy = IStrategyWrite(strategy_contract)
        strategy.add_strategy(name, symbol, contract_address)

    def update_strategy_status(self, contract_address: str, token_address: str, is_active: bool, strategy_contract):
        self._check_bot(contract_address)
        strategy = IStrategyWrite(strategy_contract)
        strategy.update_strategy_status(contract_address, token_address, is_active)

    def get_bot_info(self, contract_address: str):
        return self.bots[contract_address]
