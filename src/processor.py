import logging
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import PyPDF2
from PyPDF2.errors import PdfReadError
import concurrent.futures
import fitz  # PyMuPDF
from PIL import Image
import io

# Ensure the parent directory is in the sys.path for module resolution
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils.file_utils import get_pdf_files
from src.utils.pdf_utils import save_output
from src.utils.error_handling import PDFProcessingError, FileNotFoundErrorCustom, FileSaveError, InvalidContentError

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def read_pdf_file(pdf_file: str) -> str:
    """
    Reads and extracts text from a PDF file.

    Args:
        pdf_file (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.

    Raises:
        PDFProcessingError: If the PDF cannot be read or processed.
    """
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = []
            for page in reader.pages:
                page_text = page.extract_text() or ''
                text.append(page_text)
            return " ".join(text).strip()
    except PdfReadError as e:
        logger.error(f"Malformed PDF file: {pdf_file} - {e}")
        raise PDFProcessingError(f"Failed to read PDF file: {pdf_file}") from e
    except MemoryError as e:
        logger.error(f"Memory error while processing PDF file: {pdf_file} - {e}")
        raise PDFProcessingError(f"Memory error processing PDF file: {pdf_file}") from e
    except Exception as e:
        logger.error(f"Error processing PDF file: {pdf_file} - {e}")
        raise PDFProcessingError(f"An unknown error occurred while reading the PDF: {pdf_file}") from e

def preprocess_content(file_path: str, content: str) -> str:
    """
    Validates and preprocesses the extracted content from a PDF file.

    Args:
        file_path (str): Path to the PDF file.
        content (str): Extracted content from the PDF.

    Returns:
        str: Preprocessed content.

    Raises:
        InvalidContentError: If the content is invalid or missing expected keywords.
    """
    if not content or "expected_keyword" not in content:
        raise InvalidContentError(file_path, content)
    return content.strip()

def read_pdfs_concurrently(pdf_files: List[str], max_workers: int = 4) -> List[Dict[str, str]]:
    """
    Reads multiple PDF files concurrently and extracts their content.

    Args:
        pdf_files (List[str]): List of paths to PDF files.
        max_workers (int): Maximum number of threads for concurrent processing.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing file names and their content.
    """
    pdf_contents = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_pdf = {executor.submit(read_pdf_file, pdf_file): pdf_file for pdf_file in pdf_files}
        for future in concurrent.futures.as_completed(future_to_pdf):
            pdf_file = future_to_pdf[future]
            try:
                content = future.result()
                pdf_contents.append({"file_name": pdf_file, "content": content})
            except Exception as e:
                logger.error(f"Error reading PDF file {pdf_file}: {e}")
                pdf_contents.append({"file_name": pdf_file, "content": None})
    return pdf_contents

def extract_images_from_pdf(pdf_file: str, output_directory: str) -> None:
    """
    Extracts images from a PDF file and saves them to the specified output directory.

    Args:
        pdf_file (str): Path to the PDF file.
        output_directory (str): Directory to save extracted images.
    """
    try:
        doc = fitz.open(pdf_file)
        image_count = 0
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                image_format = base_image["ext"]
                output_path = Path(output_directory) / f"{Path(pdf_file).stem}_image_{page_num + 1}_{img_index + 1}.{image_format}"
                image.save(output_path)
                image_count += 1
                logger.info(f"Image extracted from page {page_num + 1}, saved to {output_path}")
        if image_count == 0:
            logger.info(f"No images found in {pdf_file}.")
        else:
            logger.info(f"Extracted {image_count} image(s) from {pdf_file}.")
    except Exception as e:
        logger.error(f"Error extracting images from {pdf_file}: {e}", exc_info=True)

def process_pdfs(pdf_directory: str, output_directory: str = './output') -> None:
    """
    Processes all PDF files in a specified directory by extracting text and images.

    Args:
        pdf_directory (str): Path to the directory containing PDF files.
        output_directory (str): Path to the directory for saving extracted data and images.

    Raises:
        FileNotFoundErrorCustom: If the specified PDF directory does not exist or is empty.
    """
    try:
        pdf_files = get_pdf_files(pdf_directory)
    except FileNotFoundError as e:
        raise FileNotFoundErrorCustom(pdf_directory) from e

    if not pdf_files:
        logger.warning(f"No PDF files found to process in directory: {pdf_directory}")
        return

    all_data: List[Dict[str, str]] = []

    try:
        pdf_contents = read_pdfs_concurrently(pdf_files, max_workers=4)
    except PDFProcessingError as e:
        logger.error(f"Error processing PDFs: {e.message}")
        return
    except Exception as e:
        logger.error(f"Error reading PDFs: {e}", exc_info=True)
        raise PDFProcessingError(f"Failed to read PDFs in {pdf_directory}") from e

    output_dir_path = Path(output_directory)
    try:
        output_dir_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logger.error(f"Failed to create output directory {output_directory}: {e}")
        raise FileSaveError(output_directory, "Failed to create output directory.") from e

    for pdf_data in pdf_contents:
        pdf_file = pdf_data["file_name"]
        content = pdf_data["content"]

        if content:
            try:
                processed_content = preprocess_content(pdf_file, content)
                all_data.append({
                    "file_name": Path(pdf_file).name,
                    "content": processed_content,
                    "extracted_at": datetime.now().isoformat()
                })
                logger.info(f"Content extracted and preprocessed from {pdf_file}")
            except InvalidContentError as e:
                logger.warning(f"Invalid content in {pdf_file}: {e.message}")
            except Exception as e:
                logger.error(f"Error during preprocessing content of {pdf_file}: {e}", exc_info=True)
        else:
            logger.warning(f"No content extracted from file: {pdf_file}")

        extract_images_from_pdf(pdf_file, output_directory)

    if all_data:
        try:
            output_file = output_dir_path / f"extracted_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            save_output(all_data, str(output_file))
            logger.info(f"Processed PDFs and saved content successfully to {output_file}.")
        except Exception as e:
            logger.error(f"Error while saving output: {e}", exc_info=True)
            raise FileSaveError(str(output_file), f"Failed to save extracted data to {output_file}.") from e
    else:
        logger.warning("No content extracted to save after processing PDFs.")
