from flask_restx import Namespace, Resource
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.db import db
from api.models.Bookmark import Bookmark
from api.models.User import User
from api.api_models import (
    bookmark_model_create,
    bookmark_model_out,
    bookmark_model_update,
)

# Define the namespace for bookmarks
bookmarks_ns = Namespace("bookmarks", description="Bookmark related operations")

# Define the model for a bookmark


@bookmarks_ns.route("/")
class BookmarkList(Resource):
    """BookmarkList Resource"""

    @jwt_required()
    @bookmarks_ns.marshal_list_with(bookmark_model_out, code=200)
    def get(self):
        """
        Get all bookmarks.
        """
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        # Fetch bookmarks for the authenticated user
        bookmarks = user.bookmarks.all()
        # If no bookmarks found, return 404
        if not bookmarks:
            abort(404, "No bookmarks found")
        return bookmarks, 200

    @jwt_required()
    @bookmarks_ns.expect(bookmark_model_create)
    @bookmarks_ns.marshal_with(bookmark_model_out, code=201)
    def post(self):
        """
        Create a new bookmark.
        """
        user_id = get_jwt_identity()
        # Ensure the user is authenticated
        data = bookmarks_ns.payload

        # Validate the input data
        if not data or "title" not in data or "url" not in data:
            abort(400, "Title and URL are required fields")
        if not data["url"].startswith(("http://", "https://")):
            abort(400, "URL must start with http:// or https://")
        if Bookmark.query.filter_by(user_id=user_id, title=data["title"]).first():
            abort(400, "You already have a bookmark with this title")
        if Bookmark.query.filter_by(user_id=user_id, url=data["url"]).first():
            abort(400, "You already have a bookmark with this URL")

        new_bookmark = Bookmark(title=data["title"], url=data["url"], user_id=user_id)
        db.session.add(new_bookmark)
        db.session.commit()
        return new_bookmark, 201


@bookmarks_ns.route("/<int:id>")
class SingleBookmark(Resource):
    """SingleBookmark Resource"""

    @jwt_required()
    @bookmarks_ns.marshal_with(bookmark_model_out, code=200)
    def get(self, id):
        """
        Get a bookmark by ID.
        """
        user_id = get_jwt_identity()
        # Fetch the bookmark by ID for the authenticated user
        bookmark = Bookmark.query.filter_by(id=id, user_id=user_id).first()

        if not bookmark:
            abort(404, "Bookmark not found")

        return bookmark, 200

    @jwt_required()
    @bookmarks_ns.expect(bookmark_model_update)
    @bookmarks_ns.marshal_with(bookmark_model_out, code=200)
    def put(self, id):
        """
        Update a bookmark by ID.
        """
        data = bookmarks_ns.payload
        user_id = get_jwt_identity()
        bookmark = Bookmark.query.filter_by(id=id, user_id=user_id).first()
        if not bookmark:
            abort(404, "Bookmark not found")
        bookmark.title = data["title"]
        bookmark.url = data["url"]
        db.session.commit()
        return bookmark, 200

    @jwt_required()
    @bookmarks_ns.response(200, "Bookmark deleted")
    def delete(self, id):
        """
        Delete a bookmark by ID.
        """
        user_id = get_jwt_identity()
        bookmark = Bookmark.query.filter_by(id=id, user_id=user_id).first()

        if not bookmark:
            abort(404, "Bookmark not found")

        db.session.delete(bookmark)
        db.session.commit()
        return {"message": "Bookmark deleted"}, 200
