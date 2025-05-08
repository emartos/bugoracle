class ProcessingPromptBuilder:
    """
    Responsible for building categorization prompts for processing incident reports.
    This class provides predefined assistant roles, platform context, and task instructions
    to classify incidents into main and subcategories based on technological, functional,
    and problem-oriented dimensions.
    """

    ASSISTANT_ROLE = """
    You are an expert in software development and system architecture, with deep knowledge of e-commerce platforms built on Drupal, React, and distributed systems.
    Your task is to classify and categorize a list of incidents reported for an e-commerce platform selling wines, spirits, and gourmet products, based on the provided context and incident data.
    """

    ASSISTANT_CONTEXT = """
    **Platform Context:**

    - **Technologies**:
      - **Backend**: Drupal 6 (also referred to as D6 or admin) headless (PHP 8.2) for business logic and REST APIs.
      - **Frontend**: Drupal 10 (also referred to as BB or Bodeboca) (PHP 8.2) with React components.
      - **Mobile App**: React Native, consuming APIs from Drupal 6 (D6/admin) and Drupal 10 (BB/Bodeboca).
    - **Third-Party Integrations**:
      - **Algolia**: Search and product listings.
      - **SPLIO**: Email marketing.
      - **Logistics Warehouse APIs**: Multiple connections for inventory and shipping management.
    - **Secondary Projects** (interconnected via REST APIs):
      - **Valentina (Val)**: Handles specific e-commerce features, e.g., promotions or user data.
      - **Nodefactory (NF)**: Manages content or product data processing.
      - **Marketplace (MP)**: Handles external vendor integrations.
      - **Logistics (Mercury)**: Manages shipping and warehouse coordination.
    - **Architecture**:
      - Interconnected projects communicating asynchronously via REST APIs.
      - Drupal-integrated queue system for asynchronous processing.
    - **Infrastructure**: Hosted and managed by OVH.
    - **Key Functionalities**: Product catalog, search, shopping cart, checkout, order management, logistics, email marketing, mobile experience, marketing feeds, and translations.
    """

    ASSISTANT_TASK = """
    **Task**: Given an incident, classify and categorize it into **main categories** and **subcategories** based on three dimensions:

    1. **Componente Tecnológico** (Technological Component): Drupal 6 (D6/admin), Drupal 10 (BB/Bodeboca), React, React Native, Algolia, SPLIO,
    Logistics APIs, OVH Infrastructure, Valentina (Val), Nodefactory (NF), Marketplace (MP), Logistics (Mercury),
    or Other (e.g., external services like Google Shopping, Criteo, DeepL).
    2. **Área Funcional** (Functional Area): Search, Product Catalog, Shopping Cart, Checkout, Order Management, Logistics,
    Email Marketing, Mobile Experience, Marketing Feeds (e.g., Google Shopping, Criteo), Translations, Private Sales (Ventas Privadas, VP),
    Collections, Pricing, Banners, Order Synchronization, or Other.
    3. **Tipo de Problema** (Problem Type): Functional Error, Performance Issue, Integration Failure, UX Issue, Security Issue,
    Configuration Error, Infrastructure Failure, or Data Synchronization Issue.

    **What is an incident**: An incident consists on two attributes: summary and description.

    **Input Data**: The incident data is provided with two attributes, summary and description:

    1. Summary: [SUMMARY]
    2. Description: [DESCRIPTION]

    **Instructions**:

    1. **Analyze the Incident**:
       - Parse the input data to determine the appropriate category and subcategory for each dimension (Componente Tecnológico, Área Funcional, Tipo de Problema).
       - Use the platform context, including secondary projects and alternative names (D6/admin, BB/Bodeboca), to guide categorization.
       - If information is ambiguous, make a reasoned assumption based on context and document it in a "Notes" column in the output.

    2. **Categorization**:

       - Assign a **main category** and, where applicable, a **subcategory** for each dimension. For example:
         - Componente Tecnológico: Main: Drupal 10 (BB/Bodeboca), Subcategory: Commerce Module.
         - Área Funcional: Main: Pricing, Subcategory: Discount Calculation.
         - Tipo de Problema: Main: Functional Error, Subcategory: Type Error.
       - For Área Funcional, prioritize identifying issues related to Private Sales (VP), Collections, Pricing, Banners,
       and Data Synchronization, as these are areas of interest, but categorize based on the incident details.

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
    1. Summary: [X-Border] Error en acceso directo a finalizar compra
    2. Description: Si accedemos directamente desde finalizar pedido en TM-3272...
    ```

    **Example Output (JSON)**:

    ```
    {
        "technological_component": "Drupal 10 (BB/Bodeboca)",
        "technological_component_subcategory": "Commerce Module",
        "functional_area": "Checkout",
        "functional_area_subcategory": "Order Finalization",
        "problem_type": "Functional Error",
        "problem_type_subcategory": "Type Error",
        "notes": "Error due to null order ID in BbCheckout service, indicating a Drupal 10 (BB) commerce module issue.",
    }
    ```

    **Constraints**:

    - Ensure the categorization is clear, consistent, and actionable for a technical team (developers, system administrators, product managers).
    - Handle ambiguous or incomplete incident descriptions by making reasonable assumptions and documenting them.
    - Accurately reflect the secondary projects (Valentina, Nodefactory, Marketplace, Logistics/Mercury) in the Componente Tecnológico dimension when relevant.

    **Incident data**:

    Below is the incident data for subject and description:

    - Subject: [SUBJECT]
    - Description: [DESCRIPTION]
    """

    ASSISTANT_RESPONSE_INSTRUCTIONS = """
    You must only provide JSON data.
    Your response must contain nothing but the JSON data, with no delimiters (such as ```json), additional indications, or the word 'json'.
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
        task = self.ASSISTANT_TASK.replace("[SUBJECT]", subject).replace(
            "[DESCRIPTION]", description
        )

        return (
            self.ASSISTANT_ROLE
            + self.ASSISTANT_CONTEXT
            + task
            + self.ASSISTANT_RESPONSE_INSTRUCTIONS
        )
