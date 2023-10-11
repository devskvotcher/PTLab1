# -*- coding: utf-8 -*-
from Types import DataType
from DataReader import DataReader


class TextDataReader(DataReader):

    def __init__(self) -> None:
        self.key: str = ""
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        with open(path, encoding='utf-8') as file:
            for line in file:
                if not line.startswith(" "):
                    self.key = line.strip()
                    self.students[self.key] = []
                else:
                    subj, score = line.split(":", maxsplit=1)
                    self.students[self.key].append(
                        (subj.strip(), int(score.strip())))
            return self.students

    def pretty_print(self, data: DataType):
        # Определение максимальной длины строки для колонок
        max_name_length = max(len(name) for name in data.keys())
        max_subject_length = max(len(subject) for grades in
                                 data.values() for
                                 subject, _ in grades)

        # Вывод данных в табличном формате
        print(f"{'Name': <{max_name_length}} | \
              {'Subject': <{max_subject_length}} | Score")
        # Добавим разделительную линию
        print("-" * (max_name_length + max_subject_length + 15))

        for name, grades in data.items():
            for subject, score in grades:
                print(f"{name: <{max_name_length}} | \
                      {subject: <{max_subject_length}} | {score}")
