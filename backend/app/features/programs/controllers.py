from flask import request, jsonify
from dataclasses import asdict

import traceback

from .services import ProgramServices

from ..common.dataclasses import Program

class ProgramController:
    
    @staticmethod
    def get_program_details_controller(program_code: str):

        try:
            program_details: Program = ProgramServices.get_program_details_service(program_code)

            return jsonify({"result": asdict(program_details)}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def get_total_program_count_controller():
        try:
            total_program_count_dict = ProgramServices.get_total_program_count_service()

            return jsonify({"totalCount": total_program_count_dict["count"]}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_many_programs_controller():
        params = {
            "rows_per_page": int(request.args.get("rowsPerPage")),
            "page_number": int(request.args.get("pageNumber")),
            "search_value": request.args.get("searchValue"),
            "search_by": request.args.get("searchBy"),
            "search_type": request.args.get("searchType"),
            "sort_field": request.args.get("sortField"),
            "sort_order":request.args.get("sortOrder")
        }

        try:
            programs = ProgramServices.get_many_programs_service(params)

            return jsonify({"entities": [asdict(program_details) for program_details in programs]}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def create_program_controller():
        program_data = request.json

        try:
            ProgramServices.create_program_service(program_data)

            return jsonify({"message": "Program added successfully."}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_program_controller(program_code: str):
        try:
            ProgramServices.delete_program_service(program_code)

            return jsonify({"message": "Program deleted successfully."}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def edit_program_details_controller(program_code: str):

        new_program_data = request.json

        try:
            ProgramServices.edit_program_details_service(program_code, new_program_data)

            return jsonify({"message": "Program edited successfully."}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500