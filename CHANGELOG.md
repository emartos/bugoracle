## [1.0.0] - 2025-05-08

### Added
- In `.env.template`:
  - Added configuration template with sections for application settings, parameters, OpenAI settings, xAI settings, and Redis settings, including environment variables like `ENVIRONMENT`, `LOG_LEVEL`, `CSV_DATA_PATH`, `OPENAI_API_KEY`, `XAI_API_KEY`, `REDIS_HOST`, etc.
- In `.flake8`:
  - Added Flake8 configuration with a maximum line length of 210.
- In `.gitignore`:
  - Added comprehensive ignore patterns for Node, Java, Python, log files, IDE artifacts, macOS/Windows-generated files, and environment/data directories.
- In `.pre-commit-config.yaml`:
  - Added pre-commit hooks for case conflict checks, docstring validation, symlink checks, end-of-file fixes, requirements sorting, trailing whitespace, isort, Black, Flake8, and MyPy.
- In `Makefile`:
  - Added targets for environment setup (`create-venv`, `install-requirements`, `freeze-requirements`, `delete-venv`), code analysis (`lint`, `pre-commit`, `pre-commit-force`), execution (`run`, `app-version`), cleaning (`clean`), and Redis cache management (`cache-list`, `cache-clear`).
- In `README.md`:
  - Added detailed project documentation for BugOracle, including features, installation steps, usage instructions, Makefile commands, supported bug classification categories, and example workflow.
- In `code/`:
  - Added `app.py`: Main application logic for BugOracle, handling bug retrieval, LLM processing, summarization, insights generation, and data export.
  - Added `requirements.txt`: Specified dependencies including `openai`, `redis`, `flake8`, `pre_commit`, `pydantic`, etc.
  - Added `scripts/cache.py`: Script for listing and invalidating Redis cache keys based on patterns.
  - Added `src/config/configuration_manager.py`: Singleton class for managing and validating application configurations.
  - Added `src/csv/csv_reader.py`: Class for reading and processing CSV files.
  - Added `src/exporter/exporter_provider.py`: Factory class for providing exporter instances.
  - Added `src/exporter/format/csv.py`: Exporter for CSV format, supporting processed data, totals, and insights.
  - Added `src/exporter/format/json.py`: Exporter for JSON format, creating hierarchical structures for totals and totals by date.
  - Added `src/llm/cache_manager.py`: Redis-based caching for LLM prompts.
  - Added `src/llm/model_provider.py`: Factory class for providing LLM model instances.
  - Added `src/llm/prompt/insights_prompt_builder.py`: Builds prompts for generating insights from summarized data.
  - Added `src/llm/prompt/processing_prompt_builder.py`: Builds prompts for categorizing incident reports.
  - Added `src/llm/provider/grok.py`: Interface for xAI's Grok model with caching and retry logic.
  - Added `src/llm/provider/openai.py`: Interface for OpenAI models with caching and retry logic.
  - Added `src/llm/provider/model_interface.py`: Abstract interface for LLM models.
  - Added `src/logger/formatter.py`: Custom log formatter with color-coded log levels.
  - Added `src/logger/logger.py`: Logger setup with custom formatter.
  - Added `src/summarizer/summarizer_interface.py`: Abstract interface for summarizers.
  - Added `src/summarizer/total_summarizer.py`: Summarizes bug data by totals and monthly groupings.
  - Added `version.py`: Defines the initial version `__version__ = "1.0.0"`.

## [1.1.0] - 2025-05-14

### Added
- In `code/src/llm/provider/googlegenai.py`:
  - Added support for Google Gemini API integration, enabling text generation with the `gemini-1.5-flash` model by default, configurable via `GOOGLE_TEXT_MODEL` environment variable.
  - Implemented caching with `CacheManager` and retry logic for handling rate limit errors (`ResourceExhausted`).
- In `code/src/llm/provider/ollama.py`:
  - Added support for Ollama integration with Llama models, defaulting to `llama3.2`, configurable via `LLAMA_TEXT_MODEL` and `LLAMA_BASE_URL` environment variables.
  - Included caching with `CacheManager` and retry logic for handling `ResponseError` and `RequestException`.