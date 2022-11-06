from flask_restful import Resource


class ExamResource(Resource):
    def get(self, exam_id):
        # полная копия api.get_exam_by_id, вернуть экзамен вместе со списком участников
        pass

    def put(self, exam_id):
        # полная копия метода api.set_visited
        # вернуть exam.to_json()
        pass

    def delete(self, exam_id):
        # кусок метода api.unregister
        # проверить роль -- админ, проверить что экз существует,
        # проверить что список участников пуст, проверить что экз ещё не прошел
        # удалить экзамен
        # с ролью клиент сюда нельзя
        pass
