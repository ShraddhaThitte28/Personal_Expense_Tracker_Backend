from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Expense, User
from app.schemas import ExpenseCreate, ExpenseRead, ExpenseUpdate

router = APIRouter(prefix="/expenses", tags=["expenses"])


def _get_own_expense(expense_id: int, current_user: User, db: Session) -> Expense:
    """Return the expense only if it exists AND belongs to current_user.

    Raises HTTP 404 for both a nonexistent ID and an ID owned by another user,
    so callers cannot distinguish which case applies.
    """
    try:
        expense = (
            db.query(Expense)
            .filter(Expense.id == expense_id, Expense.user_id == current_user.id)
            .first()
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while retrieving expense",
        )

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )
    return expense


# ---------------------------------------------------------------------------
# POST /expenses — create
# ---------------------------------------------------------------------------

@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense_in: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new expense for the authenticated user."""
    expense = Expense(
        user_id=current_user.id,
        amount=expense_in.amount,
        category=expense_in.category,
        date=expense_in.date,
        description=expense_in.description,
    )
    db.add(expense)
    try:
        db.commit()
        db.refresh(expense)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while creating expense",
        )
    return expense


# ---------------------------------------------------------------------------
# GET /expenses — list
# ---------------------------------------------------------------------------

@router.get("", response_model=list[ExpenseRead])
def list_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return all expenses belonging to the authenticated user."""
    try:
        return (
            db.query(Expense)
            .filter(Expense.user_id == current_user.id)
            .all()
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while fetching expenses",
        )


# ---------------------------------------------------------------------------
# GET /expenses/{expense_id} — retrieve one
# ---------------------------------------------------------------------------

@router.get("/{expense_id}", response_model=ExpenseRead)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return a single expense belonging to the authenticated user."""
    return _get_own_expense(expense_id, current_user, db)


# ---------------------------------------------------------------------------
# PUT /expenses/{expense_id} — partial update
# ---------------------------------------------------------------------------

@router.put("/{expense_id}", response_model=ExpenseRead)
def update_expense(
    expense_id: int,
    expense_in: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Partially update an expense belonging to the authenticated user.

    Only fields that are explicitly present in the request body are written.
    Fields omitted from the request are left unchanged.
    `description` may be set to null; `amount`, `category`, and `date` may not.
    """
    expense = _get_own_expense(expense_id, current_user, db)

    # exclude_unset=True relies on model_fields_set internally:
    # only keys the caller actually sent are returned.
    for field, value in expense_in.model_dump(exclude_unset=True).items():
        setattr(expense, field, value)

    try:
        db.commit()
        db.refresh(expense)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while updating expense",
        )
    return expense


# ---------------------------------------------------------------------------
# DELETE /expenses/{expense_id} — delete
# ---------------------------------------------------------------------------

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an expense belonging to the authenticated user."""
    expense = _get_own_expense(expense_id, current_user, db)
    try:
        db.delete(expense)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while deleting expense",
        )
