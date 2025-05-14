from src.llm.prompt.abstract_prompt_builder import AbstractPromptBuilder


class ProcessingPromptBuilder(AbstractPromptBuilder):
    """
    Responsible for building categorization prompts for processing incident reports.
    This class provides predefined assistant roles, platform context, and task instructions
    to classify incidents into main and subcategories based on technological, functional,
    and problem-oriented dimensions.
    """

    ASSISTANT_TASK = """
    **Task**: Given an incident, classify and categorize it into **main categories** and **subcategories** based on three dimensions:
    Technological Component, Functional Area, and Problem Type.
    Return **only** the JSON output as specified, without generating any script or additional text.

    **Dimensions**:

    1. Technological Component: [TECHNOLOGICAL_COMPONENT]
    2. Functional Area: [FUNCTIONAL_AREA]
    3. Problem Type: [PROBLEM_TYPE]

    **Incident Data**:

    - Subject: [SUBJECT]
    - Description: [DESCRIPTION]

    **Instructions**:

    1. Parse the incident data to determine the appropriate category and subcategory for each dimension (Technological component, Functional area, Problem type).
    2. Use the platform context, including secondary projects and alternative names, to guide categorization.
    3. If information is ambiguous, make a reasoned assumption based on context and document it in a "Notes" column in the output.
    4. Return **only** the JSON object with the following structure:
    {
        "technological_component": "Main technological component affected.",
        "technological_component_subcategory": "Subcategory or N/A.",
        "functional_area": "Main functional area affected.",
        "functional_area_subcategory": "Subcategory or N/A.",
        "problem_type": "Main problem type.",
        "problem_type_subcategory": "Subcategory or N/A.",
        "notes": "Brief explanation of the categorization rationale or assumptions."
    }
    - Do **not** generate a script or any additional text outside the JSON.

    **Example Input**:

    ```
    1. Summary: Checkout button unresponsive
    2. Description: When attempting to finalize an order, clicking the 'Checkout' button does not trigger any visible action. The issue occurs intermittently on certain devices and browsers.
    ```

    **Example Output (JSON)**:

    ```
    {
        "technological_component": "Frontend",
        "technological_component_subcategory": "UI Interaction",
        "functional_area": "Checkout",
        "functional_area_subcategory": "Order Submission",
        "problem_type": "User Interface Error",
        "problem_type_subcategory": "Button not responsive",
        "notes": "The issue appears to be related to an event listener not properly attached to the checkout button in certain user environments."
    }
    ```

    **Constraints**:

    - Ensure the categorization is clear, consistent, and actionable for a technical team (developers, system administrators, product managers).
    - Handle ambiguous or incomplete incident descriptions by making reasonable assumptions and documenting them.
    """

    ASSISTANT_RESPONSE_INSTRUCTIONS = """
    **Response instructions**:

    - You must only provide JSON data.
    - Return **only** the JSON output as specified, without generating any script or additional text.
    - Your response must contain nothing but the JSON data, with no delimiters (such as ```json), additional indications, or the word 'json'.
    """.strip()

    def build_prompt(self, subject: str, description: str) -> str:
        """
        Builds a complete prompt for categorizing an individual incident based on its summary and description.

        Combines the predefined assistant role, platform context, task, and incident details into a
        formatted string ready for processing in a large language model (LLM).

        Args:
            subject (str): A brief summary of the incident being analyzed.
            description (str): A detailed description of the incident containing contextual information.

        Returns:
            str: A complete formatted prompt string containing the incident analysis and categorization instructions.
        """
        dimension_technological_component = (
            self.configuration_manager.get_dimension_technological_component()
        )
        dimension_functional_area = (
            self.configuration_manager.get_dimension_functional_area()
        )
        dimension_problem_type = self.configuration_manager.get_dimension_problem_type()
        role = self.configuration_manager.get_assistant_role_processing()
        context = f"""
        **Platform Context:**

        {self.configuration_manager.get_assistant_context_processing()}
        """
        task = (
            self.ASSISTANT_TASK.replace(
                "[TECHNOLOGICAL_COMPONENT]", dimension_technological_component
            )
            .replace("[FUNCTIONAL_AREA]", dimension_functional_area)
            .replace("[PROBLEM_TYPE]", dimension_problem_type)
            .replace("[SUBJECT]", subject)
            .replace("[DESCRIPTION]", description)
        )
        response_instructions = self.ASSISTANT_RESPONSE_INSTRUCTIONS
        assistant_additional_instructions = (
            self.configuration_manager.get_assistant_additional_instructions_processing()
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
