import unittest
from datetime import datetime, timedelta


class InsufficientFundsError(Exception):
    pass


class SecurityBreachError(Exception):
    pass


class MembershipDeniedError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class EquipmentMaintenanceError(Exception):
    pass


class ClassFullError(Exception):
    pass


class TrainerUnavailableError(Exception):
    pass


class AgeRestrictionError(Exception):
    pass


class HealthRiskError(Exception):
    pass


class PaymentProcessingError(Exception):
    pass


class ScheduleConflictError(Exception):
    pass


class FacilityOvercrowdedError(Exception):
    pass


class Member:
    def __init__(self, name, surname, member_id, phone, email, age, health_conditions=None):
        self.name = name
        self.surname = surname
        self.member_id = member_id
        self.phone = phone
        self.email = email
        self.age = age
        self.health_conditions = health_conditions or []
        self.membership_status = "active"
        self.credit_score = 700
        self.attendance_count = 0

    def __str__(self):
        return f"Участник: {self.name} {self.surname}, ID: {self.member_id}"


class Trainer:
    def __init__(self, name, surname, trainer_id, specialization, salary, hire_date):
        self.name = name
        self.surname = surname
        self.trainer_id = trainer_id
        self.specialization = specialization
        self.salary = salary
        self.hire_date = hire_date
        self.schedule = {}

    def __str__(self):
        return f"Тренер: {self.name} {self.surname}, специализация: {self.specialization}"


class FitnessClass:
    def __init__(self, class_id, class_name, duration, max_capacity, difficulty_level):
        self.class_id = class_id
        self.class_name = class_name
        self.duration = duration
        self.max_capacity = max_capacity
        self.difficulty_level = difficulty_level
        self.current_enrollment = 0
        self.schedule = None

    def enroll_member(self, member):
        if self.current_enrollment >= self.max_capacity:
            raise ClassFullError("Класс переполнен")
        if member.age < 16 and self.difficulty_level == "advanced":
            raise AgeRestrictionError("Возрастное ограничение")
        self.current_enrollment += 1
        return f"{member.name} записан на {self.class_name}"


class Equipment:
    def __init__(self, equipment_id, name, category, purchase_date, maintenance_interval):
        self.equipment_id = equipment_id
        self.name = name
        self.category = category
        self.purchase_date = purchase_date
        self.maintenance_interval = maintenance_interval
        self.last_maintenance = purchase_date
        self.status = "operational"

    def needs_maintenance(self):
        next_maintenance = self.last_maintenance + timedelta(days=self.maintenance_interval)
        return datetime.now() > next_maintenance


class Membership:
    def __init__(self, membership_id, member, membership_type, start_date, end_date, price):
        self.membership_id = membership_id
        self.member = member
        self.membership_type = membership_type
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.is_active = True

    def check_validity(self):
        return datetime.now() <= self.end_date and self.is_active


class Payment:
    def __init__(self, payment_id, amount, currency, payment_date, payment_method):
        self.payment_id = payment_id
        self.amount = amount
        self.currency = currency
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.status = "pending"

    def process_payment(self):
        if self.amount <= 0:
            raise PaymentProcessingError("Неверная сумма платежа")
        self.status = "completed"
        return "Платеж обработан"


class WorkoutSession:
    def __init__(self, session_id, member, trainer, start_time, end_time, calories_burned):
        self.session_id = session_id
        self.member = member
        self.trainer = trainer
        self.start_time = start_time
        self.end_time = end_time
        self.calories_burned = calories_burned
        self.equipment_used = []

    def add_equipment(self, equipment):
        if equipment.status != "operational":
            raise EquipmentMaintenanceError("Оборудование неисправно")
        self.equipment_used.append(equipment)


class Facility:
    def __init__(self, facility_id, name, capacity, area, amenities):
        self.facility_id = facility_id
        self.name = name
        self.capacity = capacity
        self.area = area
        self.amenities = amenities
        self.current_occupancy = 0

    def check_availability(self):
        return self.current_occupancy < self.capacity


