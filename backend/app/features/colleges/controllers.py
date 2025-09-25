from flask import request, jsonify
from dataclasses import asdict

import traceback

from .services import CollegeServices

from ..common.dataclasses import College

from app.utils import dict_keys_to_camel

class CollegeController:
    
    @staticmethod
    def get_college_details_controller(college_code: str):

        try:
            college_details: College = CollegeServices.get_college_details_service(college_code)

            return jsonify(dict_keys_to_camel(asdict(college_details))), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def get_total_college_count_controller():
        try:
            total_college_count_dict = CollegeServices.get_total_college_count_service()

            return jsonify({"totalCount": total_college_count_dict["count"]}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_many_colleges_controller():
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
    def create_college_controller():
        entity_details = request.json

        new_college_data = {
            'collegeCode': entity_details['entityDetails']['collegeCode'],
            'collegeName': entity_details['entityDetails']['collegeName']
        }

        print(new_college_data)

        try:
            CollegeServices.create_college_service(new_college_data)

            return jsonify({"message": "College added successfully."}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_college_controller(college_code: str):
        try:
            CollegeServices.delete_college_service(college_code)

            return jsonify({"message": "College deleted successfully."}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def edit_college_details_controller(college_code: str):

        entity_details = request.json

        new_college_data = {
            'collegeCode': entity_details['entityDetails']['collegeCode'],
            'collegeName': entity_details['entityDetails']['collegeName']
        }

        try:
            CollegeServices.edit_college_details_service(college_code, new_college_data)

            return jsonify({"message": "College edited successfully."}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def get_college_codes_controller():
        try:
            college_codes_details = CollegeServices.get_college_codes_service()

            print(college_codes_details)

            return jsonify(college_codes_details), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        