import csv


class CsvReader:
    """
    A class to read and process CSV files.
    """

    def __init__(self, file_path):
        """
        Initializes the CSVReader object with the file path.

        Args:
            file_path (str): Path to the CSV file to be read.
        """
        self.file_path = file_path

    def read_all_rows(self):
        """
        Reads all rows from the CSV file and returns them as a list of dictionaries.

        Returns:
            list: A list of rows where each row is a dictionary (header is used as keys).

        Raises:
            FileNotFoundError: If the file path does not exist.
            Exception: For any general error while reading the file.
        """
        try:
            with open(self.file_path, mode="r", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                rows = list(reader)
            return rows
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"The file at path {self.file_path} was not found."
            ) from e
        except Exception as e:
            raise Exception("An error occurred while reading the CSV file.") from e

    def read_column(self, column_name):
        """
        Reads a specific column from the CSV file and returns it as a list.

        Args:
            column_name (str): The name of the column to extract.

        Returns:
            list: A list containing values from the specified column.

        Raises:
            KeyError: If the specified column does not exist in the file.
            Exception: For any general error while reading the file.
        """
        try:
            with open(self.file_path, mode="r", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                column = [row[column_name] for row in reader if column_name in row]
            if not column:
                raise KeyError(
                    f"Column '{column_name}' does not exist in the CSV file."
                )
            return column
        except KeyError as e:
            raise e
        except Exception as e:
            raise Exception(
                f"An error occurred while reading the column '{column_name}'."
            ) from e

    def count_rows(self):
        """
        Counts the total number of rows in the CSV file.

        Note:
            The header row is excluded from the count.

        Returns:
            int: The number of rows in the CSV file (excluding the header).

        Raises:
            Exception: For any general error while counting the rows in the file.
        """
        try:
            with open(self.file_path, mode="r", encoding="utf-8") as csv_file:
                reader = csv.reader(csv_file)
                # Subtract 1 for the header row
                row_count = sum(1 for _ in reader) - 1
            return row_count
        except Exception as e:
            raise Exception(
                "An error occurred while counting the rows in the CSV file."
            ) from e
