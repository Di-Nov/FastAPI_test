from typing import List, Annotated

from fastapi import APIRouter, Depends
from views.users import get_all_users, get_authorization_by_token
from sqlalchemy.orm import Session
from model.database import get_db
from model import schemas
from http import HTTPStatus
from controllers.users import register
import secure

router = APIRouter()


@router.get('/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_all_users(db, skip, limit)
    return users


@router.get('/{user_id}')
def read_user(user_id: int):
    return {'user_id': user_id, 'name': 'first'}


@router.post('/create_user', response_model=schemas.LiteUser, status_code=HTTPStatus.CREATED)
def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return register(user_data, db)


@router.post('/self', response_model=schemas.LiteUser)
def get_token_by_authorization(token: Annotated[str, Depends(secure.apikey_scheme)], db: Session = Depends(get_db)):
    return get_authorization_by_token(access_token=token, db=db)
