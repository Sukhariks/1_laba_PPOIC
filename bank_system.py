# Лаба 2, Сухоруков Михаил
# Банковская система

# Глобальные переменные
banks = []
current_bank = None


# Персональные исключения (12 штук)
class BankException(Exception):
    pass


class BankNotFoundError(BankException):
    pass


class CustomerNotFoundError(BankException):
    pass


class EmployeeNotFoundError(BankException):
    pass


class InsufficientFundsError(BankException):
    pass


class InvalidCardError(BankException):
    pass


class LoanDeniedError(BankException):
    pass


class SecurityBreachError(BankException):
    """Нарушение безопасности"""
    pass


class InvalidTransactionError(BankException):
    pass


class DepartmentFullError(BankException):
    """Департамент переполнен"""
    pass


class CurrencyConversionError(BankException):
    pass


class AuthenticationError(BankException):

    pass


# Классы (50 классов)
class Bank:
    def __init__(self, name_bank):
        self.name_bank = name_bank
        self.headquarters = None
        self.branches = []
        self.departments = []
        self.data_centers = []
        self.all_customers = []
        self.all_employees = []
        self.all_cards = []
        self.all_loans = []
        self.security_systems = []
        self.transactions = []
        self.accounts = []
        self.currency_rates = {}

    def __str__(self):
        return f"Банк: {self.name_bank}"

    def add_currency_rate(self, from_currency, to_currency, rate):
        self.currency_rates[(from_currency.code, to_currency.code)] = rate

    def get_currency_rate(self, from_currency, to_currency):
        return self.currency_rates.get((from_currency.code, to_currency.code))


class Headquarters:
    def __init__(self, name_headquarters, address):
        self.name_headquarters = name_headquarters
        self.address = address
        self.customers = []
        self.employees = []
        self.security_level = "high"
        self.operating_hours = "9:00-18:00"

    def add_employee(self, employee):
        #Добавить сотрудниа в главный офи
        if len(self.employees) >= 100:
            raise DepartmentFullError("Главный офис переполнен")
        self.employees.append(employee)
        employee.workplace = self


class Branch:
    def __init__(self, name_branch, address, branch_code):
        self.name_branch = name_branch
        self.address = address
        self.branch_code = branch_code
        self.customers = []
        self.employees = []
        self.atms = []
        self.cashiers = []

    def add_atm(self, atm):
        self.atms.append(atm)
        atm.branch = self


class Department:
    def __init__(self, name_department, department_type, max_employees=50):
        self.name_department = name_department
        self.department_type = department_type
        self.max_employees = max_employees
        self.employees = []
        self.manager = None

    def set_manager(self, employee):
        if not isinstance(employee, DepartmentManager):
            raise BankException("Только менеджер департамента может быть назначен")
        self.manager = employee


class DataCenter:
    def __init__(self, name_data_center, location, security_level):
        self.name_data_center = name_data_center
        self.location = location
        self.security_level = security_level
        self.employees = []
        self.servers = []
        self.backup_systems = []

    def add_server(self, server):
        self.servers.append(server)
        server.data_center = self


# Клиенты и сотрудники
class Customer:
    def __init__(self, name, surname, passport_id, phone_number, email):
        self.name = name
        self.surname = surname
        self.passport_id = passport_id
        self.phone_number = phone_number
        self.email = email
        self.accounts = []
        self.cards = []
        self.loans = []
        self.credit_score = 650
        self.registration_date = None

    def __str__(self):
        return f"Клиент: {self.name} {self.surname}, паспорт: {self.passport_id}"

    def open_account(self, account):
        """Открыть счет"""
        self.accounts.append(account)
        account.owner = self

    def apply_for_loan(self, loan_application):
        """Подать заявку на кредит"""
        if self.credit_score < 600:
            raise LoanDeniedError("Низкий кредитный рейтинг")
        return loan_application.process()


