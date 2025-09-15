import unittest
from datetime import datetime, timedelta

from fitnes_system import (
    Member, Trainer, FitnessClass, Equipment, Facility, PaymentAccount,
    HealthAssessment, GroupTraining, MembershipApplication, WorkoutSession,
    NutritionPlan, AttendanceTracker, FitnessGoal, AuthService, PasswordValidator,
    InsufficientFundsError, ClassFullError, HealthRiskError, MembershipDeniedError,
    AuthenticationError, SecurityBreachError
)

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
        self.assertEqual(self.member.surname, "Иванов")
        self.assertEqual(str(self.member), "Участник: Иван Иванов, ID: MEM001")

    def test_trainer_creation(self):
        self.assertEqual(self.trainer.trainer_id, "TRN001")
        self.assertEqual(self.trainer.specialization, "Йога")
        self.assertEqual(str(self.trainer), "Тренер: Петр Петров, специализация: Йога")

    def test_fitness_class_enrollment_success(self):
        result = self.fitness_class.enroll_member(self.member)
        self.assertEqual(result, "Иван записан на Йога для начинающих")
        self.assertEqual(self.fitness_class.current_enrollment, 1)

    def test_fitness_class_enrollment_full(self):
        self.fitness_class.current_enrollment = 20
        with self.assertRaises(ClassFullError):
            self.fitness_class.enroll_member(self.member)

    def test_equipment_maintenance_check(self):
        self.assertFalse(self.equipment.needs_maintenance())
        old_date = datetime.now() - timedelta(days=100)
        self.equipment.last_maintenance = old_date
        self.assertTrue(self.equipment.needs_maintenance())

    def test_payment_account_deposit(self):
        new_balance = self.payment_account.deposit(500)
        self.assertEqual(new_balance, 1500)

    def test_payment_account_withdraw_success(self):
        new_balance = self.payment_account.withdraw(300)
        self.assertEqual(new_balance, 700)

    def test_payment_account_withdraw_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.payment_account.withdraw(2000)

    def test_facility_availability(self):
        self.assertTrue(self.facility.check_availability())
        self.facility.current_occupancy = 30
        self.assertFalse(self.facility.check_availability())

    def test_health_assessment_low_risk(self):
        assessment = HealthAssessment("ASS001", self.member, datetime.now(), 70, 175, 22.9, "120/80")
        result = assessment.assess_health_risk()
        self.assertEqual(result, "Низкий риск")

    def test_health_assessment_high_risk(self):
        assessment = HealthAssessment("ASS002", self.member, datetime.now(), 120, 175, 39.2, "140/90")
        with self.assertRaises(HealthRiskError):
            assessment.assess_health_risk()

    def test_group_training_add_participant(self):
        training = GroupTraining("GRP001", self.trainer, self.facility, 15, "Йога")
        training.add_participant(self.member)
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

    def test_workout_session_add_equipment(self):
        session = WorkoutSession("SESS001", self.member, self.trainer, datetime.now(), datetime.now(), 300)
        session.add_equipment(self.equipment)
        self.assertEqual(len(session.equipment_used), 1)

    def test_nutrition_plan_calculation(self):
        plan = NutritionPlan("NUT001", self.member, 2000, 150, 250, 70, 30)
        end_date = plan.calculate_end_date()
        self.assertIsInstance(end_date, datetime)

    def test_attendance_tracker_duration(self):
        check_in = datetime.now()
        check_out = check_in + timedelta(hours=2)
        tracker = AttendanceTracker("TRK001", self.member, check_in, check_out)
        duration = tracker.calculate_duration()
        self.assertEqual(duration.total_seconds(), 7200)

    def test_fitness_goal_progress(self):
        goal = FitnessGoal("GOAL001", self.member, "weight_loss", 10, datetime.now(), 5)
        progress = goal.update_progress(7)
        self.assertEqual(progress, 70.0)

class TestSecuritySystems(unittest.TestCase):

    def setUp(self):
        self.auth_service = AuthService("AUTH001", "active", "high", 3, 300)

    def test_authentication_success(self):
        result = self.auth_service.authenticate_user("testuser", "password123")
        self.assertTrue(result)

    def test_authentication_failure(self):
        result = self.auth_service.authenticate_user("testuser", "wrongpass")
        self.assertFalse(result)
        self.assertEqual(self.auth_service.failed_attempts, 1)

    def test_authentication_too_many_attempts(self):
        self.auth_service.failed_attempts = 3
        with self.assertRaises(AuthenticationError):
            self.auth_service.authenticate_user("testuser", "wrongpassword")

    def test_password_validation_success(self):
        validator = PasswordValidator("PWD001", "active", "medium", 8, True)
        self.assertTrue(validator.validate_password("SecurePass123!"))

    def test_password_validation_too_short(self):
        validator = PasswordValidator("PWD001", "active", "medium", 8, True)
        with self.assertRaises(SecurityBreachError):
            validator.validate_password("short")

    def test_password_validation_no_special_chars(self):
        validator = PasswordValidator("PWD001", "active", "medium", 8, True)
        with self.assertRaises(SecurityBreachError):
            validator.validate_password("SecurePass123")

if __name__ == "__main__":
    unittest.main()