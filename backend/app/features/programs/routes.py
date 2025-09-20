from flask import Blueprint
from .controllers import ProgramController

program_bp = Blueprint("program_bp", __name__)

@program_bp.route("/<string:program_code>", methods=["GET"])
def get_program_details(program_code: str):
    return ProgramController.get_program_details_controller(program_code)

@program_bp.route("/total-count", methods=["GET"])
def get_total_program_count():
    return ProgramController.get_total_program_count_controller()

@program_bp.route("/", methods=["GET"])
def get_many_programs():
    return ProgramController.get_many_programs_controller()

@program_bp.route("/", methods=["POST"])
def create_program():
    return ProgramController.create_program_controller()

@program_bp.route("/<string:program_code>", methods=["DELETE"])
def delete_program(program_code: str):
    return ProgramController.delete_program_controller(program_code)

@program_bp.route("/<string:program_code>", methods=["PUT"])
def edit_program_details(program_code: str):
    return ProgramController.edit_program_details_controller(program_code)