from app.db.connection import Database
from app.db.queries.colleges import CollegeQueries
from app.db.queries.common import CommonQueries

class CollegeRepository:

    @staticmethod
    def get_college_by_college_code(college_code: str) -> dict | None:
        return Database().fetch_one(CommonQueries.GET_BY_ID.format(table="colleges", pk="college_code"), (college_code, ))

    @staticmethod
    def get_total_college_count() -> int:
        pass

    def get_many_colleges(params):
        pass

    def create_college(college_data):
        pass

    def delete_college(college_code: str):
        pass

    def edit_college_details(college_code: str, new_college_data):
        pass
