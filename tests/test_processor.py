import unittest
import io
from unittest.mock import patch, mock_open, MagicMock
from src.processor import read_pdf_file, preprocess_content, read_pdfs_concurrently, extract_images_from_pdf, process_pdfs
from src.utils.error_handling import InvalidContentError, PDFProcessingError


class TestProcessor(unittest.TestCase):
    """
    Test case for `processor.py`.
    Includes tests for `read_pdf_file`, `preprocess_content`, `read_pdfs_concurrently`, 
    `extract_images_from_pdf`, and `process_pdfs` functions.
    """

    @patch("src.processor.open", new_callable=mock_open, read_data="sample text")
    @patch("src.processor.PyPDF2.PdfReader")
    def test_read_pdf_file(self, mock_reader, mock_file):
        """
        Test the `read_pdf_file` function to extract text from a PDF file.
        
        Mocks the PdfReader and open functions to simulate reading a PDF file 
        and extracting text.
        """
        mock_reader.return_value.pages = [MagicMock(extract_text=lambda: "sample text")]
        expected_output = "sample text"
        self.assertEqual(read_pdf_file("path/to/pdf"), expected_output)

    @patch("os.path.exists", return_value=False)
    def test_read_pdf_file_not_found(self, mock_exists):
        """
        Test the `read_pdf_file` function handling file-not-found scenarios.
        
        Ensures the function raises PDFProcessingError when the file is not found.
        """
        with self.assertRaises(PDFProcessingError):
            read_pdf_file("nonexistent_path")

    def test_preprocess_content_valid(self):
        """
        Test the `preprocess_content` function with valid content.
        
        Validates that content containing the expected keyword is processed correctly.
        """
        valid_content = "This PDF contains the expected_keyword."
        self.assertEqual(preprocess_content("path/to/pdf", valid_content), valid_content)

    def test_preprocess_content_invalid(self):
        """
        Test the `preprocess_content` function with invalid content.
        
        Ensures the function raises InvalidContentError when expected keyword 
        is missing from the content.
        """
        invalid_content = "This PDF does not contain the expected keyword"
        with self.assertRaises(InvalidContentError):
            preprocess_content("path/to/pdf", invalid_content)

    @patch("src.processor.read_pdf_file", return_value="sample text")
    def test_read_pdfs_concurrently(self, mock_read_pdf_file):
        """
        Test the `read_pdfs_concurrently` function for concurrent PDF reading.
        
        Mocks `read_pdf_file` and validates the concurrent processing of multiple 
        PDF files with sample content.
        """
        files = ["path/to/pdf1", "path/to/pdf2"]
        results = read_pdfs_concurrently(files)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['content'], "sample text")

    @patch("src.processor.fitz.open")
    @patch("src.processor.Image.open")
    def test_extract_images_from_pdf(self, mock_open, mock_fitz_open):
        """
        Test the `extract_images_from_pdf` function for image extraction from PDF.
        
        Mocks `fitz.open` and `Image.open` functions to simulate image extraction 
        process from a PDF file.
        """
        mock_doc = mock_fitz_open.return_value
        mock_doc.page_count = 1
        mock_page = mock_doc.load_page.return_value
        mock_page.get_images.return_value = [(1,)]
        mock_image = MagicMock()
        mock_open.return_value = mock_image
        mock_image_bytes = io.BytesIO(b"fake_image_data")
        mock_doc.extract_image.return_value = {"image": mock_image_bytes, "ext": "png"}
        
        with patch("io.BytesIO", return_value=mock_image_bytes):
            extract_images_from_pdf("path/to/pdf", "output_directory")
            mock_open.assert_called()
            mock_image.save.assert_called()

    @patch("src.processor.get_pdf_files", return_value=["path/to/pdf"])
    @patch("src.processor.read_pdfs_concurrently", return_value=[{"file_name": "path/to/pdf", "content": "sample text"}])
    def test_process_pdfs_with_content(self, mock_read_pdfs_concurrently, mock_get_pdf_files):
        """
        Test the `process_pdfs` function when processing PDFs with content.
        
        Mocks the necessary functions to simulate the entire processing pipeline 
        for PDFs containing valid content.
        """
        with patch("src.processor.preprocess_content", return_value="preprocessed content"), \
             patch("src.processor.extract_images_from_pdf"), \
             patch("src.processor.save_output") as mock_save_output:
            process_pdfs("input_directory", "output_directory")
            mock_save_output.assert_called()

    @patch("src.processor.get_pdf_files", return_value=[])
    def test_process_pdfs_no_files(self, mock_get_pdf_files):
        """
        Test the `process_pdfs` function when no PDF files are found.
        
        Ensures the function handles scenarios where no PDF files are available 
        for processing.
        """
        with patch("src.processor.logger.warning") as mock_warning:
            process_pdfs("input_directory", "output_directory")
            mock_warning.assert_called_with("No PDF files found to process in directory: input_directory")

    @patch("src.processor.get_pdf_files", return_value=["path/to/pdf"])
    @patch("src.processor.read_pdfs_concurrently", return_value=[{"file_name": "path/to/pdf", "content": None}])
    def test_process_pdfs_no_content(self, mock_read_pdfs_concurrently, mock_get_pdf_files):
        """
        Test the `process_pdfs` function when no content is extracted from PDFs.
        
        Validates that the function logs appropriate warnings when content 
        extraction fails.
        """
        with patch("src.processor.logger.warning") as mock_warning:
            process_pdfs("input_directory", "output_directory")
            mock_warning.assert_any_call("No content extracted from file: path/to/pdf")
            mock_warning.assert_any_call("No content extracted to save after processing PDFs.")


if __name__ == '__main__':
    unittest.main()
