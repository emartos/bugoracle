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

    1. Technological Component:
    ```
    [TECHNOLOGICAL_COMPONENT]`
    ```

    2. Functional Area:
    ```
    [FUNCTIONAL_AREA]
    ```

    3. Problem Type:
    ```
    [PROBLEM_TYPE]
    ```

    **What is an incident**: An incident consists on two attributes: summary and description.

    **Instructions**:

    1. **Analyze the Incident**:
       - Parse the input data to determine the appropriate category and subcategory for each dimension (Technological component, Functional area, Problem type).
       - Use the platform context, including secondary projects and alternative names, to guide categorization.
       - If information is ambiguous, make a reasoned assumption based on context and document it in a "Notes" column in the output.

    2. **Categorization**:

       - Assign a **main category** and, where applicable, a **subcategory** for each dimension. For example:
         - Technological component: Main: Drupal 10, Subcategory: Commerce Module.
         - Functional area: Main: Pricing, Subcategory: Discount Calculation.
         - Problem type: Main: Functional Error, Subcategory: Type Error.

    3. **Output Format**:

       - Generate a JSON file with the following structure:
        {
            "technological_component": "Main technological component affected.",
            "technological_component_subcategory": "Subcategory for the technological component (or "N/A" if none).",
            "functional_area": "Main functional area affected.",
            "functional_area_subcategory": "Subcategory for the functional area (or "N/A" if none).",
            "problem_type": "Main problem type.",
            "problem_type_subcategory": "Subcategory for the problem type (or "N/A" if none).",
            "notes": "Brief explanation of the categorization rationale or assumptions made.",
        }

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

    **Incident data**:

    Below is the incident data for subject and description:

    - Subject:
    ```
    [SUBJECT]
    ```

    - Description:
    ```
    [DESCRIPTION]
    ```
    """

    ASSISTANT_RESPONSE_INSTRUCTIONS = """
    **Response instructions**:

    - You must only provide JSON data.
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
