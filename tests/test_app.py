
from src.boilerplate.app import is_valid_date


def test_valid_date():
    assert is_valid_date("2023-10-26")
    assert is_valid_date("2024-02-29")  # Leap year

def test_invalid_date_format():
    assert not is_valid_date("2023/10/26")
    assert not is_valid_date("26-10-2023")
    assert not is_valid_date("20231026")
    assert not is_valid_date("10-2023")

def test_invalid_date_values():
    assert not is_valid_date("2023-13-26")
    assert not is_valid_date("2023-10-32")
    

