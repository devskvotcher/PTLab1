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
