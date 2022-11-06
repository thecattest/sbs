from flask_restful import Resource


class ExamListResource(Resource):
    def get(self):
        # метод похож на api.get_exams_by_month
        # только теперь в как url параметры будут переданы start и end
        # например ?start=2022-10-11&end=2022-10-30
        # выдавать список всех экзаменов между датами включительно
        pass

    def post(self):
        # api.create_exam
        # полная копия метода
        pass
