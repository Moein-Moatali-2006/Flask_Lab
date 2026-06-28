from apps.database import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import mapped_column


class User(BaseModel):
    username =  mapped_column(String(50), nullable=False)
    email = mapped_column(String(80), unique=True, nullable=False)
    password = mapped_column(String(256), nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.id}, {self.username})"