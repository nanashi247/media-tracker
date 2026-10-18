from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from . import schemas, models
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from .config import settings
from app.database import get_db
from datetime import datetime, timedelta, timezone


oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_tokens(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def verify_access_tokens(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        user_id: str = payload.get("user_id")  #ignore

        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = user_id)

    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail=f"could not validate user credentials",
                                          headers = {"WWW-Authenticate": "Bearer"})

    token = verify_access_tokens(token, credentials_exception)

    user = db.query(models.User).filter(models.User.user_id == token.id).first()

    if user is None:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail=f"Couldn't validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
