from flask import request, jsonify, Response
from dataclasses import asdict

import traceback

from .services import CollegeServices

from ..common.dataclasses import College

from app.utils import dict_keys_to_camel

from app.exceptions.custom_exceptions import EntityNotFoundError, InvalidParameterError

from psycopg.errors import UniqueViolation

class CollegeController:
    
    @staticmethod
    def get_college_details_controller(college_code: str) -> tuple[Response, int]:
        """Retrieve detailed information about a specific college."""

        try:
            college_details: College = CollegeServices.get_college_details_service(college_code.strip())

            return jsonify(dict_keys_to_camel(asdict(college_details))), 200
        
        except EntityNotFoundError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occured."}), 500
    
    @staticmethod
    def get_total_college_count_controller() -> tuple[Response, int]:
        """Retrieve the total number of colleges based on optional search filters."""

        ALLOWED_SEARCH_BY = {"College Code", "College Name"}
        ALLOWED_SEARCH_TYPE = {"Starts With", "Contains", "Ends With"}

        try:
            params = {
                "search_value": request.args.get("searchValue"),
                "search_by": request.args.get("searchBy"),
                "search_type": request.args.get("searchType"),
            }

            if params['search_by'] not in ALLOWED_SEARCH_BY:
                raise InvalidParameterError(f"Invalid 'searchBy' value: '{params['search_by']}'. Must be one of: ['College Code', 'College Name'].")

            if params["search_type"] not in ALLOWED_SEARCH_TYPE:
                raise InvalidParameterError(f"Invalid 'searchType' value: '{params["search_type"]}'. Must be one of: ['Starts With', 'Contains', 'Ends With'].")

            total_college_count = CollegeServices.get_total_college_count_service(params)

            return jsonify({"totalCount": total_college_count}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_many_colleges_controller() -> tuple[Response, int]:
        "Retrieve details of different colleges based on pagination, optional search and sort filters."

        try:
            params = {
                "rows_per_page": int(request.args.get("rowsPerPage")),
                "page_number": int(request.args.get("pageNumber")),
                "search_value": request.args.get("searchValue"),
                "search_by": request.args.get("searchBy"),
                "search_type": request.args.get("searchType"),
                "sort_field": request.args.get("sortField"),
                "sort_order":request.args.get("sortOrder")
            }

            colleges = CollegeServices.get_many_colleges_service(params)

            return jsonify({"entities": [dict_keys_to_camel(asdict(college_details)) for college_details in colleges]}), 200

        except Exception as e:
            traceback.print_exc()  
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def create_college_controller() -> tuple[Response, int]:
        """Create a new college record."""

        entity_details = request.json

        new_college_data = {
            'collegeCode': entity_details['entityDetails']['collegeCode'],
            'collegeName': entity_details['entityDetails']['collegeName']
        }

        try:
            CollegeServices.create_college_service(new_college_data)

            return jsonify({"message": "College added successfully."}), 200
                
        except UniqueViolation as e:
            traceback.print_exc()

            constraint_name = e.diag.constraint_name

            if constraint_name == 'colleges_pkey':
                return jsonify({"errorMessage": "College code already exists."}), 500
            
            elif constraint_name == 'colleges_college_name_key':
                return jsonify({"errorMessage": "College name already exists."}), 500
            
            else:
                return jsonify({"errorMessage": "Something went wrong."}), 500

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_college_controller(college_code: str) -> tuple[Response, int]:
        """Delete a college record by its code."""

        try:
            CollegeServices.delete_college_service(college_code)

            return jsonify({"message": "College deleted successfully."}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def edit_college_details_controller(college_code: str) -> tuple[Response, int]:
        """Edit the details of an existing college."""

        entity_details = request.json

        new_college_data = {
            'collegeCode': entity_details['entityDetails']['collegeCode'],
            'collegeName': entity_details['entityDetails']['collegeName']
        }

        try:
            CollegeServices.edit_college_details_service(college_code, new_college_data)

            return jsonify({"message": "College edited successfully."}), 200
        
        except UniqueViolation as e:
            traceback.print_exc()

            constraint_name = e.diag.constraint_name

            if constraint_name == 'colleges_pkey':
                return jsonify({"errorMessage": "College code already exists."}), 500
            
            elif constraint_name == 'colleges_college_name_key':
                return jsonify({"errorMessage": "College name already exists."}), 500
            
            else:
                return jsonify({"errorMessage": "Something went wrong."}), 500

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def get_college_codes_controller() -> tuple[Response, int]:
        """Retrieve a list of all college identifiers."""

        try:
            college_codes_details = CollegeServices.get_college_codes_service()

            return jsonify(college_codes_details), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        