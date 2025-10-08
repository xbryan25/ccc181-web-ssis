from flask import request, jsonify, Response
from dataclasses import asdict

import traceback

import json

from .services import StudentServices

from ..common.dataclasses.student import Student

from app.utils import dict_keys_to_camel

from psycopg.errors import UniqueViolation

class StudentController:
 

    @staticmethod
    def get_student_details_controller(id_number: str) -> tuple[Response, int]:
        """Retrieve detailed information about a specific student."""

        try:
            student_details: Student = StudentServices.get_student_details_service(id_number)

            return jsonify(dict_keys_to_camel(asdict(student_details))), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"errorMessage": str(e)}), 500
    
    @staticmethod
    def get_total_student_count_controller() -> tuple[Response, int]:
        """Retrieve the total number of students based on optional search filters."""

        try:
            params = {
                "search_value": request.args.get("searchValue"),
                "search_by": request.args.get("searchBy"),
                "search_type": request.args.get("searchType"),
            }

            filter_by = request.args.get("filterBy")

            if filter_by:

                dict_filter_by = json.loads(filter_by)

                if 'programCode' in dict_filter_by.keys():
                    params.update({"program_code": dict_filter_by['programCode']})
                    params.update({"college_code": None})

                elif 'collegeCode' in dict_filter_by.keys():
                    params.update({"program_code": None})
                    params.update({"college_code": dict_filter_by['collegeCode']})

            else:
                params.update({"program_code": None})
                params.update({"college_code": None})

            total_student_count: int = StudentServices.get_total_student_count_service(params)

            return jsonify({"totalCount": total_student_count}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"errorMessage": str(e)}), 500

    @staticmethod
    def get_many_students_controller() -> tuple[Response, int]:
        """Retrieve details of different students based on pagination, optional search and sort filters."""

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
            students = StudentServices.get_many_students_service(params)

            return jsonify({"entities": [dict_keys_to_camel(asdict(student_details)) for student_details in students]}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"errorMessage": str(e)}), 500

    @staticmethod
    def create_student_controller() -> tuple[Response, int]:
        """Create a new student record."""

        entity_details = request.json

        new_student_data = {
            'idNumber': entity_details['entityDetails']['idNumber'],
            'firstName': entity_details['entityDetails']['firstName'],
            'lastName': entity_details['entityDetails']['lastName'],
            'yearLevel': entity_details['entityDetails']['yearLevel'],
            'gender': entity_details['entityDetails']['gender'].lower(),
            'programCode': entity_details['entityDetails']['programCode']
        }

        try:
            StudentServices.create_student_service(new_student_data)

            return jsonify({"message": "Student added successfully."}), 200

        except UniqueViolation as e:
            traceback.print_exc()

            constraint_name = e.diag.constraint_name

            if constraint_name == 'students_pkey':
                return jsonify({"errorMessage": "ID number already exists."}), 500
            
            elif constraint_name == 'unique_full_name':
                return jsonify({"errorMessage": "Name combination already exists."}), 500
            
            else:
                return jsonify({"errorMessage": "Something went wrong."}), 500

        except Exception as e:
            traceback.print_exc()
            return jsonify({"errorMessage": str(e)}), 500

    @staticmethod
    def delete_student_controller(id_number: str) -> tuple[Response, int]:
        """Delete a student record by its code."""

        try:
            StudentServices.delete_student_service(id_number)

            return jsonify({"message": "Student deleted successfully."}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"errorMessage": str(e)}), 500

    @staticmethod
    def edit_student_details_controller(id_number: str) -> tuple[Response, int]:
        """Edit the details of an existing student."""

        entity_details = request.json

        new_student_data = {
            'idNumber': entity_details['entityDetails']['idNumber'],
            'firstName': entity_details['entityDetails']['firstName'],
            'lastName': entity_details['entityDetails']['lastName'],
            'yearLevel': entity_details['entityDetails']['yearLevel'],
            'gender': entity_details['entityDetails']['gender'].lower(),
            'programCode': entity_details['entityDetails']['programCode']
        }

        try:
            StudentServices.edit_student_details_service(id_number, new_student_data)

            return jsonify({"message": "Student edited successfully."}), 200
        
        except UniqueViolation as e:
            traceback.print_exc()

            constraint_name = e.diag.constraint_name

            if constraint_name == 'students_pkey':
                return jsonify({"errorMessage": "ID number already exists."}), 500
            
            elif constraint_name == 'unique_full_name':
                return jsonify({"errorMessage": "Name combination already exists."}), 500
            
            else:
                return jsonify({"errorMessage": "Something went wrong."}), 500

        except Exception as e:
            traceback.print_exc()
            return jsonify({"errorMessage": str(e)}), 500
        
    @staticmethod
    def get_year_level_demographics_controller() -> tuple[Response, int]:
        """Retrieve student year-level demographics."""

        params = {
            "program_code": request.args.get("programCode"),
            "college_code": request.args.get("collegeCode"),
        }

        try:
            year_level_demographics = StudentServices.get_year_level_demographics_service(params)

            return jsonify(year_level_demographics), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"errorMessage": str(e)}), 500
        
    @staticmethod
    def get_gender_demographics_controller() -> tuple[Response, int]:
        """Retrieve student gender demographics."""

        params = {
            "program_code": request.args.get("programCode"),
            "college_code": request.args.get("collegeCode"),
        }

        try:
            gender_demographics = StudentServices.get_gender_demographics_service(params)

            return jsonify(gender_demographics), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"errorMessage": str(e)}), 500
        