class NutritionPlan:
    def __init__(self, plan_id, member, calories, protein, carbs, fat, duration_days):
        self.plan_id = plan_id
        self.member = member
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.duration_days = duration_days
        self.start_date = datetime.now()

    def calculate_end_date(self):
        return self.start_date + timedelta(days=self.duration_days)


class HealthAssessment:
    def __init__(self, assessment_id, member, assessment_date, weight, height, bmi, blood_pressure):
        self.assessment_id = assessment_id
        self.member = member
        self.assessment_date = assessment_date
        self.weight = weight
        self.height = height
        self.bmi = bmi
        self.blood_pressure = blood_pressure

    def assess_health_risk(self):
        if self.bmi > 30:
            raise HealthRiskError("Высокий риск для здоровья")
        return "Низкий риск"


class GroupTraining:
    def __init__(self, training_id, trainer, facility, max_participants, training_type):
        self.training_id = training_id
        self.trainer = trainer
        self.facility = facility
        self.max_participants = max_participants
        self.training_type = training_type
        self.participants = []

    def add_participant(self, member):
        if len(self.participants) >= self.max_participants:
            raise ClassFullError("Группа переполнена")
        if not self.facility.check_availability():
            raise FacilityOvercrowdedError("Помещение переполнено")
        self.participants.append(member)
        self.facility.current_occupancy += 1


class Schedule:
    def __init__(self, schedule_id, trainer, facility, start_time, end_time, activity):
        self.schedule_id = schedule_id
        self.trainer = trainer
        self.facility = facility
        self.start_time = start_time
        self.end_time = end_time
        self.activity = activity

    def check_conflict(self, other_schedule):
        if (self.trainer == other_schedule.trainer and
                self.start_time < other_schedule.end_time and
                self.end_time > other_schedule.start_time):
            raise ScheduleConflictError("Конфликт расписания тренера")


class FitnessCenter:
    def __init__(self, center_id, name, location, operating_hours):
        self.center_id = center_id
        self.name = name
        self.location = location
        self.operating_hours = operating_hours
        self.members = []
        self.trainers = []
        self.equipment = []

    def add_member(self, member):
        self.members.append(member)

    def add_trainer(self, trainer):
        self.trainers.append(trainer)


class VIPMember:
    def __init__(self, name, surname, member_id, phone, email, age, vip_level, personal_trainer):
        self.name = name
        self.surname = surname
        self.member_id = member_id
        self.phone = phone
        self.email = email
        self.age = age
        self.vip_level = vip_level
        self.personal_trainer = personal_trainer
        self.exclusive_services = []

    def request_exclusive_service(self, service_name):
        result = f"Услуга {service_name} заказана для VIP клиента"
        self.exclusive_services.append(service_name)
        return result


class CorporateMembership:
    def __init__(self, contact_name, contact_surname, company_id, phone, email, company_name, employee_count):
        self.contact_name = contact_name
        self.contact_surname = contact_surname
        self.company_id = company_id
        self.phone = phone
        self.email = email
        self.company_name = company_name
        self.employee_count = employee_count
        self.member_accounts = []

    def add_employee_account(self, member):
        self.member_accounts.append(member)


class Transaction:
    def __init__(self, transaction_id, amount, currency, description):
        self.transaction_id = transaction_id
        self.amount = amount
        self.currency = currency
        self.description = description
        self.status = "pending"

    def execute(self):
        self.status = "completed"
        return "Transaction executed"


class MoneyTransfer:
    def __init__(self, transfer_id, amount, currency, description, from_account, to_account):
        self.transfer_id = transfer_id
        self.amount = amount
        self.currency = currency
        self.description = description
        self.from_account = from_account
        self.to_account = to_account

    def validate_transfer(self):
        if self.from_account.balance < self.amount:
            raise InsufficientFundsError("Недостаточно средств")
        return True


