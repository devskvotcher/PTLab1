import yaml
from DataReader import DataReader
from Types import DataType


class YAMLDataReader(DataReader):
    def read(self, path: str) -> DataType:
        students = {}
        with open(path, encoding='utf-8') as file:
            data = yaml.safe_load(file)
            for student_name, grades in data.items():
                students[student_name] = [(subject, int(score))
                                          for subject, score in grades.items()]
        return students
