# fastAPI
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
# SQL Alchemy
from sqlalchemy.orm import Session
# Starlette
from starlette import status

# App
from app import schemas, crud
from app.core.security import verify_password, create_access_token, decode_token
from app.db.get_db import get_db
from app.utils.dates import current_time
from secrets import compare_digest

router = APIRouter()


@router.post(
	path="/login",
	response_model=schemas.Token,
	status_code=status.HTTP_202_ACCEPTED
)
def login(
		request: OAuth2PasswordRequestForm = Depends(),
		raw_request: Request = None,
		db: Session = Depends(get_db)
) -> any:
	user = crud.user.get_by(db=db, username=request.username)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Usuario o contraseña incorrectos",
		)
	if not user.active:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Usuario inactivo",
		)
	if user.deleted:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Usuario eliminado",
		)
	if not verify_password(
			plain_password=request.password,
			hashed_password=user.hashed_password
	):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Usuario o contraseña incorrectos",
		)

	if user.allowed_schedule_start is not None and user.allowed_schedule_end is not None:
		if user.allowed_schedule_start > current_time() or user.allowed_schedule_end < current_time():
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Usuario fuera de horario",
			)

	access_token = create_access_token(
		data={
			"sub": user.username,
			"role": user.role.role_name
		}
	)
	# SAVE VALID TOKEN
	token_active = crud.auth.get_valid_token(db, username=user.username)
	user_ip = raw_request.client.host
	if token_active:
		crud.auth.update_valid_token(db, token_active.username, access_token, user_ip)
	else:
		crud.auth.create_valid_token(db, user.username, access_token, user_ip)

	token = {
		"user_data": {
			"id": user.id,
			"name": user.name,
			"username": user.username,
			"role": user.role.role_name,
			"ability": user.ability,
			"phone": user.phone_number,
			"email": user.email,
			"password": None
		},
		"access_token": access_token,
		"token_type": "bearer"
	}
	return token

@router.post(
	path="/me",
	response_model=schemas.Token,
	status_code=status.HTTP_200_OK
)
def me(
		access_token: str,
		db: Session = Depends(get_db)
) -> any:
	# Delete "" from token
	access_token = access_token.replace('"', '')
	decoded_token = decode_token(access_token)
	if not decoded_token:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Token inválido",
		)

	valid_token = crud.auth.get_valid_token(db, username=decoded_token.get("sub"))
	if not compare_digest(access_token, valid_token.token):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Token inválido",
		)

	user = crud.user.get_by(db=db, username=decoded_token.get("sub"))
	token = {
		"user_data": {
			"id": user.id,
			"name": user.name,
			"username": user.username,
			"role": user.role.role_name,
			"ability": user.ability,
			"phone": user.phone_number,
			"email": user.email,
			"password": None
		},
		"access_token": access_token,
		"token_type": "bearer"
	}

	return token
