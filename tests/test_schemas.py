import datetime
from decimal import Decimal
import unittest
from pydantic import ValidationError

from app.schemas import (
    ExpenseCreate,
    ExpenseRead,
    ExpenseUpdate,
    LoginRequest,
    UserCreate,
)


class TestSchemas(unittest.TestCase):
    """Unit tests for Pydantic schema validation."""

    def test_expense_create_valid(self):
        data = {
            "amount": 149.99,
            "category": "Food & Dining",
            "date": "2026-11-03",
            "description": "Lunch with team",
        }
        exp = ExpenseCreate(**data)
        self.assertEqual(exp.amount, Decimal("149.99"))
        self.assertEqual(exp.category, "Food & Dining")
        self.assertEqual(exp.date, datetime.date(2026, 11, 3))
        self.assertEqual(exp.description, "Lunch with team")

    def test_expense_create_rejects_non_positive_amount(self):
        with self.assertRaises(ValidationError):
            ExpenseCreate(amount=0, category="Food", date="2026-11-03")

        with self.assertRaises(ValidationError):
            ExpenseCreate(amount=-50, category="Food", date="2026-11-03")

    def test_expense_create_rejects_empty_category(self):
        with self.assertRaises(ValidationError):
            ExpenseCreate(amount=100, category="", date="2026-11-03")

    def test_expense_update_partial_fields(self):
        update = ExpenseUpdate(amount=250.50, description="Updated desc")
        dump = update.model_dump(exclude_unset=True)
        self.assertEqual(dump, {"amount": Decimal("250.50"), "description": "Updated desc"})
        self.assertNotIn("category", dump)
        self.assertNotIn("date", dump)

    def test_expense_update_accepts_valid_date(self):
        update = ExpenseUpdate(date="2026-11-03")
        dump = update.model_dump(exclude_unset=True)
        self.assertEqual(dump.get("date"), datetime.date(2026, 11, 3))

    def test_expense_update_rejects_explicit_null_on_required_fields(self):
        with self.assertRaises(ValidationError):
            ExpenseUpdate(amount=None)

        with self.assertRaises(ValidationError):
            ExpenseUpdate(category=None)

        with self.assertRaises(ValidationError):
            ExpenseUpdate(date=None)

    def test_expense_update_allows_explicit_null_on_description(self):
        update = ExpenseUpdate(description=None)
        dump = update.model_dump(exclude_unset=True)
        self.assertIn("description", dump)
        self.assertIsNone(dump["description"])

    def test_user_create_validation(self):
        user = UserCreate(name="John Doe", email="john@example.com", password="password123")
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")

        with self.assertRaises(ValidationError):
            UserCreate(name="", email="john@example.com", password="password123")

    def test_login_request_validation(self):
        req = LoginRequest(email="user@test.com", password="pwd")
        self.assertEqual(req.email, "user@test.com")

        with self.assertRaises(ValidationError):
            LoginRequest(email="", password="pwd")


if __name__ == "__main__":
    unittest.main()

