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
