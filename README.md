# Data-Driven Software Engineer Candidate Evaluation

## Overview

This repository is designed to evaluate software engineering candidates on crucial data engineering and software development skills, focusing on data processing, software architecture, testing, and documentation.

## Key Features

### Data Processing
- **PDF Handling**: Functions to retrieve, read, and extract content from PDF files.
- **Concurrent Processing**: Efficiently reads multiple PDF files concurrently to enhance performance.

### Software Architecture
- **Modular Design**: Organized the codebase into modular and reusable components (`file_utils.py`, `pdf_utils.py`, `error_handling.py`).
- **Error Handling**: Custom exceptions and error-handling functions ensure robustness.

### Testing
- **Unit Tests**: Comprehensive test suite covering various edge cases and ensuring functionality.
- **Logging**: Detailed logging setup to capture relevant error messages and procedural information.

### Documentation
- **Docstrings**: Added detailed docstrings to each function explaining its purpose, arguments, and return values.
- **Comments**: Inline comments provide clarity and better code understanding.

## Project Structure

```plaintext
.
├── output                  # Directory for processed output files
├── pdfs                   # Directory containing PDF files to process
├── README.md              
├── requirements.txt        # List of dependencies required for the project
├── src                     # Source code directory
│   ├── config.py           # Configuration settings
│   ├── __init__.py         
│   ├── logger.py           # Logging configuration
│   ├── main.py             # Main script to orchestrate data processing
│   ├── processor.py        # Core processing logic for PDFs
│   └── utils               # Utility functions and submodules
│       ├── error_handling.py
│       ├── file_utils.py
│       └── pdf_utils.py
├── tests                   # Test cases for the project
│   ├── test_error_handling.py
│   ├── test_file_utils.py
│   └── test_pdf_utils.py
└── venv                    # Virtual environment directory
```

Clone the repository:
```bash
git clone https://github.com/sassihamdi-CD/data-driven-software-engineer-evaluation.git
cd data-driven-software-engineer-evaluation
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Solution

### Running the Main Program:
Navigate to the directory and start processing PDF files with the following command:
```bash
python src/main.py  # Ensure you have the main script to orchestrate data processing
```
### Running Tests:
Ensure you have pytest installed. You may need to install it if not already done:
```bash
pip install pytest
```
Run the test suite to verify everything is functioning correctly:
```bash
pytest tests/
```
This will execute all the unit tests and display the results.

### Detailed Logging

The project employs loguru for logging. Logs provide detailed information about the execution process and help in diagnosing issues efficiently.
