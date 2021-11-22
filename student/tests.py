import pytest


def test_basic_math_operation():
    assert 10 == 2 * 5


@pytest.fixture
def numbers_list():
    return [1, 2, 3, 4]


def test_list_operation(numbers_list):
    numbers_list = [x + 1 for x in numbers_list]
    assert numbers_list == [2, 3, 4, 5]
