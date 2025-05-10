import json
import logging
import time
from typing import Any, Dict, List

from src.config.configuration_manager import ConfigurationManager
from src.csv.csv_reader import CsvReader
from src.exporter.exporter_provider import ExporterProvider
from src.llm.model_provider import ModelProvider
from src.llm.prompt.insights_prompt_builder import InsightsPromptBuilder
from src.llm.prompt.processing_prompt_builder import ProcessingPromptBuilder
from src.logger.logger import Logger
from src.summarizer.total_summarizer import TotalSummarizer


class BugOracle:
    """
    Main class for handling bug analysis, processing, summarization, and insights generation
    using LLM models and exporting the data in the required format.
    """

    def __init__(self) -> None:
        """
        Initializes the BugOracle class, setting up the logger and configuration manager.
        """
        Logger.setup()
        self.configuration_manager = ConfigurationManager()

    def run(self) -> None:
        """
        Main execution workflow of the BugOracle.

        Handles the entire process, including:
        - Collecting input data
        - Retrieving bugs from CSV
        - Processing bugs with LLM
        - Summarizing processed data
        - Analyzing global insights
        - Exporting results

        Logs the total execution time and handles any exceptions raised during execution.
        """
        start_time = time.time()
        try:
            # Stage 1: Input data collection
            self.configuration_manager.collect_inputs()

            # Stage 2: Bugs retrieval
            bugs = self._retrieve_bugs()

            # Stage 3: LLM processing
            bugs_data = self._llm_processing(bugs)

            # Stage 4: Summarize
            summarized_data = self._summarize(bugs_data)

            # Stage 5: Get insights
            insights = self._get_insights(summarized_data["totals_by_date"])

            # Stage 6: Data export
            self._export(bugs_data, summarized_data, insights)
        except ValueError as err:
            logging.exception(f"Error during bugs analysis process: {err}")
        except Exception as err:
            logging.exception(f"Unexpected error during execution: {err}")
        finally:
            total_time = time.time() - start_time
            logging.info(f"Total execution time: {total_time:.2f} seconds.")

    def _retrieve_bugs(self) -> List[Dict[str, Any]]:
        """
        Retrieves bugs data from the configured CSV file.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing rows in the CSV file.
        """
        logging.info("Retrieving bugs...")
        csv_path = self.configuration_manager.get_csv_path()
        csv_reader = CsvReader(csv_path)
        return csv_reader.read_all_rows()

    def _llm_processing(self, bugs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Processes each bug entry using the LLM model.

        Args:
            bugs (List[Dict[str, Any]]): List of bug entries retrieved from the CSV.

        Returns:
            List[Dict[str, Any]]: A list of processed bug entries with added details such as subject, description,
            and model-generated insights.

        Raises:
            Exception: If the LLM model returns invalid JSON responses.
        """
        logging.info("Processing every bug with LLM...")

        prompt_builder = ProcessingPromptBuilder()
        model = self._get_llm()

        csv_header_subject = self.configuration_manager.get_csv_header_subject()
        csv_header_changed = self.configuration_manager.get_csv_header_changed()
        csv_header_description = self.configuration_manager.get_csv_header_description()

        i = 1
        total = len(bugs)
        result = []

        for bug in bugs:
            logging.info(f"Processing item {i}/{total}")
            i += 1

            subject = bug[csv_header_subject]
            changed = bug[csv_header_changed]
            description = bug[csv_header_description]
            prompt = prompt_builder.build_prompt(subject, description)

            llm_response = model.generate(prompt=prompt)
            cleaned_response = llm_response.strip("```json").strip("```").strip()

            try:
                bug_data = json.loads(cleaned_response)
                bug_data["subject"] = subject
                bug_data["description"] = description
                bug_data["changed"] = changed
                result.append(bug_data)
            except json.JSONDecodeError as err:
                raise Exception(
                    f"❌ Error: the model's response is not valid JSON: {err}\n\n{cleaned_response}"
                )

        return result

    def _summarize(self, bugs_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Summarizes processed bug data, producing totals and highlights.

        Args:
            bugs_data (List[Dict[str, Any]]): Processed bug data.

        Returns:
            Dict[str, Any]: Summarized data, grouped by relevant dimensions and metrics.
        """
        total_summarizer = TotalSummarizer()
        return total_summarizer.summarize(bugs_data)

    def _get_insights(self, summarized_data: Dict[str, Any]) -> str:
        """
        Generates insights from summarized data using the LLM model.

        Args:
            summarized_data (Dict[str, Any]): Summarized data to generate insights.

        Returns:
            str: A string representation of the global insights generated by the LLM.
        """
        logging.info("Analyzing the consolidated data with the LLM...")
        processed_summarized_data = self._preprocess_summarized_data(summarized_data)
        target_language = self.configuration_manager.get_export_language()

        prompt_builder = InsightsPromptBuilder()
        prompt = prompt_builder.build_prompt(processed_summarized_data, target_language)
        model = self._get_llm()

        return model.generate(prompt=prompt)

    def _preprocess_summarized_data(
        self, summarized_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Preprocess summarized bug data to provide a summary with totals and highlights.

        Args:
            summarized_data (Dict[str, Any]): Original bug data grouped by date and dimensions.

        Returns:
            Dict[str, Any]: Preprocessed JSON-compatible summary of bug data.
        """
        result = {}  # type: ignore

        for date, dimensions in summarized_data.items():
            result[date] = {}

            for dimension, entries in dimensions.items():
                # Calculate the total for the dimension
                dimension_total = sum(entries.values())
                highlights = dict(
                    # Top 5 significant subcategories
                    sorted(entries.items(), key=lambda x: x[1], reverse=True)[:5]
                )

                # Store the processed data for the dimension
                result[date][dimension] = {
                    "total": dimension_total,
                    "highlights": highlights,
                }

        return result

    def _export(
        self,
        bugs_data: List[Dict[str, Any]],
        summarized_data: Dict[str, Any],
        insights: str,
    ) -> None:
        """
        Exports the processed, summarized, and insights data using the configured exporter.

        Args:
            bugs_data (List[Dict[str, Any]]): The original processed bug data.
            summarized_data (Dict[str, Any]): The summarized bug data.
            insights (str): The generated insights.

        Returns:
            None
        """
        logging.info("Exporting data...")
        export_format = self.configuration_manager.get_export_format()
        exporter_provider = ExporterProvider()
        exporter = exporter_provider.get(export_format)
        export_paths = exporter.export(
            data=bugs_data, summarized_data=summarized_data, insights=insights
        )
        export_paths_str = ", ".join(export_paths)
        logging.info(f"✅ Data successfully generated at {export_paths_str}")

    def _get_llm(self) -> Any:
        """
        Retrieves the configured LLM model instance.

        Returns:
            Any: The LLM model instance configured for use.
        """
        llm_provider = self.configuration_manager.get_llm_provider()
        model_provider = ModelProvider()
        return model_provider.get(llm_provider)


if __name__ == "__main__":
    """
    Entry point of the script. Creates an instance of BugOracle and runs the workflow.
    """
    bug_oracle = BugOracle()
    bug_oracle.run()
