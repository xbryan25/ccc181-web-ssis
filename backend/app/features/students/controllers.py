from flask import request, jsonify
from dataclasses import asdict

import traceback

from .services import StudentServices

from ..common.dataclasses.student import Student

from app.utils import dict_keys_to_camel

class StudentController:
 

    @staticmethod
    def get_student_details_controller(id_number: str):

        try:
            student_details: Student = StudentServices.get_student_details_service(id_number)

            return jsonify(dict_keys_to_camel(asdict(student_details))), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def get_total_student_count_controller():
        try:
            total_student_count_dict: int = StudentServices.get_total_student_count_service()

            return jsonify({"totalCount": total_student_count_dict["count"]}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_many_students_controller():
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
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def create_student_controller():

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

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_student_controller(id_number: str):
        try:
            StudentServices.delete_student_service(id_number)

            return jsonify({"message": "Student deleted successfully."}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def edit_student_details_controller(id_number: str):

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

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500