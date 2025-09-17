from .repository import ProgramRepository

class ProgramServices:

    @staticmethod
    def get_program_details_service(program_code: str):
        return ProgramRepository.get_program_by_program_code(program_code)
    
    @staticmethod
    def get_total_program_count_service():
        return ProgramRepository.get_total_program_count()

    @staticmethod
    def get_many_programs_service(params):
        return ProgramRepository.get_many_programs(params)

    @staticmethod
    def create_program_service(program_data):
        ProgramRepository.create_program(program_data)

    @staticmethod
    def delete_program_service(program_code: str):
        ProgramRepository.create_program(program_code)

    @staticmethod
    def edit_program_details_service(program_code: str, new_program_data):
        ProgramRepository.edit_program_details(program_code, new_program_data)
