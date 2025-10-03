from app.db.connection import Database
from app.db.queries.programs import ProgramQueries
from app.db.queries.common import CommonQueries

from flask import current_app

class ProgramRepository:

    @staticmethod
    def get_program_by_program_code(program_code: str) -> dict | None:
        db = current_app.extensions['db']

        return db.fetch_one(CommonQueries.GET_BY_ID.format(table="programs", pk="program_code"), (program_code, ))

    @staticmethod
    def get_total_program_count(params) -> int:
        db = current_app.extensions['db']

        if params["search_value"]:

            if params["search_type"] == "Starts With":
                search_pattern = f"{params["search_value"]}%"
            elif params["search_type"] == "Ends With":
                search_pattern = f"%{params["search_value"]}"
            elif params["search_type"] == "Contains":
                search_pattern = f"%{params["search_value"]}%"
            else:
                search_pattern = params["search_value"]

            return db.fetch_one(CommonQueries.GET_TOTAL_COUNT_WITH_SEARCH.format(table="programs", search_by=f"{params["search_by"].lower().replace(' ', '_')}"),
                                (search_pattern,))
        
        else:
            return db.fetch_one(CommonQueries.GET_TOTAL_COUNT.format(table="programs"))

    def get_many_programs(params):
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
                            .format(table="programs", 
                                    search_by=f"{params["search_by"].lower().replace(' ', '_')}",
                                    sort_field=f"{params["sort_field"].lower().replace(' ', '_')}",
                                    sort_order=sort_order),
                            (search_pattern, params["rows_per_page"], offset))


    def create_program(program_data):
        db = current_app.extensions['db']

        db.execute_query(CommonQueries.INSERT.format(table="programs", columns="program_code, program_name, college_code", placeholders="%s, %s, %s"),
                         (program_data["programCode"], program_data["programName"], program_data["collegeCode"]))

    def delete_program(program_code: str):
        db = current_app.extensions['db']

        db.execute_query(CommonQueries.DELETE_BY_ID.format(table="programs", pk="program_code"), (program_code, ))

    def edit_program_details(program_code: str, new_program_data):
        db = current_app.extensions['db']

        db.execute_query(CommonQueries.UPDATE_BY_ID.format(table="programs", 
                                                           set_clause="program_code = %s, program_name = %s, college_code = %s", pk="program_code"), 
                                                           (new_program_data["programCode"], new_program_data["programName"], new_program_data["collegeCode"], program_code))   

    def get_program_codes():
        db = current_app.extensions['db']

        return db.fetch_all(CommonQueries.GET_ALL_IDS.format(columns="program_code, college_code", table="programs", order_column="college_code"))   
