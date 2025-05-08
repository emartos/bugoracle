# BugOracle: An intelligent system for bug categorization and reporting

This project is a robust **bug categorization and analysis tool** powered by **Large Language Models (LLM)** and advanced data processing techniques. Its primary goal is to automatically classify, summarize, and export bug reports into meaningful insights by analyzing structured datasets such as CSV files. Designed especially for **e-commerce platforms**, it leverages insights from incidents and provides clear categorizations, helping engineering teams prioritize and address issues effectively.

---

## 🚀 Features

1. **Bug Retrieval and Preprocessing**:
   - Reads data from **CSV files** containing bug reports.
   - Extracts rows and ensures data consistency for further processing.
   - Ability to handle large datasets efficiently with built-in row counting and filtering tools.

2. **Automated Categorization**:
   - Uses **Large Language Models (LLMs)** to intelligently analyze and categorize incidents.
   - Categorizes bugs across three critical dimensions:
      - **Technological Component**: Identifies affected technologies such as `Drupal`, `React`, or `Logistics APIs`.
      - **Functional Area**: Maps functions like `Order Management`, `Checkout`, `Translations`, etc., to the bug's impact.
      - **Problem Type**: Defines the type of issue (e.g., `Functional Error`, `Performance Issue`, `Integration Failure`).

3. **Incident Summary and Insights**:
   - Aggregates bug data into **total counts** and **monthly statistics**.
   - Summarizes intricate technical data into clear insights, helping decision-makers take action.
   - Highlights the most common areas and technologies affected based on historical analysis.

4. **Easy Exportation**:
   - Provides support to export both raw and summarized data into multiple formats:
      - **JSON**: For API integration or further programmatic processing.
      - **CSV**: Traditional tabular format for easy visualization and sharing.
   - High configurability to adapt export formats as per user needs.

5. **Seamless Integration**:
   - Works with existing e-commerce setups by analyzing bug data tied to technologies like APIs, infrastructure tools such as **OVH**, and third-party integrations like **Algolia** or **DeepL**.

6. **Customizable Processing**:
   - The system supports flexible configuration for CSV headers, LLM providers, and export logic, ensuring teams can tailor it to their organization’s specific workflows.

7. **Makefile for Workflow Automation**:
   - Simplifies development and deployment tasks using `make` commands:
      - Environment setup
      - Code linting and formatting
      - Execution of the application

---

## 📦 Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/bug-oracle.git
cd bug-oracle
```

### Step 2: Create and activate the virtual environment
```bash
make create-venv
```

### Step 3: Install dependencies
```bash
make install-requirements
```

### Step 4: Prepare the configuration
```bash
make env
```
This will generate an `.env` file. Update it with the required settings like CSV paths or LLM provider options.

---

## ▶️ Usage

To run the application, simply execute the following command:

```bash
make run
```

The application will:
1. Retrieve bug data from a configured CSV file.
2. Process the data using an LLM and classify reports into categories.
3. Summarize the results into meaningful monthly and overall insights.
4. Export the results to the chosen output format (e.g., JSON, CSV).

> **Tip**: Modify the settings in `.env` to adjust paths, field mappings, and providers to suit your project's needs.

---

## 🛠️ Makefile Commands

The project includes a **Makefile** to streamline development and operational tasks:

### 📂 Environment setup:
- **`make create-venv`**: Sets up the virtual environment.
- **`make install-requirements`**: Installs required Python dependencies.
- **`make freeze-requirements`**: Freezes dependencies into `requirements.txt`.
- **`make env`**: Creates the `.env` file for configuration.

### ▶️ Application execution:
- **`make run`**: Starts the application.

### 🧹 Maintenance Tools:
- **`make lint`**: Runs `flake8` for code linting.
- **`make pre-commit`**: Executes all pre-commit hooks.
- **`make check-format`**: Checks code formatting with `isort` and `black`.
- **`make clean`**: Cleans temporary files and caches.
- **`make delete-venv`**: Removes the virtual environment.

> Run `make help` to see all commands with descriptions.

---

## 🌐 Supported Categories for Bug Classification

The application organizes incidents into:
1. **Technological Components**:
   - Drupal (D6 and D10), React, React Native, Algolia, SPLIO, OVH, etc.
2. **Functional Areas**:
   - Checkout, Order Management, Search, Translations, Marketing Feeds, etc.
3. **Problem Types**:
   - Functional errors, performance issues, integration failures, security incidents, configuration problems, etc.

---

## 🌟 Example Workflow

1. Add your bug data into a CSV file as input.
2. Modify `.env` to configure paths, LLM provider, and other options.
3. Run the application with:
   ```bash
   make run
   ```
4. The system will:
   - Classify the data.
   - Summarize counts and monthly trends.
   - Export reports into desired formats for further analysis.

---

## 📊 Export Formats:

1. **CSV**:
   - Simple, structured tabular format.
2. **JSON**:
   - Programmatically rich, easy for integrations or detailed analysis.

---

## 📧 Support

If you encounter any issues or have questions, feel free to open an issue in the repository or contact the project maintainer at `info@natiboo.es`.

---

## 🤝 Contributing

We welcome contributions to this project! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch-name`).
3. Ensure all `make pre-commit` hooks pass.
4. Submit a pull request.

---

## 📜 License

This project is licensed under the GNU Affero General Public License v3.0.
You may redistribute and/or modify it under the terms of the AGPL-3.0.

See the [LICENSE](./LICENSE) file for full license details.

Copyright (C) 2025 Eduardo Martos Gómez <emartos@natiboo.es>

---

## 🎉 Acknowledgements

- [OpenAI](https://openai.com/) and [Grok](https://grok.com/) for their LLM capabilities.
- The open-source community for their incredible tools and resources.
