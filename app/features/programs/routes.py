from flask import Blueprint, Response
from .controllers import ProgramController

from flask_jwt_extended import jwt_required

program_bp = Blueprint("program_bp", __name__)

@program_bp.route("/<string:program_code>", methods=["GET"])
@jwt_required()
def get_program_details(program_code: str) -> tuple[Response, int]:
    """
    Retrieve detailed information about a specific program.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It returns information about a program based on the provided program code.

    Request parameters:

        program_code: The unique code identifying the program.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        programCode: The unique code identifying the program.

        programName: The name of the selected program.

        collegeCode: The identifier of the college in which this program belongs to.

    Possible errors:

        404 if the program with the given code does not exist.
        
        500 if an unexpected error occurs during processing.
    """
    return ProgramController.get_program_details_controller(program_code)

@program_bp.route("/total-count", methods=["GET"])
@jwt_required()
def get_total_program_count() -> tuple[Response, int]:
    """
    Retrieve the total number of programs based on optional search filters.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It returns the total count of programs, optionally filtered by search criteria. If searchValue is blank, then the count of all programs will be returned.

    Query parameters:

        searchValue: The value to search for (optional).

        searchBy: The field to search by, such as "programName" or "programCode".

        searchType: The type of search to perform, such as "Starts With", "Contains", and "Ends With".

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        totalCount: The total number of programs matching the provided filters.

    Possible errors:

        500 if an unexpected error occurs during processing.
    """
    
    return ProgramController.get_total_program_count_controller()

@program_bp.route("/", methods=["GET"])
@jwt_required()
def get_many_programs() -> tuple[Response, int]:
    """
    Retrieve details of different programs based on pagination, optional search and sort filters.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It returns the details of different programs, filtered by pagination and optionally by search and sort. 

    Query parameters:

        rowsPerPage: The number of program details to retrieve.

        pageNumber: This number will be multiplied by rowsPerPage then serve as the offset for pagination.

        searchValue: The value to search for (optional).

        searchBy: The field to search by, such as "programName" or "programCode".

        searchType: The type of search to perform, such as "Starts With", "Contains", and "Ends With".

        sortField: The field to search by, such as "programName" or "programCode".

        sortOrder: The order of sort to perform, such as "Ascending", and "Descending".

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        entities: An array of program objects with the following fields:

            programName: The name of the program.

            programCode: The unique code assigned to the program.

            collegeCode: The identifier of the program in which this program belongs to.

    Possible errors:

        500 if an unexpected error occurs during processing.
    """

    return ProgramController.get_many_programs_controller()

@program_bp.route("/", methods=["POST"])
@jwt_required()
def create_program() -> tuple[Response, int]:
    """
    Create a new program record.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It accepts a JSON body containing the program’s code and name, then creates a new entry in the database.

    Request body:

        entityDetails: An object containing:

            programCode: The unique code assigned to the program.

            programName: The name of the program.

            collegeCode: The identifier of the program in which this program belongs to.

    Response JSON:

        message: A confirmation message indicating that the program was added successfully.

    Possible errors:

        500 if the program code already exists.

        500 if the program name already exists.

        500 if an unexpected error occurs during processing.
    """

    return ProgramController.create_program_controller()

@program_bp.route("/", methods=["DELETE"])
@jwt_required()
def delete_programs() -> tuple[Response, int]:
    """
    Delete program record(s) given a single program code or a list of program codes.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It deletes a program entry from the database based on the provided program code.

    Request body:

        entityIds: A list of unique codes identifying the program(s) to be deleted.

    Response JSON:

        message: A confirmation message indicating that the program(s) was/were deleted successfully.

    Possible errors:

        404 if the program with the given code does not exist.

        500 if an unexpected error occurs during processing.
    """

    return ProgramController.delete_programs_controller()

@program_bp.route("/<string:program_code>", methods=["PATCH"])
@jwt_required()
def edit_program_details(program_code: str) -> tuple[Response, int]:
    """
    Edit the details of an existing program.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It updates the information of a program based on the provided program code and new data.

    Request parameters:

        program_code: The current unique code identifying the program to be updated.

    Request body:

        entityDetails: An object containing:

            programCode: The updated code for the program.

            programName: The updated name of the program.

            collegeCode: The identifier of the program in which this program belongs to.

    Response JSON:

        message: A confirmation message indicating that the program was edited successfully.

    Possible errors:

        500 if the new program code already exists.

        500 if the new program name already exists.

        500 if an unexpected error occurs during processing.
    """

    return ProgramController.edit_program_details_controller(program_code)

@program_bp.route("/identifiers", methods=["GET"])
@jwt_required()
def get_program_codes() -> tuple[Response, int]:
    """
    Retrieve a list of all program identifiers.

    This endpoint requires authentication via a valid access token (HTTP-only cookie).
    It returns an array of program objects, each containing the program code, program name, and college code.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

    An array of program objects with the following fields:

        programCode: The unique code assigned to the program.

        programName: The name of the program.

        collegeCode: The identifier of the program in which this program belongs to.

    Possible errors:

        500 if an unexpected error occurs during processing.
    """

    return ProgramController.get_program_codes_controller()
