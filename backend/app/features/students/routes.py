from flask import Blueprint
from .controllers import StudentController

from flask_jwt_extended import jwt_required

student_bp = Blueprint("student_bp", __name__)

@student_bp.route("/<string:id_number>", methods=["GET"])
@jwt_required()
def get_student_details(id_number: str):
    return StudentController.get_student_details_controller(id_number)

@student_bp.route("/total-count", methods=["GET"])
@jwt_required()
def get_total_student_count():
    return StudentController.get_total_student_count_controller()

@student_bp.route("/", methods=["GET"])
@jwt_required()
def get_many_students():
    return StudentController.get_many_students_controller()

@student_bp.route("/", methods=["POST"])
@jwt_required()
def create_student():
    return StudentController.create_student_controller()

@student_bp.route("/<string:id_number>", methods=["DELETE"])
@jwt_required()
def delete_student(id_number: str):
    return StudentController.delete_student_controller(id_number)

@student_bp.route("/<string:id_number>", methods=["PUT"])
@jwt_required()
def edit_student_details(id_number: str):
    return StudentController.edit_student_details_controller(id_number)