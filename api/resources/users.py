from flask_restx import Namespace, Resource
from flask import abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from api.db import db
from api.models.User import User
from api.models.RevokedToken import RevokedToken
from api.api_models import user_model_signup, user_model_login_in, user_model_login_out

# Define the namespace for users
users_ns = Namespace("users", description="User related operations")


@users_ns.route("/signup")
class UserSignUp(Resource):
    @users_ns.expect(user_model_signup)
    @users_ns.response(201, "User created successfully")
    def post(self):
        """User signup"""
        data = users_ns.payload

        if not data or "email" not in data or "password" not in data:
            abort(400, "Email and password are required")

        if User.query.filter_by(email=data["email"]).first():
            abort(400, "User with this email already exists")

        password = pbkdf2_sha256.hash(data["password"])
        new_user = User(email=data["email"], password=password)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201


@users_ns.route("/login")
class UserLogin(Resource):
    @users_ns.expect(user_model_login_in)
    @users_ns.marshal_with(user_model_login_out, code=200)
    def post(self):
        """User login"""
        data = users_ns.payload

        if not data or "email" not in data or "password" not in data:
            abort(400, "Email and password are required")

        user = User.query.filter_by(email=data["email"]).first()

        if not user or not pbkdf2_sha256.verify(data["password"], user.password):
            abort(401, "Invalid email or password")

        access_token = create_access_token(identity=str(user.id))
        return {"id": user.id, "email": user.email, "access token": access_token}, 200


@users_ns.route("/logout")
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        revoked_token = RevokedToken(token=jti)
        db.session.add(revoked_token)
        db.session.commit()
        return {"message": "successfully loged out"}
