import json
from typing import Any, Dict

from src.llm.prompt.abstract_prompt_builder import AbstractPromptBuilder


class InsightsPromptBuilder(AbstractPromptBuilder):
    """
    Responsible for building prompts for analyzing and summarizing incident datasets.
    This class provides context, a predefined assistant role, and generation instructions
    for streamlining insights extraction from summarized data.
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
         - Highlight which components present the highest concentration of incidents across the dataset.
         - Identify any recurrent subcategories of problems.

      2. **Functional Areas**:
         - Summarize which functional areas are most frequently affected.
         - Emphasize recurring problem areas that have a direct impact on user experience or business-critical functionalities.

      3. **Problem Types**:
         - Highlight the most common types of problems.
         - Address any patterns in problem dependencies.

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
       - Certain components exhibit higher frequencies of incidents, indicating potential chronic issues requiring attention.
       - Synchronization-related components often experience problems relating to data consistency or update failures.

    2. **Global Analysis of Functional Areas**:
       - Key functionalities, such as user checkout and data presentation, dominate as the most frequently affected areas.
       - Recurrent issues in critical workflows tend to stem from dependencies on external systems or integrations.

    3. **Global Analysis of Problem Types**:
       - Functional Errors make up the majority of reported incidents, heavily concentrated in core user actions such as submissions or queries.
       - Synchronization problems, while less prevalent, expose critical dependencies on external services or API connectivity.

    4. **Key Patterns and Relationships**:
       - Errors in core technologies may propagate across important functional areas, disrupting user experiences.
       - Synchronization failures in external dependencies create cascading effects that impact downstream processes, such as order management or data updates.

    5. **Recommendations**:
       - Allocate resources to enhance quality assurance and proactively identify chronic issues within high-incident components.
       - Strengthen API interaction and error-handling mechanisms to improve resilience against synchronization problems.
       - Improve incident categorization processes to reduce reliance on generic or ambiguous labels for better tracking and resolution.
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
        role = self.configuration_manager.get_assistant_role_insights()
        context = f"""
        **Platform Context:**

        {self.configuration_manager.get_assistant_context_insights()}
        """
        formatted_data = json.dumps(summarized_data, indent=4)
        task = self.ASSISTANT_TASK.replace("[INPUT_DATA]", formatted_data)
        response_instructions = self.ASSISTANT_RESPONSE_INSTRUCTIONS.replace(
            "[TARGET_LANGUAGE]", target_language
        )
        assistant_additional_instructions = (
            self.configuration_manager.get_assistant_additional_instructions_insights()
        )
        if assistant_additional_instructions:
            assistant_additional_instructions = f"""
            **Additional instructions**:

            {assistant_additional_instructions}
            """
        prompt = (
            role
            + context
            + task
            + response_instructions
            + assistant_additional_instructions
        )

        return prompt
