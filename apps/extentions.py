from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_hashing import Hashing
from flask_login import LoginManager
from kavenegar import KavenegarAPI
from flask_restx import Api
from flask_jwt_extended import JWTManager


class Base(DeclarativeBase): pass
db = SQLAlchemy(model_class=Base)

hashing = Hashing()

login_manager = LoginManager()

sms_api = KavenegarAPI("") # API key token

jwt = JWTManager()