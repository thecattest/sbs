import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Exam(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'exams'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('types.id'))
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subjects.id'))
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    places = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    registrations = orm.relation("Registration", back_populates="exam")
    type = orm.relation("Type")
    subject = orm.relation("Subject")

    def __repr__(self):
        return f"<Exam {self.id} {self.type.title} {self.subject.title} {self.date} {self.places} {self.price}>"
