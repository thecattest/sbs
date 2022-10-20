import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Subject(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'subjects'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('types.id'))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    type = orm.relation("Type")
    exams = orm.relation("Exam", back_populates="subject")

    def __repr__(self):
        return f"<Subject {self.id} {self.type_id} {self.title}>"
