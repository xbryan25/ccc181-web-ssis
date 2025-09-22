import re

def to_camel_case(s: str) -> str:
    return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), s)

def dict_keys_to_camel(d: dict) -> dict:
    return {to_camel_case(k): v for k, v in d.items()}