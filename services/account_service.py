from schemas.account import AccountCreate, AccountUpdate
from sqlalchemy.orm import Session
from models.account import Account


def create_account(db: Session, account_data: AccountCreate, user_id: int) -> Account:
    new_account = Account(
        type=account_data.type,
        interest=account_data.interest,
        user_id=user_id,
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account


def get_accounts_by_user(db: Session, user_id: int) -> list[Account]:
    accounts = db.query(Account).filter(Account.user_id == user_id).all()

    return accounts


def get_account_by_id(db: Session, user_id: int, account_id: int) -> Account | None:
    account = db.query(Account).filter(Account.user_id ==
                                       user_id, Account.id == account_id).one_or_none()

    return account


def update_account(db: Session, user_id: int, account_id: int, account_data: AccountUpdate) -> Account | None:
    account = get_account_by_id(db, user_id, account_id)

    if not account:
        return

    if account_data.type is not None:
        account.type = account_data.type

    if account_data.interest is not None:
        account.interest = account_data.interest

    db.commit()
    db.refresh(account)

    return account


def delete_account(db: Session, user_id: int, account_id: int) -> bool:
    account = get_account_by_id(db, user_id, account_id)

    if not account:
        return False

    db.delete(account)
    db.commit()

    return True
