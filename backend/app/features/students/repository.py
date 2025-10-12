from app.db.connection import Database
from app.db.queries.students import StudentQueries
from app.db.queries.common import CommonQueries

from flask import current_app

class StudentRepository:

    @staticmethod
    def get_student_by_id(id_number: str) -> dict[str, str] | None:
        """
        Retrieve a student record from the database by ID number.

        Args:
            id_number (str): The unique ID number of the student.

        Returns:
            dict: A dictionary containing the student's details if found, otherwise None.
        """

        db = current_app.extensions['db']

        return db.fetch_one(CommonQueries.GET_BY_ID.format(table="students", pk="id_number"), (id_number, ))

    @staticmethod
    def get_total_student_count(params) -> dict[str, str]:
        """
        Retrieve the total number of students based on a specific filter.

        Args:
            params (dict): A dictionary of filtering parameters. Expected keys include:
                            - "search_value" (str | None): Text to search for in a specific column.
                            - "search_type" (str | None): The search matching type. One of "Starts With", "Ends With" or "Contains".
                            - "search_by" (str | None): The column name to apply the search on.
                            - "program_code" (str | None): The program code to filter students by.
                            - "college_code" (str | None): The college code to filter students by.

        Returns:
            dict: A dictionary containing the total number of students that match the given filter.
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

            return db.fetch_one(CommonQueries.GET_TOTAL_COUNT_WITH_SEARCH.format(table="students", search_by=f"{params["search_by"].lower().replace(' ', '_')}"),
                                (search_pattern,))
        
        elif params["program_code"]:
            return db.fetch_one(StudentQueries.GET_TOTAL_COUNT_FROM_PROGRAM_CODE, (params["program_code"],))
        
        elif params["college_code"]:
            return db.fetch_one(StudentQueries.GET_TOTAL_COUNT_FROM_COLLEGE_CODE, (params["college_code"],))

        else:
            return db.fetch_one(CommonQueries.GET_TOTAL_COUNT.format(table="students"))

    @staticmethod
    def get_many_students(params) -> list[dict[str, str]]:
        """
        Retrieve a paginated list of students based on search and sorting parameters.

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
            list[dict]: A list of student records matching the given filters, 
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
                            .format(table="students", 
                                    search_by=f"{params["search_by"].lower().replace(' ', '_')}",
                                    sort_field=f"{params["sort_field"].lower().replace(' ', '_')}",
                                    sort_order=sort_order),
                            (search_pattern, params["rows_per_page"], offset))

    @staticmethod
    def create_student(student_data) -> None:
        """
        Insert a new student record into the database.

        Args:
            student_data (dict): A dictionary containing the student's details.
                Expected keys include:
                    - "id_number" (str): The unique ID number of the student.
                    - "first_name" (str): The student's first name.
                    - "last_name" (str): The student's last name.
                    - "year_level" (str): The student's year level (e.g., "1st Year").
                    - "gender" (str): The student's gender.
                    - "program_code" (str): The code of the academic program the student belongs to.

        """

        db = current_app.extensions['db']

        db.execute_query(CommonQueries.INSERT.format(table="students", 
                                                     columns="id_number, first_name, last_name, year_level, gender, program_code",
                                                     placeholders="%s, %s, %s, %s, %s, %s"),
                                                     (student_data["id_number"], student_data["first_name"], student_data["last_name"],
                                                      student_data["year_level"], student_data["gender"], student_data["program_code"]))

    @staticmethod
    def delete_student(id_number: str) -> None:
        """
        Delete a student record from the database using their ID number.

        Args:
            id_number (str): The unique ID number of the student to delete.

        """

        db = current_app.extensions['db']

        db.execute_query(CommonQueries.DELETE_BY_ID.format(table="students", pk="id_number"), (id_number, ))

    @staticmethod
    def edit_student_details(id_number: str, new_student_data) -> None:
        """
        Update an existing student's details in the database.

        Args:
            id_number (str): The unique ID number of the student to update.
            new_student_data (dict): A dictionary containing the updated student information.
                Expected keys include:
                    - "id_number" (str): The updated ID number of the student.
                    - "first_name" (str): The updated first name.
                    - "last_name" (str): The updated last name.
                    - "year_level" (str): The updated year level.
                    - "gender" (str): The updated gender.
                    - "program_code" (str): The updated program code.

        """

        db = current_app.extensions['db']

        db.execute_query(CommonQueries.UPDATE_BY_ID.format(table="students", 
                                                           set_clause="id_number = %s, first_name = %s, last_name = %s, " \
                                                           "year_level = %s, gender = %s, program_code = %s", pk="id_number"), 
                                                           (new_student_data["id_number"], new_student_data["first_name"], new_student_data["last_name"],
                                                            new_student_data["year_level"], new_student_data["gender"], new_student_data["program_code"], 
                                                            id_number))  

    @staticmethod
    def get_year_level_demographics(params) -> list[dict[str, str]]:
        """
        Retrieve the student count grouped by year level, optionally filtered by program or college.

        Args:
            params (dict): A dictionary of filter parameters. Expected keys include:
                - "program_code" (str | None): The program code to filter by. 
                Cannot be provided at the same time as "college_code".

                - "college_code" (str | None): The college code to filter by. 
                Cannot be provided at the same time as "program_code".

        Returns:
            list[dict]: A list of dictionaries containing the year level and corresponding student count.
                Each dictionary includes:
                    - "year_level" (str): The academic year level (e.g., "1st Year").
                    - "count" (int): The number of students in that year level.

        Raises:
            ValueError: If both "program_code" and "college_code" are provided simultaneously.
        """

        db = current_app.extensions['db']

        if params["program_code"]:
            return db.fetch_all(StudentQueries.GET_YEAR_LEVEL_DEMOGRAPHICS_FROM_PROGRAM_CODE, (params["program_code"], ))
        
        elif params["college_code"]:
            return db.fetch_all(StudentQueries.GET_YEAR_LEVEL_DEMOGRAPHICS_FROM_COLLEGE_CODE, (params["college_code"], ))
        
        return db.fetch_all(StudentQueries.GET_YEAR_LEVEL_DEMOGRAPHICS)
    
    @staticmethod
    def get_gender_demographics(params) -> list[dict[str, str]]:
        """
        Retrieve the student count grouped by gender, optionally filtered by program or college.

        Args:
            params (dict): A dictionary of filter parameters. Expected keys include:
                - "program_code" (str | None): The program code to filter by. 
                Cannot be provided at the same time as "college_code".
                - "college_code" (str | None): The college code to filter by. 
                Cannot be provided at the same time as "program_code".

        Returns:
            list[dict]: A list of dictionaries containing gender demographics.
                Each dictionary includes:
                    - "gender" (str): The gender category (e.g., "Male", "Female").
                    - "count" (int): The number of students in that gender group.

        Raises:
            ValueError: If both "program_code" and "college_code" are provided simultaneously.
        """

        db = current_app.extensions['db']
        
        if params["program_code"]:
            return db.fetch_all(StudentQueries.GET_GENDER_DEMOGRAPHICS_FROM_PROGRAM_CODE, (params["program_code"], ))
        
        elif params["college_code"]:
            return db.fetch_all(StudentQueries.GET_GENDER_DEMOGRAPHICS_FROM_COLLEGE_CODE, (params["college_code"], ))

        return db.fetch_all(StudentQueries.GET_GENDER_DEMOGRAPHICS)
    