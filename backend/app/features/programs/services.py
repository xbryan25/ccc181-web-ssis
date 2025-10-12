from .repository import ProgramRepository

from app.features.common.dataclasses import Program

from app.exceptions.custom_exceptions import EntityNotFoundError

class ProgramServices:

    @staticmethod
    def get_program_details_service(program_code: str) -> Program:
        """
        Get the details of a program using the program_code.

        Args:
            program_code (str): program_code of the user.

        Returns:
            Program: A Program dataclass instance if a program has the given program_code, otherwise None.
        """

        row = ProgramRepository.get_program_by_program_code(program_code)

        if not row:
            raise EntityNotFoundError(f"Program with the program_code '{program_code}' does not exist.")

        return Program(**row)

    @staticmethod
    def get_total_program_count_service(params) -> int:
        """
        Retrieve the total program count, with optional search filters.

        Args:
            params (dict): A dictionary containing the optional search filters.
                Expected keys include:
                    - "search_value" (str): The value to search for.
                    - "search_by" (str): The field to search by, such as "programName" or "programCode".
                    - "search_type" (str): The type of search to perform, such as "Starts With", "Contains", and "Ends With".

        Returns:
            int: The total program count, with search filters being optionally applied.
        """

        return ProgramRepository.get_total_program_count(params)["count"]

    @staticmethod
    def get_many_programs_service(params) -> list[Program]:
        """
        Retrieve details of different programs based on pagination, optional search and sort filters.
        
        Args:
            params (dict): A dictionary containing the pagination details, optional search and sort filters.
                Expected keys include:
                    - "rowsPerPage" (str): The number of program details to retrieve.
                    - "pageNumber" (str): This number will be multiplied by rowsPerPage then serve as the offset for pagination.
                    - "searchValue" (str): The value to search for.
                    - "searchBy" (str): The field to search by, such as "programName" or "programCode".
                    - "searchType" (str): The type of search to perform, such as "Starts With", "Contains", and "Ends With".
                    - "sortField" (str): The field to search by, such as "programName" or "programCode".
                    - "sortOrder" (str): The order of sort to perform, such as "Ascending", and "Descending".

        Returns:
            list[Program]: A list of program dataclass instances representing rowsPerPage programs.
        """

        programs = ProgramRepository.get_many_programs(params)

        program_dataclasses = []

        for program in programs:
            if not program['college_code']:
                program['college_code'] = 'N/A'

            program_dataclasses.append(Program(**program))

        return program_dataclasses

    @staticmethod
    def create_program_service(program_data) -> None:
        """
        Create a new program record.
        
        Args:
            program_data (dict): A dictionary containing the details of the new program.
                Expected keys include:
                    - "program_code" (str): The unique code identifying the program.
                    - "program_name" (str): The name of the program.
                    - "college_code" (str): The identifier of the college in which this program belongs to.
        """

        ProgramRepository.create_program(program_data)

    @staticmethod
    def delete_program_service(program_code: str) -> None:
        """
        Delete a program record by its program_code.

        Args:
            program_code (str): program_code of the program to be deleted.
        """

        ProgramRepository.delete_program(program_code)

    @staticmethod
    def edit_program_details_service(program_code: str, new_program_data) -> None:
        """
        Edit the details of an existing program.
        
        Args:
            program_code (str): The current unique code identifying the program to be updated.
            program_data (dict): A dictionary containing the details of the updated program.
                Expected keys include:
                    - "programCode" (str): The updated program code of the program.
                    - "programName" (str): The updated name of the program.
                    - "collegeCode" (str): The identifier of the college in which this program belongs to.
        """

        ProgramRepository.edit_program_details(program_code, new_program_data)

    @staticmethod
    def get_program_codes_service() -> list[dict[str, str | list[str]]]:
        """
        Retrieve all program codes.

        Returns:
            list[dict]: A list of dictionaries, each containing:
                - "collegeCode" (str): The code of the college (or "N/A" if none).
                - "programCodes" (list[str]): A sorted list of program codes under the college.
        """
        
        program_codes_details = ProgramRepository.get_program_codes()

        grouped_program_codes = {}

        for program_code_details in program_codes_details:

            if program_code_details['college_code'] not in grouped_program_codes:
                grouped_program_codes[program_code_details['college_code']] = {
                    'collegeCode': program_code_details['college_code'],
                    'programCodes': [program_code_details['program_code']]
                }

            else:
                grouped_program_codes[program_code_details['college_code']]['programCodes'].append(program_code_details['program_code'])
                
                grouped_program_codes[program_code_details['college_code']]['programCodes'].sort()


        # Rename None to "N/A"
        grouped_program_codes["N/A"] = grouped_program_codes.pop(None)
        grouped_program_codes["N/A"]['collegeCode'] = "N/A"

        # Return list of values of the dict
        return list(grouped_program_codes.values())
    