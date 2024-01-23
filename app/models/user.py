# Python
from datetime import datetime
# SQL Alchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table, Time
from sqlalchemy.orm import relationship

# App
from app.db.session import Base

user_to_abilities = Table(
    'user_to_abilities',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('ability_id', Integer, ForeignKey('user_abilities.id'))
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=True, default=None)
    email = Column(String, unique=True, nullable=True, default=None)
    role_id = Column(Integer, ForeignKey("user_roles.id"))
    active = Column(Boolean, default=True, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    allowed_schedule_start = Column(Time(timezone=True), nullable=True, default=None)
    allowed_schedule_end = Column(Time(timezone=True), nullable=True, default=None)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now())
    # Relationships
    role = relationship("UserRole", back_populates="users")
    abilities = relationship("UserAbility", secondary=user_to_abilities)   # many-to-many relationship


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    role_name = Column(String, nullable=False)
    # Relationships
    users = relationship("User", back_populates="role")


class UserAbility(Base):
    __tablename__ = "user_abilities"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    action = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
