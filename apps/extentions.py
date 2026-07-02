from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_hashing import Hashing
from flask_login import LoginManager


class Base(DeclarativeBase): pass
db = SQLAlchemy(model_class=Base)

hashing = Hashing()

login_manager = LoginManager()