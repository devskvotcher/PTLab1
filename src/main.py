# -*- coding: utf-8 -*-
import argparse
import sys
from CalcRating import CalcRating
from YAMLDataReader import YAMLDataReader
from TextDataReader import TextDataReader
from QuartileAnalyzer import QuartileAnalyzer


def get_path_from_arguments(args) -> tuple[str, str]:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str,
                        required=True, help="Path to datafile")
    parser.add_argument(
        "-f",
        dest="format",
        type=str,
        required=False,
        default="txt",
        help="Datafile format (txt or yaml)")
    args = parser.parse_args(args)

    if args.format not in ["txt", "yaml"]:
        raise ValueError(f"Unsupported format: {args.format}")

    return args.path, args.format


def print_table(students: dict[str, float], title: str):
    print(f"\n{title}")
    print("-" * len(title))
    print("ФИО               | Средний балл")
    print("------------------|-------------")
    for student, rating in students.items():
        print(f"{student: <18} | {rating:.2f}")


def main():
    path, format = get_path_from_arguments(sys.argv[1:])

    if format == "txt":
        reader = TextDataReader()
    elif format == "yaml":
        reader = YAMLDataReader()
    else:
        raise ValueError(f"Unsupported format: {format}")

    students = reader.read(path)

    rating_calculator = CalcRating(students)
    ratings = rating_calculator.calc()

    print_table(ratings, "Все студенты и их рейтинги")

    analyzer = QuartileAnalyzer(students)
    students_in_second_quartile = analyzer.find_students_in_second_quartile(
        ratings)

    print_table(students_in_second_quartile, "Студенты во второй квартили")


if __name__ == "__main__":
    main()
