from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List

from src.config.configuration_manager import ConfigurationManager
from src.summarizer.summarizer_interface import SummarizerInterface


class TotalSummarizer(SummarizerInterface):
    """
    Summarizes totals and totals grouped by date, with support for configurable inclusion/exclusion
    of specific fields based on export options.

    This class processes a dataset to produce:
    - Overall totals for various fields (e.g., technological components, functional areas, problem types).
    - Totals grouped by month to identify patterns over time.
    """

    def __init__(self):
        """
        Initializes a `TotalSummarizer` instance using configurations to determine
        which fields should be included in the summary.

        Export options are loaded via the `ConfigurationManager` class.
        """
        configuration_manager = ConfigurationManager()
        self.export_technological_component = (
            configuration_manager.get_export_technological_component()
        )
        self.export_technological_component_subcategory = (
            configuration_manager.get_export_technological_component_subcategory()
        )
        self.export_functional_area = configuration_manager.get_export_functional_area()
        self.export_functional_area_subcategory = (
            configuration_manager.get_export_functional_area_subcategory()
        )
        self.export_problem_type = configuration_manager.get_export_problem_type()
        self.export_problem_type_subcategory = (
            configuration_manager.get_export_problem_type_subcategory()
        )

    def summarize(self, data: List[Dict]) -> Dict[str, Dict]:
        """
        Summarizes the dataset by calculating totals and totals grouped by dates.

        Args:
            data (List[Dict]): A list of dictionaries representing the dataset to summarize.

        Returns:
            Dict[str, Dict]: A dictionary with two sections:
                - "totals": Contains overall counts of fields like technological components, functional areas, and problem types.
                - "totals_by_date": Contains counts of these fields grouped by month.
        """
        totals = self._count_totals(data)
        totals_by_month = self._count_totals_by_month(data)

        return {
            "totals": totals,
            "totals_by_date": totals_by_month,
        }

    def _count_totals(self, data: List[Dict]) -> Dict[str, Counter]:
        """
        Counts the totals of different fields across the dataset.

        Args:
            data (List[Dict]): A list of dictionaries representing the dataset.

        Returns:
            Dict[str, Counter]: A dictionary with the counts for each field.
                Example:
                {
                    "technological_component": Counter({"Drupal": 5, "React": 3}),
                    ...
                }
        """
        counts = self._initialize_counts()

        for entry in data:
            if self.export_technological_component:
                counts["technological_component"][
                    entry.get("technological_component", "Unknown")
                ] += 1
                if self.export_technological_component_subcategory:
                    counts["technological_component_subcategory"][
                        entry.get("technological_component_subcategory", "Unknown")
                    ] += 1
            if self.export_functional_area:
                counts["functional_area"][entry.get("functional_area", "Unknown")] += 1
                if self.export_functional_area_subcategory:
                    counts["functional_area_subcategory"][
                        entry.get("functional_area_subcategory", "Unknown")
                    ] += 1
            if self.export_problem_type:
                counts["problem_type"][entry.get("problem_type", "Unknown")] += 1
                if self.export_problem_type_subcategory:
                    counts["problem_type_subcategory"][
                        entry.get("problem_type_subcategory", "Unknown")
                    ] += 1

        return counts

    def _count_totals_by_month(self, data: List[Dict]) -> Dict[str, Dict[str, Counter]]:
        """
        Counts totals of different fields grouped by month.

        Args:
            data (List[Dict]): A list of dictionaries representing the dataset.

        Returns:
            Dict[str, Dict[str, Counter]]: A nested dictionary with counts grouped by month.
                Example:
                {
                    "2023-01": {
                        "technological_component": Counter({"Drupal": 3}),
                        ...
                    },
                }
        """
        counts_by_month = defaultdict(lambda: self._initialize_counts())  # type: ignore

        for entry in data:
            date_str = entry.get("changed", "Unknown")
            month = self._parse_date(date_str)

            if self.export_technological_component:
                counts_by_month[month]["technological_component"][
                    entry.get("technological_component", "Unknown")
                ] += 1
                if self.export_technological_component_subcategory:
                    counts_by_month[month]["technological_component_subcategory"][
                        entry.get("technological_component_subcategory", "Unknown")
                    ] += 1
            if self.export_functional_area:
                counts_by_month[month]["functional_area"][
                    entry.get("functional_area", "Unknown")
                ] += 1
                if self.export_functional_area_subcategory:
                    counts_by_month[month]["functional_area_subcategory"][
                        entry.get("functional_area_subcategory", "Unknown")
                    ] += 1
            if self.export_problem_type:
                counts_by_month[month]["problem_type"][
                    entry.get("problem_type", "Unknown")
                ] += 1
                if self.export_problem_type_subcategory:
                    counts_by_month[month]["problem_type_subcategory"][
                        entry.get("problem_type_subcategory", "Unknown")
                    ] += 1

        return counts_by_month

    def _initialize_counts(self) -> Dict[str, Counter]:
        """
        Initializes a dictionary with counters for each field.

        Returns:
            Dict[str, Counter]: A dictionary containing Counter objects for each field.
                Example:
                {
                    "technological_component": Counter(),
                    "technological_component_subcategory": Counter(),
                    ...
                }
        """
        counts = {}  # type: ignore

        # Include technological components if enabled
        if self.export_technological_component:
            counts["technological_component"] = defaultdict(int)
            if self.export_technological_component_subcategory:
                counts["technological_component_subcategory"] = defaultdict(int)

        # Include functional areas if enabled
        if self.export_functional_area:
            counts["functional_area"] = defaultdict(int)
            if self.export_functional_area_subcategory:
                counts["functional_area_subcategory"] = defaultdict(int)

        # Include problem types if enabled
        if self.export_problem_type:
            counts["problem_type"] = defaultdict(int)
            if self.export_problem_type_subcategory:
                counts["problem_type_subcategory"] = defaultdict(int)

        return counts

    def _parse_date(self, date_str: str):
        """
        Parses a date string in the format 'dd/mon/yy hh:mm AM/PM' to a datetime object.

        Args:
            date_str (str): The date string to parse.

        Returns:
            datetime: The parsed datetime object.

        Raises:
            ValueError: If the date string does not match the expected format.
        """
        # Step 1: Clean up spaces in the input string to avoid format mismatches
        date_str = date_str.strip()

        # Step 2: Map Spanish month names (if applicable) to their English equivalents
        months_mapping = {
            "ene": "Jan",
            "feb": "Feb",
            "mar": "Mar",
            "abr": "Apr",
            "may": "May",
            "jun": "Jun",
            "jul": "Jul",
            "ago": "Aug",
            "sep": "Sep",
            "oct": "Oct",
            "nov": "Nov",
            "dic": "Dec",
        }

        for es_month, en_month in months_mapping.items():
            if es_month in date_str:
                date_str = date_str.replace(es_month, en_month)
                break

        # Step 3: Remove extra spaces between parts of the date, if any
        date_str = " ".join(date_str.split())

        # Step 4: Parse the date string using the specified format
        try:
            date_obj = datetime.strptime(date_str, "%d/%b/%y %I:%M %p")
            return date_obj.strftime("%Y-%m")
        except ValueError as e:
            # If parsing fails, raise a clear error with the problematic date string
            raise ValueError(f"Error parsing date: '{date_str}' - {str(e)}")
