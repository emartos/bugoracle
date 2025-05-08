import os
from typing import Any, List, Optional

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


class ConfigurationManager:
    """
    Handles the configuration setup for the application, including
    input collection, validation, and setting up environmental variables.
    This class is implemented as a Singleton, meaning only one
    instance will exist during execution.
    """

    VALID_EXPORT_FORMATS = ["csv", "json"]
    VALID_LLM_PROVIDERS = ["openai", "grok"]

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to ensure only one instance of the class can be created.
        """
        if cls._instance is None:
            cls._instance = super(ConfigurationManager, cls).__new__(
                cls, *args, **kwargs
            )
        return cls._instance

    def __init__(self):
        """
        Initialize the ConfigurationManager. Ensure initialization
        only occurs once, even for multiple calls to the class.
        """
        if not hasattr(self, "_initialized"):
            self.csv_path = None
            self.export_format = None
            self.llm_provider = None
            self.export_technological_component = None
            self.export_technological_component_subcategory = None
            self.export_functional_area = None
            self.export_functional_area_subcategory = None
            self.export_problem_type = None
            self.export_problem_type_subcategory = None
            self.csv_delimiter = None
            self.csv_quotechar = None
            self.export_language = None
            self.export_subdirectory = None
            self._initialized = True

    def collect_inputs(self) -> None:
        """
        Collects inputs required for running the application and validates them.

        Prompts the user to input configuration details such as the CSV path,
        export format, LLM provider, and target language.

        Raises:
            ValueError: If any mandatory input is missing or invalid.

        Returns:
            None
        """
        self.csv_path = self._input("CSV_DATA_PATH", "Output CSV path")
        self.csv_delimiter = self._input(
            "CSV_DELIMITER", "Output CSV field delimiter", default=","
        )
        self.csv_quotechar = self._input(
            "CSV_QUOTECHAR", "Output CSV quote character", default='"'
        )
        self.csv_header_subject = self._input(
            "CSV_HEADER_SUBJECT", "CSV header: subject"
        )
        self.csv_header_changed = self._input(
            "CSV_HEADER_CHANGED", "CSV header: changed"
        )
        self.csv_header_description = self._input(
            "CSV_HEADER_DESCRIPTION", "CSV header: description"
        )
        self.export_format = self._input_with_options(
            self.VALID_EXPORT_FORMATS, "EXPORT_FORMAT", "Export format", "default"
        )
        self.export_language = self._input(
            "EXPORT_LANGUAGE", "Export language", default="English"
        )
        self.export_subdirectory = self._input(
            "EXPORT_SUBDIRECTORY",
            "Export subdirectory (relative to ./output path)",
            default="",
        )
        self.llm_provider = self._input_with_options(
            self.VALID_LLM_PROVIDERS, "LLM_PROVIDER", "LLM provider", "openai"
        )
        self.export_technological_component = self._input_boolean(
            "EXPORT_TECHNOLOGICAL_COMPONENT",
            "Export technological component",
            default=0,
        )
        self.export_technological_component_subcategory = self._input_boolean(
            "EXPORT_TECHNOLOGICAL_COMPONENT_SUBCATEGORY",
            "Export technological component subcategory",
            default=0,
        )
        self.export_functional_area = self._input_boolean(
            "EXPORT_FUNCTIONAL_AREA", "Export functional area", default=1
        )
        self.export_functional_area_subcategory = self._input_boolean(
            "EXPORT_FUNCTIONAL_AREA_SUBCATEGORY",
            "Export functional area subcategory",
            default=0,
        )
        self.export_problem_type = self._input_boolean(
            "EXPORT_PROBLEM_TYPE", "Export problem type", default=0
        )
        self.export_problem_type_subcategory = self._input_boolean(
            "EXPORT_PROBLEM_TYPE_SUBCATEGORY",
            "Export problem type subcategory",
            default=0,
        )

    def get_csv_path(self) -> str:
        """
        Retrieves the configured CSV path.

        Returns:
            str: The path to the CSV repository.

        Raises:
            ValueError: If the repository path is not yet configured.
        """
        if not self.csv_path:
            raise ValueError("❌ The CSV repository path has not been configured.")
        return self.csv_path

    def get_csv_delimiter(self) -> str:
        """
        Retrieves the configured CSV field delimiter.

        Returns:
            str: The CSV field delimiter.
        """
        return self.csv_delimiter

    def get_csv_quotechar(self) -> str:
        """
        Retrieves the configured CSV quote character for values.

        Returns:
            str: The CSV quote character.
        """
        return self.csv_quotechar

    def get_csv_header_subject(self) -> str:
        """
        Retrieves the CSV header for the subject.

        Returns:
            str: The configured subject header.

        Raises:
            ValueError: If the subject header is not yet configured.
        """
        if not self.csv_header_subject:
            raise ValueError("❌ The CSV header for 'subject' has not been configured.")
        return self.csv_header_subject

    def get_csv_header_changed(self) -> str:
        """
        Retrieves the CSV header for the 'changed' field.

        Returns:
            str: The configured 'changed' header.

        Raises:
            ValueError: If the 'changed' header is not yet configured.
        """
        if not self.csv_header_changed:
            raise ValueError("❌ The CSV header for 'changed' has not been configured.")
        return self.csv_header_changed

    def get_csv_header_description(self) -> str:
        """
        Retrieves the CSV header for the description.

        Returns:
            str: The configured description header.

        Raises:
            ValueError: If the description header is not yet configured.
        """
        if not self.csv_header_description:
            raise ValueError(
                "❌ The CSV header for 'description' has not been configured."
            )
        return self.csv_header_description

    def get_export_format(self) -> str:
        """
        Retrieves the selected export format.

        Returns:
            str: The configured export format, e.g., `default`.

        Raises:
            ValueError: If the export format is not yet configured.
        """
        if not self.export_format:
            raise ValueError("❌ The export method has not been configured.")
        return self.export_format

    def get_export_language(self) -> str:
        """
        Retrieves the configured export language.

        Returns:
            str: The export language.
        """
        return self.export_language

    def get_export_subdirectory(self) -> str:
        """
        Retrieves the configured export subdirectory.

        Returns:
            str: The relative path of the export subdirectory.
        """
        return self.export_subdirectory

    def get_llm_provider(self) -> str:
        """
        Returns the configured Large Language Model (LLM) provider.

        Returns:
            str: The selected LLM provider, e.g., `openai`.

        Raises:
            ValueError: If the LLM provider is not yet configured.
        """
        if not self.llm_provider:
            raise ValueError("❌ The LLM provider has not been configured.")
        return self.llm_provider

    def get_export_technological_component(self) -> bool:
        """
        Retrieves the configuration for exporting technological components.

        Returns:
            bool: True if enabled, False otherwise.
        """
        return self.export_technological_component

    def get_export_technological_component_subcategory(self) -> bool:
        """
        Retrieves the configuration for exporting technological component subcategories.

        Returns:
            bool: True if enabled, False otherwise.
        """
        return self.export_technological_component_subcategory

    def get_export_functional_area(self) -> bool:
        """
        Retrieves the configuration for exporting functional areas.

        Returns:
            bool: True if enabled, False otherwise.
        """
        return self.export_functional_area

    def get_export_functional_area_subcategory(self) -> bool:
        """
        Retrieves the configuration for exporting functional area subcategories.

        Returns:
            bool: True if enabled, False otherwise.
        """
        return self.export_functional_area_subcategory

    def get_export_problem_type(self) -> bool:
        """
        Retrieves the configuration for exporting problem types.

        Returns:
            bool: True if enabled, False otherwise.
        """
        return self.export_problem_type

    def get_export_problem_type_subcategory(self) -> bool:
        """
        Retrieves the configuration for exporting problem type subcategories.

        Returns:
            bool: True if enabled, False otherwise.
        """
        return self.export_problem_type_subcategory

    def _input(
        self, env_var: str, prompt_text: str, default: Optional[str] = None
    ) -> Any:
        """
        Prompts the user for input, with optional support for environment variable defaults.
        Allows using a default value if no input is provided.

        Args:
            env_key (str): The name of the environment variable to check for a default input value.
            label (str): The label or message displayed to the user in the input prompt.
            default (Optional[str]): The default value to use if no input is given.

        Returns:
            str: The user's input as a string.
        """
        value = os.getenv(env_var)
        # If not set, prompt the user
        if not value:
            value = prompt(f"{prompt_text} [{default}]: ") or default
        return value

    def _input_boolean(self, env_var: str, description: str, default: int) -> bool:
        """
        Reads a boolean-like value from an environment variable.

        Args:
            env_var (str): The name of the environment variable.
            description (str): Short description used for logging or prompts.
            default (int): Default boolean value if not explicitly set.

        Returns:
            bool: The boolean value (0/1 or True/False).
        """
        value = os.getenv(env_var, str(default))
        try:
            return bool(int(value))
        except ValueError:
            raise ValueError(f"❌ Invalid boolean value for {description}: {value}")

    def _input_list(self, env_key: str, label: str) -> List[str]:
        """
        Prompts the user for input, with optional support for environment variable defaults
        and formatting the input as a list.

        Args:
            env_key (str): The name of the environment variable to check for a default input value.
            label (str): The label or message displayed to the user in the input prompt.

        Returns:
            List[str]: The user's input as list of strings.
        """
        user_input = self._input(env_key, label)
        list = [part.strip() for part in user_input.split(",") if part.strip()]

        return list

    def _input_with_options(
        self,
        options: List[str],
        env_key: str,
        label: str,
        default_option: Optional[str] = None,
    ) -> str:
        """
        Prompts the user for input from a predefined list of valid options,
        with support for autocompletion and fallback to environment variables.

        Args:
            options (List[str]): A list of valid options the user can choose from.
            env_key (str): The name of the environment variable to check for a default input value.
            label (str): The label or message displayed to the user in the input prompt.
            default_option (str, optional): The default option to use if the user provides no input. Defaults to None.

        Returns:
            str: The user's selected option.

        Raises:
            ValueError: If the user's input is not in the list of valid options.
        """
        completer = WordCompleter(options, ignore_case=True)
        default_option_str = ""
        if default_option:
            default_option_str = f"; default is '{default_option}'"

        user_input = (os.getenv(env_key) or "").strip() or prompt(
            f"{label} (valid options: {', '.join(options)}{default_option_str}): ",
            completer=completer,
        ).strip().lower()

        if default_option and not user_input:
            user_input = default_option

        if user_input not in options:
            raise ValueError(f"❌ Invalid {label.lower()}: '{user_input}'.")

        return user_input
