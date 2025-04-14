import unittest
from unittest.mock import Mock
from Contracts.Factory.WebdEX_Factory import WebDEXFactory
from Interfaces.Payments.IPaymentsWrite import FeeTier

class TestWebDEXFactory(unittest.TestCase):
    def setUp(self):
        self.owner = "owner1"
        self.factory = WebDEXFactory(self.owner)
        # Cria mocks para os contratos externos utilizados pelos métodos.
        self.fake_payments_contract = Mock()
        self.fake_strategy_contract = Mock()
        # Configura os métodos esperados no contrato de pagamentos.
        self.fake_payments_contract.addFeeTiers = Mock()
        self.fake_payments_contract.revokeOrAllowCurrency = Mock()
        # Configura os métodos no contrato de estratégia.
        self.fake_strategy_contract.addStrategy = Mock()
        self.fake_strategy_contract.updateStrategyStatus = Mock()

    def create_sample_bot(self, contract_address="0xBot"):
        """Auxiliar para cadastrar um bot previamente válido nos testes."""
        fee_tiers = [FeeTier(limit=100, fee=1)]
        self.factory.add_bot(
            name="SampleBot",
            prefix="SB",
            owner=self.owner,
            contract_address=contract_address,
            strategy_address="0xStrategy",
            sub_account_address="0xSubAccount",
            payments_address="0xPayments",
            token_pass_address="0xTokenPass",
            fee_tiers=fee_tiers,
            payments_contract=self.fake_payments_contract
        )

    def test_add_bot_success(self):
        """Testa a adição de um bot com dados válidos."""
        fee_tiers = [FeeTier(limit=100, fee=1), FeeTier(limit=200, fee=2)]
        contract_addr = "0xBot1"
        self.factory.add_bot(
            name="BotOne",
            prefix="B1",
            owner=self.owner,
            contract_address=contract_addr,
            strategy_address="0xStrategy1",
            sub_account_address="0xSub1",
            payments_address="0xPayments1",
            token_pass_address="0xTokenPass1",
            fee_tiers=fee_tiers,
            payments_contract=self.fake_payments_contract
        )
        # Verifica se o bot foi cadastrado corretamente no dicionário.
        self.assertIn(contract_addr, self.factory.bots)
        bot = self.factory.bots[contract_addr]
        self.assertEqual(bot.name, "BotOne")
        self.assertEqual(bot.prefix, "B1")
        self.fake_payments_contract.addFeeTiers.assert_called_once_with(contract_addr, [(100, 1), (200, 2)])

    def test_add_bot_already_registered(self):
        """Testa a tentativa de cadastro de um bot com endereço já registrado."""
        fee_tiers = [FeeTier(limit=100, fee=1)]
        contract_addr = "0xBot1"
        # Cadastro inicial.
        self.factory.add_bot(
            name="BotOne",
            prefix="B1",
            owner=self.owner,
            contract_address=contract_addr,
            strategy_address="0xStrategy1",
            sub_account_address="0xSub1",
            payments_address="0xPayments1",
            token_pass_address="0xTokenPass1",
            fee_tiers=fee_tiers,
            payments_contract=self.fake_payments_contract
        )
        # Cadastro duplicado deve lançar uma exceção.
        with self.assertRaises(Exception) as context:
            self.factory.add_bot(
                name="BotDuplicate",
                prefix="B2",
                owner=self.owner,
                contract_address=contract_addr,
                strategy_address="0xStrategyNew",
                sub_account_address="0xSubNew",
                payments_address="0xPaymentsNew",
                token_pass_address="0xTokenPassNew",
                fee_tiers=fee_tiers,
                payments_contract=self.fake_payments_contract
            )
        self.assertEqual(str(context.exception), "Bot already registered")

    def test_update_bot(self):
        """Testa a atualização das informações de um bot cadastrado."""
        contract_addr = "0xBotUpdate"
        self.create_sample_bot(contract_addr)
        # Atualiza os parâmetros do bot.
        self.factory.update_bot(
            contract_addr,
            strategy_address="0xNewStrategy",
            sub_account_address="0xNewSub",
            payments_address="0xNewPayments"
        )
        bot = self.factory.bots[contract_addr]
        self.assertEqual(bot.strategy_address, "0xNewStrategy")
        self.assertEqual(bot.sub_account_address, "0xNewSub")
        self.assertEqual(bot.payments_address, "0xNewPayments")

    def test_remove_bot(self):
        """Testa a remoção de um bot cadastrado."""
        contract_addr = "0xBotRemove"
        self.create_sample_bot(contract_addr)
        self.factory.remove_bot(contract_addr)
        self.assertNotIn(contract_addr, self.factory.bots)

    def test_currency_allow(self):
        """Verifica se a função currency_allow invoca o método do contrato com os parâmetros corretos."""
        contract_addr = "0xBotAllow"
        self.create_sample_bot(contract_addr)
        coin = "BTC"
        self.factory.currency_allow(contract_addr, coin, self.fake_payments_contract)
        self.fake_payments_contract.revokeOrAllowCurrency.assert_called_with(contract_addr, coin, True)

    def test_currency_revoke(self):
        """Verifica se a função currency_revoke invoca o método do contrato com os parâmetros corretos."""
        contract_addr = "0xBotRevoke"
        self.create_sample_bot(contract_addr)
        coin = "ETH"
        self.factory.currency_revoke(contract_addr, coin, self.fake_payments_contract)
        self.fake_payments_contract.revokeOrAllowCurrency.assert_called_with(contract_addr, coin, False)

    def test_add_strategy(self):
        """Testa a adição de uma estratégia via o método add_strategy."""
        contract_addr = "0xBotStrategy"
        self.create_sample_bot(contract_addr)
        self.factory.add_strategy("StrategyTest", "SYM", contract_addr, self.fake_strategy_contract)
        self.fake_strategy_contract.addStrategy.assert_called_with("StrategyTest", "SYM", contract_addr)

    def test_update_strategy_status(self):
        """Testa a atualização do status da estratégia."""
        contract_addr = "0xBotStrategyStatus"
        self.create_sample_bot(contract_addr)
        token_address = "0xToken"
        self.factory.update_strategy_status(contract_addr, token_address, True, self.fake_strategy_contract)
        self.fake_strategy_contract.updateStrategyStatus.assert_called_with(contract_addr, token_address, True)

    def test_get_bot_info(self):
        """Testa se o método get_bot_info retorna o bot correto."""
        contract_addr = "0xBotInfo"
        self.create_sample_bot(contract_addr)
        bot = self.factory.get_bot_info(contract_addr)
        self.assertEqual(bot.manager_address, contract_addr)
        self.assertEqual(bot.name, "SampleBot")

if __name__ == '__main__':
    unittest.main()
