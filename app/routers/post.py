from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from .. db import get_session

router = APIRouter(prefix='/posts', tags=['posts'])

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(session: Session = Depends(get_session),
current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = session.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, session: Session = Depends(get_session), 
current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # By turning the object into a regular python dict and unpacking it you avoid
    # having to pass it's attributes one by one if you already know they match the
    # column names of a database table.
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, session: Session = Depends(get_session),
current_user: int = Depends(oauth2.get_current_user)):
    post = session.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: Session = Depends(get_session),
current_user: int = Depends(oauth2.get_current_user)):
    post_query = session.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
         detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, session: Session = Depends(get_session),
current_user: int = Depends(oauth2.get_current_user)):
    post_query = session.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
         detail="Not authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    session.commit()
    return post_query.first()