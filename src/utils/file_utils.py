import os
from loguru import logger
import pdfplumber
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_pdf_files(directory: str):
    """
    Recursively fetches all PDF files from the given directory and its subdirectories.

    Args:
        directory (str): The directory to search for PDF files.

    Returns:
        list: A list of paths to all found PDF files.
    """
    pdf_files = []  # List to store paths of PDF files found in the directory
    try:
        for root, _, files in os.walk(directory):  # Traverse the directory and its subdirectories
            for file in files:
                if file.endswith('.pdf'):  # Check if the file has a .pdf extension
                    pdf_files.append(os.path.join(root, file))  # Add full path of the PDF to the list
                else:
                    logger.debug(f"Non-PDF file found: {file}")
        logger.info(f"Found {len(pdf_files)} PDF file(s) in '{directory}'.")
    except Exception as e:
        logger.error(f"Error occurred while scanning directory '{directory}': {str(e)}")
    return pdf_files

def read_pdf_file(file_path: str):
    """
    Reads a PDF file and returns its text content.

    Args:
        file_path (str): The full path of the PDF file to read.

    Returns:
        str: The text content of the PDF file, or None if the file cannot be read.
    """
    if not os.path.exists(file_path):  # Check if the file exists
        logger.error(f"File not found: {file_path}")
        return None

    try:
        # Open the PDF file using pdfplumber
        with pdfplumber.open(file_path) as pdf:
            full_text = ""
            # Loop through each page and extract text
            for page in pdf.pages:
                page_text = page.extract_text()
                full_text += page_text if page_text else ""  # Avoid NoneType error by appending empty string if no text
            logger.info(f"Successfully read PDF: {file_path} with {len(pdf.pages)} pages")
            return full_text
    except PermissionError:
        logger.error(f"Permission denied: {file_path}")
        return None
    except Exception as e:  # Catch any other exceptions that occur while reading the PDF
        logger.error(f"Failed to process {file_path} due to: {str(e)}")
        return None

def read_pdfs_concurrently(pdf_files: list, max_workers: int = 4):
    """
    Reads PDF files concurrently using threading.

    Args:
        pdf_files (list): A list of PDF file paths to read.
        max_workers (int): The maximum number of threads to use for concurrent reading.

    Returns:
        list: A list of tuples containing the file path and its content.
    """
    pdf_contents = []  # List to store results (file path and content)
    
    # Use ThreadPoolExecutor for concurrent reading of PDF files
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(read_pdf_file, file): file for file in pdf_files}  # Submit tasks
        for future in as_completed(futures):  # Wait for all futures to complete
            file = futures[future]
            try:
                content = future.result()
                if content:  # Only append non-empty content
                    pdf_contents.append((file, content))
            except Exception as e:
                logger.error(f"Error reading {file}: {str(e)}")

    logger.info(f"Completed reading {len(pdf_contents)} PDFs.")
    return pdf_contents
