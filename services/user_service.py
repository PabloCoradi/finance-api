from schemas.user import UserCreate
from models.user import User
from sqlalchemy.orm import Session
from services.auth_service import hash_password


def create_user(db: Session, user_data: UserCreate) -> User:
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=(hash_password(user_data.password)
                  ))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_by_email(db: Session, email: str) -> User | None:
    user = db.query(User).filter(User.email == email).one_or_none()

    return user
