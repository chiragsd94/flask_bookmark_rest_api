from api.db import db


class User(db.Model):
    """User model for storing user information in the database."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    bookmarks = db.relationship("Bookmark", back_populates="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.email}>"
