import unittest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.routers.expenses import create_expense, update_expense, delete_expense, list_expenses
from app.routers.auth import register, login
from app.schemas import ExpenseCreate, ExpenseUpdate, UserCreate, LoginRequest
from app.models import User, Expense
import datetime


class TestRouteErrorHandling(unittest.TestCase):
    """Unit tests verifying route error handling and db.rollback() behavior."""

    def setUp(self):
        self.mock_user = User(id=1, name="Test User", email="test@example.com")
        self.mock_db = MagicMock()

    def test_create_expense_db_error_triggers_rollback_and_http500(self):
        self.mock_db.commit.side_effect = SQLAlchemyError("DB Connection Lost")
        expense_in = ExpenseCreate(
            amount=100.0,
            category="Food & Dining",
            date=datetime.date(2026, 11, 3),
            description="Test"
        )
        with self.assertRaises(HTTPException) as ctx:
            create_expense(expense_in=expense_in, db=self.mock_db, current_user=self.mock_user)

        self.assertEqual(ctx.exception.status_code, 500)
        self.assertIn("Database error", ctx.exception.detail)
        self.mock_db.rollback.assert_called_once()

    def test_update_expense_db_error_triggers_rollback_and_http500(self):
        # Setup mock expense owned by user
        mock_expense = Expense(id=10, user_id=1, amount=50, category="Food", date=datetime.date(2026, 11, 1))
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_expense
        self.mock_db.commit.side_effect = SQLAlchemyError("DB lock failure")

        update_in = ExpenseUpdate(amount=75.0)
        with self.assertRaises(HTTPException) as ctx:
            update_expense(expense_id=10, expense_in=update_in, db=self.mock_db, current_user=self.mock_user)

        self.assertEqual(ctx.exception.status_code, 500)
        self.assertIn("Database error", ctx.exception.detail)
        self.mock_db.rollback.assert_called_once()

    def test_delete_expense_db_error_triggers_rollback_and_http500(self):
        mock_expense = Expense(id=10, user_id=1, amount=50, category="Food", date=datetime.date(2026, 11, 1))
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_expense
        self.mock_db.commit.side_effect = SQLAlchemyError("DB disk full")

        with self.assertRaises(HTTPException) as ctx:
            delete_expense(expense_id=10, db=self.mock_db, current_user=self.mock_user)

        self.assertEqual(ctx.exception.status_code, 500)
        self.assertIn("Database error", ctx.exception.detail)
        self.mock_db.rollback.assert_called_once()

    def test_list_expenses_db_error_raises_http500(self):
        self.mock_db.query.return_value.filter.return_value.all.side_effect = SQLAlchemyError("Query error")

        with self.assertRaises(HTTPException) as ctx:
            list_expenses(db=self.mock_db, current_user=self.mock_user)

        self.assertEqual(ctx.exception.status_code, 500)
        self.assertIn("Database error", ctx.exception.detail)

    def test_register_db_error_triggers_rollback_and_http500(self):
        # Email check passes (no existing user)
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        self.mock_db.commit.side_effect = SQLAlchemyError("Insert error")

        user_in = UserCreate(name="New User", email="new@example.com", password="password123")
        with self.assertRaises(HTTPException) as ctx:
            register(user_in=user_in, db=self.mock_db)

        self.assertEqual(ctx.exception.status_code, 500)
        self.mock_db.rollback.assert_called_once()


if __name__ == "__main__":
    unittest.main()

