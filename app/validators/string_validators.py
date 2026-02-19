import re
from app.exceptions.exception import EmptyError,NoAlphabetsError,MobNoError
pattern_number=re.compile(r"^\d{10}$")
pattern_string_check=re.compile(r"^[A-Za-z]+([ -][A-Za-z0-9\,\.]+)*$")
pattern_password_small=re.compile(r"""(?=.*[a-z])""")
pattern_password_caps=re.compile(r"""(?=.*[A-Z])""")
pattern_password_digits=re.compile(r"""(?=.*\d)""")                       
pattern_password_characters=re.compile(r"""(?=.*[^A-Za-z0-9])""")
pattern_salary = re.compile(
    r"""^
    [₹$]?\s* 
    \d+(?:\.\d+)?                  
    (?:[kK]|LPA)?                     
    (?:\s*-\s*
        \d+(?:\.\d+)?                
        (?:[kK]|LPA)?                
    )?
    (?:\s*/\s*(month|year))?          
    $
    """,
    re.VERBOSE
)


from app.exceptions.exception import (
    EmptyError,
    NoAlphabetsError,
    MobNoError,
    PasswordLenError,
    PasswordLowerCaseError,
    PasswordUpperCaseError,
    PasswordDigitError,
    PasswordCharactersError,
)

def require_valid_non_empty(value: str, field_name: str) -> str:
    if value is None:
        raise EmptyError(f"{field_name} cannot be None")

    value = value.strip()

    if not value:
        raise EmptyError(f"{field_name} cannot be empty")

    if not pattern_string_check.fullmatch(value):
        raise NoAlphabetsError(f"{field_name} must contain alphabets")

    return value


def require_non_empty(value: str, field_name: str) -> str:
    if value is None:
        raise EmptyError(f"{field_name} cannot be None")

    value = value.strip()

    if not value:
        raise EmptyError(f"{field_name} cannot be empty")

    return value


def number_pattern(value: str, field_name: str) -> str:
    if not pattern_number.fullmatch(value):
        raise MobNoError(f"{field_name} must be 10 digits")

    return value


def password_check(value: str, field_name: str) -> str:
    if len(value) < 8:
        raise PasswordLenError(f"{field_name} must be at least 8 characters")

    if not pattern_password_small.search(value):
        raise PasswordLowerCaseError(f"{field_name} must contain lowercase letter")

    if not pattern_password_caps.search(value):
        raise PasswordUpperCaseError(f"{field_name} must contain uppercase letter")

    if not pattern_password_digits.search(value):
        raise PasswordDigitError(f"{field_name} must contain digit")

    if not pattern_password_characters.search(value):
        raise PasswordCharactersError(f"{field_name} must contain special character")

    return value
