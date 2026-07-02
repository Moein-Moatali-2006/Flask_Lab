from apps.database import BaseModel
from apps.extentions import db, login_manager
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from flask_login import UserMixin


@login_manager.user_loader
def user_loader(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()


class User(BaseModel, UserMixin):
    username =  mapped_column(String(50), nullable=False)
    email = mapped_column(String(80), unique=True, nullable=False)
    password = mapped_column(String(256), nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.id}, {self.username})"