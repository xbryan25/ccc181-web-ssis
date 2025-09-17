from .repository import CollegeRepository

class CollegeServices:

    @staticmethod
    def get_college_details_service(college_code: str):
        return CollegeRepository.get_college_by_college_code(college_code)
    
    @staticmethod
    def get_total_college_count_service():
        return CollegeRepository.get_total_college_count()

    @staticmethod
    def get_many_colleges_service(params):
        return CollegeRepository.get_many_colleges(params)

    @staticmethod
    def create_college_service(college_data):
        CollegeRepository.create_college(college_data)

    @staticmethod
    def delete_college_service(college_code: str):
        CollegeRepository.create_college(college_code)

    @staticmethod
    def edit_college_details_service(college_code: str, new_college_data):
        CollegeRepository.edit_college_details(college_code, new_college_data)
