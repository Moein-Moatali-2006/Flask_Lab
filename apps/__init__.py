from flask import Flask
from apps.users.routes import blueprint as users_blueprint
from apps.posts.routes import blueprint as posts_blueprint
from apps.home.routes import blueprint as home_blueprint
from apps.extentions import db, hashing
import apps.exceptions as app_exception 


def register_blueprints(app):
    app.register_blueprint(users_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(home_blueprint)

def register_error_handlers(app):
    app.register_error_handler(404, app_exception.page_not_found)
    app.register_error_handler(500, app_exception.server_error)


app = Flask(__name__)
register_blueprints(app)
register_error_handlers(app)
app.config.from_object("config.DevConfig")


db.init_app(app)
from apps.users.models import User # is here due to circular_imports for db.create_all() use
with app.app_context(): db.create_all()

hashing.init_app(app)


