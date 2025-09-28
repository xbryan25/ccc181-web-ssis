from .repository import ProgramRepository

from app.features.common.dataclasses import Program

class ProgramServices:

    @staticmethod
    def get_program_details_service(program_code: str):
        row = ProgramRepository.get_program_by_program_code(program_code)

        return Program(**row)

    @staticmethod
    def get_total_program_count_service():
        return ProgramRepository.get_total_program_count()

    @staticmethod
    def get_many_programs_service(params):
        programs = ProgramRepository.get_many_programs(params)

        program_dataclasses = []

        for program in programs:
            if not program['college_code']:
                program['college_code'] = 'N/A'

            program_dataclasses.append(Program(**program))

        return program_dataclasses

    @staticmethod
    def create_program_service(program_data):
        ProgramRepository.create_program(program_data)

    @staticmethod
    def delete_program_service(program_code: str):
        ProgramRepository.delete_program(program_code)

    @staticmethod
    def edit_program_details_service(program_code: str, new_program_data):
        ProgramRepository.edit_program_details(program_code, new_program_data)

    @staticmethod
    def get_program_codes_service():
        program_codes_details = ProgramRepository.get_program_codes()

        print(program_codes_details)

        grouped_program_codes = {}

        for program_code_details in program_codes_details:

            if program_code_details['college_code'] not in grouped_program_codes:
                grouped_program_codes[program_code_details['college_code']] = {
                    'collegeCode': program_code_details['college_code'],
                    'programCodes': [program_code_details['program_code']]
                }

            else:
                grouped_program_codes[program_code_details['college_code']]['programCodes'].append(program_code_details['program_code'])
                
                grouped_program_codes[program_code_details['college_code']]['programCodes'].sort()


        # Rename None to "N/A"
        grouped_program_codes["N/A"] = grouped_program_codes.pop(None)
        grouped_program_codes["N/A"]['collegeCode'] = "N/A"

        # Return list of values of the dict
        return list(grouped_program_codes.values())
    