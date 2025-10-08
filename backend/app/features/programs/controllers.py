from flask import request, jsonify, Response
from dataclasses import asdict

import traceback

import json

from .services import ProgramServices

from ..common.dataclasses import Program

from app.utils import dict_keys_to_camel

from psycopg.errors import UniqueViolation

class ProgramController:
    
    @staticmethod
    def get_program_details_controller(program_code: str) -> tuple[Response, int]:
        """Retrieve detailed information about a specific program."""

        try:
            program_details: Program = ProgramServices.get_program_details_service(program_code)

            return jsonify(dict_keys_to_camel(asdict(program_details))), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def get_total_program_count_controller() -> tuple[Response, int]:
        """Retrieve the total number of programs based on optional search filters."""

        try:
            params = {
                "search_value": request.args.get("searchValue"),
                "search_by": request.args.get("searchBy"),
                "search_type": request.args.get("searchType"),
            }

            filter_by = request.args.get("filterBy")

            if filter_by:
                dict_filter_by = json.loads(filter_by)
                
                if 'collegeCode' in dict_filter_by.keys():
                    params.update({"college_code": dict_filter_by['collegeCode']})
            else:
                params.update({"college_code": None})

            total_program_count = ProgramServices.get_total_program_count_service(params)

            return jsonify({"totalCount": total_program_count}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_many_programs_controller() -> tuple[Response, int]:
        """Retrieve details of different programs based on pagination, optional search and sort filters."""

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
    def create_program_controller() -> tuple[Response, int]:
        """Create a new program record."""
        
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
    def delete_program_controller(program_code: str) -> tuple[Response, int]:
        """Delete a program record by its code."""

        try:
            ProgramServices.delete_program_service(program_code)

            return jsonify({"message": "Program deleted successfully."}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def edit_program_details_controller(program_code: str) -> tuple[Response, int]:
        """Edit the details of an existing program."""

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
    def get_program_codes_controller() -> tuple[Response, int]:
        """Retrieve a list of all program identifiers."""

        try:
            program_codes_details = ProgramServices.get_program_codes_service()

            return jsonify(program_codes_details), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        