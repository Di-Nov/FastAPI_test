from typing import List

from fastapi import APIRouter, Depends
from controllers.users import get_all_users
from sqlalchemy.orm import Session
from model.database import get_db
from model import schemas

router = APIRouter()


@router.get('/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_all_users(db, skip, limit)
    return users


@router.get('/{user_id}')
def read_user(user_id: int):
    return {'user_id': user_id, 'name': 'first'}