class AuthService:
    def __init__(self, service_id, status, security_level, max_attempts, timeout_duration):
        self.service_id = service_id
        self.status = status
        self.security_level = security_level
        self.max_attempts = max_attempts
        self.timeout_duration = timeout_duration
        self.failed_attempts = 0

    def authenticate_user(self, username, password):
        if self.failed_attempts >= self.max_attempts:
            raise AuthenticationError("Слишком много попыток")
        if username == "testuser" and password == "password123":
            self.failed_attempts = 0
            return True
        self.failed_attempts += 1
        return False


class PasswordValidator:
    def __init__(self, validator_id, status, strength_level, min_length, require_special_chars):
        self.validator_id = validator_id
        self.status = status
        self.strength_level = strength_level
        self.min_length = min_length
        self.require_special_chars = require_special_chars

    def validate_password(self, password):
        if len(password) < self.min_length:
            raise SecurityBreachError("Пароль слишком короткий")
        if self.require_special_chars and not any(char in "!@#$%^&*" for char in password):
            raise SecurityBreachError("Требуются специальные символы")
        return True


class MembershipApplication:
    def __init__(self, application_id, applicant, membership_type, duration, purpose):
        self.application_id = application_id
        self.applicant = applicant
        self.membership_type = membership_type
        self.duration = duration
        self.purpose = purpose
        self.status = "pending"

    def process(self):
        if self.applicant.credit_score < 600:
            raise MembershipDeniedError("Заявка отклонена")
        self.status = "approved"
        return "Заявка одобрена"


class EquipmentMaintenance:
    def __init__(self, maintenance_id, equipment, technician, maintenance_date, cost):
        self.maintenance_id = maintenance_id
        self.equipment = equipment
        self.technician = technician
        self.maintenance_date = maintenance_date
        self.cost = cost
        self.status = "scheduled"

    def perform_maintenance(self):
        self.status = "completed"
        self.equipment.last_maintenance = self.maintenance_date
        self.equipment.status = "operational"


class AttendanceTracker:
    def __init__(self, tracker_id, member, check_in_time, check_out_time):
        self.tracker_id = tracker_id
        self.member = member
        self.check_in_time = check_in_time
        self.check_out_time = check_out_time
        self.duration = None

    def calculate_duration(self):
        if self.check_out_time:
            self.duration = self.check_out_time - self.check_in_time
            return self.duration
        return None


class FitnessGoal:
    def __init__(self, goal_id, member, goal_type, target_value, deadline, current_value):
        self.goal_id = goal_id
        self.member = member
        self.goal_type = goal_type
        self.target_value = target_value
        self.deadline = deadline
        self.current_value = current_value
        self.progress = 0

    def update_progress(self, new_value):
        self.current_value = new_value
        self.progress = (self.current_value / self.target_value) * 100
        return self.progress


class PaymentAccount:
    def __init__(self, account_id, account_type, currency, balance):
        self.account_id = account_id
        self.account_type = account_type
        self.currency = currency
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if self.balance < amount:
            raise InsufficientFundsError("Недостаточно средств")
        self.balance -= amount
        return self.balance


class PersonalTraining:
    def __init__(self, training_id, member, trainer, start_time, end_time, focus_area):
        self.training_id = training_id
        self.member = member
        self.trainer = trainer
        self.start_time = start_time
        self.end_time = end_time
        self.focus_area = focus_area
        self.completed = False

    def mark_completed(self):
        self.completed = True
        return "Тренировка завершена"


class FitnessChallenge:
    def __init__(self, challenge_id, name, start_date, end_date, target_metric, prize):
        self.challenge_id = challenge_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.target_metric = target_metric
        self.prize = prize
        self.participants = []

    def add_participant(self, member):
        self.participants.append(member)
        return f"{member.name} присоединился к челленджу"


class Locker:
    def __init__(self, locker_id, size, location, rental_fee):
        self.locker_id = locker_id
        self.size = size
        self.location = location
        self.rental_fee = rental_fee
        self.occupied = False
        self.rented_to = None

    def rent_locker(self, member):
        if self.occupied:
            raise Exception("Шкафчик занят")
        self.occupied = True
        self.rented_to = member
        return f"Шкафчик {self.locker_id} арендован"


