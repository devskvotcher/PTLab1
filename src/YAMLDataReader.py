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
