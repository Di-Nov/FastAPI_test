from sqlalchemy.orm import Session
from sqlalchemy import select
from model import core
from fastapi import HTTPException
from starlette import status


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(core.User).offset(skip).limit(limit).all()


def get_authorization_by_token(access_token: str, db: Session):
    try:
        token = db.scalar(select(core.Token).where(access_token == core.Token.access_token))
        return token.user
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='UNAUTHORIZED')
