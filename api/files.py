import io
from xlsxwriter import *
from datetime import *
from flask import Blueprint, send_file

from db_init import *

files_blueprint = Blueprint('files', __name__)


def return_phone(user):
    return user.phone


@files_blueprint.route('/files/day/<datas>', methods=['GET'])
def generate_upload_file(datas):
    session = db_session.create_session()
    Exams = session.query(Exam).filter(Exam.date.contains(datetime.strptime(datas, "%Y-%m-%d").date())).all()
    print(Exams)
    table_of_contents = (["Дата:", datas], ["Экзамен", "Предмет", "Время", "Участники", "Цена", "Участники"])
    Alterable = list()
    for exam in Exams:
        Listing = list()
        Listing.append(exam.type.title)
        Listing.append(exam.subject.title)
        Listing.append(str(exam.date)[11:16])
        Listing.append(
            f'{session.query(Exam).filter((exam.date == Exam.date) and (exam.type.title == Exam.type.title) and (exam.subject.title == Exam.subject.title)and(exam.price ==Exam.price)).count()} / {exam.places}')
        Listing.append(exam.price)
        Listing.append(return_phone(session.query(User).filter(exam.id == User.id).first()))
        Alterable.append(Listing)

    new_list = list()
    for var in Alterable:
        new_list.append(var[:5])

    for var in sorted(new_list):
        if new_list.count(var) > 1:
            new_list.remove(var)

    close_list = list()
    for var in new_list:
        var.append('Номера')
        close_list.append(var)
        for j in Alterable:
            if var[:5] == j[:5]:
                if close_list.count(j[:5]) > 1:
                    close_list.append(j)
                else:
                    for i in range(0, len(j), 1):
                        if i == 5:
                            break
                        j[i] = ' '

                close_list.append(j)

    for var in range(0, len(table_of_contents), 1):
        close_list.insert(var, table_of_contents[var])

    file_io = io.BytesIO()
    wb = Workbook(file_io)
    ws = wb.add_worksheet(f'{datas}')
    ws.set_column(1, 6, 13)

    for row_num, dat in enumerate(close_list):
        ws.write_row(row_num, 0, dat)

    wb.close()
    file_io.seek(0)
    return send_file(file_io, as_attachment=True, download_name=f'{datas}.xlsx')
