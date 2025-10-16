from .repository import CollegeRepository

from app.features.common.dataclasses import College

from app.exceptions.custom_exceptions import EntityNotFoundError

class CollegeServices:

    @staticmethod
    def get_college_details_service(college_code: str) -> College:
        """
        Get the details of a college using the college_code.

        Args:
            college_code (str): college_code of the user.

        Returns:
            College: A College dataclass instance if a college has the given college_code, otherwise None.
        """

        row = CollegeRepository.get_college_by_college_code(college_code)

        if not row:
            raise EntityNotFoundError(f"College with the college_code '{college_code}' does not exist.")

        return College(**row)
    
    @staticmethod
    def get_total_college_count_service(params) -> int:
        """
        Retrieve the total college count, with optional search filters.

        Args:
            params (dict): A dictionary containing the optional search filters.
                Expected keys include:
                    - "search_value" (str): The value to search for.
                    - "search_by" (str): The field to search by, such as "collegeName" or "collegeCode".
                    - "search_type" (str): The type of search to perform, such as "Starts With", "Contains", and "Ends With".

        Returns:
            int: The total college count, with search filters being optionally applied.
        """

        return CollegeRepository.get_total_college_count(params)["count"]

    @staticmethod
    def get_many_colleges_service(params) -> list[College]:
        """
        Retrieve details of different colleges based on pagination, optional search and sort filters.
        
        Args:
            params (dict): A dictionary containing the pagination details, optional search and sort filters.
                Expected keys include:
                    - "rowsPerPage" (str): The number of college details to retrieve.
                    - "pageNumber" (str): This number will be multiplied by rowsPerPage then serve as the offset for pagination.
                    - "searchValue" (str): The value to search for.
                    - "searchBy" (str): The field to search by, such as "collegeName" or "collegeCode".
                    - "searchType" (str): The type of search to perform, such as "Starts With", "Contains", and "Ends With".
                    - "sortField" (str): The field to search by, such as "collegeName" or "collegeCode".
                    - "sortOrder" (str): The order of sort to perform, such as "Ascending", and "Descending".

        Returns:
            list[College]: A list of college dataclass instances representing rowsPerPage colleges.
        """

        colleges = CollegeRepository.get_many_colleges(params)

        college_dataclasses = []

        for college in colleges:
            college_dataclasses.append(College(**college))

        return college_dataclasses

    @staticmethod
    def create_college_service(college_data) -> None:
        """
        Create a new college record.
        
        Args:
            college_data (dict): A dictionary containing the details of the new college.
                Expected keys include:
                    - "college_code" (str): The unique code identifying the college.
                    - "college_name" (str): The name of the college.
        """

        CollegeRepository.create_college(college_data)

    @staticmethod
    def delete_college_service(college_code: str) -> None:
        """
        Delete a college record by its college_code.

        Args:
            college_code (str): college_code of the college to be deleted.
        """

        CollegeRepository.delete_college(college_code)

    @staticmethod
    def edit_college_details_service(college_code: str, new_college_data) -> None:
        """
        Edit the details of an existing college.
        
        Args:
            college_code (str): The current unique code identifying the college to be updated.
            college_data (dict): A dictionary containing the details of the updated college.
                Expected keys include:
                    - "college_code" (str): The updated college code of the college.
                    - "college_name" (str): The updated name of the college.
        """

        CollegeRepository.edit_college_details(college_code, new_college_data)

    @staticmethod
    def get_college_codes_service() -> list[dict[str, str]]:
        """
        Retrieve all college codes.

        Returns:
            list[dict]: A list of dictionaries, each containing:
                - "collegeCode" (str): The code of the college (or "N/A" if none).
        """

        college_codes_details = CollegeRepository.get_college_codes()

        for college_code_details in college_codes_details:
            college_code_details["collegeCode"] = college_code_details.pop('college_code')

        return college_codes_details
