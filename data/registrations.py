import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Registration(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'registrations'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    exam_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('exams.id'))
    visited = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=False)

    user = orm.relation("User")
    exam = orm.relation("Exam")

    def __repr__(self):
        return f"<Registration {self.id} {self.user_id} {self.exam_id} {self.visited}>"
