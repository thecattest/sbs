from db_init import *
from datetime import datetime


db = db_session.create_session()

t = Type()
t.title = 'ЕГЭ'
db.add(t)
db.commit()

s = Subject()
s.title = 'Математика профиль'
s.type_id = db.query(Type).first().id
db.add(s)
db.commit()

u = User()
u.phone = '+79286209317'
u.role = u.ROLE_ADMIN
db.add(u)
db.commit()

e = Exam()
e.type_id = t.id
e.subjects = '[1]'
e.places = 30
e.price = 350
e.date = datetime.utcnow()
db.add(e)
db.commit()

r = Registration()
r.exam_id = e.id
r.user_id = u.id
db.add(r)
db.commit()

print(t)
print(s)
print(u)
print(u.registrations)
print(e)
print(e.registrations)
print(r)
print(r.exam, r.user)
db.close()