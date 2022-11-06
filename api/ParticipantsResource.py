from flask_restful import Resource


class ParticipantsResource(Resource):
    def post(self, exam_id, participant_id):
        # копия метода api.order_exam + сотрудник теперь тоже может записывать
        # проверить, что экзамен существует, до него минимум 3 дня, клиент существует
        # если это сотрудник, то
        # записать клиента с id=participant_id на экзамен с id=exam_id
        # если это клиент, то
        # записать клиента с id=current_user.id на экзамен с id=exam_id
        # значение participant_id в этом случае не используется и ни на что не влияет
        pass

    def delete(self, exam_id, participant_id):
        # кусок метода api.unregister + сотрудник теперь тоже может удалять
        # проверить, что экзамен существует, ещё не прошёл, клиент существует
        # если это сотрудник, то
        # выписать клиента с id=participant_id с экзамена с id=exam_id
        # если это клиент, то
        # выписать клиента с id=current_user.id с экзамена с id=exam_id
        # значение participant_id в этом случае не используется и ни на что не влияет
        pass


