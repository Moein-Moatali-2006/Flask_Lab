from apps.database import BaseModel
from apps.extentions import db, login_manager
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import mapped_column, relationship
from flask_login import UserMixin


@login_manager.user_loader
def user_loader(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()


class User(BaseModel, UserMixin):
    username =  mapped_column(String(50))
    email = mapped_column(String(80), unique=True)
    password = mapped_column(String(256), nullable=False)
    phone = mapped_column(String(11), unique=True)
    profile_pic = mapped_column(String, nullable=True)
    posts = relationship("Post", cascade="all, delete", backref="author")
    # age = mapped_column(Integer)

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.id}, {self.username})"


class Follow(BaseModel):
    follower = mapped_column(Integer)
    followed = mapped_column(Integer)


class Code(BaseModel):
    number = mapped_column(Integer)
    expire = mapped_column(DateTime, nullable=False)
    phone = mapped_column(String(11), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.phone}, {self.number})"