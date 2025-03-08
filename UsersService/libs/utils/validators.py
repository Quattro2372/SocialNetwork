import re

PHONE_REGEXP = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
EMAIL_REGEXP = r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)'
PASSWORD_REGEXP = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'

def validate_phone_number(phone_number: str) -> bool:
    return bool(re.match(PHONE_REGEXP, phone_number))

def validate_email(email: str) -> bool:
    return bool(re.match(EMAIL_REGEXP, email))

def validate_password(password: str) -> bool:
    return bool(re.match(PASSWORD_REGEXP, password))