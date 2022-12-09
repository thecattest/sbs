import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

from random import randrange


class User(UserMixin, SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'
    ROLE_CLIENT = 0
    ROLE_ADMIN = 1

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    secondname = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    sms_code = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    sms_code_valid_thru = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    role = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True, default=ROLE_CLIENT)

    registrations = orm.relation("Registration", back_populates="user")

    @staticmethod
    def generate_sms_code():
        # return randrange(1111, 10000)
        return 1234

    def is_client(self):
        return self.role == self.ROLE_CLIENT

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def __repr__(self):
        return f"<User {self.id} {self.surname} {self.phone} {self.role}>"
