from flask_restx import Api, fields

api = Api()

# User Request/response models
user_model_signup = api.model(
    "UserSignUp",
    {
        "email": fields.String(required=True, description="The email of the user"),
        "password": fields.String(
            required=True, description="The password of the user"
        ),
    },
)

user_model_login_in = api.model(
    "UserLoginIn",
    {
        "email": fields.String(required=True, description="The email of the user"),
        "password": fields.String(
            required=True, description="The password of the user"
        ),
    },
)

user_model_login_out = api.model(
    "UserLoginOut",
    {
        "id": fields.Integer(readonly=True, description="The ID of the user"),
        "email": fields.String(required=True, description="The email of the user"),
        "access token": fields.String(readonly=True, description="JWT access token"),
        "refresh token": fields.String(readonly=True, description="JWT refresh token"),
    },
)

# Bookmarks Request/Response model

bookmark_model_create = api.model(
    "BookmarkCreate",
    {
        "title": fields.String(required=True, description="The title of the bookmark"),
        "url": fields.String(required=True, description="The URL of the bookmark"),
        "user_id": fields.Integer(
            readonly=True, description="The ID of the user who owns the bookmark"
        ),
    },
)

bookmark_model_update = api.model(
    "BookmarksUpdate",
    {
        "title": fields.String(description="The title of the bookmark"),
        "url": fields.String(description="The URL of the bookmark"),
    },
)

bookmark_model_out = api.model(
    "BookmarksOut",
    {
        "id": fields.Integer(readonly=True, description="The ID of the bookmark"),
        "title": fields.String(required=True, description="The title of the bookmark"),
        "url": fields.String(required=True, description="The URL of the bookmark"),
        "user_id": fields.Integer(
            readonly=True, description="The ID of the user who owns the bookmark"
        ),
    },
)
