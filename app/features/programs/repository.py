from app.db.connection import Database
from app.db.queries.programs import ProgramQueries
from app.db.queries.common import CommonQueries

from flask import current_app

class ProgramRepository:

    @staticmethod
    def get_program_by_program_code(program_code: str) -> dict[str, str] | None:
        """
        Retrieve a program record from the database by program code.

        Args:
            program_code (str): The unique program code of the program.

        Returns:
            dict: A dictionary containing the program's details if found, otherwise None.
        """

        db = current_app.extensions['db']

        return db.fetch_one(CommonQueries.GET_BY_ID.format(table="programs", pk="program_code"), (program_code, ))

    @staticmethod
    def get_total_program_count(params) -> dict[str, int]:
        """
        Retrieve the total number of programs based on a specific filter.

        Args:
            params (dict): A dictionary of filtering parameters. Expected keys include:
                            - "search_value" (str | None): Text to search for in a specific column.
                            - "search_type" (str | None): The search matching type. One of "Starts With", "Ends With" or "Contains".
                            - "search_by" (str | None): The column name to apply the search on.
                            - "college_code" (str | None): The college code to filter programs by.

        Returns:
            dict: A dictionary containing the total number of programs that match the given filter.

        Raises:
            ValueError: If more than one of "search_value", or "college_code" is provided.

        Note:
            Only one of "search_value", or "college_code" should be provided at a time. Otherwise, a ValueError is raised.
        """

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
        
        elif params["college_code"]:
            return db.fetch_one(ProgramQueries.GET_TOTAL_COUNT_FROM_COLLEGE_CODE, (params["college_code"],))
        
        else:
            return db.fetch_one(CommonQueries.GET_TOTAL_COUNT.format(table="programs"))

    @staticmethod
    def get_many_programs(params) -> list[dict[str, str]]:
        """
        Retrieve a paginated list of programs based on search and sorting parameters.

        Args:
            params (dict): A dictionary of query parameters. Expected keys include:
                - "search_value" (str): Text to search for in a specific column.
                - "search_type" (str): Search matching type. One of "Starts With", "Ends With" or "Contains".
                - "search_by" (str): Column name to apply the search on.
                - "sort_field" (str): Column name to sort the results by.
                - "sort_order" (str): Sort direction, either "Ascending" or "Descending".
                - "page_number" (int): Current page number for pagination.
                - "rows_per_page" (int): Number of records to retrieve per page.

        Returns:
            list[dict]: A list of program records matching the given filters, 
            where each record is represented as a dictionary.
        """

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

        offset = 0 if params["page_number"] <= 0 else (params["page_number"] - 1) * params["rows_per_page"]

        return db.fetch_all(CommonQueries.GET_MANY
                            .format(table="programs", 
                                    search_by=f"{params["search_by"].lower().replace(' ', '_')}",
                                    sort_field=f"{params["sort_field"].lower().replace(' ', '_')}",
                                    sort_order=sort_order),
                            (search_pattern, params["rows_per_page"], offset))

    @staticmethod
    def create_program(program_data) -> None:
        """
        Insert a new program record into the database.

        Args:
            program_data (dict): A dictionary containing the program's details.
                Expected keys include:
                    - "program_code" (str): The unique code of the program.
                    - "program_name" (str): The name of the program.
                    - "college_code" (str): The code of the academic program the student belongs to.
        """

        db = current_app.extensions['db']

        db.execute_query(CommonQueries.INSERT.format(table="programs", columns="program_code, program_name, college_code", placeholders="%s, %s, %s"),
                         (program_data["program_code"], program_data["program_name"], program_data["college_code"]))

    @staticmethod
    def delete_programs(program_codes: list[str]) -> None:
        """
        Delete program records from the database using their program codes.

        Args:
            program_codes (list[str]): A list of unique program codes of the programs to delete.
        """

        db = current_app.extensions['db']

        db.execute_query(CommonQueries.DELETE_BY_ID.format(table="programs", pk="program_code"), (program_codes, ))

    @staticmethod
    def edit_program_details(program_code: str, new_program_data) -> None:
        """
        Update an existing program's details in the database.

        Args:
            program_code (str): The unique program code of the program to update.
            new_program_data (dict): A dictionary containing the updated program information.
                Expected keys include:
                    - "program_code" (str): The unique code of the program.
                    - "program_name" (str): The name of the program.
                    - "college_code" (str): The code of the academic program the student belongs to.
        """

        db = current_app.extensions['db']

        db.execute_query(CommonQueries.UPDATE_BY_ID.format(table="programs", 
                                                           set_clause="program_code = %s, program_name = %s, college_code = %s", pk="program_code"), 
                                                           (new_program_data["program_code"], new_program_data["program_name"], new_program_data["college_code"], program_code))   
    
    @staticmethod
    def get_program_codes() -> list[dict[str, str | list[str]]]:
        """
        Retrieve all program codes and their associated college codes from the database.

        Returns:
            list[dict[str, list[str] | str]]: A list of dictionaries, each containing:
                - "collegeCode" (str): The code of the college.
                - "programCodes" (list[str]): A list of program codes under that college.
        """

        db = current_app.extensions['db']

        return db.fetch_all(CommonQueries.GET_ALL_IDS.format(columns="program_code, college_code", table="programs", order_column="college_code"))   
