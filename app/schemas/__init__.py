# Pydantic
from pydantic import BaseModel
# App schemas
from .user import User, UserCreate, UserUpdate, UserPasswordUpdate, UserRole, RoleCreate, RoleUpdate, UserAbility, \
    UserAbilityCreate, UserAbilityUpdate

from .auth import Token, TokenData, Login, TokenStr


class HelloResponse(BaseModel):
    message: str


class DefaultMessage(BaseModel):
    detail: str
