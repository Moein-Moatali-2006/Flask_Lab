from apps.extentions import db
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import mapped_column

class BaseModel(db.Model):
    __abstract__ = True

    id = mapped_column(Integer, primary_key=True)
    created_at = mapped_column(DateTime, default=db.func.current_timestamp())
    updated_at = mapped_column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

