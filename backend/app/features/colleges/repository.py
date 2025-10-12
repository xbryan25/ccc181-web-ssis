from app.db.connection import Database
from app.db.queries.colleges import CollegeQueries
from app.db.queries.common import CommonQueries

from flask import current_app

class CollegeRepository:

    @staticmethod
    def get_college_by_college_code(college_code: str) -> dict[str, str] | None:
        """
        Retrieve a college record from the database by college code.

        Args:
            college_code (str): The unique college code of the college.

        Returns:
            dict: A dictionary containing the college's details if found, otherwise None.
        """

        db = current_app.extensions['db']

        return db.fetch_one(CommonQueries.GET_BY_ID.format(table="colleges", pk="college_code"), (college_code, ))

    @staticmethod
    def get_total_college_count(params) -> dict[str, str]:
        """
        Retrieve the total number of colleges based on a specific filter.

        Args:
            params (dict): A dictionary of filtering parameters. Expected keys include:
                            - "search_value" (str | None): Text to search for in a specific column.
                            - "search_type" (str | None): The search matching type. One of "Starts With", "Ends With" or "Contains".
                            - "search_by" (str | None): The column name to apply the search on.
                            - "college_code" (str | None): The college code to filter colleges by.

        Returns:
            dict: A dictionary containing the total number of colleges that match the given filter.
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

            return db.fetch_one(CommonQueries.GET_TOTAL_COUNT_WITH_SEARCH.format(table="colleges", search_by=f"{params["search_by"].lower().replace(' ', '_')}"),
                                (search_pattern,))
        
        else:
            return db.fetch_one(CommonQueries.GET_TOTAL_COUNT.format(table="colleges"))

    @staticmethod
    def get_many_colleges(params) -> list[dict[str, str]]:
        """
        Retrieve a paginated list of colleges based on search and sorting parameters.

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
            list[dict]: A list of college records matching the given filters, 
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

        offset = (params["page_number"] - 1) * params["rows_per_page"]

        return db.fetch_all(CommonQueries.GET_MANY
                            .format(table="colleges", 
                                    search_by=f"{params["search_by"].lower().replace(' ', '_')}",
                                    sort_field=f"{params["sort_field"].lower().replace(' ', '_')}",
                                    sort_order=sort_order),
                            (search_pattern, params["rows_per_page"], offset))

    @staticmethod
    def create_college(college_data) -> None:
        """
        Insert a new college record into the database.

        Args:
            college_data (dict): A dictionary containing the college's details.
                Expected keys include:
                    - "college_code" (str): The unique code of the college.
                    - "college_name" (str): The name of the college.
        """

        db = current_app.extensions['db']

        db.execute_query(CommonQueries.INSERT.format(table="colleges", columns="college_code, college_name", placeholders="%s, %s"),
                         (college_data["college_code"], college_data["college_name"]))

    @staticmethod
    def delete_college(college_code: str) -> None:
        """
        Delete a college record from the database using their college code.

        Args:
            college_code (str): The unique college code of the college to delete.
        """

        db = current_app.extensions['db']

        db.execute_query(CommonQueries.DELETE_BY_ID.format(table="colleges", pk="college_code"), (college_code, ))

    @staticmethod
    def edit_college_details(college_code: str, new_college_data) -> None:
        """
        Update an existing college's details in the database.

        Args:
            college_code (str): The unique college code of the college to update.
            new_college_data (dict): A dictionary containing the updated college information.
                Expected keys include:
                    - "college_code" (str): The unique code of the college.
                    - "college_name" (str): The name of the college.
        """

        db = current_app.extensions['db']

        db.execute_query(CommonQueries.UPDATE_BY_ID.format(table="colleges", 
                                                           set_clause="college_code = %s, college_name = %s", pk="college_code"), 
                                                           (new_college_data["college_code"], new_college_data["college_name"], college_code))   
    @staticmethod
    def get_college_codes() -> list[dict[str, str]]:
        """
        Retrieve all college codes from the database.

        Returns:
            list[dict[str]]: A list of dictionaries, each containing:
                - "collegeCode" (str): The code of the college.
        """

        db = current_app.extensions['db']

        return db.fetch_all(CommonQueries.GET_ALL_IDS.format(columns="college_code", table="colleges", order_column="college_code"))   
