# FastAPI
from fastapi import APIRouter, Depends, Body
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

# Get all abilities
@router.get("/", response_model=list[schemas.UserAbility], status_code=status.HTTP_200_OK)
def get_all(
		db: Session = Depends(get_db),
		skip: int = 0,
		limit: int = 100,
		*,
		current_user: schemas.User = Depends(jwt.get_current_user),
) -> list[schemas.UserAbility]:
	"""
	Get all abilities
	"""
	abilities = crud.user_ability.get_all(db, skip=skip, limit=limit)
	return abilities


# Create a new ability
@router.post("/", response_model=schemas.DefaultMessage, status_code=status.HTTP_201_CREATED,)
def create(
		request: schemas.UserAbilityCreate = Body(...),
		db: Session = Depends(get_db),
		current_user: schemas.User = Depends(jwt.get_current_user),
) -> schemas.DefaultMessage:
	"""
	Create a new ability
	"""
	crud.user_ability.create(db, obj_in=request)
	return schemas.DefaultMessage(detail="Ability created")
