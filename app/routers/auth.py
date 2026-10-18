from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, oauth2


router = APIRouter(
    tags=  ['Authentication']
)

@router.post("/login", response_model= schemas.Token)
def login (UserCredentials: OAuth2PasswordRequestForm = Depends(), db:  Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == UserCredentials.username).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"invalid credentials")

    if not utils.verify(UserCredentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "invalid credentials")

    access_token = oauth2.create_access_tokens(data = {"user_id": user.user_id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

    






