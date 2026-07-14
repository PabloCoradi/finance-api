from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from db.database import get_db
from sqlalchemy.orm import Session
from models.user import User
from jose import jwt, JOSEError
import os
from dotenv import load_dotenv
from services.user_service import get_user_by_email

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(credentials.credentials,
                             SECRET_KEY, algorithms=["HS256"])
    except JOSEError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessão não autorizada."
        )

    user = get_user_by_email(db, payload['sub'])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessão não autorizada."
        )
    else:
        return user
