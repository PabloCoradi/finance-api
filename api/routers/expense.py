from fastapi import APIRouter, Depends, HTTPException, status
from db.database import get_db
from sqlalchemy.orm import Session
from models.account import Account
from schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from services.expense_service import create_expense, get_expenses_by_account, get_expense_by_id, delete_expense, update_expense
from api.dependencies import get_owned_account

router = APIRouter()


@router.post("/accounts/{account_id}/expenses")
def create_expense_route(account_id: int, expense_data: ExpenseCreate, account: Account = Depends(get_owned_account), db: Session = Depends(get_db)) -> ExpenseResponse:
    new_expense = create_expense(db, expense_data, account_id)

    return ExpenseResponse.model_validate(new_expense)


@router.get("/accounts/{account_id}/expenses")
def get_expenses_route(account_id: int, account: Account = Depends(get_owned_account), db: Session = Depends(get_db)) -> list[ExpenseResponse]:
    expenses_list = get_expenses_by_account(db, account_id)

    new_list = [ExpenseResponse.model_validate(
        expense) for expense in expenses_list]

    return new_list


@router.get("/accounts/{account_id}/expenses/{expense_id}")
def get_expense_by_id_route(account_id: int, expense_id: int, account: Account = Depends(get_owned_account), db: Session = Depends(get_db)) -> ExpenseResponse | None:
    expense_exist = get_expense_by_id(db, account_id, expense_id)

    if expense_exist is not None:
        expense = ExpenseResponse.model_validate(expense_exist)
        return expense

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gasto não encontrado."
        )


@router.put("/accounts/{account_id}/expenses/{expense_id}")
def update_expense_route(account_id: int, expense_id: int, expense_data: ExpenseUpdate, account: Account = Depends(get_owned_account), db: Session = Depends(get_db)) -> ExpenseResponse | None:
    expense = update_expense(db, account_id, expense_id, expense_data)

    if expense is not None:
        return ExpenseResponse.model_validate(expense)

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gasto não encontrado."
        )


@router.delete("/accounts/{account_id}/expenses/{expense_id}")
def delete_expense_route(account_id: int, expense_id: int, account: Account = Depends(get_owned_account), db: Session = Depends(get_db)) -> dict:
    expense = delete_expense(db, account_id, expense_id)

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gasto não encontrado."
        )

    else:
        return {"detail": "Gasto deletado com sucesso"}
