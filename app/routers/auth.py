from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. db import get_session
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        #The idea is to just tell the user that the credentials are invalid, and not be specific
        #about which input was the invalid one
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token" : access_token, "token_type": "bearer"}