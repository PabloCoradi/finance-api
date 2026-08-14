from sqlalchemy.orm import Session
from models.expense import Expense
from schemas.expense import ExpenseCreate, ExpenseUpdate


def create_expense(db: Session, expense_data: ExpenseCreate) -> Expense:
    new_expense = Expense(
        description=expense_data.description,
        amount=expense_data.amount,
        date=expense_data.date,
        account_id=expense_data.account_id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


def get_expense_by_id(db: Session, account_id: int, expense_id: int) -> Expense | None:
    expense = db.query(Expense).filter(Expense.account_id ==
                                       account_id, Expense.id == expense_id).one_or_none()

    return expense


def get_expenses_by_account(db: Session, account_id: int) -> list[Expense]:
    expenses = db.query(Expense).filter(Expense.account_id ==
                                        account_id).all()

    return expenses


def update_expense(db: Session, account_id: int, expense_id: int, expense_data: ExpenseUpdate) -> Expense | None:
    expense = get_expense_by_id(db, account_id, expense_id)

    if not expense:
        return

    if expense_data.description is not None:
        expense.description = expense_data.description

    if expense_data.amount is not None:
        expense.amount = expense_data.amount

    if expense_data.date is not None:
        expense.date = expense_data.date

    db.commit()
    db.refresh(expense)

    return expense


def delete_expense(db: Session, account_id: int, expense_id: int) -> bool:
    expense = get_expense_by_id(db, account_id, expense_id)

    if not expense:
        return False

    db.delete(expense)
    db.commit()

    return True
