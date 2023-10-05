import pytest
from unittest.mock import mock_open, patch
from src.YAMLDataReader import YAMLDataReader

# Ваши входные данные для тестирования в формате строки
yaml_example = """\
- Тихонов Николай Игоревич:
    математика: '80'
    астрономия: '79'
    физика: '75'
"""

# Ожидаемый словарь данных после чтения и преобразования
expected_output = {'Тихонов Николай Игоревич': [
    ('математика', 80), ('астрономия', 79), ('физика', 75)]}


@pytest.fixture
def yaml_reader():
    return YAMLDataReader()


def test_read_correct_data(yaml_reader):
    # Используем mock_open, чтобы сымитировать чтение файла
    m = mock_open(read_data=yaml_example)
    m.return_value.__iter__ = lambda self: self
    m.return_value.__next__ = lambda self: next(iter(self.readline, ''))

    # Патчим встроенную функцию open, чтобы использовать нашу имитацию чтения
    # файла
    with patch("builtins.open", m, create=True):
        result = yaml_reader.read("dummy_path")

    assert result == expected_output, f"Expected \
    {expected_output}, got {result}"
