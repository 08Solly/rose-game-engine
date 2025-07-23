import csv
from pathlib import Path
from typing import Union

class CsvFileHandler:
    @staticmethod
    def add_line(file_path: Union[Path, str], row: list[str]) -> bool:
        """
        Appends a list of strings as a new row to a CSV file.

        Args:
            file_path (Path | str): Path to the CSV file.
            row (list[str]): List of strings representing a row.

        Returns:
            bool: True if the row was successfully written, False on failure.
        """
        try:
            path = Path(file_path)

            if not path.exists():
                print(f"[ERROR] File '{path}' does not exist.")
                return False

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
        Reads a CSV file and returns its contents as a matrix (list of rows).

        Args:
            file_path (Path | str): Path to the CSV file.

        Returns:
            list[list[str]]: Matrix of strings representing the CSV content.
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
                matrix = [row for row in reader]

            return matrix

        except OSError as os_err:
            print(f"[ERROR] File system error: {os_err}")
            return []
        except Exception as e:
            print(f"[ERROR] Unexpected error while reading from CSV: {e}")
            return []

    @staticmethod
    def write_matrix_to_csv(file_path: Union[Path, str], matrix: list[list[str]]) -> bool:
        """
        Writes a matrix to a CSV file, ensuring:
        - Each row is exactly 6 columns (padded or truncated with "").
        - Matrix is written as-is up to 30 rows (no padding to 30).
        - If matrix is empty, the CSV file will be cleared.

        Args:
            file_path (Path | str): The path to the CSV file to write.
            matrix (list[list[str]]): The matrix of string rows.

        Returns:
            bool: True if writing was successful, False otherwise.
        """
        try:
            path = Path(file_path)
            processed_matrix: list[list[str]] = []

            if not matrix:
                # Clear the file
                path.write_text("")
                return True

            # Process existing rows up to 30
            for row in matrix[:30]:
                processed_matrix.append((row + [""] * 6)[:6])

            with path.open('w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(processed_matrix)

            return True

        except Exception as e:
            print(f"[ERROR] Failed to write matrix to CSV: {e}")
            return False