# fastAPI
from fastapi import APIRouter, Depends, HTTPException, Path, Body, Query
# SQL Alchemy
from sqlalchemy.orm import Session
# Starlette
from starlette import status

# App
from app import schemas, crud
from app.api import jwt
from app.db.get_db import get_db

router = APIRouter()


# HTTP - GET

# Get users
# Search
@router.get(
    path="/",
    description="Please specify username or user id: [/users/?user_name=alex] or  [/users/?user_id=3]",
    response_model=list[schemas.User],
    status_code=status.HTTP_200_OK)
def get_users(
        user_id: int | None = Query(
            default=None,
            gt=0
        ),
        username: str | None = Query(
            default=None,
            min_length=2,
            max_length=30
        ),
        role_id: int | None = Query(
            default=None,
            gt=0
        ),
        email: str | None = Query(
            default=None,
            min_length=5,
            max_length=250
        ),
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(jwt.get_current_user)
) -> list[schemas.User]:
    return crud.user.get_all(db=db, user_id=user_id, username=username, role_id=role_id, email=email)

# HTTP - POST


# Post a user
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DefaultMessage,
)
def create(
        request: schemas.UserCreate = Body(...),
        db: Session = Depends(get_db),
        # current_user: schemas.User = Depends(jwt.get_current_user)
) -> any:
    user = crud.user.get_by(db, username=request.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe."
        )
    user = crud.user.get_by(db, email=request.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya existe."
        )

    try:
        crud.user.create(db, obj_in=request)
        return {"detail": "Usuario creado exitosamente."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# HTTP - PUT

# Update user by id
@router.put(
    path="/id/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.DefaultMessage
)
def update(
        user_id: int,
        request: schemas.UserUpdate = Body(...),
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(jwt.get_current_user)
) -> any:
    # Validate if user_id exists
    user = crud.user.get_by(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario con ese ID no existe."
        )
    # Validate if user(form) to update is not equal to user inDB
    if user.username != request.username:
        # Validate if username exists
        user = crud.user.get_by(db, username=request.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya existe."
            )

    crud.user.update(db, user_id=user_id, obj_in=request)
    return {"detail": "Usuario actualizado exitosamente."}


# Update user's password by id
@router.put(
    path="/password-update/id/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.DefaultMessage
)
def password_update(
        user_id: int,
        request: schemas.user.UserPasswordUpdate = Body(...),
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(jwt.get_current_user)
) -> any:
    user = crud.user.get_by(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario con ese ID no existe."
        )
    crud.user.password_update(db, user_id=user_id, obj_in=request)
    return {"detail": "Contraseña actualizada exitosamente."}


# HTTP - DELETE

# Delete user by id
@router.delete(
    path="/id/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.DefaultMessage,
)
def delete(
        user_id: int = Path(
            ...,
            gt=0
        ),
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(jwt.get_current_user)
) -> schemas.DefaultMessage:
    user = crud.user.get_by(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario con ese ID no existe."
        )
    crud.auth.delete_valid_token(db, user.username)
    crud.user.delete(db=db, user_id=user_id)
    return schemas.DefaultMessage(detail="Usuario eliminado exitosamente")
