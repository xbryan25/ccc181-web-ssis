from flask import Blueprint
from .controllers import StudentController

student_bp = Blueprint("student_bp", __name__)

@student_bp.route("/<str:id_number>", methods=["GET"])
def get_student_details(id_number: str):
    return StudentController.get_student_details_controller(id_number)

@student_bp.route("/total-count", methods=["GET"])
def get_total_student_count():
    return StudentController.get_total_student_count_controller()

@student_bp.route("/", methods=["GET"])
def get_many_students():
    return StudentController.get_many_students_controller()

@student_bp.route("/", methods=["POST"])
def create_student():
    return StudentController.create_student_controller()

@student_bp.route("/<str:id_number>", methods=["DELETE"])
def delete_student(id_number: str):
    return StudentController.delete_student_controller(id_number)

@student_bp.route("/<str:id_number>", methods=["PUT"])
def edit_student_details(id_number: str):
    return StudentController.delete_student_controller(id_number)