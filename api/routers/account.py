from fastapi import APIRouter, Depends, HTTPException, status
from db.database import get_db
from sqlalchemy.orm import Session
from models.user import User
from api.dependencies import get_current_user
from schemas.account import AccountCreate, AccountResponse, AccountUpdate
from services.account_service import create_account, get_accounts_by_user, get_account_by_id, update_account, delete_account

router = APIRouter()


@router.post("")
def create_account_route(account_data: AccountCreate, user_data: User = Depends(get_current_user), db: Session = Depends(get_db)) -> AccountResponse:
    new_account = AccountResponse.model_validate(
        create_account(db, account_data, user_data.id))

    return new_account


@router.get("")
def get_accounts_route(user_data: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[AccountResponse]:
    accounts_list = get_accounts_by_user(db, user_data.id)

    new_list = [AccountResponse.model_validate(
        account) for account in accounts_list]

    return new_list


@router.get("/{account_id}")
def get_account_by_id_route(account_id: int, user_data: User = Depends(get_current_user), db: Session = Depends(get_db)) -> AccountResponse | None:
    account_exists = get_account_by_id(db, user_data.id, account_id)

    if account_exists is not None:
        account = AccountResponse.model_validate(account_exists)
        return account

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada."
        )


@router.put("/{account_id}")
def update_account_route(account_id: int, account_data: AccountUpdate, user_data: User = Depends(get_current_user), db: Session = Depends(get_db)) -> AccountResponse | None:
    account = update_account(
        db, user_data.id, account_id, account_data)

    if account is not None:
        return AccountResponse.model_validate(account)

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada."
        )


@router.delete("/{account_id}")
def delete_account_route(account_id: int, user_data: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    account = delete_account(db, user_data.id, account_id)

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada."
        )

    else:
        return {"detail": "Conta deletada com sucesso"}
