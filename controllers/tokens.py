import uuid
from starlette import status
from fastapi import HTTPException
from sqlalchemy import select

from model import schemas
from sqlalchemy.orm import Session
from model.core import User, Token
from secure import pwd_context

def create_token(user_data: schemas.UserCreate, db: Session):
    user: User = db.scalar(select(User).where(User.email == user_data.email))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')

    try:
        pwd_context.verify(user_data.password, user.hashed_password)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD_REQUEST')
    token: Token = Token(user_id=user.id, access_token=str(uuid.uuid4()))
    db.add(token)
    db.commit()
    return {'access_token': token.access_token}

