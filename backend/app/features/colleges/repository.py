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
        db = current_app.extensions['db']

        return db.fetch_one(CommonQueries.GET_TOTAL_COUNT.format(table="colleges"))

    def get_many_colleges(params):
        db = current_app.extensions['db']

        if params["search_type"] == "Starts With":
            search_pattern = f"{params["search_value"]}%"
        elif params["search_type"] == "Ends With":
            search_pattern = f"%{params["search_value"]}"
        elif params["search_type"] == "Contains":
            search_pattern = f"%{params["search_value"]}%"
        else:
            search_pattern = params["search_value"]

        if params["sort_order"] == "Ascending":
            sort_order = "ASC"
        else:
            sort_order = "DESC"

        offset = (params["page_number"] - 1) * params["rows_per_page"]

        return db.fetch_all(CommonQueries.GET_MANY
                            .format(table="colleges", 
                                    search_by=f"{params["search_by"].lower().replace(' ', '_')}",
                                    sort_field=f"{params["sort_field"].lower().replace(' ', '_')}",
                                    sort_order=sort_order),
                            (search_pattern, params["rows_per_page"], offset))

    def create_college(college_data):
        db = current_app.extensions['db']

        db.execute_query(CommonQueries.INSERT.format(table="colleges", columns="college_code, college_name", placeholders="%s, %s"),
                         (college_data["collegeCode"], college_data["collegeName"]))

    def delete_college(college_code: str):
        db = current_app.extensions['db']

        return db.execute_query(CommonQueries.DELETE_BY_ID.format(table="colleges", pk="college_code"), (college_code, ))

    def edit_college_details(college_code: str, new_college_data):
        db = current_app.extensions['db']

        db.execute_query(CommonQueries.UPDATE_BY_ID.format(table="colleges", set_clause="college_code = %s, college_name = %s", pk="college_code"), (new_college_data["collegeCode"], new_college_data["collegeName"], college_code))   
