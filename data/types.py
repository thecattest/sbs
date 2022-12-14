import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Type(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'types'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    subjects = orm.relation("Subject", back_populates="type")
    exams = orm.relation("Exam", back_populates="type")

    def __repr__(self):
        return f"<Type {self.id} {self.title}>"
