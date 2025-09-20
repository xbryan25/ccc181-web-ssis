from .repository import CollegeRepository

from app.features.common.dataclasses import College

class CollegeServices:

    @staticmethod
    def get_college_details_service(college_code: str):

        row = CollegeRepository.get_college_by_college_code(college_code)

        return College(**row)
    
    @staticmethod
    def get_total_college_count_service():
        return CollegeRepository.get_total_college_count()

    @staticmethod
    def get_many_colleges_service(params):
        colleges = CollegeRepository.get_many_colleges(params)

        college_dataclasses = []

        for college in colleges:
            college_dataclasses.append(College(**college))

        return college_dataclasses

    @staticmethod
    def create_college_service(college_data):
        CollegeRepository.create_college(college_data)

    @staticmethod
    def delete_college_service(college_code: str):
        CollegeRepository.delete_college(college_code)

    @staticmethod
    def edit_college_details_service(college_code: str, new_college_data):
        CollegeRepository.edit_college_details(college_code, new_college_data)
