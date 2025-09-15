import unittest
from bank_system import (
    Bank, Customer, Employee, Currency, BankAccount, DebitCard,
    LoanApplication, VIPClient, CorporateClient, Transaction, MoneyTransfer,
    InsufficientFundsError, SecurityBreachError, LoanDeniedError, AuthenticationError,
    AuthService, PasswordValidator
)

class TestBankSystem(unittest.TestCase):

    def setUp(self):
        """Настройка тестовых данных"""
        self.bank = Bank("Test Bank")
        self.customer = Customer("Иван", "Иванов", "1234567890", "+79991234567", "ivan@mail.com")
        self.employee = Employee("Петр", "Петров", "EMP001", "Менеджер", 50000, "2023-01-01")
        self.currency_rub = Currency("RUB", "Рубль", "₽")
        self.currency_usd = Currency("USD", "Доллар", "$")

    def test_bank_creation(self):
        """Тест создания банка"""
        self.assertEqual(self.bank.name_bank, "Test Bank")
        self.assertEqual(str(self.bank), "Банк: Test Bank")

    def test_customer_creation(self):
        """Тест создания клиента"""
        self.assertEqual(self.customer.name, "Иван")
        self.assertEqual(self.customer.surname, "Иванов")
        self.assertEqual(str(self.customer), "Клиент: Иван Иванов, паспорт: 1234567890")

    def test_employee_creation(self):
        """Тест создания сотрудника"""
        self.assertEqual(self.employee.name, "Петр")
        self.assertEqual(self.employee.position, "Менеджер")
        self.assertEqual(str(self.employee), "Сотрудник: Петр Петров, должность: Менеджер")

    def test_bank_account_operations(self):
        """Тест операций со счетом"""
        account = BankAccount("ACC001", "текущий", self.currency_rub, 1000)

        # Тест внесения средств
        new_balance = account.deposit(500)
        self.assertEqual(new_balance, 1500)

        # Тест снятия средств
        new_balance = account.withdraw(300)
        self.assertEqual(new_balance, 1200)

        # Тест недостатка средств
        with self.assertRaises(InsufficientFundsError):
            account.withdraw(2000)

    def test_debit_card_operations(self):
        """Тест операций с дебетовой картой"""
        card = DebitCard("1234567812345678", "Иван Иванов", "12/25", "123", "2023-01-01", 1000, "RUB")

        # Тест проверки баланса
        self.assertEqual(card.check_balance(), 1000)

        # Тест изменения PIN
        result = card.change_pin("5678")
        self.assertEqual(result, "PIN changed successfully")

        # Тест неверного PIN
        with self.assertRaises(SecurityBreachError):
            card.change_pin("12")

    def test_currency_conversion(self):
        """Тест конвертации валют"""
        self.bank.add_currency_rate(self.currency_usd, self.currency_rub, 75.0)
        rate = self.bank.get_currency_rate(self.currency_usd, self.currency_rub)
        self.assertEqual(rate, 75.0)

    def test_loan_application_approval(self):
        """Тест одобрения кредитной заявки"""
        application = LoanApplication("APP001", self.customer, "personal", 100000, 12, "покупка техники")

        # Клиент с хорошей кредитной историей
        self.customer.credit_score = 750
        result = application.process()
        self.assertEqual(result, "Заявка одобрена")
        self.assertEqual(application.status, "approved")

    def test_loan_application_denial(self):
        """Тест отказа в кредитной заявке"""
        application = LoanApplication("APP002", self.customer, "personal", 100000, 12, "покупка техники")

        # Клиент с плохой кредитной историей
        self.customer.credit_score = 550
        with self.assertRaises(LoanDeniedError):
            application.process()
        self.assertEqual(application.status, "denied")

    def test_vip_client_services(self):
        """Тест VIP клиента"""
        vip_client = VIPClient("Алексей", "VIP", "VIP001", "+79998887766", "vip@mail.com", "Platinum", "Менеджер VIP")

        result = vip_client.request_exclusive_service("Персональный консьерж")
        self.assertEqual(result, "Услуга Персональный консьерж заказана для VIP клиента")
        self.assertIn("Персональный консьерж", vip_client.exclusive_services)

    def test_corporate_client_operations(self):
        """Тест корпоративного клиента"""
        corp_client = CorporateClient("Мария", "Сидорова", "CORP001", "+79997776655",
                                      "corp@mail.com", "ООО Тест", "123456789", 50)

        account = BankAccount("CORP_ACC001", "бизнес", self.currency_rub, 50000)
        corp_client.open_business_account(account)

        self.assertEqual(account.corporate_owner, corp_client)
        self.assertIn(account, corp_client.business_accounts)

    def test_transaction_execution(self):
        """Тест выполнения транзакции"""
        transaction = Transaction("TXN001", 1000, self.currency_rub, "Тестовая транзакция")

        result = transaction.execute()
        self.assertEqual(result, "Transaction executed")
        self.assertEqual(transaction.status, "completed")

    def test_money_transfer_validation(self):
        """Тест валидации денежного перевода"""
        sender_account = BankAccount("SEND001", "текущий", self.currency_rub, 1000)
        receiver_account = BankAccount("RECV001", "текущий", self.currency_rub, 500)

        transfer = MoneyTransfer("TRF001", 800, self.currency_rub, "Тестовый перевод",
                                 sender_account, receiver_account)

        # Валидный перевод
        self.assertTrue(transfer.validate_transfer())

        # Невалидный перевод (недостаточно средств)
        invalid_transfer = MoneyTransfer("TRF002", 2000, self.currency_rub, "Невалидный перевод",
                                         sender_account, receiver_account)
        with self.assertRaises(InsufficientFundsError):
            invalid_transfer.validate_transfer()

    def test_currency_class(self):
        """Тест класса валюты"""
        self.assertEqual(str(self.currency_rub), "RUB (Рубль)")
        formatted = self.currency_rub.format_amount(1234.567)
        self.assertEqual(formatted, "1234.57 ₽")

    def test_employee_vacation_request(self):
        """Тест запроса отпуска сотрудника"""
        result = self.employee.request_vacation("2024-07-01", "2024-07-14")
        expected = "Запрос отпуска с 2024-07-01 по 2024-07-14 для Петр"
        self.assertEqual(result, expected)


class TestSecuritySystems(unittest.TestCase):

    def setUp(self):
        self.auth_service = AuthService("AUTH001", "active", "high", 3, 300)

    def test_authentication_success(self):
        """Тест успешной аутентификации"""
        result = self.auth_service.authenticate_user("testuser", "password123")
        self.assertTrue(result)

    def test_authentication_too_many_attempts(self):
        """Тест слишком многих попыток аутентификации"""
        self.auth_service.failed_attempts = 3
        with self.assertRaises(AuthenticationError):
            self.auth_service.authenticate_user("testuser", "wrongpassword")

    def test_password_validation(self):
        """Тест валидации пароля"""
        validator = PasswordValidator("PWD001", "active", "medium", 8, True)

        # Валидный пароль
        self.assertTrue(validator.validate_password("SecurePass123!"))

        # Невалидный пароль (слишком короткий)
        with self.assertRaises(SecurityBreachError):
            validator.validate_password("short")


if __name__ == "__main__":
    unittest.main()