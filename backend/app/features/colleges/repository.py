from app.db.connection import Database
from app.db.queries.colleges import CollegeQueries
from app.db.queries.common import CommonQueries

from flask import current_app

class CollegeRepository:

    @staticmethod
    def get_college_by_college_code(college_code: str) -> dict | None:
        db = current_app.extensions['db']

        return db.fetch_one(CommonQueries.GET_BY_ID.format(table="colleges", pk="college_code"), (college_code, ))

    @staticmethod
    def get_total_college_count() -> int:
        pass

    def get_many_colleges(params):
        pass

    def create_college(college_data):
        db = current_app.extensions['db']

        db.execute_query(CommonQueries.INSERT.format(table="colleges", columns="college_code, college_name", placeholders="%s, %s"),
                         (college_data["collegeCode"], college_data["collegeName"]))

    def delete_college(college_code: str):
        pass

    def edit_college_details(college_code: str, new_college_data):
        pass
