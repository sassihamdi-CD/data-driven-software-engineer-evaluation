"""
This module contains unit tests for the `file_utils.py` module.
The tests cover the following functions:
- `get_pdf_files`: Scans a directory for PDF files and returns their paths.
- `read_pdfs_concurrently`: Reads multiple PDF files concurrently and returns their contents.
- `read_pdf_file`: Reads the contents of a single PDF file.

These tests employ mocking to simulate file system operations and ensure the functions behave as expected under various scenarios.
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from src.utils.file_utils import get_pdf_files, read_pdf_file, read_pdfs_concurrently

class TestFileUtils(unittest.TestCase):
    """
    Test case for `file_utils.py`.
    Includes tests for the functions `get_pdf_files`, `read_pdf_file`, and `read_pdfs_concurrently`.
    """

    @patch("os.walk")
    def test_get_pdf_files(self, mock_walk):
        """
        Test the `get_pdf_files` function for retrieving PDF files.
        
        Simulates directory traversal and PDF file detection, including nested directories.
        Ensures the function correctly identifies and returns all PDF files within the directory and its subdirectories.
        """
        mock_walk.return_value = [
            ("root/pdfs", ["dir"], ["file1.pdf"]),
            ("root/pdfs/subdir", [], ["file2.pdf"]),
            ("root/pdfs/subdir/subsubdir", [], ["file3.pdf"])
        ]
        expected_files = [
            "root/pdfs/file1.pdf",
            "root/pdfs/subdir/file2.pdf",
            "root/pdfs/subdir/subsubdir/file3.pdf"
        ]
        self.assertEqual(get_pdf_files("dummy_directory"), expected_files)

    @patch("os.walk")
    def test_get_pdf_files_no_pdfs(self, mock_walk):
        """
        Test the `get_pdf_files` function in an empty directory.
        
        Ensures the function returns an empty list when no PDF files are found within the directory.
        """
        mock_walk.return_value = [
            ("root/pdfs", ["dir"], ["file1.txt", "file2.docx"])
        ]
        self.assertEqual(get_pdf_files("dummy_directory"), [])

    @patch("os.walk")
    def test_get_pdf_files_with_mixed_files(self, mock_walk):
        """
        Test the `get_pdf_files` function with mixed file types. 
        
        Ensures the function only returns PDF files, excluding other file types found within the directory.
        """
        mock_walk.return_value = [
            ("root/pdfs", ["dir"], ["file1.pdf", "file2.txt"]),
            ("root/pdfs/subdir", [], ["file3.pdf", "file4.docx"])
        ]
        expected_files = [
            "root/pdfs/file1.pdf",
            "root/pdfs/subdir/file3.pdf"
        ]
        self.assertEqual(get_pdf_files("dummy_directory"), expected_files)

    @patch("os.path.exists", return_value=False)
    def test_read_pdf_file_not_found(self, mock_exists):
        """
        Test the `read_pdf_file` function when the file is not found.

        Simulates a 'file not found' scenario to ensure the function handles this case correctly and returns `None`.
        """
        self.assertIsNone(read_pdf_file("nonexistent_path"))

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    @patch("pdfplumber.open")
    def test_read_pdf_file_success(self, mock_plumber, mock_open, mock_exists):
        """
        Test the `read_pdf_file` function to extract text from a PDF file.
        
        Mocks the pdfplumber.open and built-in open to simulate reading a PDF file and correctly extracting its text content.
        """
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock(extract_text=lambda: "sample text")]
        mock_plumber.return_value.__enter__.return_value = mock_pdf
        expected_output = "sample text"
        self.assertEqual(read_pdf_file("path/to/pdf"), expected_output)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    @patch("pdfplumber.open", side_effect=PermissionError)
    def test_read_pdf_file_permission_error(self, mock_plumber, mock_open, mock_exists):
        """
        Test the `read_pdf_file` function when permission is denied.
        
        Simulates a PermissionError during the file processing and ensures the function handles it properly.
        """
        self.assertIsNone(read_pdf_file("path/to/forbidden.pdf"))

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="")
    @patch("pdfplumber.open")
    def test_read_pdf_file_empty(self, mock_plumber, mock_open, mock_exists):
        """
        Test the `read_pdf_file` function with an empty PDF file.
        
        Simulates an empty PDF file and ensures the function correctly returns an empty string.
        """
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock(extract_text=lambda: "")]
        mock_plumber.return_value.__enter__.return_value = mock_pdf
        self.assertEqual(read_pdf_file("path/to/empty.pdf"), "")

    @patch("src.utils.file_utils.read_pdf_file", return_value="sample text")
    def test_read_pdfs_concurrently(self, mock_read_pdf_file):
        """
        Test the `read_pdfs_concurrently` function for concurrent PDF reading.
        
        Mocks the `read_pdf_file` function and validates concurrent processing of multiple PDF files.
        """
        pdf_files = ["path/to/pdf1.pdf", "path/to/pdf2.pdf"]
        results = read_pdfs_concurrently(pdf_files)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][1], "sample text")

    @patch("src.utils.file_utils.read_pdf_file", return_value="")
    def test_read_pdfs_concurrently_empty(self, mock_read_pdf_file):
        """
        Test the `read_pdfs_concurrently` function with no PDF files.
        
        Ensures the function handles an empty list of PDF files gracefully.
        """
        results = read_pdfs_concurrently([])
        self.assertEqual(results, [])


if __name__ == '__main__':
    unittest.main()
