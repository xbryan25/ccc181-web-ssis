from flask import request, jsonify
from dataclasses import asdict

import traceback

from .services import ProgramServices

from ..common.dataclasses import Program

from app.utils import dict_keys_to_camel

from psycopg.errors import UniqueViolation

class ProgramController:
    
    @staticmethod
    def get_program_details_controller(program_code: str):

        try:
            program_details: Program = ProgramServices.get_program_details_service(program_code)

            return jsonify(dict_keys_to_camel(asdict(program_details))), 200

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

            return jsonify({"entities": [dict_keys_to_camel(asdict(program_details)) for program_details in programs]}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def create_program_controller():
        entity_details = request.json

        new_program_data = {
            'programCode': entity_details['entityDetails']['programCode'],
            'programName': entity_details['entityDetails']['programName'],
            'collegeCode': entity_details['entityDetails']['collegeCode']
        }

        try:
            ProgramServices.create_program_service(new_program_data)

            return jsonify({"message": "Program added successfully."}), 200
        
        except UniqueViolation as e:
            traceback.print_exc()

            constraint_name = e.diag.constraint_name

            if constraint_name == 'programs_pkey':
                return jsonify({"errorMessage": "Program code already exists."}), 500
            
            elif constraint_name == 'programs_program_name_key':
                return jsonify({"errorMessage": "Program name already exists."}), 500
            
            else:
                return jsonify({"errorMessage": "Something went wrong."}), 500

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

        entity_details = request.json

        new_program_data = {
            'programCode': entity_details['entityDetails']['programCode'],
            'programName': entity_details['entityDetails']['programName'],
            'collegeCode': entity_details['entityDetails']['collegeCode']
        }

        try:
            ProgramServices.edit_program_details_service(program_code, new_program_data)

            return jsonify({"message": "Program edited successfully."}), 200
              
        except UniqueViolation as e:
            traceback.print_exc()

            constraint_name = e.diag.constraint_name

            if constraint_name == 'programs_pkey':
                return jsonify({"errorMessage": "Program code already exists."}), 500
            
            elif constraint_name == 'programs_program_name_key':
                return jsonify({"errorMessage": "Program name already exists."}), 500
            
            else:
                return jsonify({"errorMessage": "Something went wrong."}), 500

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def get_program_codes_controller():
        try:
            program_codes_details = ProgramServices.get_program_codes_service()

            return jsonify(program_codes_details), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        