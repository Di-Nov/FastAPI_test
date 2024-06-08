from model import schemas
from sqlalchemy.orm import Session
from sqlalchemy import select
from starlette import status

from model.core import User
from fastapi import HTTPException
from secure import pwd_context


def register(user_data: schemas.UserCreate, db: Session):
    if db.scalar(select(User).where(User.email == user_data.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='BAD_REQUEST'
        )
    user = User(email=user_data.email)
    user.hashed_password = pwd_context.hash(user_data.password)
    db.add(user)
    db.commit()
    return user