class CorporateClient(Customer):
    def __init__(self, name, surname, passport_id, phone_number, email, company_name, tax_id, company_size):
        super().__init__(name, surname, passport_id, phone_number, email)
        self.company_name = company_name
        self.tax_id = tax_id
        self.company_size = company_size
        self.business_accounts = []
        self.commercial_loans = []

    def __str__(self):
        return f"{super().__str__()}, компания: {self.company_name}"

    def open_business_account(self, account):
        """Открыть бизнес-счет"""
        self.business_accounts.append(account)
        account.corporate_owner = self


class VIPClient(Customer):
    def __init__(self, name, surname, passport_id, phone_number, email, vip_status, personal_manager):
        super().__init__(name, surname, passport_id, phone_number, email)
        self.vip_status = vip_status
        self.personal_manager = personal_manager
        self.exclusive_services = []
        self.priority_support = True

    def __str__(self):
        return f"{super().__str__()}, VIP статус: {self.vip_status}"

    def request_exclusive_service(self, service):
        self.exclusive_services.append(service)
        return f"Услуга {service} заказана для VIP клиента"


# Сотрудники
class Employee:
    def __init__(self, name, surname, employee_id, position, salary, hire_date):
        self.name = name
        self.surname = surname
        self.employee_id = employee_id
        self.position = position
        self.salary = salary
        self.hire_date = hire_date
        self.workplace = None
        self.department = None
        self.access_level = "basic"

    def __str__(self):
        return f"Сотрудник: {self.name} {self.surname}, должность: {self.position}"

    def request_vacation(self, start_date, end_date):
        #Запрсить отпуск
        return f"Запрос отпуска с {start_date} по {end_date} для {self.name}"


class Manager(Employee):
    def __init__(self, name, surname, employee_id, position, salary, hire_date, team_size):
        super().__init__(name, surname, employee_id, position, salary, hire_date)
        self.team_size = team_size
        self.subordinates = []
        self.access_level = "manager"

    def add_subordinate(self, employee):
       #добавить подчиненного
        self.subordinates.append(employee)


class BranchManager(Manager):
    def __init__(self, name, surname, employee_id, salary, hire_date, team_size, branch):
        super().__init__(name, surname, employee_id, "Менеджер филиала", salary, hire_date, team_size)
        self.branch = branch
        self.access_level = "branch_manager"

    def approve_loan(self, loan_application):
        if loan_application.amount > 1000000:
            raise LoanDeniedError("Требуется одобрение главного офиса")
        loan_application.status = "approved"
        return "Кредит одобрен"


class DepartmentManager(Manager):
    def __init__(self, name, surname, employee_id, salary, hire_date, team_size, department):
        super().__init__(name, surname, employee_id, "Менеджер департамента", salary, hire_date, team_size)
        self.department = department
        self.access_level = "department_manager"


class Cashier(Employee):
    def __init__(self, name, surname, employee_id, salary, hire_date, cash_drawer):
        super().__init__(name, surname, employee_id, "Кассир", salary, hire_date)
        self.cash_drawer = cash_drawer
        self.transactions_processed = 0

    def process_transaction(self, transaction):
        """Обработать транзакцию"""
        self.transactions_processed += 1
        return transaction.execute()


class Teller(Cashier):
    def __init__(self, name, surname, employee_id, salary, hire_date, cash_drawer, customer_service_rating):
        super().__init__(name, surname, employee_id, salary, hire_date, cash_drawer)
        self.position = "Кассир-операционист"
        self.customer_service_rating = customer_service_rating


class FinancialAdvisor(Employee):
    def __init__(self, name, surname, employee_id, salary, hire_date, specialization, certifications):
        super().__init__(name, surname, employee_id, "Финансовый советник", salary, hire_date)
        self.specialization = specialization
        self.certifications = certifications
        self.clients = []

    def provide_advice(self, client, advice_type):
        return f"Консультация по {advice_type} для клиента {client.name}"


class InvestmentAdvisor(FinancialAdvisor):
    def __init__(self, name, surname, employee_id, salary, hire_date, specialization, certifications,
                 investment_license):
        super().__init__(name, surname, employee_id, salary, hire_date, specialization, certifications)
        self.position = "Инвестиционный советник"
        self.investment_license = investment_license