class Supplement:
    def __init__(self, supplement_id, name, category, price, dosage, benefits):
        self.supplement_id = supplement_id
        self.name = name
        self.category = category
        self.price = price
        self.dosage = dosage
        self.benefits = benefits
        self.in_stock = True

    def check_availability(self):
        return self.in_stock


class FitnessApp:
    def __init__(self, app_id, name, version, supported_platforms):
        self.app_id = app_id
        self.name = name
        self.version = version
        self.supported_platforms = supported_platforms
        self.users = []

    def add_user(self, member):
        self.users.append(member)
        return f"Пользователь {member.name} добавлен"


class WorkoutPlan:
    def __init__(self, plan_id, member, trainer, duration_weeks, workouts_per_week, focus):
        self.plan_id = plan_id
        self.member = member
        self.trainer = trainer
        self.duration_weeks = duration_weeks
        self.workouts_per_week = workouts_per_week
        self.focus = focus
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)
        return "Тренировка добавлена в план"


class BodyMeasurement:
    def __init__(self, measurement_id, member, measurement_date, chest, waist, hips, arms, legs):
        self.measurement_id = measurement_id
        self.member = member
        self.measurement_date = measurement_date
        self.chest = chest
        self.waist = waist
        self.hips = hips
        self.arms = arms
        self.legs = legs

    def calculate_change(self, previous_measurement):
        changes = {
            'chest': self.chest - previous_measurement.chest,
            'waist': self.waist - previous_measurement.waist,
            'hips': self.hips - previous_measurement.hips
        }
        return changes


class FitnessReport:
    def __init__(self, report_id, member, report_date, content, metrics):
        self.report_id = report_id
        self.member = member
        self.report_date = report_date
        self.content = content
        self.metrics = metrics

    def generate_summary(self):
        return f"Отчет для {self.member.name}: {self.content}"


class EmergencyContact:
    def __init__(self, contact_id, member, name, relationship, phone, email):
        self.contact_id = contact_id
        self.member = member
        self.name = name
        self.relationship = relationship
        self.phone = phone
        self.email = email

    def notify_emergency(self, message):
        return f"Уведомление отправлено {self.name}: {message}"


class FitnessCenterChain:
    def __init__(self, chain_id, name, headquarters, number_of_centers):
        self.chain_id = chain_id
        self.name = name
        self.headquarters = headquarters
        self.number_of_centers = number_of_centers
        self.centers = []

    def add_center(self, center):
        self.centers.append(center)
        return "Центр добавлен в сеть"


class MembershipPromotion:
    def __init__(self, promotion_id, name, description, discount_percent, start_date, end_date):
        self.promotion_id = promotion_id
        self.name = name
        self.description = description
        self.discount_percent = discount_percent
        self.start_date = start_date
        self.end_date = end_date
        self.eligible_members = []

    def add_eligible_member(self, member):
        self.eligible_members.append(member)
        return f"{member.name} добавлен в акцию"


class TrainerCertification:
    def __init__(self, certification_id, trainer, certification_name, issuing_organization, issue_date, expiry_date):
        self.certification_id = certification_id
        self.trainer = trainer
        self.certification_name = certification_name
        self.issuing_organization = issuing_organization
        self.issue_date = issue_date
        self.expiry_date = expiry_date
        self.valid = True

    def check_validity(self):
        if datetime.now() > self.expiry_date:
            self.valid = False
        return self.valid


class FitnessEquipmentRental:
    def __init__(self, rental_id, equipment, member, rental_date, return_date, deposit):
        self.rental_id = rental_id
        self.equipment = equipment
        self.member = member
        self.rental_date = rental_date
        self.return_date = return_date
        self.deposit = deposit
        self.returned = False

    def process_return(self):
        self.returned = True
        return "Оборудование возвращено"


class FitnessSocial:
    def __init__(self, social_id, member, post_content, post_date, likes, comments):
        self.social_id = social_id
        self.member = member
        self.post_content = post_content
        self.post_date = post_date
        self.likes = likes
        self.comments = comments

    def add_like(self):
        self.likes += 1
        return self.likes


