# Python
from jose import jwt, JWTError
# FastAPI
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
# SQL Alchemy
from sqlalchemy.orm import Session
# Starlette
from starlette import status

# App
from app import crud
from app.schemas import TokenData
from app.db.get_db import get_db
from app.core.config import settings
from app.utils.dates import current_time
from secrets import compare_digest

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.replace('"', ''), settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    user = crud.user.get_by(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    if not user.active:
        raise credentials_exception
    # if user.allowed_schedule_start is not None and user.allowed_schedule_end is not None:
    #     if user.allowed_schedule_start > current_time() or user.allowed_schedule_end < current_time():
    #         raise credentials_exception

    valid_token = crud.auth.get_valid_token(db, username=token_data.username)
    if valid_token is None or valid_token.token != token.replace('"', ''):
        raise credentials_exception
    return user