class SecurityOfficer(Employee):
    def __init__(self, name, surname, employee_id, salary, hire_date, security_clearance, weapons_trained):
        super().__init__(name, surname, employee_id, "Охранник", salary, hire_date)
        self.security_clearance = security_clearance
        self.weapons_trained = weapons_trained
        self.patrol_routes = []

    def perform_patrol(self, route):
        #выполнить патрулирование
        return f"Патрулирование маршрута {route}"


class SystemAdmin(Employee):
    def __init__(self, name, surname, employee_id, salary, hire_date, admin_rights, systems_managed):
        super().__init__(name, surname, employee_id, "Системный администратор", salary, hire_date)
        self.admin_rights = admin_rights
        self.systems_managed = systems_managed
        self.access_level = "admin"

    def reset_password(self, user, new_password):
        return f"Пароль для {user} сброшен"


class NetworkAdmin(SystemAdmin):
    def __init__(self, name, surname, employee_id, salary, hire_date, admin_rights, systems_managed,
                 network_certifications):
        super().__init__(name, surname, employee_id, salary, hire_date, admin_rights, systems_managed)
        self.position = "Сетевой администратор"
        self.network_certifications = network_certifications


class LoanOfficer(Employee):
    def __init__(self, name, surname, employee_id, salary, hire_date, loan_types_handled, approval_rate):
        super().__init__(name, surname, employee_id, "Кредитный специалист", salary, hire_date)
        self.loan_types_handled = loan_types_handled
        self.approval_rate = approval_rate
        self.loans_processed = []

    def review_application(self, loan_application):
        """Рассмотреть заявку на кредит"""
        return loan_application.review()


class MortgageOfficer(LoanOfficer):
    def __init__(self, name, surname, employee_id, salary, hire_date, loan_types_handled, approval_rate,
                 real_estate_license):
        super().__init__(name, surname, employee_id, salary, hire_date, loan_types_handled, approval_rate)
        self.position = "Ипотечный специалист"
        self.real_estate_license = real_estate_license


# Карты и счета
class BankAccount:
    def __init__(self, account_number, account_type, currency, initial_balance=0):
        self.account_number = account_number
        self.account_type = account_type
        self.currency = currency
        self.balance = initial_balance
        self.owner = None
        self.corporate_owner = None
        self.transactions = []
        self.overdraft_limit = 0
        self.interest_rate = 0.01

    def deposit(self, amount):
        """Внести средства на счет"""
        if amount <= 0:
            raise InvalidTransactionError("Сумма должна быть положительной")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """Снять средства со счета"""
        if amount <= 0:
            raise InvalidTransactionError("Сумма должна быть положительной")
        if self.balance + self.overdraft_limit < amount:
            raise InsufficientFundsError("Недостаточно средств")
        self.balance -= amount
        return self.balance


class PaymentCard:
    def __init__(self, card_number, card_holder, expiration_date, cvv, issue_date, balance=0.0, currency="RUB"):
        self.card_number = card_number
        self.card_holder = card_holder
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.balance = balance
        self.currency = currency
        self.status = "active"
        self.daily_limit = 50000
        self.linked_account = None
        self.transaction_history = []

    def check_balance(self):
        return self.balance

    def change_pin(self, new_pin):
        """Изменить ПИН-код"""
        if len(new_pin) != 4:
            raise SecurityBreachError("ПИН-код должен содержать 4 цифры")
        return "PIN changed successfully"

    def transfer_money(self, target_card, amount):
        #Перевести деньги на другую карту
        if self.balance < amount:
            raise InsufficientFundsError("Недостаточно средств для перевода")
        if target_card.status != "active":
            raise InvalidCardError("Целевая карта не активна")

        self.balance -= amount
        target_card.balance += amount
        self.transaction_history.append(f"Transfer to {target_card.card_number}: {amount}")
        return "Transfer successful"


class DebitCard(PaymentCard):
    def __init__(self, card_number, card_holder, expiration_date, cvv, issue_date, balance=0.0, currency="RUB"):
        super().__init__(card_number, card_holder, expiration_date, cvv, issue_date, balance, currency)
        self.card_type = "Дебетовая"
        self.overdraft_protection = False


