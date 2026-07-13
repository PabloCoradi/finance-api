from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse, UserLogin
from db.database import get_db
from services.user_service import get_user_by_email, create_user
from schemas.token import Token
from services.auth_service import verify_password, create_access_token

router = APIRouter()


@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:

    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado."
        )

    else:
        new_user = UserResponse.model_validate(create_user(db, user_data))

        return new_user


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)) -> Token:
    user_exists = get_user_by_email(db, user_data.email)

    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    if not verify_password(user_data.password, user_exists.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    data = {
        "sub": user_exists.email
    }

    created_token = create_access_token(data)

    return Token(access_token=created_token, token_type="bearer")
