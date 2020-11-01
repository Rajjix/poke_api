import csv
from typing import Callable, Iterator


class CsvReader:

    @staticmethod
    def read_csv_with_filter(path: str, custom_filter: Callable) -> Iterator:
        with open(path, 'r') as file:
            file_data = csv.reader(file)
            for row in filter(custom_filter, csv.DictReader(file)):
                yield row

    @staticmethod
    def read_csv(path: str) -> Iterator:
        with open(path, 'r') as file:
            for row in csv.DictReader(file):
                yield row
