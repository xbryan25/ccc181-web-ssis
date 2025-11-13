from flask import request, jsonify, Response
from dataclasses import asdict

import traceback

import json

from .services import StudentServices

from ..programs.services import ProgramServices

from ..colleges.services import CollegeServices

from ..common.dataclasses.student import Student

from app.utils import dict_keys_to_camel, validate_id_number, validate_name, validate_year_level, validate_gender, validate_program_code, validate_college_code

from app.exceptions.custom_exceptions import EntityNotFoundError, InvalidParameterError, ValidationError

from psycopg.errors import UniqueViolation, ForeignKeyViolation

class StudentController:
 
    @staticmethod
    def get_student_details_controller(id_number: str) -> tuple[Response, int]:
        """Retrieve detailed information about a specific student."""

        try:
            validate_id_number(id_number)

            student_details: Student = StudentServices.get_student_details_service(id_number.strip())

            return jsonify(dict_keys_to_camel(asdict(student_details))), 200

        except EntityNotFoundError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400
        
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
    def get_total_student_count_controller() -> tuple[Response, int]:
        """Retrieve the total number of students based on optional search filters."""

        ALLOWED_SEARCH_BY = {"ID Number", "First Name", "Last Name", "Gender", "Year Level", "Program Code"}
        ALLOWED_SEARCH_TYPE = {"Starts With", "Contains", "Ends With"}

        try:
            params = {
                "search_value": request.args.get("searchValue"),
                "search_by": request.args.get("searchBy"),
                "search_type": request.args.get("searchType"),
            }

            # Validate search_by and search_type parameters

            if params['search_by'] and params['search_by'] not in ALLOWED_SEARCH_BY:
                raise InvalidParameterError(f"Invalid 'searchBy' value: '{params['search_by']}'. Must be one of: ['ID Number', 'First Name', 'Last Name', 'Gender', 'Year Level', 'Program Code'].")

            if params['search_type'] and params["search_type"] not in ALLOWED_SEARCH_TYPE:
                raise InvalidParameterError(f"Invalid 'searchType' value: '{params["search_type"]}'. Must be one of: ['Starts With', 'Contains', 'Ends With'].")

            filter_by = request.args.get("filterBy")

            # Apply filter_by logic

            if filter_by and filter_by != '{}':
                try:
                    dict_filter_by = json.loads(filter_by)
                except json.JSONDecodeError:
                    raise InvalidParameterError("'filterBy' must be a valid JSON object string.")

                if not isinstance(dict_filter_by, dict):
                    raise InvalidParameterError("'filterBy' must be a JSON object (e.g., {\"programCode\": \"BSCS\"}).")

                allowed_keys = {"programCode", "collegeCode"}
                keys_present = set(dict_filter_by.keys())

                # Check for invalid keys
                unknown_keys = keys_present - allowed_keys
                if unknown_keys:
                    raise InvalidParameterError(f"Invalid key(s) in 'filterBy': {', '.join(unknown_keys)}")

                # Check that exactly one key is present
                if len(keys_present) != 1:
                    raise InvalidParameterError("'filterBy' must contain exactly one of 'programCode' or 'collegeCode'.")

                # Apply filter logic
                if "programCode" in dict_filter_by:
                    params.update({
                        "program_code": dict_filter_by["programCode"],
                        "college_code": None
                    })
                elif "collegeCode" in dict_filter_by:
                    params.update({
                        "program_code": None,
                        "college_code": dict_filter_by["collegeCode"]})

            else:
                params.update({
                    "program_code": None,
                    "college_code": None
                })

            # Only one of these should be present at a time
            if sum(bool(x) for x in [params["search_value"], params["program_code"], params["college_code"]]) > 1:
                raise InvalidParameterError("Only one should exist at a time between 'searchValue', 'programCode', and 'collegeCode'.")

            total_student_count: int = StudentServices.get_total_student_count_service(params)

            return jsonify({"totalCount": total_student_count}), 200
        
        except InvalidParameterError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500

    @staticmethod
    def get_many_students_controller() -> tuple[Response, int]:
        """Retrieve details of different students based on pagination, optional search and sort filters."""

        ALLOWED_SEARCH_BY = {"ID Number", "First Name", "Last Name", "Year Level", "Gender", "Program Code"}
        ALLOWED_SEARCH_TYPE = {"Starts With", "Contains", "Ends With"}
        ALLOWED_SORT_FIELD = {"ID Number", "First Name", "Last Name", "Year Level", "Gender", "Program Code"}
        ALLOWED_SORT_ORDER = {"Ascending", "Descending"}

        try:
            params = {
            "rows_per_page": int(request.args.get("rowsPerPage", 10)),
            "page_number": int(request.args.get("pageNumber", 1)),
            "search_value": (request.args.get("searchValue") or "").strip(),
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
                raise InvalidParameterError(f"Invalid 'searchBy' value: '{params['search_by']}'. Must be one of: ['ID Number', 'First Name', 'Last Name', 'Year Level', 'Gender', 'Program Code'].")

            if params["search_type"] not in ALLOWED_SEARCH_TYPE:
                raise InvalidParameterError(f"Invalid 'searchType' value: '{params["search_type"]}'. Must be one of: ['Starts With', 'Contains', 'Ends With'].")
            
            if params['sort_field'] not in ALLOWED_SORT_FIELD:
                raise InvalidParameterError(f"Invalid 'sortField' value: '{params['sort_field']}'. Must be one of: ['ID Number', 'First Name', 'Last Name', 'Year Level', 'Gender', 'Program Code'].")

            if params["sort_order"] not in ALLOWED_SORT_ORDER:
                raise InvalidParameterError(f"Invalid 'sortOrder' value: '{params["sort_order"]}'. Must be one of: ['Ascending', 'Descending'].")

            students = StudentServices.get_many_students_service(params)

            return jsonify({"entities": [dict_keys_to_camel(asdict(student_details)) for student_details in students]}), 200
        
        except InvalidParameterError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400
        
        except (ValueError, TypeError) as e:
            return jsonify({
                "error": "Invalid query parameter. 'rowsPerPage' and 'pageNumber' must be positive integers."
            }), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def create_student_controller() -> tuple[Response, int]:
        """Create a new student record. If avatar is provided, upload to Supabase bucket."""

        new_student_data = {}

        try:
            new_student_data = {
                "id_number": request.form.get("idNumber", "-"),
                "first_name": request.form.get("firstName", "-"),
                "last_name": request.form.get("lastName", "-"),
                "year_level": request.form.get("yearLevel", "-"),
                "gender": request.form.get("gender", "-"),
                "program_code": request.form.get("programCode", "-")
            }

            student_avatar = request.files.get('avatar')
            
            validate_id_number(new_student_data['id_number'])

            validate_name(new_student_data['first_name'], "First")

            validate_name(new_student_data['last_name'], "Last")

            validate_year_level(new_student_data['year_level'])

            validate_gender(new_student_data['gender'])

            validate_program_code(new_student_data['program_code'])

            new_student_data['id_number'] = new_student_data['id_number'].strip()
            new_student_data['first_name'] = new_student_data['first_name'].strip()
            new_student_data['last_name'] = new_student_data['last_name'].strip()
            new_student_data['year_level'] = new_student_data['year_level'].strip()
            new_student_data['gender'] = new_student_data['gender'].strip().lower()
            new_student_data['program_code'] = new_student_data['program_code'].strip().upper()

            StudentServices.create_student_service(new_student_data, student_avatar)

            return jsonify({"message": "Student added successfully."}), 200

        except UniqueViolation as e:
            traceback.print_exc()

            constraint_name = e.diag.constraint_name

            if constraint_name == 'students_pkey':
                return jsonify({"error": "ID number already exists."}), 500
            
            elif constraint_name == 'unique_full_name':
                return jsonify({"error": "Name combination already exists."}), 500
            
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
            return jsonify({"error": f"The program_code '{new_student_data['program_code']}' doesn't exist in the 'programs' table."}), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500

    @staticmethod
    def delete_student_controller(id_number: str) -> tuple[Response, int]:
        """Delete a student record by its code."""

        try:
            validate_id_number(id_number)
            
            # Check if ID number exists or not
            StudentServices.get_student_details_service(id_number.strip())

            # If it exists, delete it
            StudentServices.delete_student_service(id_number.strip())

            return jsonify({"message": "Student deleted successfully."}), 200
        
        except EntityNotFoundError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
        except ValidationError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def edit_student_details_controller(id_number: str) -> tuple[Response, int]:
        """Edit the details of an existing student."""

        new_student_data = {}

        try:
            new_student_data = {
                "existing_avatar_url": request.form.get("existingAvatarUrl"),
                "id_number": request.form.get("idNumber", "-"),
                "first_name": request.form.get("firstName", "-"),
                "last_name": request.form.get("lastName", "-"),
                "year_level": request.form.get("yearLevel", "-"),
                "gender": request.form.get("gender", "-"),
                "program_code": request.form.get("programCode", "-")
            }

            new_student_avatar = request.files.get('avatar')

            validate_id_number(id_number)

            id_number = id_number.strip()

            # Check if ID number exists or not
            StudentServices.get_student_details_service(id_number)

            validate_id_number(new_student_data['id_number'])

            validate_name(new_student_data['first_name'], "First")

            validate_name(new_student_data['last_name'], "Last")

            validate_year_level(new_student_data['year_level'])

            validate_gender(new_student_data['gender'])

            validate_program_code(new_student_data['program_code'])

            new_student_data['id_number'] = new_student_data['id_number'].strip()
            new_student_data['first_name'] = new_student_data['first_name'].strip()
            new_student_data['last_name'] = new_student_data['last_name'].strip()
            new_student_data['year_level'] = new_student_data['year_level'].strip()
            new_student_data['gender'] = new_student_data['gender'].strip().lower()
            new_student_data['program_code'] = new_student_data['program_code'].strip().upper()

            StudentServices.edit_student_details_service(id_number, new_student_data, new_student_avatar)

            return jsonify({"message": "Student edited successfully."}), 200
        
        except UniqueViolation as e:
            traceback.print_exc()

            constraint_name = e.diag.constraint_name

            if constraint_name == 'students_pkey':
                return jsonify({"error": "ID number already exists."}), 500
            
            elif constraint_name == 'unique_full_name':
                return jsonify({"error": "Name combination already exists."}), 500
            
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
            return jsonify({"error": f"The program_code '{new_student_data['program_code']}' doesn't exist in the 'programs' table."}), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def get_year_level_demographics_controller() -> tuple[Response, int]:
        """Retrieve student year-level demographics."""

        try:
            params = {
                "program_code": request.args.get("programCode") or "",
                "college_code": request.args.get("collegeCode") or "",
            }

            validate_program_code(params["program_code"], can_be_none=True)
            validate_college_code(params["college_code"], can_be_none=True)

            if params['program_code']:
                params['program_code'] = params['program_code'].strip().upper()
                ProgramServices.get_program_details_service(params['program_code'])
            
            if params['college_code']:
                params['college_code'] = params['college_code'].strip().upper()
                CollegeServices.get_college_details_service(params['college_code'])

            # Only one of these should be present at a time
            if sum(bool(x) for x in [params["program_code"], params["college_code"]]) > 1:
                raise InvalidParameterError("Only one should exist at a time between 'programCode', and 'collegeCode'.")

            year_level_demographics = StudentServices.get_year_level_demographics_service(params)

            return jsonify(year_level_demographics), 200
        
        except EntityNotFoundError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400

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
    def get_gender_demographics_controller() -> tuple[Response, int]:
        """Retrieve student gender demographics."""

        try:
            params = {
                "program_code": request.args.get("programCode") or "",
                "college_code": request.args.get("collegeCode") or "",
            }

            validate_program_code(params["program_code"], can_be_none=True)
            validate_college_code(params["college_code"], can_be_none=True)

            if params['program_code']:
                params['program_code'] = params['program_code'].strip().upper()
                ProgramServices.get_program_details_service(params['program_code'])
            
            if params['college_code']:
                params['college_code'] = params['college_code'].strip().upper()
                CollegeServices.get_college_details_service(params['college_code'])

            # Only one of these should be present at a time
            if sum(bool(x) for x in [params["program_code"], params["college_code"]]) > 1:
                raise InvalidParameterError("Only one should exist at a time between 'programCode', and 'collegeCode'.")

            gender_demographics = StudentServices.get_gender_demographics_service(params)

            return jsonify(gender_demographics), 200

        except EntityNotFoundError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400

        except InvalidParameterError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400
        
        except ValidationError as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500
        