import pytest
from ..validators import validate_email, validate_phone_number, validate_password

@pytest.mark.parametrize('email, valid', [
    ("abc", False),
    ("mail@google.ru", True),
    ("mailgoogle.ru", False),
    ("", False),
    ("example@yandex.ru", True),
])
def test_email_validation(email: str, valid: bool) -> None:
    assert validate_email(email) == valid

@pytest.mark.parametrize('phone, valid', [
    ("+79273451232", True),
    ("8(927)0873254", True),
    ("0943434314324323432", False),
    ("", False),
    ("feafeafeafea89271133212", False),
])
def test_phone_validation(phone: str, valid: bool) -> None:
    assert validate_phone_number(phone) == valid

@pytest.mark.parametrize('password, valid', [
    ("abcdef", False),
    ("", False),
    ("PasswordExample123", True),
    ("PasswordExample", False),
    ("123456", False),
])
def test_password_validation(password: str, valid: bool) -> None:
    assert validate_password(password) == valid
