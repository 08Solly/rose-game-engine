import csv
from pathlib import Path
from

class CsvFileHandler:

    @staticmethod
    def add_line(self,file_path: Path | str, row: list[str]) -> bool:
        """
        Appends a list of strings as a new row to the CSV file.

        Parameters:
        row (list[str]): A list of strings to write as one row.

        Returns:
        bool: True if the write succeeded.
        """

        # Making sure file path is type Path
        file_path: Path = Path(file_path)

        # Checking if file exists
        if not file_path.exists():
            print(f"File {file_path.name} doesnt exist")
            return False

        # Checking if file is CSV
        if not file_path.name.endswith('.csv'):
            print(f"File {file_path.name} isn't CSV file")
            return False


        # Writing to file
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