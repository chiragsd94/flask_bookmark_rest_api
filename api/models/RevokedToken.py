from api.db import db


class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(5000))
