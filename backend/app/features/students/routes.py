from flask import Blueprint
from .controllers import StudentController

from flask_jwt_extended import jwt_required

student_bp = Blueprint("student_bp", __name__)

@student_bp.route("/<string:id_number>", methods=["GET"])
@jwt_required()
def get_student_details(id_number: str):
    """
    Retrieve detailed information about a specific student.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It returns information about a student based on the provided ID number.

    Request parameters:

        id_number: The unique code identifying the student.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        idNumber: The unique code identifying the student.

        firstName: The first name of the selected student.

        lastName: The last name of the selected student.

        yearLevel: The year level of the selected student.

        gender: The gender of the selected student.

        programCode: The identifier of the program in which this student belongs to.

    Possible errors:

        404 if the student with the given ID number does not exist.
        
        500 if an unexpected error occurs during processing.
    """

    return StudentController.get_student_details_controller(id_number)

@student_bp.route("/total-count", methods=["GET"])
@jwt_required()
def get_total_student_count():
    """
    Retrieve the total number of students based on optional search filters.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It returns the total count of students, optionally filtered by search criteria. If searchValue is blank, then the count of all students will be returned.

    Query parameters:

        searchValue: The value to search for (optional).

        searchBy: The field to search by, such as "idNumber" or "yearLevel".

        searchType: The type of search to perform, such as "Starts With", "Contains", and "Ends With".

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        totalCount: The total number of students matching the provided filters.

    Possible errors:

        500 if an unexpected error occurs during processing.
    """

    return StudentController.get_total_student_count_controller()

@student_bp.route("/", methods=["GET"])
@jwt_required()
def get_many_students():
    """
    Retrieve details of different students based on pagination, optional search and sort filters.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It returns the details of different students, filtered by pagination and optionally by search and sort. 

    Query parameters:

        rowsPerPage: The number of student details to retrieve.

        pageNumber: This number will be multiplied by rowsPerPage then serve as the offset for pagination.

        searchValue: The value to search for (optional).

        searchBy: The field to search by, such as "idNumber" or "yearLevel".

        searchType: The type of search to perform, such as "Starts With", "Contains", and "Ends With".

        sortField: The field to search by, such as "idNumber" or "yearLevel".

        sortOrder: The order of sort to perform, such as "Ascending", and "Descending".

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        entities: An array of student objects with the following fields:

            idNumber: The unique code identifying the student.

            firstName: The first name of the selected student.

            lastName: The last name of the selected student.

            yearLevel: The year level of the selected student.

            gender: The gender of the selected student.

            programCode: The identifier of the program in which this student belongs to.

    Possible errors:

        500 if an unexpected error occurs during processing.
    """

    return StudentController.get_many_students_controller()

@student_bp.route("/", methods=["POST"])
@jwt_required()
def create_student():
    """
    Create a new student record.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It accepts a JSON body containing the student’s code and name, then creates a new entry in the database.

    Request body:

        entityDetails: An object containing:

            idNumber: The unique code identifying the student.

            firstName: The first name of the selected student.

            lastName: The last name of the selected student.

            yearLevel: The year level of the selected student.

            gender: The gender of the selected student.

            programCode: The identifier of the program in which this student belongs to.

    Response JSON:

        message: A confirmation message indicating that the student was added successfully.

    Possible errors:

        500 if the ID number already exists.

        500 if the combination of the first and last names of the student already exists.

        500 if an unexpected error occurs during processing.
    """

    return StudentController.create_student_controller()

@student_bp.route("/<string:id_number>", methods=["DELETE"])
@jwt_required()
def delete_student(id_number: str):
    """
    Delete a student record by its code.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It deletes a student entry from the database based on the provided ID number.

    Request parameters:

        id_number: The unique code identifying the student to be deleted.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        message: A confirmation message indicating that the student was deleted successfully.

    Possible errors:

        404 if the student with the given code does not exist.

        500 if an unexpected error occurs during processing.
    """

    return StudentController.delete_student_controller(id_number)

@student_bp.route("/<string:id_number>", methods=["PUT"])
@jwt_required()
def edit_student_details(id_number: str):
    """
    Edit the details of an existing student.

    This endpoint requires authentication via a valid access token (HTTP-only cookie). It updates the information of a student based on the provided ID number and new data.

    Request parameters:

        id_number: The current unique code identifying the student to be updated.

    Request body:

        entityDetails: An object containing:

            idNumber: The updated ID number of the student.

            firstName: The updated first name of the student.

            lastName: The updated last name of the student.

            yearLevel: The updated year level of the student.

            gender: The updated gender of the student.

            programCode: The identifier of the program in which this student belongs to.

    Response JSON:

        message: A confirmation message indicating that the student was edited successfully.

    Possible errors:

        500 if the ID number already exists.

        500 if the combination of the first and last names of the student already exists.

        500 if an unexpected error occurs during processing.
    """

    return StudentController.edit_student_details_controller(id_number)

@student_bp.route("/year-level-demographics", methods=["GET"])
@jwt_required()
def get_year_level_demographics():
    """Retrieve student year-level demographics.

    This endpoint requires authentication via a valid access token (HTTP-only cookie).
    It returns the number of students in each year level, optionally filtered by either program or college.
    Only one of the query parameters should be provided at a time; providing both will raise an error.

    Query parameters:

        programCode: The code of the program to filter by (optional, cannot be combined with collegeCode).

        collegeCode: The code of the college to filter by (optional, cannot be combined with programCode).

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        An array of objects representing year-level demographics. Each object contains:

            count: The number of students in that year level.

            yearLevel: The year level as a string, e.g., "1st", "2nd", "3rd", "4th", "4th+".

    Possible errors:

        400 if both programCode and collegeCode are provided simultaneously.

        500 if an unexpected error occurs during processing.
    """

    return StudentController.get_year_level_demographics_controller()

@student_bp.route("/gender-demographics", methods=["GET"])
@jwt_required()
def get_gender_demographics():
    """
    Retrieve student gender demographics.

    This endpoint requires authentication via a valid access token (HTTP-only cookie).
    It returns the number of students for each gender, optionally filtered by either program or college.
    Only one of the query parameters should be provided at a time; providing both will raise an error.

    Query parameters:

        programCode: The code of the program to filter by (optional, cannot be combined with collegeCode).

        collegeCode: The code of the college to filter by (optional, cannot be combined with programCode).

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        An array of objects representing gender demographics. Each object contains:

            count: The number of students of that gender.

            gender: The gender as a string, e.g., "male", "female", "others".

    Possible errors:

        400 if both programCode and collegeCode are provided simultaneously.

        500 if an unexpected error occurs during processing.
    """

    return StudentController.get_gender_demographics_controller()
