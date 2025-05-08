import os
from abc import ABC, abstractmethod
from typing import List

from src.config.configuration_manager import ConfigurationManager


class FormatInterface(ABC):
    """
    Abstract base class (interface) for defining a contract for exporter classes.

    All concrete classes implementing this interface must provide their own implementation
    for the `export` method.

    Attributes:
        output_dir (str): The directory in which the exported files will be saved.
        output_subdir (str): The subdirectory under the output directory configured for exporting files.
        config_manager (ConfigurationManager): Configuration manager instance for retrieving global settings.
    """

    def __init__(self, output_dir: str = "./output") -> None:
        """
        Initializes the FormatInterface with the base output directory and configuration settings.

        Args:
            output_dir (str): The directory where exported files will be saved. Defaults to "./output".
        """
        self.config_manager = ConfigurationManager()
        self.output_subdir = self.config_manager.get_export_subdirectory()
        self.output_dir = output_dir

    @abstractmethod
    def export(
        self, data: List[dict], summarized_data: dict, insights: str
    ) -> List[str]:
        """
        Abstract method that must be implemented by all subclasses.

        This is responsible for exporting processed data, summarized data, and insights
        into specific formats (e.g., CSV, JSON, plain text).

        Args:
            data (List[dict]): List of dictionaries containing processed data to export.
            summarized_data (dict): Dictionary containing summarized totals and additional processed data.
            insights (str): Insights or analysis generated from the summarized data.

        Returns:
            List[str]: A list of file paths where the exported data was written.
        """
        pass

    def _prepare_output_dir(self) -> None:
        """
        Prepares the output directory structure where the exported files will be saved.

        It ensures the existence of the subdirectory defined in the configuration. If the directory
        does not exist, it is created.

        Returns:
            None
        """
        output_dir = f"{self.output_dir}/{self.output_subdir}"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def _save_as_text(self, output_file: str, data: str) -> None:
        """
        Exports the given text data to a plain text file.

        Args:
            output_file (str): The path of the file where text will be exported.
            data (str): The text data to export. Can be a single string.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the writing process, it will print an error message.
        """
        try:
            # Write the data to the specified file
            with open(output_file, mode="w", encoding="utf-8") as file:
                file.write(data)
        except Exception as e:
            print(f"An error occurred while saving data to {output_file}: {e}")
