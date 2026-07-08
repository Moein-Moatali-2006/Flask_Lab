import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CSRF_ENABLE = True
    CSRF_SESSION_KEY = "39e730d49a4005b9db3aacaec86a29980a20405b22bd85e0810a7ed3cbdbf41b"
    SECRET_KEY = "12f470cbd545add20835e8293002a5870aac464b27818345d3af4db44190ee5a"
    JWT_SECRET_KEY = "50b6eb86ef6f0d44495efbc5872507cadb43e2025ff88d58a1dce467a391d215"
    UPLOAD_FOLDER = "apps/static/uploads/"
    ALLOWED_EXTENTIONS = {"png", "jpg", "jpeg", "gif"}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ... # ellipsis


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Config.BASE_DIR, "project.db")
