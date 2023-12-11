# SQLAlchemy
from sqlalchemy.orm import Session

# App
from .CRUDBase import CRUDBase
from app.models import ValidToken
from app.utils.dates import now


class CRUDAuth(CRUDBase):

    def create_valid_token(
            self, db: Session, username: str = None, token: str = None, user_ip: str = None
    ) -> ValidToken:
        db_obj = ValidToken(
            username=username,
            token=token,
            user_ip=user_ip,
            updated_at=now()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_valid_token(
            self, db: Session, username: str = None
    ) -> ValidToken:
        return db.query(ValidToken).filter(ValidToken.username == username).first()

    def update_valid_token(
            self, db: Session, username: str = None, token: str = None, user_ip: str = None
    ) -> ValidToken:
        db_obj = db.query(ValidToken).filter(
            ValidToken.username == username
        ).first()
        if db_obj:
            db_obj.token = token
            db_obj.user_ip = user_ip
            db_obj.updated_at = now()
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_valid_token(
            self, db: Session, username: str = None
    ) -> bool:
        db_obj = db.query(ValidToken).filter(
            ValidToken.username == username
        ).first()
        if db_obj:
            db.delete(db_obj)
        db.commit()
        return True


auth = CRUDAuth()
