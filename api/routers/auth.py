from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse
from db.database import get_db
from services.user_service import get_user_by_email, create_user

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
