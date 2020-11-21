from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):  # database buat flask sqlalchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# cobacoba sapatau bisa, keren
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sender = db.Column(db.String(100), nullable=True)
    msg = db.Column(db.String(300), nullable=False)
    reply = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return '<Messages {}>'.format(self.msg)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
