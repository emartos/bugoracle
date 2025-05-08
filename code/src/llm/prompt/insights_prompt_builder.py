import json
from typing import Any, Dict


class InsightsPromptBuilder:
    """
    Responsible for building prompts for analyzing and summarizing incident datasets.
    This class provides context, a predefined assistant role, and generation instructions
    for streamlining insights extraction from summarized data.
    """

    ASSISTANT_ROLE = """
    You are an expert in software development and system architecture, with deep knowledge of e-commerce platforms built on technologies like Drupal, React, React Native, and distributed systems.
    Your task is to analyze the dataset of summarized incidents and produce a global overview. Focus on key trends, recurring issues, and areas of improvement affecting the platform.
    """

    ASSISTANT_CONTEXT = """
    **Platform Context:**

    - **Technological Components**: Includes backend (Drupal 6 for business logic and APIs, headless), frontend (Drupal 10 with React components), and mobile (React Native consuming APIs).
    - **Functional Areas**: Key areas include catalog, checkout, translations, marketing feeds, logistics, email marketing, and translations.
    - **Integrity and Issues**: The platform uses API integrations (e.g., Algolia for search, SPLIO for marketing) and asynchronous queues (internal and external to Drupal).
    """

    ASSISTANT_TASK = """
    **Task**:

    Analyze the provided dataset and focus on identifying **overarching trends** and actionable insights **without breaking the analysis by periods**.

    **Input Data**:

    ```json
    [INPUT_DATA]
    ```

    **Instructions**:

    - Review the input dataset as a whole, ignoring breakdowns by period or time frame.
    - Compile a **comprehensive and unified analysis** across the following dimensions:
      1. **Technological Components**:
         - Highlight which components (e.g., Drupal 10, Algolia, Mercury Logistics) present the highest concentration of incidents across the dataset.
         - Identify any recurrent subcategories of problems (e.g., Commerce Module issues under Drupal 10).

      2. **Functional Areas**:
         - Summarize which functional areas (e.g., Checkout, Product Catalog) are most frequently affected.
         - Emphasize recurring problem areas that have a direct impact on user experience or business-critical functionalities.

      3. **Problem Types**:
         - Highlight the most common types of problems (e.g., Functional Errors, Synchronization Issues).
         - Address any patterns in problem dependencies (e.g., synchronization errors frequently related to API interactions).

    - **Identify Patterns and Relationships**:
       - Correlate technological components with functional areas impacted. For example:
         - How issues in Drupal 10 affect the Checkout experience.
         - How synchronization errors impact multiple functional areas like Product Catalog or Order Management.
       - Assess whether any specific categories labeled "N/A" or missing data might indicate reporting gaps.

    - **Extract Key Trends**:
       - Summarize the most critical global trends across the dataset, such as:
         - Components or functional areas with **chronic issues**.
         - Any noticeable **improvements or declines** in specific areas.
         - Key **root causes** or recurring combinations of problems.

    - **Provide Actionable Recommendations**:
       - Based on the global analysis, suggest:
         1. Which technological components or functional areas should be **prioritized for improvement**.
         2. High-level strategies to address recurring issues (e.g., better QA for specific components, optimizing API integrations).
         3. Actions to reduce problem occurrences, enhance performance, or improve data accuracy.

    **Output Example**:

    1. **Global Analysis of Technological Components**:
       - Drupal 10 (Commerce Module) exhibits the highest number of incidents, indicating chronic issues.
       - Mercury Logistics shows frequent synchronization issues, particularly in the context of inventory data updates.

    2. **Global Analysis of Functional Areas**:
       - Checkout and Product Catalog functionality dominate as the most affected areas.
       - Recurrent issues in Checkout are tied to both payment gateway integrations and API synchronization dependencies.

    3. **Global Analysis of Problem Types**:
       - Functional Errors constitute over 70% of all incidents, heavily concentrated in Checkout and Catalog features.
       - Synchronization problems, while less frequent, highlight problematic dependencies on API integrations.

    4. **Key Patterns and Relationships**:
       - Issues in Drupal 10 frequently disrupt functional areas critical to user interaction, like Checkout or Catalog.
       - Mercury Logistics synchronization failures cascade into delays in order processing.

    5. **Recommendations**:
       - Prioritize QA and debugging processes for Drupal 10’s Commerce Module.
       - Streamline API interaction mechanisms to reduce synchronization issues (e.g., Mercury Logistics, Algolia).
       - Introduce better incident categorization mechanisms to minimize entries labeled "N/A".
    """

    ASSISTANT_RESPONSE_INSTRUCTIONS = """
    **Response instructions**:

    - Ensure that your response content is written in "[TARGET_LANGUAGE]".
    - Your response must not contain delimiters (such as ```text).
    """.strip()

    def build_prompt(
        self, summarized_data: Dict[str, Any], target_language: str
    ) -> str:
        """
        Builds a complete prompt for analyzing and summarizing a dataset of incidents.

        Combines assistant role, context, task, and the input dataset into a formatted string
        to be used in generating insights using an external LLM.

        Args:
            summarized_data (Dict[str, Any]): The summarized dataset to analyze, structured as a dictionary.
            target_language (str): The target language for the generated prompt. Defaults to "en".

        Returns:
            str: A formatted string containing the assistant role, platform context,
                 analysis task, and the injected input dataset.
        """
        formatted_data = json.dumps(summarized_data, indent=4)

        task = self.ASSISTANT_TASK.replace("[INPUT_DATA]", formatted_data)

        instructions = self.ASSISTANT_RESPONSE_INSTRUCTIONS.replace(
            "[TARGET_LANGUAGE]", target_language
        )

        return self.ASSISTANT_ROLE + self.ASSISTANT_CONTEXT + task + instructions
