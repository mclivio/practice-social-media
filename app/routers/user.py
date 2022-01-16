from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. db import get_session

router = APIRouter(prefix='/users', tags=['users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, session : Session = Depends(get_session)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    #hashing the password that will be posted in the db
    new_user = models.User(**user.dict())
    # By turning the object into a regular python dict and unpacking it you avoid
    # having to pass it's attributes one by one if you already know they match the
    # column names of a database table.
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, session : Session = Depends(get_session)):
    user = session.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id: {id} does not exist")
    return user
