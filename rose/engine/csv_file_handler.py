import csv
from pathlib import Path
from typing import Union, Optional


class CsvFileHandler:

    def __init__(self, file_path: Union[Path, str, None] = None) -> None:
        self.file_path: Optional[Path] = Path(file_path)

        if not file_path.with_suffix('.csv'):
            self.file_path = None
        if not file_path.exists():
            self.file_path = None



    def add_line(self, row: list[str]) -> bool:
        """
        Appends a list of strings as a new row to the CSV file.

        Parameters:
        row (list[str]): A list of strings to write as one row.

        Returns:
        bool: True if the write succeeded.
        """
        try:
            with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(row)  # Append the list as a new row
            return True
        except Exception as e:
            print(f"Error writing to CSV: {e}")
            return False

    def read_as_matrix(self) -> list[list[str]]:
        """
        Reads the CSV file and returns its content as a matrix (list of rows).

        Returns:
        list[list[str]]: The content of the CSV as a list of string rows.
        """
        matrix = []
        try:
            with self.file_path.open('r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    matrix.append(row)
            return matrix
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return []