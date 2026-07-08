from flask import Blueprint
from flask_restx import Resource, Api, fields
from apps.users.models import User
from apps.extentions import db
from flask_jwt_extended import create_access_token, jwt_required


blueprint = Blueprint("users_api", __name__, url_prefix="/root")
api = Api(blueprint, prefix="/api")

post_api_model = api.model("Post", {
    "title": fields.String,
    "created_at": fields.DateTime
})

user_api_model = api.model("User", {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "posts": fields.Nested(post_api_model)
})

user_input_api_model = api.model("UserInput", {
    "username": fields.String,
    "email": fields.String,
    "password": fields.String
})

@api.route("/users/<string:username>")
class UserApi(Resource):

    method_decorators = [jwt_required()]

    @api.marshal_with(user_api_model)
    def get(self, username):
        users = db.session.execute(db.select(User).where(User.username==username)).scalars().all()
        return users
    
    @api.marshal_with(user_api_model)
    @api.expect(user_input_api_model)
    def put(self, username):
        user = db.session.execute(db.select(User).where(User.username==username)).scalar()
        user.username = api.payload["username"]
        user.email = api.payload["email"]
        user.password = api.payload["password"]
        db.session.commit()
        return user, 200
    

    def delete(self, username):
        user = db.session.execute(db.select(User).where(User.username==username)).scalar()
        db.session.delete(user)
        db.session.commit()
        return {"result": "deleted"}, 200
    

@api.route("/users")
class UserCreateApi(Resource):
    @api.marshal_with(user_api_model)
    @api.expect(user_input_api_model)
    def post(Self):
        user = User(username=api.payload["username"], email=api.payload["email"], password=api.payload["password"])
        db.session.add(user)
        db.session.commit()
        return user, 201
    

@api.route("/users/login")
class UserLoginApi(Resource):

    @api.expect(user_input_api_model)
    def post(self):
        user = db.session.execute(db.select(User).where(username=api.payload["username"],
                                                        email=api.payload["email"],
                                                        password=api.payload["password"])).scalar()
        
        if not user:
            return {"result": "user not found"}, 404
        
        access_token = create_access_token(identity=user.email)
        return {"access_token": access_token}