from app.db.connection import Database
from app.db.queries.students import StudentQueries
from app.db.queries.common import CommonQueries

from flask import current_app

class StudentRepository:

    @staticmethod
    def get_student_by_id(id_number: str) -> dict | None:
        db = current_app.extensions['db']

        return db.fetch_one(CommonQueries.GET_BY_ID.format(table="students", pk="id_number"), (id_number, ))

    @staticmethod
    def get_total_student_count(params) -> int:
        db = current_app.extensions['db']

        if sum(x is not None for x in [params["search_value"] , params["program_code"], params["college_code"]]) > 1:
            raise ValueError("Only one should exist at a time between search_value, program_code, and college_code")

        if params["search_value"]:

            if params["search_type"] == "Starts With":
                search_pattern = f"{params["search_value"]}%"
            elif params["search_type"] == "Ends With":
                search_pattern = f"%{params["search_value"]}"
            elif params["search_type"] == "Contains":
                search_pattern = f"%{params["search_value"]}%"
            else:
                search_pattern = params["search_value"]

            return db.fetch_one(CommonQueries.GET_TOTAL_COUNT_WITH_SEARCH.format(table="students", search_by=f"{params["search_by"].lower().replace(' ', '_')}"),
                                (search_pattern,))
        
        elif params["program_code"]:
            return db.fetch_one(StudentQueries.GET_TOTAL_COUNT_FROM_PROGRAM_CODE, (params["program_code"],))

        else:
            return db.fetch_one(CommonQueries.GET_TOTAL_COUNT.format(table="students"))

    def get_many_students(params):
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
                            .format(table="students", 
                                    search_by=f"{params["search_by"].lower().replace(' ', '_')}",
                                    sort_field=f"{params["sort_field"].lower().replace(' ', '_')}",
                                    sort_order=sort_order),
                            (search_pattern, params["rows_per_page"], offset))

    def create_student(student_data):
        db = current_app.extensions['db']

        db.execute_query(CommonQueries.INSERT.format(table="students", 
                                                     columns="id_number, first_name, last_name, year_level, gender, program_code",
                                                     placeholders="%s, %s, %s, %s, %s, %s"),
                                                     (student_data["idNumber"], student_data["firstName"], student_data["lastName"],
                                                      student_data["yearLevel"], student_data["gender"], student_data["programCode"]))

    def delete_student(id_number: str):
        db = current_app.extensions['db']

        db.execute_query(CommonQueries.DELETE_BY_ID.format(table="students", pk="id_number"), (id_number, ))

    def edit_student_details(id_number: str, new_student_data):
        db = current_app.extensions['db']

        db.execute_query(CommonQueries.UPDATE_BY_ID.format(table="students", 
                                                           set_clause="id_number = %s, first_name = %s, last_name = %s, " \
                                                           "year_level = %s, gender = %s, program_code = %s", pk="id_number"), 
                                                           (new_student_data["idNumber"], new_student_data["firstName"], new_student_data["lastName"],
                                                            new_student_data["yearLevel"], new_student_data["gender"], new_student_data["programCode"], 
                                                            id_number))  

    @staticmethod
    def get_year_level_demographics(params):
        db = current_app.extensions['db']

        if sum(x is not None for x in [params["program_code"], params["college_code"]]) > 1:
            raise ValueError("Only one should exist at a time between program_code, and college_code")
        
        if params["program_code"]:
            return db.fetch_all(StudentQueries.GET_YEAR_LEVEL_DEMOGRAPHICS_FROM_PROGRAM_CODE, (params["program_code"], ))
        
        return db.fetch_all(StudentQueries.GET_YEAR_LEVEL_DEMOGRAPHICS)
    
    @staticmethod
    def get_gender_demographics(params):
        db = current_app.extensions['db']

        if sum(x is not None for x in [params["program_code"], params["college_code"]]) > 1:
            raise ValueError("Only one should exist at a time between program_code, and college_code")
        
        if params["program_code"]:
            return db.fetch_all(StudentQueries.GET_GENDER_DEMOGRAPHICS_FROM_PROGRAM_CODE, (params["program_code"], ))

        return db.fetch_all(StudentQueries.GET_GENDER_DEMOGRAPHICS)
    