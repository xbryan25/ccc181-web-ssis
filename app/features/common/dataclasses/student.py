from dataclasses import dataclass

@dataclass
class Student:
    id_number: str
    first_name: str
    last_name: str
    year_level: str
    gender: str
    avatar_url: str
    program_code: str
    