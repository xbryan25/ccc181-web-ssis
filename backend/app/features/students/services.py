from .repository import StudentRepository

from app.features.common.dataclasses import Student

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