from fastapi import APIRouter, Depends
from model import schemas, database
from http import HTTPStatus
from sqlalchemy.orm import Session
from controllers import tokens

router = APIRouter()


@router.post('', response_model=schemas.Token, status_code=HTTPStatus.CREATED)
def create_token(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return tokens.create_token(user_data=user_data, db=db)