class TestFitnessSystem(unittest.TestCase):

    def setUp(self):
        self.member = Member("Иван", "Иванов", "MEM001", "+79991234567", "ivan@mail.com", 25)
        self.trainer = Trainer("Петр", "Петров", "TRN001", "Йога", 50000, "2023-01-01")
        self.fitness_class = FitnessClass("CLS001", "Йога для начинающих", 60, 20, "beginner")
        self.equipment = Equipment("EQP001", "Беговая дорожка", "Кардио", datetime.now(), 90)
        self.facility = Facility("FAC001", "Зал йоги", 30, 100, ["маты", "зеркала"])
        self.payment_account = PaymentAccount("ACC001", "личный", "RUB", 1000)

    def test_member_creation(self):
        self.assertEqual(self.member.name, "Иван")
        self.assertEqual(str(self.member), "Участник: Иван Иванов, ID: MEM001")

    def test_trainer_creation(self):
        self.assertEqual(self.trainer.specialization, "Йога")
        self.assertEqual(str(self.trainer), "Тренер: Петр Петров, специализация: Йога")

    def test_fitness_class_enrollment(self):
        result = self.fitness_class.enroll_member(self.member)
        self.assertEqual(result, "Иван записан на Йога для начинающих")
        self.assertEqual(self.fitness_class.current_enrollment, 1)

    def test_equipment_maintenance_check(self):
        self.assertFalse(self.equipment.needs_maintenance())

    def test_payment_account_operations(self):
        new_balance = self.payment_account.deposit(500)
        self.assertEqual(new_balance, 1500)
        new_balance = self.payment_account.withdraw(300)
        self.assertEqual(new_balance, 1200)
        with self.assertRaises(InsufficientFundsError):
            self.payment_account.withdraw(2000)

    def test_facility_availability(self):
        self.assertTrue(self.facility.check_availability())
        self.facility.current_occupancy = 30
        self.assertFalse(self.facility.check_availability())

    def test_health_assessment_risk(self):
        assessment = HealthAssessment("ASS001", self.member, datetime.now(), 70, 175, 22.9, "120/80")
        result = assessment.assess_health_risk()
        self.assertEqual(result, "Низкий риск")
        risky_assessment = HealthAssessment("ASS002", self.member, datetime.now(), 120, 175, 39.2, "140/90")
        with self.assertRaises(HealthRiskError):
            risky_assessment.assess_health_risk()

    def test_group_training_participation(self):
        training = GroupTraining("GRP001", self.trainer, self.facility, 15, "Йога")
        result = training.add_participant(self.member)
        self.assertEqual(len(training.participants), 1)
        self.assertEqual(self.facility.current_occupancy, 1)

    def test_membership_application_approval(self):
        application = MembershipApplication("APP001", self.member, "годовой", 12, "фитнес")
        self.member.credit_score = 750
        result = application.process()
        self.assertEqual(result, "Заявка одобрена")
        self.assertEqual(application.status, "approved")

    def test_membership_application_denial(self):
        application = MembershipApplication("APP002", self.member, "годовой", 12, "фитнес")
        self.member.credit_score = 550
        with self.assertRaises(MembershipDeniedError):
            application.process()
        self.assertEqual(application.status, "pending")


class TestSecuritySystems(unittest.TestCase):

    def setUp(self):
        self.auth_service = AuthService("AUTH001", "active", "high", 3, 300)

    def test_authentication_success(self):
        result = self.auth_service.authenticate_user("testuser", "password123")
        self.assertTrue(result)

    def test_authentication_too_many_attempts(self):
        self.auth_service.failed_attempts = 3
        with self.assertRaises(AuthenticationError):
            self.auth_service.authenticate_user("testuser", "wrongpassword")

    def test_password_validation(self):
        validator = PasswordValidator("PWD001", "active", "medium", 8, True)
        self.assertTrue(validator.validate_password("SecurePass123!"))
        with self.assertRaises(SecurityBreachError):
            validator.validate_password("short")


if __name__ == "__main__":
    unittest.main()