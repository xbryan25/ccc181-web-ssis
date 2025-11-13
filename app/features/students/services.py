from flask import current_app

from .repository import StudentRepository

from app.features.common.dataclasses import Student

from app.utils import to_camel_case, upload_images_to_bucket_from_add_book_service

from app.exceptions.custom_exceptions import EntityNotFoundError

from supabase import create_client, Client

class StudentServices:

    @staticmethod
    def get_student_details_service(id_number: str) -> Student:
        """
        Get the details of a student using the id_number.

        Args:
            id_number (str): id_number of the student.

        Returns:
            Student: A Student dataclass instance if a student has the given id_number, otherwise None.
        """
    
        row = StudentRepository.get_student_by_id(id_number)

        if not row:
            raise EntityNotFoundError(f"Student with the id_number '{id_number}' does not exist.")

        return Student(**row)
    
    @staticmethod
    def get_total_student_count_service(params) -> int:
        """
        Retrieve the total student count, with optional search filters.

        Args:
            params (dict): A dictionary containing the optional search filters.
                Expected keys include:
                    - "search_value" (str): The value to search for.
                    - "search_by" (str): The field to search by, such as "idNumber" or "yearLevel".
                    - "search_type" (str): The type of search to perform, such as "Starts With", "Contains", and "Ends With".

        Returns:
            int: The total student count, with search filters being optionally applied.
        """

        return StudentRepository.get_total_student_count(params)["count"]

    @staticmethod
    def get_many_students_service(params) -> list[Student]:
        """
        Retrieve details of different students based on pagination, optional search and sort filters.
        
        Args:
            params (dict): A dictionary containing the pagination details, optional search and sort filters.
                Expected keys include:
                    - "rowsPerPage" (str): The number of student details to retrieve.
                    - "pageNumber" (str): This number will be multiplied by rowsPerPage then serve as the offset for pagination.
                    - "searchValue" (str): The value to search for.
                    - "searchBy" (str): The field to search by, such as "idNumber" or "yearLevel".
                    - "searchType" (str): The type of search to perform, such as "Starts With", "Contains", and "Ends With".
                    - "sortField" (str): The field to search by, such as "idNumber" or "yearLevel".
                    - "sortOrder" (str): The order of sort to perform, such as "Ascending", and "Descending".

        Returns:
            list[Student]: A list of Student dataclass instances representing rowsPerPage students.
        """

        students = StudentRepository.get_many_students(params)

        student_dataclasses = []

        for student in students:
            student['gender'] = student['gender'].capitalize()

            if not student['program_code']:
                student['program_code'] = 'N/A'

            student_dataclasses.append(Student(**student))

        return student_dataclasses

    @staticmethod
    def create_student_service(student_data, student_avatar) -> None:
        """
        Create a new student record.
        
        Args:
            student_data (dict): A dictionary containing the details of the new student.
                Expected keys include:
                    - "id_number" (str): The unique code identifying the student.
                    - "first_name" (str): The first name of the student.
                    - "last_name" (str): The last name of the student.
                    - "year_level" (str): The year level of the student.
                    - "gender" (str): The gender of the student.
                    - "program_code" (str): The identifier of the program in which this student belongs to.
            student_avatar (FileStorage | None): The uploaded avatar image file, if provided.
        """

        StudentRepository.create_student(student_data=student_data)

        id_number = student_data['id_number']

        if student_avatar:

            supabase: Client = create_client(
                current_app.config.get("SUPABASE_URL", ""),
                current_app.config.get("SUPABASE_SERVICE_KEY", ""),
            )

            bucket_name = current_app.config.get("SUPABASE_BUCKET_NAME", "avatars")

            avatar_url = upload_images_to_bucket_from_add_book_service(
                supabase, student_avatar, bucket_name
            )

            StudentRepository.update_avatar_url(id_number, avatar_url)
            

    @staticmethod
    def delete_student_service(id_number: str) -> None:
        """
        Delete a student record by its id_number.

        Args:
            id_number (str): id_number of the student to be deleted.
        """

        StudentRepository.delete_student(id_number=id_number)

    @staticmethod
    def edit_student_details_service(id_number: str, new_student_data) -> None:
        """
        Edit the details of an existing student.
        
        Args:
            id_number (str): The current unique code identifying the student to be updated.
            new_student_data (dict): A dictionary containing the details of the updated program.
                Expected keys include:
                    - "id_number" (str): The updated ID number of the student.
                    - "first_name" (str): The updated first name of the student.
                    - "last_name" (str): The updated last name of the student.
                    - "year_level" (str): The updated year level of the student.
                    - "gender" (str): The updated gender of the student.
                    - "program_code" (str): The identifier of the program in which this student belongs to.
        """

        StudentRepository.edit_student_details(id_number=id_number, new_student_data=new_student_data)

    @staticmethod
    def get_year_level_demographics_service(params) -> list[dict[str, int | str]]:
        """
        Retrieve student year-level demographics.
        
        Args:
            params (dict): A dictionary containing the program code and college code filters.
                Expected keys include:
                    - "programCode" (str):  The code of the program to filter by (optional, cannot be combined with collegeCode).
                    - "collegeCode" (str): The code of the college to filter by (optional, cannot be combined with programCode).

        Returns:
            list[dict]: A list of dictionaries, each containing:
                - "count" (int): The number of students in that year level.
                - "year_level" (str): The name or label of the year level.
        """

        year_level_demographics = StudentRepository.get_year_level_demographics(params)

        formatted_year_level_demographics = [{to_camel_case(k): v for k, v in year_level_demographic.items()} for year_level_demographic in year_level_demographics]

        return formatted_year_level_demographics
    
    @staticmethod
    def get_gender_demographics_service(params) -> list[dict[str, int | str]]:
        """
        Retrieve student gender demographics.
        
        Args:
            params (dict): A dictionary containing the program code and college code filters.
                Expected keys include:
                    - "programCode" (str):  The code of the program to filter by (optional, cannot be combined with collegeCode).
                    - "collegeCode" (str): The code of the college to filter by (optional, cannot be combined with programCode).

        Returns:
            list[dict]: A list of dictionaries, each containing:
                - "count" (int): The number of students of the gender.
                - "gender" (str): The name or label of the gender.
        """

        gender_demographics = StudentRepository.get_gender_demographics(params)

        formatted_gender_demographics = [{to_camel_case(k): v for k, v in gender_demographic.items()} for gender_demographic in gender_demographics]

        return formatted_gender_demographics
    