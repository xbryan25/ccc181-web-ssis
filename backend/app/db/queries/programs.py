

class ProgramQueries:
    GET_TOTAL_COUNT_FROM_COLLEGE_CODE = "SELECT COUNT(*) FROM programs WHERE college_code = %s"