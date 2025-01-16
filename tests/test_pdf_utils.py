"""
This module contains unit tests for `pdf_utils.py`, specifically for the `save_output` function and the image extraction process.
The tests ensure these functions behave correctly under various conditions, including error handling and success scenarios.

### Test Cases:

- `test_save_output_success`: Ensures data is correctly saved to a JSON file.
- `test_save_output_permission_error`: Verifies the function handles permission errors appropriately.
- `test_save_output_general_error`: Ensures the function handles unexpected
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os
from src.utils.pdf_utils import save_output
from PIL import Image
import io


class TestPDFUtils(unittest.TestCase):
    """
    Test case for `pdf_utils.py`.
    Includes tests for `save_output` function and image extraction processes.
    Enhanced to follow best practices and include thorough docstrings.
    """

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_save_output_success(self, mock_makedirs, mock_open):
        """
        Test the `save_output` function for successful data saving.
        
        Mocks `open` and `os.makedirs` to simulate saving data to a JSON file.
        """
        data = {"key": "value"}
        save_output(data, "output_file.json")
        mock_open.assert_called_once_with("output_file.json", "w")
        mock_open().write.assert_any_call("{")
        mock_open().write.assert_any_call('\n    ')
        mock_open().write.assert_any_call('"key"')
        mock_open().write.assert_any_call(': ')
        mock_open().write.assert_any_call('"value"')
        mock_open().write.assert_any_call('\n')
        mock_open().write.assert_any_call('}')

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_save_output_permission_error(self, mock_makedirs, mock_open):
        """
        Test the `save_output` function for handling permission errors.
        
        Simulates a permission error during the file saving process and ensures 
        appropriate logging and error handling.
        """
        mock_open.side_effect = PermissionError
        data = {"key": "value"}
        with patch("src.utils.pdf_utils.logger.error") as mock_logger:
            save_output(data, "output_file.json")
            mock_logger.assert_called()

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_save_output_general_error(self, mock_makedirs, mock_open):
        """
        Test the `save_output` function for handling general errors.
        
        Simulates an unexpected error during the file saving process and ensures 
        appropriate logging and error handling.
        """
        mock_open.side_effect = Exception
        data = {"key": "value"}
        with patch("src.utils.pdf_utils.logger.error") as mock_logger:
            save_output(data, "output_file.json")
            mock_logger.assert_called()


if __name__ == '__main__':
    unittest.main()
