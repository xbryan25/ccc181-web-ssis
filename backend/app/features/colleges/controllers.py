from flask import request, jsonify
from dataclasses import asdict

from .services import CollegeServices

from ..common.dataclasses import College

class CollegeController:
    
    @staticmethod
    def get_college_details_controller(college_code: str):

        try:
            college_details: College = CollegeServices.get_college_details_service(college_code)

            return jsonify({"result": asdict(college_details)}), 200

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def get_total_college_count_controller():
        try:
            total_college_count: int = CollegeServices.get_total_college_count_service()

            return jsonify({"totalCount": total_college_count}), 200

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_many_colleges_controller():
        params = {
            "rows_per_page": request.args.get("rowsPerPage"),
            "page_number": request.args.get("pageNumber"),
            "search_value": request.args.get("searchValue"),
            "search_by": request.args.get("searchBy"),
            "search_type": request.args.get("searchType"),
            "search_value": request.args.get("sortField"),
            "sort_order":request.args.get("sortOrder")
        }

        try:
            colleges = CollegeServices.get_many_colleges_service(params)

            return jsonify({"entities": [asdict(college_details) for college_details in colleges]}), 200

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def create_college_controller():
        college_data = request.json

        try:
            CollegeServices.create_college_service(college_data)

            return jsonify({"message": "College added successfully."}), 200

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_college_controller(college_code: str):
        try:
            CollegeServices.delete_college_service(college_code)

            return jsonify({"message": "College deleted successfully."}), 200

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def edit_college_details_controller(college_code: str):

        new_college_data = request.json

        try:
            CollegeServices.edit_college_details_service(college_code, new_college_data)

            return jsonify({"message": "College edited successfully."}), 200

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500