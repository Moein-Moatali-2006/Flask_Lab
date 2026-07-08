from flask import Flask
from apps.users.routes import blueprint as users_blueprint
from apps.posts.routes import blueprint as posts_blueprint
from apps.home.routes import blueprint as home_blueprint
from apps.users.api_routes import blueprint as users_api_blueprint
from apps.extentions import db, hashing, login_manager, jwt
import apps.exceptions as app_exception
from flask_migrate import Migrate


def register_blueprints(app):
    app.register_blueprint(users_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(users_api_blueprint)

def register_error_handlers(app):
    app.register_error_handler(404, app_exception.page_not_found)
    app.register_error_handler(403, app_exception.no_permission)
    app.register_error_handler(500, app_exception.server_error)

def register_shell_context(app):
    def shell_context():
        return {
            "db": db,
            "User": User,
            "Post": Post
        }

    app.shell_context_processor(shell_context)


app = Flask(__name__)
register_blueprints(app)
register_error_handlers(app)
register_shell_context(app)
app.config.from_object("config.DevConfig")


db.init_app(app)
from apps.users.models import User, Follow, Code # is here due to circular_imports for db.create_all() use
from apps.posts.models import Post
# with app.app_context(): db.create_all()
migrate = Migrate(app, db)

hashing.init_app(app)
jwt.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "users.login"
login_manager.login_message = "Please login first."
login_manager.login_message_category = "info"

@app.before_request
def befor_request():
    print("This is befor any request..!")

@app.after_request
def after_request(response):
    print("This is after any request..!")
    print(response)
    return response