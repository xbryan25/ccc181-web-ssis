from app.db.connection import Database
from app.db.queries.programs import ProgramQueries
from app.db.queries.common import CommonQueries

class ProgramRepository:

    @staticmethod
    def get_program_by_program_code(program_code: str) -> dict | None:
        return Database().fetch_one(CommonQueries.GET_BY_ID.format(table="programs", pk="program_code"), (program_code, ))

    @staticmethod
    def get_total_program_count() -> int:
        pass

    def get_many_programs(params):
        pass

    def create_program(program_data):
        pass

    def delete_program(program_code: str):
        pass

    def edit_program_details(program_code: str, new_program_data):
        pass
