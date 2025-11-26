import re
from app.exceptions.custom_exceptions import ValidationError

COLLEGE_CODE_REGEX = r"^[A-Z-]{2,}$"
COLLEGE_NAME_REGEX = r"^[A-Za-z- ]{3,}$"

PROGRAM_CODE_REGEX = r"^[A-Z-]{2,}$"
PROGRAM_NAME_REGEX = r"^[A-Za-z- ]{3,}$"

ID_NUMBER_REGEX = r"^\d{4}-\d{4}$"
NAME_REGEX = r"^[A-Za-z\s'-]{1,}$"
ALLOWED_YEAR_LEVELS = {"1st", "2nd", "3rd", "4th", "4th+"}
ALLOWED_GENDERS = {"male", "female", "others", "prefer not to say"}

def validate_college_code(college_code: str, can_be_none: bool = False) -> None:
    """Validates inputted college code according to COLLEGE_CODE_REGEX."""

    if not college_code and can_be_none:
        return

    if not college_code:
        raise ValidationError("A college code cannot be blank.")
    
    if not isinstance(college_code, str):
        raise ValidationError("A college code must be a string.")
    
    college_code = college_code.strip().upper()
    
    if len(college_code) < 2:
        raise ValidationError("College code must be at least 2 characters long.")
    
    if not re.match(COLLEGE_CODE_REGEX, college_code):
        raise ValidationError(f"The college_code '{college_code}' is not in the proper format.")

def validate_college_name(college_name: str) -> None:
    """Validates inputted college name according to COLLEGE_NAME_REGEX."""

    if not college_name:
        raise ValidationError("College name cannot be blank.")
    
    if not isinstance(college_name, str):
        raise ValidationError("College name must be a string.")
    
    college_name = college_name.strip()
    
    if len(college_name) < 3:
        raise ValidationError("College name must be at least 3 characters long.")
    
    if not re.match(COLLEGE_NAME_REGEX, college_name):
        raise ValidationError(f"The college_name '{college_name}' is not in the proper format.")
    
def validate_program_code(program_code: str, can_be_none: bool = False) -> None:
    """Validates inputted program code according to PROGRAM_CODE_REGEX."""

    if not program_code and can_be_none:
        return

    if not program_code:
        raise ValidationError("A program code cannot be blank.")
    
    if not isinstance(program_code, str):
        raise ValidationError("A program code must be a string.")
    
    program_code = program_code.strip().upper()
    
    if len(program_code) < 2:
        raise ValidationError("Program code must be at least 2 characters long.")
    
    if not re.match(PROGRAM_CODE_REGEX, program_code):
        raise ValidationError(f"The college_code '{program_code}' is not in the proper format.")

def validate_program_name(program_name: str) -> None:
    """Validates inputted program name according to PROGRAM_NAME_REGEX."""

    if not program_name:
        raise ValidationError("Program name cannot be blank.")
    
    if not isinstance(program_name, str):
        raise ValidationError("Program name must be a string.")
    
    program_name = program_name.strip()
    
    if len(program_name) < 3:
        raise ValidationError("Program name must be at least 3 characters long.")
    
    if not re.match(PROGRAM_NAME_REGEX, program_name):
        raise ValidationError(f"The program_name '{program_name}' is not in the proper format.")
    
def validate_id_number(id_number: str) -> None:
    """Validates inputted ID number according to ID_NUMBER_REGEX."""

    if not id_number:
        raise ValidationError(f"An ID number cannot be blank.")
    
    if not isinstance(id_number, str):
        raise ValidationError(f"An ID number must be a string.")
    
    id_number = id_number.strip()

    if not re.match(ID_NUMBER_REGEX, id_number):
        raise ValidationError(f"The id_number '{id_number}' is not in the proper format.")
    
def validate_name(name: str, name_type: str) -> None:
    """Validates inputted name according to NAME_REGEX."""

    if not name:
        raise ValidationError(f"{name_type.capitalize()} name cannot be blank.")
    
    if not isinstance(name, str):
        raise ValidationError(f"{name_type.capitalize()} name must be a string.")
    
    name = name.strip()
    
    if not re.match(NAME_REGEX, name):
        raise ValidationError(f"The name '{name}' is not in the proper format.")

def validate_year_level(year_level: str) -> None:
    """Validates inputted year level according to ALLOWED_YEAR_LEVELS."""

    if not year_level:
        raise ValidationError("Year level cannot be blank.")
    
    if not isinstance(year_level, str):
        raise ValidationError("Year level must be a string.")
    
    year_level = year_level.strip()
    
    if not year_level in ALLOWED_YEAR_LEVELS:
        raise ValidationError(f"Invalid 'year_level' value: '{year_level}'. Must be one of: ['1st', '2nd', '3rd', '4th', '4th'].")
    
def validate_gender(gender: str) -> None:
    """Validates inputted gender according to ALLOWED_GENDERS."""

    if not gender:
        raise ValidationError("Gender cannot be blank.")
    
    if not isinstance(gender, str):
        raise ValidationError("Gender must be a string.")
    
    gender = gender.strip().lower()
    
    if not gender in ALLOWED_GENDERS:
        raise ValidationError(f"Invalid 'gender' value: '{gender}'. Must be one of: ['male', 'female', 'others', 'prefer not to say'].")