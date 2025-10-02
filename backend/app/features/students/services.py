from .repository import StudentRepository

from app.features.common.dataclasses import Student

from app.utils import to_camel_case

class StudentServices:

    @staticmethod
    def get_student_details_service(id_number: str):
    
        row = StudentRepository.get_student_by_id(id_number)

        return Student(**row)
    
    @staticmethod
    def get_total_student_count_service():
        return StudentRepository.get_total_student_count()

    @staticmethod
    def get_many_students_service(params):
        students = StudentRepository.get_many_students(params)

        student_dataclasses = []

        for student in students:
            student['gender'] = student['gender'].capitalize()

            if not student['program_code']:
                student['program_code'] = 'N/A'

            student_dataclasses.append(Student(**student))

        return student_dataclasses

    @staticmethod
    def create_student_service(student_data):
        StudentRepository.create_student(student_data=student_data)

    @staticmethod
    def delete_student_service(id_number: str):
       StudentRepository.delete_student(id_number=id_number)

    @staticmethod
    def edit_student_details_service(id_number: str, new_student_data):
        StudentRepository.edit_student_details(id_number=id_number, new_student_data=new_student_data)

    @staticmethod
    def get_year_level_demographics_service():
        
        # TODO: do get for programs and services params

        year_level_demographics = StudentRepository.get_year_level_demographics()

        formatted_year_level_demographics = [{to_camel_case(k): v for k, v in year_level_demographic.items()} for year_level_demographic in year_level_demographics]

        return formatted_year_level_demographics
    
    @staticmethod
    def get_gender_demographics_service():
        
        # TODO: do get for programs and services params

        gender_demographics = StudentRepository.get_gender_demographics()

        formatted_gender_demographics = [{to_camel_case(k): v for k, v in gender_demographic.items()} for gender_demographic in gender_demographics]

        return formatted_gender_demographics
    