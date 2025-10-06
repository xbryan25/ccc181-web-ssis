from flask import Blueprint
from .controllers import CollegeController

from flask_jwt_extended import jwt_required

college_bp = Blueprint("college_bp", __name__)

@college_bp.route("/<string:college_code>", methods=["GET"])
@jwt_required()
def get_college_details(college_code: str):
    """
    Retrieve detailed information about a specific college.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It returns information about a college based on the provided college code.

    Request parameters:

        college_code: The unique code identifying the college.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        college_code: The unique code identifying the college.

        college_name: The name of the selected college.

    Possible errors:

        404 if the college with the given code does not exist.
        
        500 if an unexpected error occurs during processing.
    """

    return CollegeController.get_college_details_controller(college_code)

@college_bp.route("/total-count", methods=["GET"])
@jwt_required()
def get_total_college_count():
    """
    Retrieve the total number of colleges based on optional search filters.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It returns the total count of colleges, optionally filtered by search criteria. If searchValue is blank, then the count of all colleges will be returned.

    Query parameters:

        searchValue: The value to search for (optional).

        searchBy: The field to search by, such as "collegeName" or "collegeCode".

        searchType: The type of search to perform, such as "Starts With", "Contains", and "Ends With".

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        totalCount: The total number of colleges matching the provided filters.

    Possible errors:

        500 if an unexpected error occurs during processing.
    """
    return CollegeController.get_total_college_count_controller()

@college_bp.route("/", methods=["GET"])
@jwt_required()
def get_many_colleges():
    """
    Retrieve details of different colleges based on pagination, optional search and sort filters.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It returns the details of different colleges, filtered by pagination and optionally by search and sort. 

    Query parameters:

        rowsPerPage: The number of college details to retrieve.

        pageNumber: This number will be multiplied by rowsPerPage then serve as the offset for pagination.

        searchValue: The value to search for (optional).

        searchBy: The field to search by, such as "collegeName" or "collegeCode".

        searchType: The type of search to perform, such as "Starts With", "Contains", and "Ends With".

        sortField: The field to search by, such as "collegeName" or "collegeCode".

        sortOrder: The order of sort to perform, such as "Ascending", and "Descending".

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        entities: An array of college objects with the following fields:

            collegeName: The name of the college.

            collegeCode: The unique code assigned to the college.

    Possible errors:

        500 if an unexpected error occurs during processing.
    """

    return CollegeController.get_many_colleges_controller()

@college_bp.route("/", methods=["POST"])
@jwt_required()
def create_college():
    """
    Create a new college record.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It accepts a JSON body containing the college’s code and name, then creates a new entry in the database.

    Request body:

        entityDetails: An object containing:

            collegeCode: The unique code assigned to the college.

            collegeName: The name of the college.

    Response JSON:

        message: A confirmation message indicating that the college was added successfully.

    Possible errors:

        500 if the college code already exists.

        500 if the college name already exists.

        500 if an unexpected error occurs during processing.
    """

    return CollegeController.create_college_controller()

@college_bp.route("/<string:college_code>", methods=["DELETE"])
@jwt_required()
def delete_college(college_code: str):
    """
    Delete a college record by its code.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It deletes a college entry from the database based on the provided college code.

    Request parameters:

        college_code": The unique code identifying the college to be deleted.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        message: A confirmation message indicating that the college was deleted successfully.

    Possible errors:

        404 if the college with the given code does not exist.

        500 if an unexpected error occurs during processing.
    """

    return CollegeController.delete_college_controller(college_code)

@college_bp.route("/<string:college_code>", methods=["PUT"])
@jwt_required()
def edit_college_details(college_code: str):
    """
    Edit the details of an existing college.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It updates the information of a college based on the provided college code and new data.

    Request parameters:

        college_code: The current unique code identifying the college to be updated.

    Request body:

        entityDetails: An object containing:

            collegeCode: The updated code for the college.

            collegeName: The updated name of the college.

    Response JSON:

        message: A confirmation message indicating that the college was edited successfully.

    Possible errors:

        500 if the new college code already exists.

        500 if the new college name already exists.

        500 if an unexpected error occurs during processing.
    """

    return CollegeController.edit_college_details_controller(college_code)

@college_bp.route("/identifiers", methods=["GET"])
@jwt_required()
def get_college_codes():
    """
    Retrieve a list of all college identifiers.

    This endpoint requires authentication via a valid access token (HTTP-only cookie).
    It returns an array of college objects, each containing the college code and name.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

    An array of college objects with the following fields:

        collegeCode: The unique code assigned to the college.

        collegeName: The name of the college.

    Possible errors:

        500 if an unexpected error occurs during processing.
    """

    return CollegeController.get_college_codes_controller()
