from flask import Flask
from apps.users.routes import blueprint as users_blueprint
from apps.posts.routes import blueprint as posts_blueprint
from apps.extentions import db


def register_blueprints(app):
    app.register_blueprint(users_blueprint)
    app.register_blueprint(posts_blueprint)


app = Flask(__name__)
register_blueprints(app)
app.config.from_object("config.DevConfig")


db.init_app(app)
from apps.users.models import User # is here due to circular_imports for db.create_all() use
with app.app_context(): db.create_all()


