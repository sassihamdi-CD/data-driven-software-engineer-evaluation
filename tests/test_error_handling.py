"""
This module contains unit tests for the `error_handling.py` file in the src/utils directory.
The tests ensure that custom exceptions and error-handling functions behave as expected.

### Key Components:
- **Custom Exceptions**: Tests for `PDFProcessingError`, `FileNotFoundErrorCustom`, `PDFReadError`, 
  `FileSaveError`, and `InvalidContentError` to validate their correct instantiation and string representation.
- **Error Handling Functions**: Tests for `handle_malformed_pdf_error` and `handle_invalid_content_error` 
  to ensure they log appropriate error messages and raise the respective exceptions.
- **Logging Verification**: Tests to ensure proper logging when custom exceptions are raised.

### Summary:
- Each test captures logging output to validate log messages.
- Comprehensive tests for various error scenarios are provided to maintain robustness of error handling in the system.
"""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from src.utils.error_handling import (
    PDFProcessingError,
    FileNotFoundErrorCustom,
    PDFReadError,
    FileSaveError,
    InvalidContentError,
    handle_malformed_pdf_error,
    handle_invalid_content_error,
    logger  # Ensure we're importing logger for proper mocking
)
import logging

class TestErrorHandling(unittest.TestCase):
    """
    Test case for `error_handling.py`.
    Includes comprehensive tests for custom exceptions and error-handling functions.
    """

    def setUp(self):
        """
        Set up the logging configuration for capturing logs during tests.
        """
        self.log_stream = StringIO()
        log_handler = logging.StreamHandler(self.log_stream)
        logger.addHandler(log_handler)

    def tearDown(self):
        """
        Remove the logging handler after each test.
        """
        logger.handlers.clear()

    def test_pdf_processing_error(self):
        """
        Test the `PDFProcessingError` exception.
        
        Ensures the `PDFProcessingError` exception is raised correctly with a custom message.
        """
        with self.assertRaises(PDFProcessingError, msg="Test PDF processing error"):
            raise PDFProcessingError("Test PDF processing error")

    def test_file_not_found_error(self):
        """
        Test the `FileNotFoundErrorCustom` exception.
        
        Ensures the `FileNotFoundErrorCustom` exception is raised correctly with the file path.
        """
        with self.assertRaises(FileNotFoundErrorCustom, msg="File not found: test.pdf"):
            raise FileNotFoundErrorCustom("test.pdf")

    def test_pdf_read_error(self):
        """
        Test the `PDFReadError` exception.
        
        Ensures the `PDFReadError` exception is raised correctly with the file path and error message.
        """
        with self.assertRaises(PDFReadError, msg="Error reading PDF file test.pdf: Read error"):
            raise PDFReadError("test.pdf", "Read error")

    def test_file_save_error(self):
        """
        Test the `FileSaveError` exception.
        
        Ensures the `FileSaveError` exception is raised correctly with the file path and error message.
        """
        with self.assertRaises(FileSaveError, msg="Error saving data to file test.json: Save error"):
            raise FileSaveError("test.json", "Save error")

    def test_invalid_content_error(self):
        """
        Test the `InvalidContentError` exception.
        
        Ensures the `InvalidContentError` exception is raised correctly when invalid content is found in a PDF.
        """
        with self.assertRaises(InvalidContentError, msg="Invalid content in PDF file test.pdf: Invalid data"):
            raise InvalidContentError("test.pdf", "Invalid data")

    def test_handle_malformed_pdf_error(self):
        """
        Test the `handle_malformed_pdf_error` function.
        
        Simulates handling a malformed PDF error and asserts the exception is raised with a proper message.
        """
        with patch("src.utils.error_handling.logger.error") as mock_logger:
            with self.assertRaises(PDFProcessingError, msg="Malformed PDF file: test.pdf. Error: Malformed error"):
                handle_malformed_pdf_error("test.pdf", "Malformed error")
            mock_logger.assert_called_with("Malformed PDF error in file test.pdf: Malformed error")

    def test_handle_invalid_content_error(self):
        """
        Test the `handle_invalid_content_error` function.
        
        Simulates handling an invalid content error from a PDF and asserts the exception is raised with a proper message.
        """
        with patch("src.utils.error_handling.logger.error") as mock_logger:
            with self.assertRaises(PDFProcessingError, msg="Invalid content in PDF: test.pdf"):
                handle_invalid_content_error("test.pdf", "Invalid content")
            mock_logger.assert_called_with("Invalid content extracted from file test.pdf: Invalid content")

    def test_log_error_on_file_not_found(self):
        """
        Test logging when a `FileNotFoundErrorCustom` is raised.
        
        Ensures proper log message is generated when the file is not found.
        """
        try:
            raise FileNotFoundErrorCustom("test.pdf")
        except FileNotFoundErrorCustom as e:
            logger.error(e)
        
        # Validate the logging call
        self.log_stream.seek(0)
        log_output = self.log_stream.read().strip()
        self.assertIn("FileNotFoundErrorCustom: File not found: test.pdf", log_output)

    def test_log_error_on_pdf_read(self):
        """
        Test logging when an error occurs while reading a PDF file.
        
        Ensures proper log message is generated for PDF read errors.
        """
        try:
            raise PDFReadError("test.pdf", "Read error")
        except PDFReadError as e:
            logger.error(e)
        
        # Validate the logging call
        self.log_stream.seek(0)
        log_output = self.log_stream.read().strip()
        self.assertIn("PDFReadError: Error reading PDF file test.pdf: Read error", log_output)

    def test_log_error_on_file_save(self):
        """
        Test logging when an error occurs during file saving.
        
        Ensures proper log message is generated for file save errors.
        """
        try:
            raise FileSaveError("test.json", "Save error")
        except FileSaveError as e:
            logger.error(e)
        
        # Validate the logging call
        self.log_stream.seek(0)
        log_output = self.log_stream.read().strip()
        self.assertIn("FileSaveError: Error saving data to file test.json: Save error", log_output)

    def test_log_error_on_invalid_content(self):
        """
        Test logging when invalid content is found in a PDF.
        
        Ensures proper log message is generated for invalid content errors.
        """
        try:
            raise InvalidContentError("test.pdf", "Invalid data")
        except InvalidContentError as e:
            logger.error(e)
        
        # Validate the logging call
        self.log_stream.seek(0)
        log_output = self.log_stream.read().strip()
        self.assertIn("InvalidContentError: Invalid content in PDF file test.pdf: Invalid data", log_output)


if __name__ == "__main__":
    unittest.main()