class CreditCard(PaymentCard):
    def __init__(self, card_number, card_holder, expiration_date, cvv, issue_date, credit_limit=100000, balance=0.0,
                 currency="RUB"):
        super().__init__(card_number, card_holder, expiration_date, cvv, issue_date, balance, currency)
        self.credit_limit = credit_limit
        self.card_type = "Кредитная"
        self.interest_rate = 0.25
        self.minimum_payment = 0

    def make_payment(self, amount):
        """Внести платеж по кредиту"""
        if amount < self.minimum_payment:
            raise InvalidTransactionError("Сумма меньше минимального платежа")
        self.balance -= amount
        return f"Payment of {amount} {self.currency} made"


# Кредитные продукты
class Loan:
    def __init__(self, loan_id, customer, amount, interest_rate, term_months):
        self.loan_id = loan_id
        self.customer = customer
        self.amount = amount
        self.interest_rate = interest_rate
        self.term_months = term_months
        self.remaining_amount = amount
        self.status = "active"
        self.monthly_payment = self.calculate_monthly_payment()

    def calculate_monthly_payment(self):
        """Рассчитать ежемесячный платеж"""
        monthly_rate = self.interest_rate / 12
        return (self.amount * monthly_rate) / (1 - (1 + monthly_rate) ** -self.term_months)

    def make_payment(self, amount):
        """Внести платеж по кредиту"""
        if amount < self.monthly_payment:
            raise InvalidTransactionError("Сумма меньше минимального платежа")
        self.remaining_amount -= amount
        return f"Остаток долга: {self.remaining_amount}"


class PersonalLoan(Loan):
    def __init__(self, loan_id, customer, amount, interest_rate, term_months, purpose):
        super().__init__(loan_id, customer, amount, interest_rate, term_months)
        self.loan_type = "Персональный"
        self.purpose = purpose


class CarLoan(Loan):
    def __init__(self, loan_id, customer, amount, interest_rate, term_months, car_model, vin):
        super().__init__(loan_id, customer, amount, interest_rate, term_months)
        self.loan_type = "Автокредит"
        self.car_model = car_model
        self.vin = vin
        self.collateral_value = amount * 0.8


class Mortgage(Loan):
    def __init__(self, loan_id, customer, amount, interest_rate, term_months, property_address, property_value):
        super().__init__(loan_id, customer, amount, interest_rate, term_months)
        self.loan_type = "Ипотека"
        self.property_address = property_address
        self.property_value = property_value
        self.down_payment = amount * 0.2


class BusinessLoan(Loan):
    def __init__(self, loan_id, customer, amount, interest_rate, term_months, business_plan, collateral):
        super().__init__(loan_id, customer, amount, interest_rate, term_months)
        self.loan_type = "Бизнес-кредит"
        self.business_plan = business_plan
        self.collateral = collateral


class LoanApplication:
    def __init__(self, application_id, customer, loan_type, amount, term_months, purpose):
        self.application_id = application_id
        self.customer = customer
        self.loan_type = loan_type
        self.amount = amount
        self.term_months = term_months
        self.purpose = purpose
        self.status = "pending"
        self.credit_check = None

    def process(self):
        if self.customer.credit_score < 600:
            self.status = "denied"
            raise LoanDeniedError("Низкий кредитный рейтинг")
        self.status = "approved"
        return "Заявка одобрена"

    def review(self):
        """Рассмотреть заявку"""
        return f"Заявка {self.application_id} на рассмотрении"


# Операции и транзакции
class Transaction:
    def __init__(self, transaction_id, amount, currency, description):
        self.transaction_id = transaction_id
        self.amount = amount
        self.currency = currency
        self.description = description
        self.status = "pending"
        self.timestamp = None

    def execute(self):
        self.status = "completed"
        self.timestamp = "now"
        return "Transaction executed"


