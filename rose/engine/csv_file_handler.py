import csv
from pathlib import Path

class CsvFileHandler:

    def __init__(self, file_path: Path | str | None = None) -> None:
        assert file_path.with_suffix('.csv')
        self.file_path: Path | None= Path(file_path)


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

