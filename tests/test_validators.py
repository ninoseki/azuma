import pytest

from azuma.validators import is_valid_date_format


@pytest.mark.parametrize(
    "v,expected", [("2020/01/01", True), ("2020/01/01 10:00:00", False), ("foo", False)]
)
def test_is_valid_date_format(v: str, expected: bool):
    assert is_valid_date_format(v) is expected
