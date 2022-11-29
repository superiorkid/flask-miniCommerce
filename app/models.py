from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from itsdangerous.serializer import Serializer
from hashlib import md5
from datetime import datetime

from . import login_manager, db


class User(UserMixin, db.Model):
    # user auth
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(40), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    # user information
    fname = db.Column(db.String(30), nullable=True)
    lname = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(30), nullable=True)
    city = db.Column(db.String(30), nullable=True)
    state = db.Column(db.String(30), nullable=True)
    country = db.Column(db.String(30), nullable=True)
    zipcode = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(20), nullable=True)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['IS_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self) -> str:
        return f'<User {self.fname} {self.lname}>'

    @property
    def password(self):
        raise AttributeError("Password is not a readable attributes")

    @password.setter
    def password(self, passwords):
        self.password_hash = generate_password_hash(passwords)

    def verify_password(self, passwords):
        return check_password_hash(self.password_hash, passwords)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({"confirm": self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get("confirm") != self.id:
            return False

        self.confirmed = True
        self.confirmed_on = datetime.now()
        db.session.add(self)
        db.session.commit()
        return True


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return f"<Role {self.name}>"

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.SHOPPING, True),
            'Operator': (Permission.SHOPPING | Permission.PRODUCT_MANAGEMENT, False),
            'Administrator': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    SHOPPING = 0x01
    PRODUCT_MANAGEMENT = 0x02
    ADMINISTER = 0x80


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    regural_price = db.Column(db.DECIMAL)

    def __repr__(self):
        return f"<{self.id} | {self.product_name}>"
