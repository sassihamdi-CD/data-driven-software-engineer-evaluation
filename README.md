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
├── src
│   └── utils
│       ├── error_handling.py
│       ├── file_utils.py
│       └── pdf_utils.py
├── tests
│   ├── test_error_handling.py
│   ├── test_file_utils.py
│   └── test_pdf_utils.py
├── README.md
└── requirements.txt

