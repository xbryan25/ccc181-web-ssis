from app.db.connection import Database
from app.db.queries.students import StudentQueries
from app.db.queries.common import CommonQueries

class StudentRepository:

    @staticmethod
    def get_student_by_id(id_number: str) -> dict | None:
        return Database().fetch_one(CommonQueries.GET_BY_ID.format(table="students", pk="id_number"), (id_number, ))

    @staticmethod
    def get_total_student_count() -> int:
        pass

    def get_many_students(params):
        pass

    def create_student(student_data):
        pass

    def delete_student(id_number: str):
        pass

    def edit_student_details(id_number: str, new_student_data):
        pass
