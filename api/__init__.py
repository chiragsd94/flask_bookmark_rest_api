from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from api.models.User import User
from api.models.Bookmark import Bookmark
from api.models.RevokedToken import RevokedToken
import os

from .db import db
import api.resources.bookmarks as bookmarks_ns
import api.resources.users as users_ns

# Load environment variables
load_dotenv()


# flask app factory pattern
def create_app():
    # define flask app
    app = Flask(__name__)

    # Config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # Extensions
    CORS(app)  # add cors
    db.init_app(app)  # initialize db
    Migrate(app, db)  # initialize db migrate
    api = Api(app)  # initialize api
    jwt = JWTManager(app)  # initialize jwt

    # check is token in blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        revoked_t = RevokedToken.query.filter_by(token=jwt_payload["jti"]).first()
        return revoked_t

    # check is token revoked
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    # check is token expired
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "toekn_expired"}),
            401,
        )

    # check is token invalid
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    # check token is unauthorized
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # Namespaces
    api.add_namespace(bookmarks_ns.bookmarks_ns, path="/api/v1/bookmarks")
    api.add_namespace(users_ns.users_ns, path="/api/v1/users")

    # return app
    return app