class MoneyTransfer(Transaction):
    def __init__(self, transaction_id, amount, currency, description, sender, receiver):
        super().__init__(transaction_id, amount, currency, description)
        self.sender = sender
        self.receiver = receiver
        self.transfer_type = "internal"

    def validate_transfer(self):
        #Проверить валидность перевода
        if self.sender.balance < self.amount:
            raise InsufficientFundsError("Недостаточно средств у отправителя")
        return True


class DomesticTransfer(MoneyTransfer):
    def __init__(self, transaction_id, amount, currency, description, sender, receiver, bank_code):
        super().__init__(transaction_id, amount, currency, description, sender, receiver)
        self.bank_code = bank_code
        self.transfer_type = "domestic"


class InternationalTransfer(MoneyTransfer):
    def __init__(self, transaction_id, amount, currency, description, sender, receiver, swift_code):
        super().__init__(transaction_id, amount, currency, description, sender, receiver)
        self.swift_code = swift_code
        self.transfer_type = "international"
        self.exchange_rate = None

    def apply_exchange_rate(self, rate):
        """Применить курс обмена"""
        self.exchange_rate = rate
        self.amount *= rate


class Payment(Transaction):
    def __init__(self, transaction_id, amount, currency, description, payer, payee):
        super().__init__(transaction_id, amount, currency, description)
        self.payer = payer
        self.payee = payee
        self.payment_method = "bank_transfer"


class UtilityPayment(Payment):
    def __init__(self, transaction_id, amount, currency, description, payer, payee, utility_type, account_number):
        super().__init__(transaction_id, amount, currency, description, payer, payee)
        self.utility_type = utility_type
        self.account_number = account_number


class TaxPayment(Payment):
    def __init__(self, transaction_id, amount, currency, description, payer, payee, tax_type, tax_year):
        super().__init__(transaction_id, amount, currency, description, payer, payee)
        self.tax_type = tax_type
        self.tax_year = tax_year


class Withdrawal(Transaction):
    def __init__(self, transaction_id, amount, currency, description, account, location):
        super().__init__(transaction_id, amount, currency, description)
        self.account = account
        self.location = location


class CashWithdrawal(Withdrawal):
    def __init__(self, transaction_id, amount, currency, description, account, branch):
        super().__init__(transaction_id, amount, currency, description, account, branch)
        self.withdrawal_type = "cash"
        self.branch = branch


class ATMWithdrawal(Withdrawal):
    def __init__(self, transaction_id, amount, currency, description, account, atm):
        super().__init__(transaction_id, amount, currency, description, account, atm)
        self.withdrawal_type = "atm"
        self.atm = atm
        self.fee = 0 if account.bank == atm.bank else 1.5


class CurrencyExchange(Transaction):
    def __init__(self, transaction_id, amount, from_currency, to_currency, description, account):
        super().__init__(transaction_id, amount, from_currency, description)
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.account = account
        self.exchange_rate = None

    def calculate_conversion(self, rate):
        #раарассчитать конвертацию
        self.exchange_rate = rate
        return self.amount * rate


# Безопасность
class SecuritySystem:
    def __init__(self, system_id, system_type, status, security_level):
        self.system_id = system_id
        self.system_type = system_type
        self.status = status
        self.security_level = security_level
        self.last_maintenance = None

    def perform_maintenance(self):
       #Выполнить техническое обслужива
        self.last_maintenance = "now"
        return "Maintenance performed"


class AuthService(SecuritySystem):
    def __init__(self, system_id, status, security_level, max_attempts, timeout_duration):
        super().__init__(system_id, "authentication", status, security_level)
        self.max_attempts = max_attempts
        self.timeout_duration = timeout_duration
        self.two_factor_enabled = True
        self.failed_attempts = 0

    def authenticate_user(self, username, password):
        if self.failed_attempts >= self.max_attempts:
            raise AuthenticationError("Слишком много неудачных попыток")
        # Логика аутентификации
        return True


class PasswordValidator(SecuritySystem):
    def __init__(self, system_id, status, security_level, min_length, require_complexity):
        super().__init__(system_id, "password_validation", status, security_level)
        self.min_length = min_length
        self.require_complexity = require_complexity

    def validate_password(self, password):
        if len(password) < self.min_length:
            raise SecurityBreachError("Пароль слишком короткий")
        return True


