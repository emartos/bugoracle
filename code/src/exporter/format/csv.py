import csv
from collections import defaultdict
from typing import Dict, List

from src.exporter.format.format_interface import FormatInterface


class Csv(FormatInterface):
    """
    Concrete implementation of the FormatInterface for exporting data to CSV files.

    This class provides methods to export processed data, summarized data,
    and insights into various CSV and plain text file formats.
    """

    def __init__(self) -> None:
        """
        Initializes the Csv exporter with configuration for delimiter and quote character.
        """
        super().__init__()
        self.csv_delimiter = self.config_manager.get_csv_delimiter()
        self.csv_quotechar = self.config_manager.get_csv_quotechar()

    def export(
        self,
        data: List[Dict[str, str]],
        summarized_data: Dict[str, Dict],
        insights: str,
    ) -> List[str]:
        """
        Exports processed data, summarized totals, and insights into CSV and plain text files.

        Args:
            data (List[Dict[str, str]]): The processed data to be saved as a CSV file.
            summarized_data (Dict[str, Dict]): The summarized data containing totals and totals_by_date.
            insights (str): The insights to be saved as a plain text file.

        Returns:
            List[str]: Paths of the generated files (processed data CSV, totals CSV, totals by date CSV, and insights text file).
        """
        # Path configuration
        self._prepare_output_dir()
        processed_data_file = (
            f"{self.output_dir}/{self.output_subdir}/processed-data.csv"
        )
        totals_file = f"{self.output_dir}/{self.output_subdir}/totals.csv"
        totals_by_date_file = (
            f"{self.output_dir}/{self.output_subdir}/totals-by-date.csv"
        )
        insights_file = f"{self.output_dir}/{self.output_subdir}/insights.txt"

        # Export full data as CSV
        self._list_to_csv(processed_data_file, data, list(data[0].keys()))

        # Export totals as CSV
        self._dict_to_csv(
            totals_file, summarized_data["totals"], ["Category", "Subcategory", "Count"]
        )

        # Export totals by date as CSV
        self._dict_to_csv(
            totals_by_date_file,
            summarized_data["totals_by_date"],
            ["Date", "Category", "Subcategory", "Count"],
        )

        # Export insights as plain text
        self._save_as_text(insights_file, insights)

        return [
            processed_data_file,
            totals_file,
            totals_by_date_file,
            insights_file,
        ]

    def _list_to_csv(
        self, output_file: str, data: List[Dict[str, str]], keys: List[str]
    ) -> None:
        """
        Writes a list of dictionaries into a CSV file with the specified keys as column headers.

        Args:
            output_file (str): The path to the output CSV file.
            data (List[Dict[str, str]]): The list of dictionaries to be written into the CSV file.
            keys (List[str]): The list of keys to use as column headers in the CSV file.

        Returns:
            None
        """
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=keys,
                delimiter=self.csv_delimiter,
                quotechar=self.csv_quotechar,
                quoting=csv.QUOTE_MINIMAL,
            )
            writer.writeheader()
            writer.writerows(data)

    def _dict_to_csv(
        self, output_file: str, data: Dict[str, Dict], keys: List[str]
    ) -> None:
        """
        Writes a multi-level dictionary into a CSV file by unfolding its structure into rows.

        Args:
            output_file (str): The path to the output CSV file.
            data (Dict[str, Dict]): The dictionary to be written into the CSV file.
                Each key represents a category, and the values are subcategories or counts.
            keys (List[str]): The list of keys used as column headers in the CSV file.

        Returns:
            None
        """
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(
                file,
                delimiter=self.csv_delimiter,
                quotechar=self.csv_quotechar,
                quoting=csv.QUOTE_MINIMAL,
            )
            writer.writerow(keys)

            for category, subcategories in data.items():
                if isinstance(subcategories, defaultdict):
                    subcategories = dict(subcategories)

                for subcategory, counts in subcategories.items():
                    if isinstance(counts, defaultdict):
                        counts = dict(counts)

                    if isinstance(counts, dict):
                        for item, count in counts.items():
                            writer.writerow([category, subcategory, item, count])
                    else:
                        writer.writerow([category, subcategory, counts])
