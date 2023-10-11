[![Build Status](https://app.travis-ci.com/AnSpi/TPLab1.svg?branch=main)](https://app.travis-ci.com/AnSpi/TPLab1)
# Лабораторная 1 по дисциплине "Технологии программирования"
Знакомство с системой контроля версий Git и инструментом CI/CD Travis CI
## Цели работы
1. Познакомиться c распределенной системой контроля версий кода Git и ее функциями;
2. Познакомиться с понятиями «непрерывная интеграция» (CI) и «непрерывное развертывание»
(CD), определить их место в современной разработке программного обеспечения;
3. Получить навыки разработки ООП-программ и написания модульных тестов к ним на
современных языках программирования;
4. Получить навыки работы с системой Git для хранения и управления версиями ПО;
5. Получить навыки управления автоматизированным тестированием программного обеспечения,
расположенного в системе Git, с помощью инструмента Travis CI.
## Индивидуальное задание:
Формат входного файла: YAML
Расчетная процедура: Определить и вывести на экран всех студентов, чей рейтинг попадает во вторую квартиль распределения по рейтингам.

## Ход работы
Для выполнения индивидуального задания согласно 8 варианту создадим файл формата YAML, класс YAMLDataReader.py как наследник класса DataReader, тест этого класса и изменим файл main для работы с новым класом. Для этого откроем ветку YAMLDataReader проекта.

#### Представленный в файле src/YAMLDataReader.py класс реализует чтение данных из  файлов формата .yaml
```python
import yaml
from typing import Dict, List, Tuple


class YAMLDataReader:
    def read(self, path: str) -> Dict[str, List[Tuple[str, int]]]:
        students = {}
        with open(path, encoding='utf-8') as file:
            data = yaml.safe_load(file)
            for student_data in data:
                for name, grades in student_data.items():
                    clean_name = name.lstrip('- ')
                    students[clean_name] = [
                        (subject, int(score)) for subject,
                        score in grades.items()]
        return students

    def pretty_print(self, data: Dict[str, List[Tuple[str, int]]]):
        max_name_length = max(len(name) for name in data.keys())
        max_subject_length = max(
            len(subject) for grades in data.values() for subject,
            _ in grades)

        print(f"{'Name': <{max_name_length}} | \
              {'Subject': <{max_subject_length}} | Score")
        print("-" * (max_name_length + max_subject_length + 15))

        for name, grades in data.items():
            for subject, score in grades:
                print(f"{name: <{max_name_length}} | \
                      {subject: <{max_subject_length}} | {score}")

```
#### Тестирование класса XMLDataReader осуществляется с помощью класса, реализованного в файле test/test_YAMLDataReader.py:
```python
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
    m = mock_open(read_data=yaml_example)
    m.return_value.__iter__ = lambda self: self
    m.return_value.__next__ = lambda self: next(iter(self.readline, ''))

    with patch("builtins.open", m, create=True):
        result = yaml_reader.read("dummy_path")

    assert result == expected_output, f"Expected \
        {expected_output}, got {result}"


```
#### main.py:
```python
# -*- coding: utf-8 -*-
from src.main import get_path_from_arguments
import pytest


@pytest.fixture()
def correct_arguments_string() -> tuple[list[str], str]:
    return ["-p", "/home/user/file.txt"], "/home/user/file.txt"


@pytest.fixture()
def noncorrect_arguments_string() -> list[str]:
    return ["/home/user/file.txt"]


def test_get_path_from_correct_arguments(correct_arguments_string: tuple
                                         [list[str], str]) -> None:
    path = get_path_from_arguments(correct_arguments_string[0])
    assert path == correct_arguments_string[1]


def test_get_path_from_noncorrect_arguments(noncorrect_arguments_string:
                                            list[str]) -> None:
    with pytest.raises(SystemExit) as e:
        get_path_from_arguments(noncorrect_arguments_string[0])
    assert e.type == SystemExit

```
####Добавим в проект класс QuartileAnalyzer, реализующий расчет и вывод на экран количество студентов, чей рейтинг попадает во вторую квартиль распределения по
рейтингам.

```python
import numpy as np
from Types import DataType, RatingType


class QuartileAnalyzer:
    def __init__(self, data: DataType):
        self.data = data

    def calculate_ratings(self) -> RatingType:
        ratings = {}
        for student, grades in self.data.items():
            ratings[student] = np.mean([grade for _, grade in grades])
        return ratings

    def find_students_in_second_quartile(self, ratings: RatingType):
        score_list = list(ratings.values())
        first_quartile = np.percentile(score_list, 25)
        second_quartile = np.percentile(score_list, 50)

        students_in_second_quartile = {
            student: score for student, score in ratings.items()
            if first_quartile <= score < second_quartile
        }
        return students_in_second_quartile


```
#### Тестирование класса QuartileAnalyzer осуществляется с помощью класса, реализованного в файле test/test_TestQuartileAnalyzer.py:
```python
# -*- coding: utf-8 -*-
import pytest
import numpy as np

from src.QuartileAnalyzer import QuartileAnalyzer
from src.Types import DataType


class TestQuartileAnalyzer:
    @pytest.fixture()
    def input_data(self) -> DataType:
        data: DataType = {
            "Иванов Иван Иванович": [("математика", 80),
                                     ("программирование", 90),
                                     ("литература", 76)],
            "Петров Петр Петрович": [("математика", 100),
                                     ("социология", 90),
                                     ("химия", 61)],
            "Смирнов Александр Александрович": [("математика", 82),
                                                ("физика", 88),
                                                ("химия", 81)],
            "Васильев Василий Васильевич": [("математика", 92),
                                            ("астрономия", 89),
                                            ("биология", 85)],
            "Соболева Елена Игоревна": [("математика", 86),
                                        ("география", 74),
                                        ("история", 88)],
            "Козлов Андрей Петрович": [("математика", 90),
                                       ("физика", 92),
                                       ("информатика", 88)],
            "Жукова Ольга Николаевна": [("математика", 95),
                                        ("биология", 90),
                                        ("химия", 89)],
            "Романов Дмитрий Андреевич": [("математика", 88),
                                          ("история", 82),
                                          ("литература", 89)],
            "Осипова Светлана Викторовна": [("математика", 72),
                                            ("география", 80),
                                            ("астрономия", 87)],
            "Макаров Никита Игоревич": [("математика", 81),
                                        ("программирование", 95),
                                        ("история", 76)],
            "Ковалев Артем Ильич": [("математика", 95),
                                    ("биология", 92),
                                    ("химия", 94)],
            "Николаева Анна Михайловна": [("математика", 87),
                                          ("социология", 78),
                                          ("история", 89)],
            "Белов Сергей Викторович": [("математика", 75),
                                        ("физика", 70),
                                        ("астрономия", 80)],
            "Миронова Татьяна Алексеевна": [("математика", 89),
                                            ("история", 84),
                                            ("социология", 76)],
            "Ларионова Вера Олеговна": [("математика", 92),
                                        ("программирование", 85),
                                        ("история", 88)],
            "Сорокин Илья Владимирович": [("математика", 90),
                                          ("биология", 92),
                                          ("химия", 88)],
            "Федорова Дарья Сергеевна": [("математика", 91),
                                         ("астрономия", 88),
                                         ("программирование", 85)],
            "Гусев Владимир Александрович": [("математика", 85),
                                             ("литература", 87),
                                             ("география", 80)],
            "Александрова Юлия Евгеньевна": [("математика", 90),
                                             ("история", 92),
                                             ("литература", 94)],
            "Тихонов Николай Игоревич": [("математика", 80),
                                         ("астрономия", 79),
                                         ("физика", 75)]
        }
        return data

    def test_find_students_in_second_quartile(
            self, input_data: DataType) -> None:
        analyzer = QuartileAnalyzer(input_data)
        calculated_ratings = analyzer.calculate_ratings()

        students_in_2nd_quartile = analyzer.find_students_in_second_quartile(
            calculated_ratings)

        def expected_students_in_2nd_quartile(ratings):
            score_list = list(ratings.values())
            first_quartile = np.percentile(score_list, 25)
            second_quartile = np.percentile(score_list, 50)

            expected_students = {
                student: score for student, score in ratings.items()
                if first_quartile <= score < second_quartile
            }
            return expected_students

        expected_students = expected_students_in_2nd_quartile(
            calculated_ratings)

        assert students_in_2nd_quartile == pytest.approx(
            expected_students, abs=0.001)

```
#### main.py:
```python
# -*- coding: utf-8 -*-
from src.main import get_path_from_arguments
import pytest


@pytest.fixture()
def correct_arguments_string() -> tuple[list[str], str]:
    return ["-p", "/home/user/file.txt"], "/home/user/file.txt"


@pytest.fixture()
def noncorrect_arguments_string() -> list[str]:
    return ["/home/user/file.txt"]


def test_get_path_from_correct_arguments(correct_arguments_string: tuple
                                         [list[str], str]) -> None:
    path = get_path_from_arguments(correct_arguments_string[0])
    assert path == correct_arguments_string[1]


def test_get_path_from_noncorrect_arguments(noncorrect_arguments_string:
                                            list[str]) -> None:
    with pytest.raises(SystemExit) as e:
        get_path_from_arguments(noncorrect_arguments_string[0])
    assert e.type == SystemExit

```
#### Работа кода ветки XMLReader
![program_result](/images/program_result.PNG)
#### Проверка кода прошла успешно
![test](/images/tests_result.PNG)
#### Структура файлов проекта
![structure](/images/structure.PNG)
#### UML-диаграмма
![UML-diagram](/images/UML.PNG)
#### Пакеты:
- pytest - тестирование
- mypy - корректность работы с типами
- pycodestyle - соответствие кода стандарту РЕР-8
- YAMLDataReader - модуль для работы с yaml

## Выводы
1. Закреплено представление о распределенной системе контроля версий кода Git и ее функциях;
2. Закреплены понятия «непрерывная интеграция» (CI) и «непрерывное развертывание»
(CD), определено их место в современной разработке программного обеспечения;
3. Получены навыки разработки ООП-программ и написания модульных тестов к ним на
современных языках программирования;
4. Получены навыки работы с системой Git для хранения и управления версиями ПО;
5. Получены навыки управления автоматизированным тестированием программного обеспечения, расположенного в системе Git, с помощью инструмента Travis CI.