class BiometricScanner:
    def __init__(self, scanner_id, scanner_type, accuracy, is_enabled):
        self.scanner_id = scanner_id
        self.scanner_type = scanner_type
        self.accuracy = accuracy
        self.is_enabled = is_enabled


class FingerprintScanner(BiometricScanner):
    def __init__(self, scanner_id, accuracy, is_enabled, resolution):
        super().__init__(scanner_id, "fingerprint", accuracy, is_enabled)
        self.resolution = resolution
        self.false_accept_rate = 0.001

    def scan_fingerprint(self):
        return "Fingerprint scanned"


class FacialRecognition(BiometricScanner):
    def __init__(self, scanner_id, accuracy, is_enabled, recognition_speed):
        super().__init__(scanner_id, "facial", accuracy, is_enabled)
        self.recognition_speed = recognition_speed
        self.mask_detection = True

    def recognize_face(self):
        """Распознать лицо"""
        return "Face recognized"


class AccessControl(SecuritySystem):
    def __init__(self, system_id, status, security_level, access_levels):
        super().__init__(system_id, "access_control", status, security_level)
        self.access_levels = access_levels
        self.access_log = []

    def grant_access(self, user, area):
        """Предоставить доступ"""
        if user.access_level not in self.access_levels.get(area, []):
            raise SecurityBreachError("Доступ запрещен")
        self.access_log.append(f"{user} accessed {area}")
        return "Access granted"


class FraudDetector(SecuritySystem):
    def __init__(self, system_id, status, security_level, detection_threshold):
        super().__init__(system_id, "fraud_detection", status, security_level)
        self.detection_threshold = detection_threshold
        self.suspicious_activities = []

    def detect_fraud(self, transaction):
        """Обнаружить мошенничество"""
        if transaction.amount > self.detection_threshold:
            self.suspicious_activities.append(transaction)
            raise SecurityBreachError("Подозрительная транзакция обнаружена")
        return "Transaction safe"


class SecurityCamera:
    def __init__(self, camera_id, location, resolution, is_recording):
        self.camera_id = camera_id
        self.location = location
        self.resolution = resolution
        self.is_recording = is_recording
        self.footage = []

    def start_recording(self):
        """Начать запись"""
        self.is_recording = True
        return "Recording started"


# Вспомогательные классы
class Currency:
    def __init__(self, code, name, symbol, decimal_places=2):
        self.code = code
        self.name = name
        self.symbol = symbol
        self.decimal_places = decimal_places

    def __str__(self):
        return f"{self.code} ({self.name})"

    def format_amount(self, amount):
        """Форматировать сумму"""
        return f"{amount:.{self.decimal_places}f} {self.symbol}"


class InterestRate:
    def __init__(self, rate, rate_type, effective_date, term):
        self.rate = rate
        self.rate_type = rate_type
        self.effective_date = effective_date
        self.term = term

    def calculate_interest(self, principal):
        """Рассчитать проценты"""
        if self.rate_type == "annual":
            return principal * self.rate
        elif self.rate_type == "monthly":
            return principal * self.rate / 12
        return 0


class ExchangeRate:
    def __init__(self, from_currency, to_currency, rate, last_updated):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.rate = rate
        self.last_updated = last_updated

    def convert(self, amount):
        """Конвертировать сумму"""
        return amount * self.rate

    def get_reverse_rate(self):
        """Получить обратный курс"""
        return ExchangeRate(self.to_currency, self.from_currency, 1 / self.rate, self.last_updated)


# Документы
class BankStatement:
    def __init__(self, statement_id, account, period_start, period_end, transactions):
        self.statement_id = statement_id
        self.account = account
        self.period_start = period_start
        self.period_end = period_end
        self.transactions = transactions
        self.opening_balance = 0
        self.closing_balance = 0

    def generate_statement(self):
        """Сгенерировать выписку"""
        self.closing_balance = self.opening_balance + sum(t.amount for t in self.transactions)
        return f"Выписка для счета {self.account.account_number}"


