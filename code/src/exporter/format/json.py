import json
from typing import Any, Dict, List

from src.exporter.format.format_interface import FormatInterface


class Json(FormatInterface):
    """
    Exporter class to generate hierarchical JSON from summarized data.
    """

    def export(
        self, data: List[Dict], summarized_data: Dict, insights: str
    ) -> List[str]:
        """
        Generate exports in JSON format for all records and summarized data.

        Args:
            data (list): The full list of records.
            summarized_data (dict): The summarized data, including "totals" and "totals_by_date".

        Returns:
            list: Paths to the generated JSON files.
        """
        # Path configuration
        self._prepare_output_dir()
        processed_data_file = (
            f"{self.output_dir}/{self.output_subdir}/processed-data.json"
        )
        totals_file = f"{self.output_dir}/{self.output_subdir}/totals.json"
        totals_by_date_file = (
            f"{self.output_dir}/{self.output_subdir}/totals-by-date.json"
        )
        insights_file = f"{self.output_dir}/{self.output_subdir}/insights.txt"

        # Export full data as JSON
        self._save_as_json(processed_data_file, data)

        # Export totals as JSON
        hierarchical_totals = self._build_hierarchy(summarized_data["totals"])
        self._save_as_json(totals_file, hierarchical_totals)

        # Export totals by date as JSON
        hierarchical_totals_by_date = self._build_hierarchy_by_date(
            summarized_data["totals_by_date"]
        )
        self._save_as_json(totals_by_date_file, hierarchical_totals_by_date)

        # Export insights as plain text
        self._save_as_text(insights_file, insights)

        return [
            processed_data_file,
            totals_file,
            totals_by_date_file,
            insights_file,
        ]

    def _save_as_json(self, file_path: str, data: Any) -> None:
        """
        Saves any given data as a JSON file.

        Args:
            file_path (str): The path to the output file.
            data (Any): The data to save.
        """
        with open(file_path, mode="w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def _build_hierarchy(self, data: Dict) -> Dict:
        """
        Build a hierarchical structure for "totals" with "children" and "total".

        Args:
            data (dict): The "totals" data.

        Returns:
            dict: A hierarchical structure where each category is a key, containing
                  "children" (subcategories and their counts) and "total" (sum of all counts).
        """
        hierarchy = {}

        for category, subcategories in data.items():
            # Calculate the total for the category
            total = sum(subcategories.values())
            # Assign children and total in the new structure
            hierarchy[category] = {
                "children": {
                    subcategory: count for subcategory, count in subcategories.items()
                },
                "total": total,
            }

        return hierarchy

    def _build_hierarchy_by_date(self, data: Dict) -> Dict:
        """
        Build a hierarchical structure for "totals_by_date" with "children" and "total".

        Args:
            data (dict): The "totals_by_date" data.

        Returns:
            dict: A hierarchical structure where each date is a key, containing categories
                  with "children" (subcategories and their counts) and "total" (sum of all counts).
        """
        hierarchy: Dict[str, Dict[str, Any]] = {}

        for date, categories in data.items():
            hierarchy[date] = {}
            for category, subcategories in categories.items():
                # Calculate the total for the category within this date
                total = sum(subcategories.values())
                # Assign children and total in the new structure
                hierarchy[date][category] = {
                    "children": {
                        subcategory: count
                        for subcategory, count in subcategories.items()
                    },
                    "total": total,
                }

        return hierarchy
