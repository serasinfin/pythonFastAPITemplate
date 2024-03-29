# FastAPI
from fastapi import APIRouter, Depends, HTTPException, Body, Query
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

# Get all roles
@router.get(
	path="/",
	response_model=list[schemas.UserRole],
	status_code=status.HTTP_200_OK
)
def get_all(
		db: Session = Depends(get_db),
		current_user: schemas.User = Depends(jwt.get_current_user)
) -> list:
	user_roles = crud.user_roles.get_all(db)
	return user_roles


# Search
@router.get(
	path="/search/",
	response_model=schemas.UserRole,
	status_code=status.HTTP_200_OK
)
def search(
		role_id: int = Query(
			default=None,
			gt=0
		),
		role_name: str = Query(
			default=None,
			min_length=2,
			max_length=30
		),
		db: Session = Depends(get_db),
		current_user: schemas.User = Depends(jwt.get_current_user)
) -> any:
	if role_id:
		role = crud.user_roles.get_by(db, role_id=role_id)
		if not role:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="El rol con este id no existe en el sistema."
			)
		return role
	if role_name:
		role = crud.user_roles.get_by(db, role_name=role_name)
		if not role:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="El rol con este nombre no existe en el sistema."
			)
		return role
	if not role_id or role_name:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Por favor especifique el id o el nombre del rol."
		)
	return None


# HTTP - POST

# Create a new role
@router.post(
	path="/",
	status_code=status.HTTP_201_CREATED,
	response_model=schemas.DefaultMessage,
)
def create(
		request: schemas.RoleCreate = Body(...),
		db: Session = Depends(get_db),
		# current_user: schemas.User = Depends(jwt.get_current_user)
) -> schemas.DefaultMessage:
	role = crud.user_roles.get_by_name(db, role_name=request.role_name)
	if role:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="El rol ya existe."
		)
	crud.user_roles.create(db, obj_in=request)
	return schemas.DefaultMessage(detail="Rol creado exitosamente.")
