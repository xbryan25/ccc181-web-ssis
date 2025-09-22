from flask import Blueprint
from .controllers import CollegeController

college_bp = Blueprint("college_bp", __name__)

@college_bp.route("/<string:college_code>", methods=["GET"])
def get_college_details(college_code: str):
    return CollegeController.get_college_details_controller(college_code)

@college_bp.route("/total-count", methods=["GET"])
def get_total_college_count():
    return CollegeController.get_total_college_count_controller()

@college_bp.route("/", methods=["GET"])
def get_many_colleges():
    return CollegeController.get_many_colleges_controller()

@college_bp.route("/", methods=["POST"])
def create_college():
    return CollegeController.create_college_controller()

@college_bp.route("/<string:college_code>", methods=["DELETE"])
def delete_college(college_code: str):
    return CollegeController.delete_college_controller(college_code)

@college_bp.route("/<string:college_code>", methods=["PUT"])
def edit_college_details(college_code: str):
    return CollegeController.edit_college_details_controller(college_code)

@college_bp.route("/identifiers", methods=["GET"])
def get_college_codes():
    return CollegeController.get_college_codes_controller()
