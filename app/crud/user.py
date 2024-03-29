# SQL Alchemy
from sqlalchemy import asc
from sqlalchemy.orm import Session

# App
from app.core.security import get_password_hash
from app.schemas import UserCreate, UserUpdate, UserPasswordUpdate, RoleCreate, RoleUpdate, UserAbilityCreate, UserAbilityUpdate
from app.models.user import User, UserRole, UserAbility
from .CRUDBase import CRUDBase
from app.utils.dates import now


class CRUDUser(CRUDBase):

	def create(
			self, db: Session, *, obj_in: UserCreate
	) -> User:
		db_obj = User(
			name=obj_in.name,
			username=obj_in.username,
			phone_number=obj_in.phone_number,
			email=obj_in.email,
			role_id=obj_in.role_id,
			allowed_schedule_start=obj_in.allowed_schedule_start,
			allowed_schedule_end=obj_in.allowed_schedule_end,
			hashed_password=get_password_hash(obj_in.password),
			created_at=now(),
		)
		# Relations for Many-to-Many
		if obj_in.ability_list:
			db_obj.ability = []
			for ability_id in obj_in.ability_list:
				ability = db.query(UserAbility).filter(UserAbility.id == ability_id).first()
				db_obj.ability.append(ability)
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj

	def update(
			self, db: Session, user_id: int, *, obj_in: UserUpdate
	) -> None:
		db_obj = db.query(User).filter(User.id == user_id, User.deleted == False).first()
		try:
			if obj_in.name:
				db_obj.name = obj_in.name   # update name
			if obj_in.username:
				db_obj.username = obj_in.username   # update username
			if obj_in.phone_number:
				db_obj.phone_number = obj_in.phone_number   # update phone_number
			if obj_in.email:
				db_obj.email = obj_in.email  # update email
			if obj_in.role_id:
				db_obj.role_id = obj_in.role_id   # update role_id
			db_obj.active = obj_in.active   # update is_active
			# Relations for Many-to-Many
			if obj_in.ability_list:
				db_obj.abilities.clear()
				for ability_id in obj_in.ability_list:
					ability = db.query(UserAbility).filter(UserAbility.id == ability_id).first()
					db_obj.abilities.append(ability)
			db_obj.updated_at = now()
			db.add(db_obj)
			db.commit()
			db.refresh(db_obj)
			return db_obj
		except Exception as e:
			print(e)
			return None

	def password_update(
			self, db: Session, user_id: int, *, obj_in: UserPasswordUpdate
	) -> None:
		db_obj = {
			"hashed_password": get_password_hash(obj_in.password)
		}
		db.query(User).filter(User.id == user_id).update(db_obj)
		db.commit()
		return None

	def delete(
			self, db: Session, user_id: int
	) -> None:
		db_obj = {
			"deleted": True
		}
		db.query(User).filter(User.id == user_id).update(db_obj)
		db.commit()
		return None

	def get_by(
			self,
			db: Session,
			user_id: int = None,
			username: str = None,
			email: str = None,
			role_id: int = None,
	) -> User | None:
		if user_id:
			return db.query(User).filter(User.id == user_id).first()
		elif username:
			return db.query(User).filter(User.username == username).first()
		elif email:
			return db.query(User).filter(User.email == email).first()
		elif role_id:
			return db.query(User).filter(User.role_id == role_id).first()
		else:
			return None

	def get_all(
			self,
			db: Session,
			user_id: int = None,
			username: str = None,
			email: str = None,
			role_id: int = None,
	) -> list[User]:
		users = db.query(User).filter(User.deleted == False)

		if user_id:
			users = users.filter(User.id == user_id)
		if username:
			users = users.filter(User.username == username)
		if email:
			users = users.filter(User.email == email)
		if role_id:
			users = users.filter(User.role_id == role_id)

		return users.order_by(asc(User.name)).all()


class CRUDUserRoles(CRUDBase):

	def create(
			self, db: Session, *, obj_in: RoleCreate
	) -> RoleCreate:
		db_obj = UserRole(
			role_name=obj_in.role_name
		)
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj

	def update(
			self, db: Session, role_id: int, *, obj_in: RoleUpdate
	) -> None:
		db_obj = {
			"role_name": obj_in.role_name
		}
		db.query(UserRole).filter(UserRole.id == role_id).update(db_obj)
		db.commit()
		return None

	def get_all(
			self, db: Session
	) -> list[UserRole]:
		return db.query(UserRole).order_by(asc(UserRole.role_name)).all()

	def get_by_name(
			self, db: Session, *, role_name: str
	) -> UserRole | None:
		return db.query(UserRole).filter(UserRole.role_name == role_name).first()

	def get_by_id(
			self, db: Session, *, role_id: int
	) -> UserRole | None:
		return db.query(UserRole).filter(UserRole.id == role_id).first()


class CRUDUserAbility(CRUDBase):

	def create(
			self, db: Session, *, obj_in: UserAbilityCreate
	) -> UserAbilityCreate:
		db_obj = UserAbility(
			action=obj_in.action,
			subject=obj_in.subject,
			name=obj_in.name,
			description=obj_in.description
		)
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj

	def update(
			self, db: Session, user_ability_id: int, *, obj_in: UserAbilityUpdate
	) -> None:
		db_obj = {
			"action": obj_in.action,
			"subject": obj_in.subject,
			"name": obj_in.name,
			"description": obj_in.description
		}
		db.query(UserAbility).filter(UserAbility.id == user_ability_id).update(db_obj)
		db.commit()
		return None

	def get_all(
			self, db: Session
	) -> list[UserAbility]:
		return db.query(UserAbility).order_by(asc(UserAbility.name)).all()


user = CRUDUser()
user_roles = CRUDUserRoles()
user_ability = CRUDUserAbility()
