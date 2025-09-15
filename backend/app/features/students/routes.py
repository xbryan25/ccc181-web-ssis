from flask import Blueprint
from .controllers import StudentController

student_bp = Blueprint("student_bp", __name__)

@student_bp.route("/:id", methods=["GET"])
def get_student_details():
    return StudentController.get_student_details_controller()