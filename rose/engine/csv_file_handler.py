import csv
from pathlib import Path
from typing import Union

__all__ = ["CsvFileHandler"]

class CsvFileHandler:
    @staticmethod
    def add_line(file_path: Union[Path, str], row: list[str]) -> bool:
        """
        Appends a single row to a CSV file.

        This function checks that the provided file exists and has a '.csv' extension.
        The given list of strings is appended as a new row. Errors are caught and logged.

        Args:
            file_path (Union[Path, str]): Path to the CSV file.
            row (list[str]): A list of strings representing the row to append.

        Returns:
            bool: True if the row was successfully written, False otherwise.
        """
        try:
            path = Path(file_path)

            if path.suffix.lower() != ".csv":
                print(f"[ERROR] File '{path}' is not a CSV file.")
                return False

            with path.open(mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(row)

            return True

        except OSError as os_err:
            print(f"[ERROR] File system error: {os_err}")
            return False
        except Exception as e:
            print(f"[ERROR] Unexpected error while writing to CSV: {e}")
            return False

    @staticmethod
    def read_as_matrix(file_path: Union[Path, str]) -> list[list[str]]:
        """
        Reads a CSV file and returns its contents as a matrix of strings.

        Args:
            file_path (Union[Path, str]): Path to the CSV file.

        Returns:
            list[list[str]]: Matrix of strings representing the CSV content,
                             or an empty list if an error occurs.
        """
        try:
            path = Path(file_path)

            if not path.exists():
                print(f"[ERROR] File '{path}' does not exist.")
                return []

            if path.suffix.lower() != ".csv":
                print(f"[ERROR] File '{path}' is not a CSV file.")
                return []

            with path.open(mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                return [row for row in reader]

        except OSError as os_err:
            print(f"[ERROR] File system error: {os_err}")
            return []
        except Exception as e:
            print(f"[ERROR] Unexpected error while reading from CSV: {e}")
            return []

    @staticmethod
    def write_matrix_to_csv(file_path: Union[Path, str], matrix: list[list[str]]) -> bool:
        """
        Writes a matrix to a CSV file with the following constraints:
        - Each row is exactly 6 columns (padded or truncated with "").
        - Writes at most 30 rows.
        - If matrix is empty, clears the CSV file.

        Args:
            file_path (Union[Path, str]): The CSV file path.
            matrix (list[list[str]]): The matrix to write (rows of strings).

        Returns:
            bool: True if writing was successful, False otherwise.
        """
        try:
            path = Path(file_path)

            if path.suffix.lower() != ".csv":
                print(f"[ERROR] File '{path}' is not a CSV file.")
                return False

            if not matrix:
                path.write_text("", encoding='utf-8')
                return True

            processed = [(row + [""] * 6)[:6] for row in matrix[:30]]

            with path.open(mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(processed)

            return True

        except OSError as os_err:
            print(f"[ERROR] File system error: {os_err}")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to write matrix to CSV: {e}")
            return False