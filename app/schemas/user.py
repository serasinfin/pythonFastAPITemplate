# Python
from datetime import time, datetime
# Pydantic
from pydantic import BaseModel, Field


# Basic user role
class RoleBase(BaseModel):
    role_name: str = Field(
        ...,
        min_length=2,
        max_length=30
    )


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):

    class Config:
        from_attributes = True


class RoleInDBBase(RoleBase):
    id: int

    class Config:
        from_attributes = True


class UserRole(RoleInDBBase):
    pass


# Basic user ability
class UserAbilityBase(BaseModel):
    action: str = Field(
        ...,
        min_length=2,
        max_length=30
    )
    subject: str = Field(
        ...,
        min_length=2,
        max_length=30
    )
    name: str = Field(
        ...,
        min_length=2,
        max_length=30
    )
    description: str = Field(
        max_length=250,
        default=None,
        description="Details of the ability"
    )


class UserAbilityCreate(UserAbilityBase):
    pass


class UserAbilityUpdate(UserAbilityBase):
    pass


class UserAbilityInDBBase(UserAbilityBase):
    id: int

    class Config:
        from_attributes = True


class UserAbility(UserAbilityInDBBase):
    pass


# Basic properties
class UserBase(BaseModel):
    """This class initializes a base User-class
    """
    username: str = Field(
        ...,
        min_length=2,
        max_length=30
    )
    name: str = Field(
        ...,
        min_length=2,
        max_length=30
    )
    phone_number: str = Field(
        min_length=10,
        max_length=12,
        default=""
    )
    email: str = Field(
        ...,
        min_length=5,
        max_length=250
    )
    active: bool = Field(
        default=True
    )
    allowed_schedule_start: time | None = Field(
        default=None
    )
    allowed_schedule_end: time | None = Field(
        default=None
    )


# Creation properties
class UserCreate(UserBase):
    role_id: int = Field(
        ...,
        gt=0
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=30
    )
    ability_list: list[int] = Field(..., description="List of abilities")


# Update user properties
class UserUpdate(UserBase):
    role_id: int = Field(
        ...,
        gt=0
    )
    ability_list: list[int] = Field(..., description="List of abilities")


class UserPasswordUpdate(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
        max_length=30
    )


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


# Additional properties to return via API
class User(UserInDBBase):
    role: UserRole
    abilities: list[UserAbility]


# User basic info to return in registers and logs
class UserBasicInfo(BaseModel):
    id: int
    name: str
    username: str
    role: UserRole

    class Config:
        from_attributes = True


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
