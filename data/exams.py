import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from json import loads, dumps

class Exam(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'exams'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('types.id'))
    subjects = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='[]')
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    places = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    registrations = orm.relation("Registration", back_populates="exam")
    type = orm.relation("Type")

    def add_subject(self, subject):
        self.subjects = dumps(loads(self.subjects).append(subject))

    def get_subjects(self):
        return loads(self.subjects)

    def __repr__(self):
        return f"<Exam {self.id} {self.type.title} {self.subjects} {self.date} {self.places} {self.price}>"