class Contract:
    def __init__(self, contract_id, parties, start_date, end_date, terms):
        self.contract_id = contract_id
        self.parties = parties
        self.start_date = start_date
        self.end_date = end_date
        self.terms = terms
        self.status = "active"

    def terminate_contract(self):
        """Расторгнуть договор"""
        self.status = "terminated"
        return "Contract terminated"


class LoanContract(Contract):
    def __init__(self, contract_id, parties, start_date, end_date, terms, loan_amount, interest_rate):
        super().__init__(contract_id, parties, start_date, end_date, terms)
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.remaining_balance = loan_amount


class DepositContract(Contract):
    def __init__(self, contract_id, parties, start_date, end_date, terms, deposit_amount, interest_rate):
        super().__init__(contract_id, parties, start_date, end_date, terms)
        self.deposit_amount = deposit_amount
        self.interest_rate = interest_rate
        self.maturity_date = end_date


class Receipt:
    def __init__(self, receipt_id, transaction, amount, currency, timestamp):
        self.receipt_id = receipt_id
        self.transaction = transaction
        self.amount = amount
        self.currency = currency
        self.timestamp = timestamp
        self.merchant = None

    def print_receipt(self):
        """Распечатать квитанцию"""
        return f"Квитанция #{self.receipt_id} на сумму {self.amount} {self.currency}"


class Notification:
    def __init__(self, notification_id, recipient, message, notification_type):
        self.notification_id = notification_id
        self.recipient = recipient
        self.message = message
        self.notification_type = notification_type
        self.status = "sent"

    def send_notification(self):
        """Отправить уведомление"""
        return f"Уведомление отправлено {self.recipient}"


class SMSNotification(Notification):
    def __init__(self, notification_id, recipient, message, phone_number):
        super().__init__(notification_id, recipient, message, "SMS")
        self.phone_number = phone_number

    def send_sms(self):
        """Отправить SMS"""
        return f"SMS отправлено на {self.phone_number}"


class EmailNotification(Notification):
    def __init__(self, notification_id, recipient, message, email_address):
        super().__init__(notification_id, recipient, message, "Email")
        self.email_address = email_address

    def send_email(self):
        """Отправить email"""
        return f"Email отправлен на {self.email_address}"


class Report:
    def __init__(self, report_id, report_type, generation_date, data):
        self.report_id = report_id
        self.report_type = report_type
        self.generation_date = generation_date
        self.data = data

    def generate_report(self):
        """Сгенерировать отчет"""
        return f"Отчет {self.report_type} сгенерирован"


class FinancialReport(Report):
    def __init__(self, report_id, generation_date, data, period):
        super().__init__(report_id, "financial", generation_date, data)
        self.period = period
        self.revenue = 0
        self.expenses = 0

    def calculate_profit(self):
        """Рассчитать прибыль"""
        return self.revenue - self.expenses


class AuditReport(Report):
    def __init__(self, report_id, generation_date, data, auditor):
        super().__init__(report_id, "audit", generation_date, data)
        self.auditor = auditor
        self.findings = []
        self.recommendations = []

    def add_finding(self, finding):
        """Добавить находку аудита"""
        self.findings.append(finding)


# Оборудование и системы
class ATM:
    def __init__(self, atm_id, location, cash_balance, status):
        self.atm_id = atm_id
        self.location = location
        self.cash_balance = cash_balance
        self.status = status
        self.branch = None
        self.transactions = []

    def dispense_cash(self, amount):
        """Выдать наличные"""
        if self.cash_balance < amount:
            raise InsufficientFundsError("В банкомате недостаточно средств")
        self.cash_balance -= amount
        return f"Выдано {amount} наличных"


class Server:
    def __init__(self, server_id, server_type, capacity, status):
        self.server_id = server_id
        self.server_type = server_type
        self.capacity = capacity
        self.status = status
        self.data_center = None
        self.uptime = 0

    def restart_server(self):
        """Перезагрузить сервер"""
        self.status = "restarting"
        return "Server restarting"


class Database:
    def __init__(self, db_id, db_type, size, backup_enabled):
        self.db_id = db_id
        self.db_type = db_type