from flask import request, jsonify, Response
from dataclasses import asdict

import traceback

import json

from .services import ProgramServices

from ..common.dataclasses import Program

from app.utils import dict_keys_to_camel, validate_program_code, validate_program_name, validate_college_code

from app.exceptions.custom_exceptions import EntityNotFoundError, InvalidParameterError, ValidationError

from psycopg.errors import UniqueViolation, ForeignKeyViolation

class ProgramController:
    
    @staticmethod
    def get_program_details_controller(program_code: str) -> tuple[Response, int]:
        """Retrieve detailed information about a specific program."""

        try:
            validate_program_code(program_code)

            program_details: Program = ProgramServices.get_program_details_service(program_code.strip())

            return jsonify(dict_keys_to_camel(asdict(program_details))), 200
        
        except EntityNotFoundError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
        except InvalidParameterError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400
        
        except ValidationError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500
    
    @staticmethod
    def get_total_program_count_controller() -> tuple[Response, int]:
        """Retrieve the total number of programs based on optional search filters."""

        ALLOWED_SEARCH_BY = {"Program Code", "Program Name", "College Code"}
        ALLOWED_SEARCH_TYPE = {"Starts With", "Contains", "Ends With"}

        try:
            params = {
                "search_value": request.args.get("searchValue"),
                "search_by": request.args.get("searchBy"),
                "search_type": request.args.get("searchType"),
            }

            # Validate search_by and search_type parameters

            if params['search_by'] and params['search_by'] not in ALLOWED_SEARCH_BY:
                raise InvalidParameterError(f"Invalid 'searchBy' value: '{params['search_by']}'. Must be one of: ['Program Code', 'Program Name', 'College Code'].")

            if params["search_type"] and params["search_type"] not in ALLOWED_SEARCH_TYPE:
                raise InvalidParameterError(f"Invalid 'searchType' value: '{params["search_type"]}'. Must be one of: ['Starts With', 'Contains', 'Ends With'].")

            filter_by = request.args.get("filterBy")

            # Apply filter_by logic

            if filter_by:
                try:
                    dict_filter_by = json.loads(filter_by)
                except json.JSONDecodeError:
                    raise InvalidParameterError("'filterBy' must be a valid JSON object string.")

                if not isinstance(dict_filter_by, dict):
                    raise InvalidParameterError("'filterBy' must be a JSON object (e.g., {\"collegeCode\": \"CCS\"}).")

                allowed_keys = {"collegeCode"}
                keys_present = set(dict_filter_by.keys())

                # Check for invalid keys
                unknown_keys = keys_present - allowed_keys
                if unknown_keys:
                    raise InvalidParameterError(f"Invalid key(s) in 'filterBy': {', '.join(unknown_keys)}")

                # Check that exactly one key is present
                if len(keys_present) != 1:
                    raise InvalidParameterError("'filterBy' must contain exactly 'collegeCode'.")

                # Apply filter logic
                if "collegeCode" in dict_filter_by:
                    params.update({"college_code": dict_filter_by["collegeCode"]})

            else:
                params.update({
                    "college_code": None
                })

            # Only one of these should be present at a time
            if sum(bool(x) for x in [params["search_value"], params["college_code"]]) > 1:
                raise InvalidParameterError("Only one should exist at a time between 'searchValue', and 'collegeCode'.")

            total_program_count = ProgramServices.get_total_program_count_service(params)

            return jsonify({"totalCount": total_program_count}), 200
        
        except InvalidParameterError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500

    @staticmethod
    def get_many_programs_controller() -> tuple[Response, int]:
        """Retrieve details of different programs based on pagination, optional search and sort filters."""

        ALLOWED_SEARCH_BY = {"Program Code", "Program Name", "College Code"}
        ALLOWED_SEARCH_TYPE = {"Starts With", "Contains", "Ends With"}
        ALLOWED_SORT_FIELD = {"Program Code", "Program Name", "College Code"}
        ALLOWED_SORT_ORDER = {"Ascending", "Descending"}

        try:
            
            params = {
                "rows_per_page": int(request.args.get("rowsPerPage", 10)),
                "page_number": int(request.args.get("pageNumber", 1)),
                "search_value": ((request.args.get("searchValue")) or "").strip(),
                "search_by": request.args.get("searchBy"),
                "search_type": request.args.get("searchType"),
                "sort_field": request.args.get("sortField"),
                "sort_order":request.args.get("sortOrder")
            }

            if params['rows_per_page'] < 0:
                raise InvalidParameterError(f"Invalid 'rowsPerPage' value: '{params['rows_per_page']}'. Must be a positive integer.")
            
            if params['page_number'] < 0:
                raise InvalidParameterError(f"Invalid 'pageNumber' value: '{params['page_number']}'. Must be a positive integer.")
            
            if params['search_by'] not in ALLOWED_SEARCH_BY:
                raise InvalidParameterError(f"Invalid 'searchBy' value: '{params['search_by']}'. Must be one of: ['Program Code', 'Program Name', 'College Code'].")

            if params["search_type"] not in ALLOWED_SEARCH_TYPE:
                raise InvalidParameterError(f"Invalid 'searchType' value: '{params["search_type"]}'. Must be one of: ['Starts With', 'Contains', 'Ends With'].")
            
            if params['sort_field'] not in ALLOWED_SORT_FIELD:
                raise InvalidParameterError(f"Invalid 'sortField' value: '{params['sort_field']}'. Must be one of: ['Program Code', 'Program Name', 'College Code'].")

            if params["sort_order"] not in ALLOWED_SORT_ORDER:
                raise InvalidParameterError(f"Invalid 'sortOrder' value: '{params["sort_order"]}'. Must be one of: ['Ascending', 'Descending'].")
            
            programs = ProgramServices.get_many_programs_service(params)

            return jsonify({"entities": [dict_keys_to_camel(asdict(program_details)) for program_details in programs]}), 200
        
        except InvalidParameterError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400
        
        except (ValueError, TypeError) as e:
            return jsonify({
                "error": "Invalid query parameter. 'rowsPerPage' and 'pageNumber' must be positive integers."
            }), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500

    @staticmethod
    def create_program_controller() -> tuple[Response, int]:
        """Create a new program record."""
        
        entity_details = request.json or {}

        new_program_data = {}

        try:
            new_program_data = {
                'program_code': entity_details['entityDetails']['programCode'],
                'program_name': entity_details['entityDetails']['programName'],
                'college_code': entity_details['entityDetails']['collegeCode']
            }

            validate_program_code(new_program_data['program_code'])

            validate_program_name(new_program_data['program_name'])

            validate_college_code(new_program_data['college_code'])

            new_program_data['program_code'] = new_program_data['program_code'].strip().upper()
            new_program_data['program_name'] = new_program_data['program_name'].strip()
            new_program_data['college_code'] = new_program_data['college_code'].strip().upper()

            ProgramServices.create_program_service(new_program_data)

            return jsonify({"message": "Program added successfully."}), 200
        
        except UniqueViolation as e:
            traceback.print_exc()

            constraint_name = e.diag.constraint_name

            if constraint_name == 'programs_pkey':
                return jsonify({"error": "Program code already exists."}), 500
            
            elif constraint_name == 'programs_program_name_key':
                return jsonify({"error": "Program name already exists."}), 500
            
            else:
                return jsonify({"error": "Something went wrong."}), 500
            
        except KeyError as e:
            traceback.print_exc()
            return jsonify({"error": f"The key {str(e)} doesn't exist in the body."}), 400

        except ValidationError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400
            
        except ForeignKeyViolation as e:
            traceback.print_exc()
            return jsonify({"error": f"The college_code '{new_program_data['college_code']}' doesn't exist in the 'colleges' table."}), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500

    @staticmethod
    def delete_program_controller(program_code: str) -> tuple[Response, int]:
        """Delete a program record by its code."""

        try:
            validate_program_code(program_code)

            # Check if program code exists or not
            ProgramServices.get_program_details_service(program_code.strip().upper())

            # If it exists, delete it
            ProgramServices.delete_program_service(program_code.strip().upper())

            return jsonify({"message": "Program deleted successfully."}), 200
        
        except EntityNotFoundError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
        except ValidationError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500

    @staticmethod
    def edit_program_details_controller(program_code: str) -> tuple[Response, int]:
        """Edit the details of an existing program."""

        entity_details = request.json or {}

        new_program_data = {}

        try:
            new_program_data = {
            'program_code': entity_details['entityDetails']['programCode'],
            'program_name': entity_details['entityDetails']['programName'],
            'college_code': entity_details['entityDetails']['collegeCode']
            }

            validate_program_code(program_code)

            program_code = program_code.strip().upper()

            # Check if program code exists or not
            ProgramServices.get_program_details_service(program_code)

            validate_program_code(new_program_data['program_code'])

            validate_program_name(new_program_data['program_name'])

            validate_college_code(new_program_data['college_code'])

            new_program_data['program_code'] = new_program_data['program_code'].strip().upper()
            new_program_data['program_name'] = new_program_data['program_name'].strip()
            new_program_data['college_code'] = new_program_data['college_code'].strip().upper()

            ProgramServices.edit_program_details_service(program_code, new_program_data)

            return jsonify({"message": "Program edited successfully."}), 200
              
        except UniqueViolation as e:
            traceback.print_exc()

            constraint_name = e.diag.constraint_name

            if constraint_name == 'programs_pkey':
                return jsonify({"error": "Program code already exists."}), 500
            
            elif constraint_name == 'programs_program_name_key':
                return jsonify({"error": "Program name already exists."}), 500
            
            else:
                return jsonify({"error": "Something went wrong."}), 500
            
        except EntityNotFoundError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
        except KeyError as e:
            traceback.print_exc()
            return jsonify({"error": f"The key {str(e)} doesn't exist in the body."}), 400

        except ValidationError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400
            
        except ForeignKeyViolation as e:
            traceback.print_exc()
            return jsonify({"error": f"The college_code '{new_program_data['college_code']}' doesn't exist in the 'colleges' table."}), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500
        
    @staticmethod
    def get_program_codes_controller() -> tuple[Response, int]:
        """Retrieve a list of all program identifiers."""

        try:
            program_codes_details = ProgramServices.get_program_codes_service()

            return jsonify(program_codes_details), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        