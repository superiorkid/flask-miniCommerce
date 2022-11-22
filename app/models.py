from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

from . import login_manager, db


class User(UserMixin, db.Model):
    # user auth
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String)

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    @property
    def password(self):
        raise AttributeError("Password is not a readable attributes")

    @password.setter
    def password(self, passwords):
        self.password_hash = generate_password_hash(passwords)

    def verify_password(self, passwords):
        return check_password_hash(self.password_hash, passwords)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
